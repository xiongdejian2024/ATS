#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : USD_data.py
@time         : 2024/03/01 14:19
@author       : o_junnan.zhou@external.jiduauto.com
@description  : 
'''

import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


#pytest basetech/diagnostics/test_diag_data.py::TestRoutineControl::test_caseid_1986131
# pytest basetech/diagnostics/test_diag_data.py::TestRoutineControl::


@allure.feature('TCAM BaseTech/诊断/诊断数据')
class TestRoutineControl(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        
        logger.info("tcam 上下电操作 防止因为诊断 操作ssh 导致ssh 以后小时候自动关闭")
        self.io.tcam_power_off()
        sleep(10)
        self.io.tcam_power_on()
        logger.info("tcam 上下电操作 延时3分钟")
        sleep(3 * 60)
        super().after_class(self, ecu)


    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-01')
    def test_caseid_1986487(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-02')
    def test_caseid_1986486(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-03')
    def test_caseid_1986485(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-01-02')
    def test_caseid_1986484(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下01-03')
    def test_caseid_1986483(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-02-01')
    def test_caseid_1986482(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','710102061001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-02-03')
    def test_caseid_1986481(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-03-01')
    def test_caseid_1986480(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','710102061001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_01会话下-03-02')
    def test_caseid_1986479(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-01')
    def test_caseid_1986478(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-02')
    def test_caseid_1986477(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-03')
    def test_caseid_1986476(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-01-02')
    def test_caseid_1986475(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下01-03')
    def test_caseid_1986474(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-02-01')
    def test_caseid_1986473(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-02-03')
    def test_caseid_1986472(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-03-01')
    def test_caseid_1986471(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_02会话下-03-02')
    def test_caseid_1986470(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-01')
    def test_caseid_1986469(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EXTENDED,UnLock.L0,'','710102061001')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-02')
    def test_caseid_1986468(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-03')
    def test_caseid_1986467(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-01-02')
    def test_caseid_1986466(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EXTENDED,UnLock.L0,'','710102061001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下01-03')
    def test_caseid_1986465(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EXTENDED,UnLock.L0,'','710102061001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-02-01')
    def test_caseid_1986464(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','710102061001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-02-03')
    def test_caseid_1986463(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-03-01')
    def test_caseid_1986462(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x01,SESSION.EMPTY,UnLock.L0,'','710102061001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check programming pre-conditions(0x31)_0206_03会话下-03-02')
    def test_caseid_1986461(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-01')
    def test_caseid_1986460(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-02')
    def test_caseid_1986459(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-03')
    def test_caseid_1986458(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-01-02')
    def test_caseid_1986457(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下01-03')
    def test_caseid_1986456(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-02-01')
    def test_caseid_1986455(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-02-03')
    def test_caseid_1986454(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-03-01')
    def test_caseid_1986453(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_01会话下-03-02')
    def test_caseid_1986452(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-01')
    def test_caseid_1986451(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3133')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-02')
    def test_caseid_1986450(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-03')
    def test_caseid_1986449(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-01-02')
    def test_caseid_1986448(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下01-03')
    def test_caseid_1986447(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-02-01')
    def test_caseid_1986446(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3133')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-02-03')
    def test_caseid_1986445(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-03-01')
    def test_caseid_1986444(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3133')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_02会话下-03-02')
    def test_caseid_1986443(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-01')
    def test_caseid_1986442(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3131')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-02')
    def test_caseid_1986441(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-03')
    def test_caseid_1986440(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-01-02')
    def test_caseid_1986439(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下01-03')
    def test_caseid_1986438(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-02-01')
    def test_caseid_1986437(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-02-03')
    def test_caseid_1986436(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-03-01')
    def test_caseid_1986435(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_03会话下-03-02')
    def test_caseid_1986434(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-01')
    def test_caseid_1986433(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L1,'','710102051000000001')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-02')
    def test_caseid_1986432(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-03')
    def test_caseid_1986431(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-01-02')
    def test_caseid_1986430(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L1,'','710102051000000001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下01-03')
    def test_caseid_1986429(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.PROGRAMMING,UnLock.L1,'','710102051000000001')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-02-01')
    def test_caseid_1986428(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','710102051000000001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-02-03')
    def test_caseid_1986427(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-03-01')
    def test_caseid_1986426(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x01,SESSION.EMPTY,UnLock.L0,'','710102051000000001')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Check Complete & Compatible(0x31)_0205_L1_02会话下-03-02')
    def test_caseid_1986425(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x03,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-01')
    def test_caseid_1986424(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-02')
    def test_caseid_1986423(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话-03下')
    def test_caseid_1986422(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-01-02')
    def test_caseid_1986421(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-01-03')
    def test_caseid_1986420(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-02-01')
    def test_caseid_1986419(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-02-03')
    def test_caseid_1986418(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-03-01')
    def test_caseid_1986417(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_01会话下-03-02')
    def test_caseid_1986416(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-01')
    def test_caseid_1986415(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-02')
    def test_caseid_1986414(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-03')
    def test_caseid_1986413(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-01-02')
    def test_caseid_1986412(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-01-03')
    def test_caseid_1986411(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-02-01')
    def test_caseid_1986410(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-02-03')
    def test_caseid_1986409(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-03-01')
    def test_caseid_1986408(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_02会话下-03-02')
    def test_caseid_1986407(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-01')
    def test_caseid_1986406(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-02')
    def test_caseid_1986405(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-03')
    def test_caseid_1986404(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-01-02')
    def test_caseid_1986403(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-01-03')
    def test_caseid_1986402(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-02-01')
    def test_caseid_1986401(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-02-03')
    def test_caseid_1986400(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-03-01')
    def test_caseid_1986399(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_03会话下-03-02')
    def test_caseid_1986398(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 512}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_L1_02会话下-01')
    def test_caseid_1986397(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','71010212')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_L1_02会话下-02')
    def test_caseid_1986396(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_L1_02会话下-03')
    def test_caseid_1986395(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_L1_02会话下-01-02')
    def test_caseid_1986394(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','71010212')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_L1_02会话下-01-03')
    def test_caseid_1986393(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','71010212')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_L1_02会话下-02-01')
    def test_caseid_1986392(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','71010212')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_L1_02会话下-02-03')
    def test_caseid_1986391(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_L1_02会话下-03-01')
    def test_caseid_1986390(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','71010212')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_L1_02会话下-03-02')
    def test_caseid_1986389(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 512}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x02,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_check memory(0x31)_0212_L1_02会话下-RID的值错误')
    def test_caseid_1986388(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 510}','71010212')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 514}','71010212')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-01')
    def test_caseid_1986387(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-02')
    def test_caseid_1986386(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-03')
    def test_caseid_1986385(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-01-02')
    def test_caseid_1986384(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-01-03')
    def test_caseid_1986383(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-02-01')
    def test_caseid_1986382(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-02-03')
    def test_caseid_1986381(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-03-01')
    def test_caseid_1986380(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_01会话下-03-02')
    def test_caseid_1986379(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.DEFAULT,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-01')
    def test_caseid_1986378(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-02')
    def test_caseid_1986377(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-03')
    def test_caseid_1986376(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-01-02')
    def test_caseid_1986375(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-01-03')
    def test_caseid_1986374(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-02-01')
    def test_caseid_1986373(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-02-03')
    def test_caseid_1986372(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-03-01')
    def test_caseid_1986371(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_02会话下-03-02')
    def test_caseid_1986370(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-01')
    def test_caseid_1986369(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-02')
    def test_caseid_1986368(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-03')
    def test_caseid_1986367(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-01-02')
    def test_caseid_1986366(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-01-03')
    def test_caseid_1986365(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-02-01')
    def test_caseid_1986364(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-02-03')
    def test_caseid_1986363(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-03-01')
    def test_caseid_1986362(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_03会话下-03-02')
    def test_caseid_1986361(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EXTENDED,UnLock.L0,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L0,'0000000000000000','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-01')
    def test_caseid_1986360(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7101ff0010')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-02')
    def test_caseid_1986359(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-03')
    def test_caseid_1986358(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-01-02')
    def test_caseid_1986357(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7101ff0010')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-01-03')
    def test_caseid_1986356(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7101ff0010')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-02-01')
    def test_caseid_1986355(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L1,'0000000000000000','7101ff0010')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-02-03')
    def test_caseid_1986354(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.EMPTY,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-03-01')
    def test_caseid_1986353(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L1,'0000000000000000','7101ff0010')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-03-02')
    def test_caseid_1986352(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x03,SESSION.PROGRAMMING,UnLock.L1,'0000000000000000','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x02,SESSION.EMPTY,UnLock.L1,'0000000000000000','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Erase Memory(0x31)_FF00_L1_02会话下-RID的值错误')
    def test_caseid_1986351(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.PROGRAMMING,UnLock.L1,'00000000000000','7101ff00')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xFF00,0x01,SESSION.EMPTY,UnLock.L1,'000000000000000000','7101ff00')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-01')
    def test_caseid_1986350(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-02')
    def test_caseid_1986349(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-03')
    def test_caseid_1986348(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-01-02')
    def test_caseid_1986347(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-01-03')
    def test_caseid_1986346(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-02-01')
    def test_caseid_1986345(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-02-03')
    def test_caseid_1986344(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-03-01')
    def test_caseid_1986343(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_01会话下-03-02')
    def test_caseid_1986342(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-01')
    def test_caseid_1986341(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-02')
    def test_caseid_1986340(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-03')
    def test_caseid_1986339(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-01-02')
    def test_caseid_1986338(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-01-03')
    def test_caseid_1986337(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-02-01')
    def test_caseid_1986336(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-02-03')
    def test_caseid_1986335(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-03-01')
    def test_caseid_1986334(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_02会话下-03-02')
    def test_caseid_1986333(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-01')
    def test_caseid_1986332(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-02')
    def test_caseid_1986331(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-03')
    def test_caseid_1986330(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-01-02')
    def test_caseid_1986329(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-01-03')
    def test_caseid_1986328(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-02-01')
    def test_caseid_1986327(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-02-03')
    def test_caseid_1986326(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-03-01')
    def test_caseid_1986325(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_03会话下-03-02')
    def test_caseid_1986324(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-01')
    def test_caseid_1986323(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','71018020')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-02')
    def test_caseid_1986322(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-03')
    def test_caseid_1986321(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-01-02')
    def test_caseid_1986320(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','71018020')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-01-03')
    def test_caseid_1986319(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','71018020')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-02-01')
    def test_caseid_1986318(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','71018020')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-02-03')
    def test_caseid_1986317(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-03-01')
    def test_caseid_1986316(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','71018020')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-03-02')
    def test_caseid_1986315(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 4098}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Certificate install(0x31)_8020_L7_03会话下-RID的值错误')
    def test_caseid_1986314(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 4096}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x8020,0x01,SESSION.EMPTY,UnLock.L0,f'03000c6c6e34686969376c33616465{"f" * 4064}6760','71018020')

    # @pytest.mark.repeat(500)
    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-01')
    def test_caseid_1986313(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.DEFAULT,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'02','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-02')
    def test_caseid_1986312(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-03')
    def test_caseid_1986311(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-01-02')
    def test_caseid_1986310(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.DEFAULT,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-01-03')
    def test_caseid_1986309(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.DEFAULT,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-02-01')
    def test_caseid_1986308(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-02-03')
    def test_caseid_1986307(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    # @pytest.mark.repeat(500)
    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-03-01')
    def test_caseid_1986306(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-03-02')
    def test_caseid_1986305(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-01')
    def test_caseid_1986304(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'02','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-02')
    def test_caseid_1986303(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-03')
    def test_caseid_1986302(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-01-02')
    def test_caseid_1986301(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-01-03')
    def test_caseid_1986300(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-02-01')
    def test_caseid_1986299(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-02-03')
    def test_caseid_1986298(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-03-01')
    def test_caseid_1986297(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_02会话下-03-02')
    def test_caseid_1986296(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    
    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-01')
    def test_caseid_1986295(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EXTENDED,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'02','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-02')
    def test_caseid_1986294(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-03')
    def test_caseid_1986293(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-01-02')
    def test_caseid_1986292(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EXTENDED,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-01-03')
    def test_caseid_1986291(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EXTENDED,UnLock.L0,'01','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-02-01')
    def test_caseid_1986290(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-02-03')
    def test_caseid_1986289(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-03-01')
    def test_caseid_1986288(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a1001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-03-02')
    def test_caseid_1986287(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_01会话下-RID的值错误')
    def test_caseid_1986286(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.DEFAULT,UnLock.L0,'00','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'05','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'0100','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3112')
        # 短的或者值错误，期望回复31，长的期望正响应，实际接受偏差，SOA-21877

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_VehicleFOTAMode(0x31)_A100_03会话下-RID的值错误')
    def test_caseid_1986285(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EXTENDED,UnLock.L0,'00','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'05','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'0100','7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-01')
    def test_caseid_1986284(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-02')
    def test_caseid_1986283(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-03')
    def test_caseid_1986282(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-01-02')
    def test_caseid_1986281(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-01-03')
    def test_caseid_1986280(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-02-01')
    def test_caseid_1986279(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-02-03')
    def test_caseid_1986278(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-03-01')
    def test_caseid_1986277(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_01会话下-03-02')
    def test_caseid_1986276(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.DEFAULT,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-01')
    def test_caseid_1986275(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3133')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-02')
    def test_caseid_1986274(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-03')
    def test_caseid_1986273(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-01-02')
    def test_caseid_1986272(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-01-03')
    def test_caseid_1986271(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-02-01')
    def test_caseid_1986270(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3133')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-02-03')
    def test_caseid_1986269(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-03-01')
    def test_caseid_1986268(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3133')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_02会话下-03-02')
    def test_caseid_1986267(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-01')
    def test_caseid_1986266(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-02')
    def test_caseid_1986265(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-03')
    def test_caseid_1986264(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-01-02')
    def test_caseid_1986263(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-01-03')
    def test_caseid_1986262(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-02-01')
    def test_caseid_1986261(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-02-03')
    def test_caseid_1986260(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-03-01')
    def test_caseid_1986259(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3131')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_03会话下-03-02')
    def test_caseid_1986258(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EXTENDED,UnLock.L0,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-01')
    def test_caseid_1986257(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','710102081000')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-02')
    def test_caseid_1986256(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-03')
    def test_caseid_1986255(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')

    @pytest.mark.smoke
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-01-02')
    def test_caseid_1986254(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','710102081000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-01-03')
    def test_caseid_1986253(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','710102081000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-02-01')
    def test_caseid_1986252(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','710102081000')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-02-03')
    def test_caseid_1986251(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-03-01')
    def test_caseid_1986250(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 688}','710102081000')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-03-02')
    def test_caseid_1986249(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x03,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 688}','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x02,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Transfer Key Info(0x31)_0208_L1_02会话下-RID的值错误')
    def test_caseid_1986248(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.PROGRAMMING,UnLock.L1,f'{"0" * 686}','71010208')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 690}','710102081000')
        

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-01')
    def test_caseid_1986247(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'02','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-02')
    def test_caseid_1986246(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-03')
    def test_caseid_1986245(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-01-02')
    def test_caseid_1986244(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-01-03')
    def test_caseid_1986243(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-02-01')
    def test_caseid_1986242(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-02-03')
    def test_caseid_1986241(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-03-01')
    def test_caseid_1986240(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_01会话下-03-02')
    def test_caseid_1986239(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.sanity
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-01')
    def test_caseid_1986238(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'02','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-02')
    def test_caseid_1986237(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-03')
    def test_caseid_1986236(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-01-02')
    def test_caseid_1986235(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-01-03')
    def test_caseid_1986234(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-02-01')
    def test_caseid_1986233(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-02-03')
    def test_caseid_1986232(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-03-01')
    def test_caseid_1986231(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_02会话下-03-02')
    def test_caseid_1986230(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-01')
    def test_caseid_1986229(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'02','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-02')
    def test_caseid_1986228(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-03')
    def test_caseid_1986227(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-01-02')
    def test_caseid_1986226(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-01-03')
    def test_caseid_1986225(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-02-01')
    def test_caseid_1986224(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-02-03')
    def test_caseid_1986223(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-03-01')
    def test_caseid_1986222(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_03会话下-03-02')
    def test_caseid_1986221(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-01')
    def test_caseid_1986220(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM, 0xA041, 0x01, SESSION.EMPTY, UnLock.L0, '02','7101a04110')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM, 0xA041, 0x01, SESSION.EMPTY, UnLock.L0, '01', '7101a04110')
            
       

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-02')
    def test_caseid_1986219(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-03')
    def test_caseid_1986218(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-01-02')
    def test_caseid_1986217(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a04110')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-01-03')
    def test_caseid_1986216(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a04110')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-02-01')
    def test_caseid_1986215(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a04110')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-02-03')
    def test_caseid_1986214(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-03-01')
    def test_caseid_1986213(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'01','7101a04110')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下-03-02')
    def test_caseid_1986212(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_enable/disable SSH(0x31)_A041_L7_03会话下_RID的值错误')
    def test_caseid_1986211(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'','7101a04111')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'03','7101a04111')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'','7101a04111')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x01,SESSION.EMPTY,UnLock.L0,'0100','7101a04110')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01')
    def test_caseid_1986210(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02')
    def test_caseid_1986209(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03')
    def test_caseid_1986208(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-02')
    def test_caseid_1986207(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-03')
    def test_caseid_1986206(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.DEFAULT,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-01')
    def test_caseid_1986205(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-03')
    def test_caseid_1986204(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-01')
    def test_caseid_1986203(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-02')
    def test_caseid_1986202(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.DEFAULT,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_02会话下-01')
    def test_caseid_1986201(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_02会话下-02')
    def test_caseid_1986200(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_02会话下-03')
    def test_caseid_1986199(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-02')
    def test_caseid_1986198(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-03')
    def test_caseid_1986197(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.PROGRAMMING,UnLock.L0,'01','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-01')
    def test_caseid_1986196(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-03')
    def test_caseid_1986195(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-01')
    def test_caseid_1986194(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-02')
    def test_caseid_1986193(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.PROGRAMMING,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_03会话下-01')
    def test_caseid_1986192(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_03会话下-02')
    def test_caseid_1986191(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_03会话下-03')
    def test_caseid_1986190(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-02')
    def test_caseid_1986189(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-01-03')
    def test_caseid_1986188(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L0,'01','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-01')
    def test_caseid_1986187(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-02-03')
    def test_caseid_1986186(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-01')
    def test_caseid_1986185(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_01会话下-03-02')
    def test_caseid_1986184(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L0,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-01')
    def test_caseid_1986183(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L5,'01','7101ea1d')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-02')
    def test_caseid_1986182(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L5,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-03')
    def test_caseid_1986181(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L5,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-01-02')
    def test_caseid_1986180(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L5,'01','7101ea1d')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-01-03')
    def test_caseid_1986179(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L5,'01','7101ea1d')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-02-01')
    def test_caseid_1986178(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L5,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7101ea1d')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-02-03')
    def test_caseid_1986177(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EXTENDED,UnLock.L5,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EMPTY,UnLock.L5,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-03-01')
    def test_caseid_1986176(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L5,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'01','7101ea1d')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下-03-02')
    def test_caseid_1986175(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x03,SESSION.EXTENDED,UnLock.L5,'01','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x02,SESSION.EMPTY,UnLock.L0,'01','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_upload LOG(0x31)_EA1D_L5_03会话下_RID的值错误')
    def test_caseid_1986174(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EXTENDED,UnLock.L5,'00','7101ea1d')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'08','7101ea1d')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'','7101ea1d')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA1D,0x01,SESSION.EMPTY,UnLock.L0,'0100','7101ea1d')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-01')
    def test_caseid_1986173(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-02')
    def test_caseid_1986172(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-03')
    def test_caseid_1986171(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-01-02')
    def test_caseid_1986170(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-01-03')
    def test_caseid_1986169(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.DEFAULT,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-02-01')
    def test_caseid_1986168(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-02-03')
    def test_caseid_1986167(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-03-01')
    def test_caseid_1986166(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_01会话下-03-02')
    def test_caseid_1986165(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.DEFAULT,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-01')
    def test_caseid_1986164(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-02')
    def test_caseid_1986163(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-03')
    def test_caseid_1986162(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-01-02')
    def test_caseid_1986161(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-01-03')
    def test_caseid_1986160(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.PROGRAMMING,UnLock.L0,'','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-02-01')
    def test_caseid_1986159(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-02-03')
    def test_caseid_1986158(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-03-01')
    def test_caseid_1986157(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3131')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_02会话下-03-02')
    def test_caseid_1986156(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-01')
    def test_caseid_1986155(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-02')
    def test_caseid_1986154(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-03')
    def test_caseid_1986153(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-01-02')
    def test_caseid_1986152(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-01-03')
    def test_caseid_1986151(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L0,'','7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-02-01')
    def test_caseid_1986150(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-02-03')
    def test_caseid_1986149(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-03-01')
    def test_caseid_1986148(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','7f3133')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_03会话下-03-02')
    def test_caseid_1986147(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5_03会话下-01')
    def test_caseid_1986146(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L5,'','710121001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5_03会话下-02')
    def test_caseid_1986145(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L5,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5_03会话下-03')
    def test_caseid_1986144(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L5,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-01-02')
    def test_caseid_1986143(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L5,'','710121001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-01-03')
    def test_caseid_1986142(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EXTENDED,UnLock.L5,'','710121001000')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-02-01')
    def test_caseid_1986141(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L5,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','710121001000')


    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-02-03')
    def test_caseid_1986140(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EXTENDED,UnLock.L5,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-03-01')
    def test_caseid_1986139(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L5,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,SESSION.EMPTY,UnLock.L0,'','710121001000')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_Clear Data for env change(0x31)_2100_L5__03会话下-03-02')
    def test_caseid_1986138(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x03,SESSION.EXTENDED,UnLock.L5,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x02,SESSION.EMPTY,UnLock.L0,'','7f3112')


    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_01会话下')
    def test_caseid_1986136(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x00,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x20,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_02会话下')
    def test_caseid_1986135(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x20,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_L1_02会话下')
    def test_caseid_1986134(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x00,SESSION.PROGRAMMING,UnLock.L1,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0205,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_03会话下')
    def test_caseid_1986133(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x00,SESSION.EXTENDED,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x0206,0x20,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_L5_03会话下')
    def test_caseid_1986132(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA29,0x00,SESSION.EXTENDED,UnLock.L5,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xEA29,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC12_L7_03会话下')
    def test_caseid_1986131(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x00,SESSION.EMPTY,UnLock.L0,'','7f3112')
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0xA041,0x10,SESSION.EMPTY,UnLock.L0,'','7f3112')

    
    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_01会话下')
    def test_caseid_1986130(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_02会话下')
    def test_caseid_1986129(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_03会话下')
    def test_caseid_1986128(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_L1_02会话下')
    def test_caseid_1986127(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_L5_03会话下')
    def test_caseid_1986126(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断数据')
    @allure.title('UDS_(0x31)_NRC13_L7_03会话下')
    def test_caseid_1986125(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.send_data_and_check(TA.TCAM,'31','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'3101','7f3113')
        self.sd_tester.send_data_and_check(TA.TCAM,'310102','7f3113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

