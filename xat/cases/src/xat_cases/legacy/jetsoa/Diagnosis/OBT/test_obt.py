#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     : test_basetechdemo.py
@time         : 2024/05/14 14:19
@author       : quan.sun@jiduauto.com
@description  : 
"""


import os
import sys
import pytest
import allure
import ctypes

cur_path = os.path.join(os.getcwd().split('sat')[0], 'sat')
sys.path.append(cur_path)

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *


@allure.feature("Demon")
@allure.story("OBT")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        super().before_class(self, ecu)
        self.jetlog = start_process(os.path.join(cur_path, "sotest/juds_demo/start_jetlog.sh"))
        # 启动diag
        # env_cmd = "sudo JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib"
        # print(start_process(env_cmd))
        self.diagd = start_process(os.path.join(cur_path, "sotest/juds_demo/start_diagd.sh"))
        # 启动obt server
        # obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        # self.obt_server = start_process(obt_server_cmd)
        self.obt_server = start_process(os.path.join(cur_path, "sotest/juds_demo/start_obt_server.sh"))
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cppobt_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_obt_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        assert 0 == self.cpp_case_lib.start_uds_server()

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)        

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        
        if self.diagd:
            stop_process(self.diagd)
        if self.obt_server:
            stop_process(self.obt_server)
        if self.jetlog:
            stop_process(self.jetlog)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        super().after_class(self, ecu)
        
    @allure.title("OBT_init对象a1进行诊断全流程")
    @pytest.mark.full
    def test_caseid_1985768(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        self.cppobt_case_lib.test_all.restype = ctypes.c_int  # 初始化，然后反初始化
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        assert 0 == self.cppobt_case_lib.test_all(1, b"a1",0x1001,pdu, len(pdu), exp_pdu, len(exp_pdu), 5000)
        
    @allure.title("OBT_仲裁优先级11业务名称相同")
    @pytest.mark.full
    def test_caseid_1985769(self):
        assert 0 == self.cppobt_case_lib.Same_priority(1, b"a1")
        
    @allure.title("OBT_仲裁优先级11业务名称不同proxy1未stop,proxy2start失败")#这里面调用了deinit也报了coredump
    @pytest.mark.full
    def test_caseid_1985770(self):
        assert 0 == self.cppobt_case_lib.name_different_false(1, b"a1", 1, b"b1")
        
    @allure.title("OBT_仲裁优先级11业务名称不同proxy1stop后,proxy2start成功")
    @pytest.mark.full
    def test_caseid_1987168(self):
        assert 0 == self.cppobt_case_lib.name_different_true(1, b"a1", 1, b"b1")
        
    @allure.title("OBT_仲裁优先级打断012")
    @pytest.mark.full
    def test_caseid_1985774(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        assert 0 == self.cppobt_case_lib.priority_interrupt(0, b"a0", 1, b"a1", 2, b"a2", 0x1001, pdu, len(pdu), exp_pdu, len(exp_pdu), 5000)#失败了报了3也产生了coredump
        
    @allure.title("OBT_仲裁优先级打断后再次下发指令")
    @pytest.mark.full
    def test_caseid_1985775(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        proxy_pdu = b'\x22\xf1\x86'
        proxy_exp_pdu = b'\x62\xf1\x86'
        assert 0 == self.cppobt_case_lib.priority_fazhiling(
            0, b"a0", 1, b"a1", 0x1001, pdu, len(pdu), exp_pdu, len(exp_pdu), 5000,
            0x1001, proxy_pdu, len(proxy_pdu), proxy_exp_pdu, len(proxy_exp_pdu), 5000)#失败了报了1也产生了coredump
        
    @allure.title("OBT_仲裁优先级特殊规则同等级同时拿到仲裁")
    @pytest.mark.full
    def test_caseid_1985772(self):
        assert 0 == self.cppobt_case_lib.priority_same(0, b"fota", 0, b"local_diag", 0, b"fod")
        
    @allure.title("OBT_仲裁优先级最大连接5个小时")
    @pytest.mark.full
    @pytest.mark.long_time
    def test_caseid_1985773(self):
        assert 0 == self.cppobt_case_lib.time_max(0, b"fota")
        
    @allure.title("OBT_针对指定地址进行功能寻址")
    @pytest.mark.full
    def test_caseid_1989028(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        self.cppobt_case_lib.test_fota.restype = ctypes.c_int
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        assert 0 == self.cppobt_case_lib.test_fota(1, b"a1",0x1FFF, pdu, len(pdu), exp_pdu, len(exp_pdu), 5000)