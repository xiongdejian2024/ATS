#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     : test_UdsServer.py
@time         : 2024/05/14 14:19
@author       : jingjing.wang@jiduauto.com
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
from xat_ecu.legacy.protocol.ProtocolClientKeywords import ProtocolClientKeywords

@allure.feature("Demon")
@allure.story("UdsServer")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.obt_server = None
        super().before_class(self, ecu)

        # 启动diag
        diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/modify_config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
        self.diagd = start_process(diagd_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_diagd.sh &")
        # 启动obt server
        obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/modify_config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        self.obt_server = start_process(obt_server_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_obt_server.sh &")


    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(
            "../../sotest/juds_demo/build/libtest_uds_app.so"
        )
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        logger.info(f"function before run finished.")
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并自动激活路由

    def after_each_func(self, ecu):
        self.doip_client.doip_sock_obj.tcp_client_sock.stop()#反初始化
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

    @allure.title("UdsServer_会话服务_时间戳")
    @pytest.mark.full
    def test_caseid_1987651(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x10, 0x01])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())#("p2_star": 十进制6500=16进制的1964,6500x10ms(单位)=65000ms)
        assert result == [0x7F, 0x10, 0x78]
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())#("p2_star": 十进制6500=16进制的1964,6500x10ms(单位)=65000ms)
        assert result == [0x50, 0x01, 0x00, 0x00, 0x19, 0x64]
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x01], 
                                                      check_return_data=['7f2278','500100001964'])#向1001发送22 90 03拿到78再拿到正响应
        
    
        
    @allure.title("10服务_正响应_正响应抑制位2s不回复")
    @pytest.mark.full
    def test_caseid_aaa(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x82])
        sleep(5)
        result = (self.sd_tester.sd_tester.check_and_print_response_result())#校验返回值为空,有3E 80维持的话就是5s,没有就是3s
        assert result == None