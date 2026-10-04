#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_basetechdemo.py
@time         : 2023/11/23 14:19
@author       : quan.sun@jiduauto.com
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
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("Demon")
@allure.story("BaseTech Demo")
class TestBasetechAbstract(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")

    @pytest.mark.diag_server_demo
    @allure.title("diag_server_demo")
    def test_basetech_caseid_112590(self):
        self.sd_tester.enter_bgm_default_session()
        self.sd_tester.send_data_and_check(0x1001,[0x22, 0xB1, 0x65],'62b16502')
        self.sd_tester.enter_bgm_programming_session()
        self.sd_tester.send_data_and_check(0x1001, [0x22, 0xB1, 0x65], '62b16502')
        self.sd_tester.enter_bgm_default_session()
        self.sd_tester.enter_bgm_extended_session()
        self.sd_tester.send_data_and_check(0x1001, [0x22, 0xB1, 0x65],'62b16502')

    def test_read_did_and_check(self):
        #向SOC MCU发送22F186，并读取是否写入值成功，测试完成后恢复写入前的值
        self.sd_tester.read_did_and_check([TA.BGM_MCU,TA.BGM_SOC],0xf186,SESSION.DEFAULT,['62f18601','62f18601'],[8,8])
    
    def test_write_did_and_check(self):
        #向SOC的DID 0xB200写入值0a，并读取是否写入值成功，发送1181重启后,再重新读取值确认是否写入值成功，测试完成后恢复写入前的值
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb200,SESSION.EXTENDED,UnLock.L5,'0a','62b2000a')
    
    def test_io_ctrl_and_check(self):
        #向MCU的IO Control 0xB200写入值0a，并读取是否写入值成功，测试完成后恢复写入前的值
        self.sd_tester.io_ctrl_and_check(ta=TA.BGM_MCU,did=0x40E2,io_type=0x03,session=SESSION.EXTENDED,unlock_level=UnLock.L0,write_data='7FFF',check_data='6240e27fff',check_length=10)
    
    def test_routine_ctrl_and_check(self):
        #向MCU的Routine Control 0x2072 01写入值ff01
        self.sd_tester.routine_ctrl_and_check(ta=TA.BGM_MCU,did=0x2072,routine_type=0x01,session=SESSION.EXTENDED,unlock_level=UnLock.L0,write_data='ff01',check_data='7101207210',check_length=10)
        
    def test_get_ecu_core_assembly_part_number(self):
        #获取BGM的硬件号
        self.sd_tester.get_ecu_core_assembly_part_number()
    
    def test_f190(self):
        #4A445330415445535442454E4348303637
        #向MCU写入F190值，并读取是否写入值成功，发送1181重启后,再重新读取值确认是否写入值成功，测试完成后恢复写入前的值
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf190,SESSION.EXTENDED,UnLock.L5,'ffffffffffffffffffffffffffffffffff','62f190ffffffffffffffffffffffffffffffffff',check_method=Check_Method.reset)    
    
    def test_init_boot_pre(self):
        #初始化进boot环境
        self.mix.init_boot_per()
    
    def test_control_dtc_setting_and_check(self):
        #控制bgm dtc记录开关并检查返回值
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU,setting_type=0x01,session=SESSION.EXTENDED)
    
    def test_clear_dtc_and_check(self):
        #清除dtc并检查返回值
        self.sd_tester.clear_dtc_and_check(TA.BGM_MCU,session=SESSION.EXTENDED)
    
    def test_communication_control_and_check(self):
        #控制bgm 总线数据发送接收并检查返回值
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,control_did=0x03,control_type=0x01,session=SESSION.EXTENDED)
    
    def test_hard_reset(self):
        #硬重启
        self.sd_tester.hard_reset(TA.BGM_SOC)
    
    def test_soft_reset(self):
        #软重启
        self.sd_tester.soft_reset(TA.BGM_SOC)
    
    def test_send_data_and_check(self):
        #发送数据并检查
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x22,0xf1,0x86],[0x62,0xf1,0x86])
        self.sd_tester.send_data_and_check([TA.BGM_SOC,TA.BGM_MCU],[0x22,0xf1,0x86],[[0x62,0xf1,0x86],[0x62,0xf1,0x86]])
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f186','62f186')
        self.sd_tester.send_data_and_check([TA.BGM_SOC,TA.BGM_MCU],'22f186',['62f186','62f186'])
    
    def test_unlock_and_check(self):
        #测试解锁
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,0x19B834DCA2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5,UnlockStep.key,0x19B834DCA2)
        
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5,UnlockStep.key)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
    
    def test_write_bncm(self):
        #测试写入BNCM值
        self.sd_tester.write_bncm_key(bncm_key=__import__("os").environ['XAT_CREDENTIAL_SCAN_A095D57704F5D68FEA1A'])
        
    def test_caculate_key(self):
        #测试计算key值
        key=self.sd_tester.caculate_key(level=UnLock.L5,seed='00000000')
        logger.info(f'key={key}')
        
    def test_read_dtc_and_check(self):
        #测试19服务并检查返回值
        self.sd_tester.read_dtc_and_check(TA.TCAM,0x02,0x09,SESSION.DEFAULT,'59')
    
    def test_bgm_unlock_l7(self):
        #测试bgm安全等级7解锁
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L7,constant=self.ssh.get_bgm_l7_constant())
    
    def test_tcam_unlock_l7(self):
        #测试tcam安全等级7解锁
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.ssh.get_tcam_l7_constant())
    
    def test_dtc(self):
        self.sd_tester.read_dtc_and_check(TA.BGM_MCU,0x04,0xA01312,0x20,SESSION.DEFAULT)
        self.sd_tester.read_dtc_and_check(TA.BGM_MCU,0x02,None,0x09,SESSION.DEFAULT)
        
#pytest basetech_demo/test_basetechdemo.py::TestBasetechAbstract::test_dtc
