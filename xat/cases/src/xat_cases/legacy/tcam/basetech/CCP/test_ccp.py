#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : CCP.py
@time         : 2024/03/05 15:31
@author       : o_junnan.zhou@external.jiduauto.com
@description  : 
'''

import os
import sys
import allure
import pytest

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


#pytest basetech/CCP/test_ccp.py::TestCarconfiguration::test_caseid_1990355

# @pytest.mark.repeat(20)

@allure.feature('TCAM BaseTech/诊断/诊断数据')
class TestCarconfiguration(TestABCBase):
    def before_class(self, ecu):
        # 整个脚本开始跑之前执行一次
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
            self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')

    def before_each_func(self, ecu):
        # 每条用例开始前执行一次
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','6f429e',check_method=Check_Method.response,recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x429E,SESSION.EMPTY,'62429e')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        time.sleep(40)
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(40)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a00')
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        # 每条用例执行完之后执行一次
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # 所有用例跑完之后执行一次恢复默认值
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','6f429e',check_method=Check_Method.response,recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x429E,SESSION.EMPTY,'62429e')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        time.sleep(40)
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(40)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a00')
        super().after_class(self, ecu)
   

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入')
    def test_caseid_1987620(self):
        self.sd_tester.write_ccp({181:0x02,189:0x02,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x01,189:0x01,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入')
    def test_caseid_1987652(self):
        self.sd_tester.write_ccp({181:0x02,189:0x02,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x01,189:0x01,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    
    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_180')
    def test_caseid_1987619(self):
        self.sd_tester.write_ccp({180:0x05})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b405000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_181')
    def test_caseid_1987618(self):
        self.sd_tester.write_ccp({181:0x03})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b503000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_182')
    def test_caseid_1987617(self):
        self.sd_tester.write_ccp({182:0x02})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b602000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_186')
    def test_caseid_1987616(self):
        self.sd_tester.write_ccp({186:0x15})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100ba15000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_189')
    def test_caseid_1987615(self):
        self.sd_tester.write_ccp({189:0x03})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100bd03000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_566')
    def test_caseid_1987614(self):
        self.sd_tester.write_ccp({566:0xFF})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_950')
    def test_caseid_1987613(self):
        self.sd_tester.write_ccp({950:0x32})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b632000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_969')
    def test_caseid_1987612(self):
        self.sd_tester.write_ccp({969:0x12})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103c912000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_2byte错误的值')
    def test_caseid_1987611(self):
        self.sd_tester.write_ccp({180:0x08,181:0x06})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10302',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_3byte错误的值')
    def test_caseid_1987610(self):
        self.sd_tester.write_ccp({182:0x09,186:0x07,189:0x04})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10303',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_4byte错误的值')
    def test_caseid_1987609(self):
        self.sd_tester.write_ccp({186:0x04,189:0x05,950:0x06,969:0x07})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10304',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')


    
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_5byte错误的值')
    def test_caseid_1987608(self):
        self.sd_tester.write_ccp({180:0x04,182:0x05,186:0x06,950:0x11,969:0x12})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10305',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_6byte错误的值')
    def test_caseid_1987607(self):
        self.sd_tester.write_ccp({180:0x11,181:0x22,186:0x12,189:0x15,950:0x03,969:0x03})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10306',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_7byte错误的值')
    def test_caseid_1987606(self):
        self.sd_tester.write_ccp({180:0x33,181:0x44,182:0x55,186:0x66,189:0x77,950:0x88,969:0x99})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10307',check_length=68)
        # time.sleep(30)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')
    
    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_8byte错误的值')
    def test_caseid_1987605(self):
        self.sd_tester.write_ccp({180:0x33,181:0x44,182:0x55,186:0x66,189:0x77,566:0xff,950:0x88,969:0x99})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10307',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_全00错误值')
    def test_caseid_1987604(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{"00" * 1556}f7b9','6ef106',check_method=Check_Method.response,recover=False)
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10306',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

   
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_全FF错误值')
    def test_caseid_1987603(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,UnLock.L5,f'{"ff" * 1556}eaf1','6ef106',check_method=Check_Method.response,recover=False)
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10307',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_180_active')
    def test_caseid_1987602(self):
        self.sd_tester.write_ccp({180:0x08})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b408000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_181_active')
    def test_caseid_1987601(self):
        self.sd_tester.write_ccp({181:0x09})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b509000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_182_active')
    def test_caseid_1987600(self):
        self.sd_tester.write_ccp({182:0x11})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100b611000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_186_active')
    def test_caseid_1987599(self):
        self.sd_tester.write_ccp({186:0x08})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100ba08000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_189_active')
    def test_caseid_1987598(self):
        self.sd_tester.write_ccp({189:0x16})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030100bd16000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_566_active')
    def test_caseid_1987597(self):
        self.sd_tester.write_ccp({566:0xff})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')

    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_950_active')
    def test_caseid_1987596(self):
        self.sd_tester.write_ccp({950:0x88})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b688000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_969_active')
    def test_caseid_1987595(self):
        self.sd_tester.write_ccp({969:0x89})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103c989000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_2byte错误的值_active')
    def test_caseid_1987594(self):
        self.sd_tester.write_ccp({180:0x88,181:0x87})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10302',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_3byte错误的值_active')
    def test_caseid_1987593(self):
        self.sd_tester.write_ccp({182:0x32,186:0x65,189:0x76})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10303',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_4byte错误的值_active')
    def test_caseid_1987592(self):
        self.sd_tester.write_ccp({186:0x21,189:0x22,950:0x31,969:0x32})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10304',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_5byte错误的值_active')
    def test_caseid_1987591(self):
        self.sd_tester.write_ccp({180:0x56,182:0x66,186:0x67,950:0x78,969:0x34})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10305',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_6byte错误的值_active')
    def test_caseid_1987590(self):
        self.sd_tester.write_ccp({180:0x32,181:0x23,186:0x44,189:0x34,950:0x65,969:0x87})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10306',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.sanity
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_7byte错误的值_active')
    def test_caseid_1987589(self):
        self.sd_tester.write_ccp({180:0x89,181:0x87,182:0x86,186:0x85,189:0x83,950:0x81,969:0x82})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10307',check_length=68)
        # time.sleep(30)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_8byte错误的值_active')
    def test_caseid_1987588(self):
        self.sd_tester.write_ccp({180:0x55,181:0x56,182:0x57,186:0x58,189:0x59,566:0xff,950:0x89,969:0x15})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10307',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_01')
    def test_caseid_1990368(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x01,948:0x01,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_02')
    def test_caseid_1990367(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x02,948:0x02,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_03')
    def test_caseid_1990366(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x03,948:0x03,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_04')
    def test_caseid_1990365(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x04,948:0x04,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致
   
    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_05')
    def test_caseid_1990364(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x05,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致
   
    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_06')
    def test_caseid_1990363(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x06,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_07')
    def test_caseid_1990362(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x07,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_08')
    def test_caseid_1990361(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x08,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_09')
    def test_caseid_1990360(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x09,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0A')
    def test_caseid_1990359(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0A,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0B')
    def test_caseid_1990358(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0B,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0C')
    def test_caseid_1990357(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0C,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0D')
    def test_caseid_1990356(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0D,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0E')
    def test_caseid_1990355(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0E,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_948byte_0F')
    def test_caseid_1990354(self):
        self.sd_tester.write_ccp({181:0x01,189:0x01,947:0x00,948:0x00,950:0x01,969:0x00})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        self.sd_tester.write_ccp({181:0x02,189:0x02,947:0x05,948:0x0F,950:0x02,969:0x01})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10300000000000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005600')
        #看日志bgm写入的是否和tcam存储的一致

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_947')
    def test_caseid_1990353(self):
        self.sd_tester.write_ccp({947:0x06})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b306000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_948')
    def test_caseid_1990352(self):
        self.sd_tester.write_ccp({948:0x16})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b416000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_9byte错误的值')
    def test_caseid_1990351(self):
        self.sd_tester.write_ccp({180:0x01,181:0x03,182:0x03,186:0x03,189:0x03,947:0x07,948:0x16,950:0x03,969:0x02})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10309',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_10byte错误的值')
    def test_caseid_1990350(self):
        self.sd_tester.write_ccp({180:0x01,181:0x03,182:0x03,186:0x03,189:0x03,566:0xff,947:0x07,948:0x16,950:0x03,969:0x02})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10309',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_947_active')
    def test_caseid_1990349(self):
        self.sd_tester.write_ccp({947:0x09})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b309000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_错误的值_948_active')
    def test_caseid_1990348(self):
        self.sd_tester.write_ccp({948:0x21})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e1030103b421000000000000000000000000000000000000000000000000000000',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_9byte错误的值_active')
    def test_caseid_1990347(self):
        self.sd_tester.write_ccp({180:0x21,181:0x12,182:0x99,186:0x76,189:0x35,947:0x23,948:0x65,950:0x90,969:0x91})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10309',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_10byte错误的值_active')
    def test_caseid_1990346(self):
        self.sd_tester.write_ccp({180:0x22,181:0x33,182:0x44,186:0x55,189:0x66,566:0xff,947:0x77,948:0x88,950:0x99,969:0x89})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10309',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_8byte错误的值_active_V2.2')
    def test_caseid_1990568(self):
        self.sd_tester.write_ccp({180:0x55,181:0x56,182:0x57,186:0x58,189:0x59,947:0x88,950:0x89,969:0x15})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0b')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10308',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')
   
    @pytest.mark.full
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_全FF错误值_V2.2')
    def test_caseid_1990567(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,UnLock.L5,f'{"ff" * 1556}eaf1','6ef106',check_method=Check_Method.response,recover=False)
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10309',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')

    @pytest.mark.smoke
    @allure.story('TCAM BaseTech/车辆配置/车辆配置')
    @allure.title('TCAM_CCP写入_8byte错误的值_V2.2')
    def test_caseid_1990566(self):
        self.sd_tester.write_ccp({180:0x55,181:0x56,182:0x57,186:0x58,189:0x59,948:0x99,950:0x89,969:0x15})
        # 切换driving模式
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EMPTY,UnLock.L0,'0080','62429e00',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EMPTY,'62dd0a0d')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EMPTY,'62e10308',check_length=68)
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005620','5904e3005609')
   
