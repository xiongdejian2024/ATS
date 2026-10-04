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
import time
import subprocess

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *


@allure.feature("Demon")
@allure.story("OBT")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.obt_server = None
        super().before_class(self, ecu)

        # 启动diag
        # diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;/root/wjj1/sat/CarinaX86_64/bin/jetdiagd"
        # self.diagd = start_process(diagd_cmd)
        os.system("/root/wjj1/sat/sotest/juds_demo/start_diagd.sh &")
        # 启动obt server
        # obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        # self.obt_server = start_process(obt_server_cmd)
        os.system("/root/wjj1/sat/sotest/juds_demo/start_obt_server.sh &")


    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

        sleep(2)
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(
            "../../sotest/juds_demo/build/libtest_uds_app.so"
        )
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        
         #  load c++ library
        self.cppobt_case_lib = ctypes.cdll.LoadLibrary(
            "../../sotest/juds_demo/build/libtest_obt_app.so"
        )

    def after_each_func(self, ecu):
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        if self.diagd:
            stop_process(self.diagd)
        if self.obt_server:
            stop_process(self.obt_server)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        super().after_class(self, ecu)
        
    @allure.title("OBT_init对象a1进行诊断全流程")
    @pytest.mark.full
    def test_caseid_1985768(self):
        # int setup_read_did_cb1(uint16_t server_addr_exp, uint16_t client_addr_exp, uint16_t did_exp,
        # const unsigned char* data_ret, int data_ret_len, uint8_t ret_nrc)
        self.cpp_case_lib.setup_read_did_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.setup_read_did_cb1.restype = ctypes.c_int
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(
            0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0
        )
        # int test_all(int level, const char *name, uint16_t addr, const unsigned char *request_pdu传参,
                    #   int request_pdu_len传参, const unsigned char *expect_pdu, int expect_pdu_len, int timeout_ms);//OBT_init对象a1进行诊断全流程
        self.cppobt_case_lib.test_all.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int, 
        ]
        self.cppobt_case_lib.test_all.restype = ctypes.c_int  # 初始化，然后反初始化
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        result = self.cppobt_case_lib.test_all(
            1, b"a1",0x1001,pdu, len(pdu), exp_pdu, len(exp_pdu), 5000
        )
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级11业务名称相同")
    @pytest.mark.full
    def test_caseid_1985769(self):
        # int Same_priority(int level, const char *name); // OBT_仲裁优先级11业务名称相同
        self.cppobt_case_lib.Same_priority.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p, 
        ]
        self.cppobt_case_lib.Same_priority.restype = ctypes.c_int  # 初始化，然后反初始化
        result = self.cppobt_case_lib.Same_priority(1, b"a1")
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级11业务名称不同proxy1未stop,proxy2start失败")
    @pytest.mark.full
    def test_caseid_1985770(self):
        # int name_different_false(int level, const char *name,int level2, const char *name2) //OBT_仲裁优先级11业务名称不同proxy1未stop,proxy2start失败
        self.cppobt_case_lib.name_different_false.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p, 
        ]
        self.cppobt_case_lib.name_different_false.restype = ctypes.c_int  # 初始化，然后反初始化
        result = self.cppobt_case_lib.name_different_false(1, b"a1", 1, b"b1")
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级11业务名称不同proxy1stop后,proxy2start成功")
    @pytest.mark.full
    def test_caseid_1987168(self):
        # int name_different_true(int level, const char *name,int level2, const char *name2); //OBT_仲裁优先级11业务名称不同proxy1stop后,proxy2start成功
        self.cppobt_case_lib.name_different_true.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p, 
        ]
        self.cppobt_case_lib.name_different_true.restype = ctypes.c_int  # 初始化，然后反初始化
        result = self.cppobt_case_lib.name_different_true(1, b"a1", 1, b"b1")
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级打断012")
    @pytest.mark.full
    def test_caseid_1985774(self):
        # int setup_read_did_cb1(uint16_t server_addr_exp, uint16_t client_addr_exp, uint16_t did_exp,
        # const unsigned char* data_ret, int data_ret_len, uint8_t ret_nrc)
        self.cpp_case_lib.setup_read_did_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.setup_read_did_cb1.restype = ctypes.c_int
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(
            0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0
        )
        # int priority_interrupt(int level0, const char *name0,int level1, const char *name1,const char *name,int level2, const char *name2,
        #                 uint16_t addr, const unsigned char *request_pdu,
        #      int request_pdu_len, const unsigned char *expect_pdu, int expect_pdu_len, int timeout_ms) //OBT_仲裁优先级打断012
        self.cppobt_case_lib.priority_interrupt.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int, 
        ]
        self.cppobt_case_lib.priority_interrupt.restype = ctypes.c_int  # 初始化，然后反初始化
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        result = self.cppobt_case_lib.priority_interrupt(
            0, b"a0", 1, b"a1", 2, b"a2", 0x1001, pdu, len(pdu), exp_pdu, len(exp_pdu), 5000
        )
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级打断后再次下发指令")
    @pytest.mark.full
    def test_caseid_1985775(self):
        # int setup_read_did_cb1(uint16_t server_addr_exp, uint16_t client_addr_exp, uint16_t did_exp,
        # const unsigned char* data_ret, int data_ret_len, uint8_t ret_nrc)
        self.cpp_case_lib.setup_read_did_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.setup_read_did_cb1.restype = ctypes.c_int
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(
            0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0
        )
    # int priority_fazhiling(int level0, const char *name0, int level1, const char *name1,
    #                    uint16_t addr, const unsigned char *request_pdu,
    #                    int request_pdu_len, const unsigned char *expect_pdu, int expect_pdu_len, int timeout_ms,
    #                    uint16_t addrproxy,const unsigned char *proxy_request_pdu,int proxy_request_pdu_len,
    #                    const unsigned char *proxy_expect_pdu, int proxy_expect_pdu_len, int proxy_timeout_ms); // OBT_仲裁优先级打断后再次下发指令
        self.cppobt_case_lib.priority_fazhiling.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int, 
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int, 
        ]
        self.cppobt_case_lib.priority_fazhiling.restype = ctypes.c_int  # 初始化，然后反初始化
        pdu = b'\x22\xf1\x90'
        exp_pdu = b'\x62\xf1\x90'
        proxy_pdu = b'\x22\xf1\x86'
        proxy_exp_pdu = b'\x62\xf1\x86'
        result = self.cppobt_case_lib.priority_fazhiling(
            0, b"a0", 1, b"a1", 0x1001, pdu, len(pdu), exp_pdu, len(exp_pdu), 5000,
            0x1001, proxy_pdu, len(proxy_pdu), proxy_exp_pdu, len(proxy_exp_pdu), 5000
        )
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级特殊规则同等级同时拿到仲裁")
    @pytest.mark.full
    def test_caseid_1985772(self):
        # int priority_same(int level0, const char *name0, int level1, const char *name1, int level2, const char *name2,
        #   ); // OBT_仲裁优先级特殊规则同等级同时拿到仲裁
        self.cppobt_case_lib.priority_same.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p
        ]
        self.cppobt_case_lib.priority_same.restype = ctypes.c_int  # 初始化，然后反初始化
        result = self.cppobt_case_lib.priority_same(
            0, b"fota", 0, b"local_diag", 0, b"fod"
        )
        sleep(0.2)
        assert 0 == result
        
    @allure.title("OBT_仲裁优先级最大连接5个小时")
    @pytest.mark.full
    def test_caseid_1985773(self):
        # int time_max(int level, const char *name);//OBT_仲裁优先级最大连接5个小时
        self.cppobt_case_lib.time_max.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p
        ]
        self.cppobt_case_lib.time_max.restype = ctypes.c_int  # 初始化，然后反初始化
        result = self.cppobt_case_lib.time_max(
            0, b"fota"
        )
        sleep(0.2)
        assert 0 == result