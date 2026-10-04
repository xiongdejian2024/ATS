#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     : test_example_new.py
@time         : 2024/06/07 14:19
@author       : quan.sun@jiduauto.com
@description  : doip 采取手动控制方式
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
from xat_ecu.legacy.sdk.ethernet.doip_client_sim_odx import Doip_Client_Sim_Odx


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
        diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
        self.diagd = start_process(diagd_cmd)
        # 启动obt server
        obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        self.obt_server = start_process(obt_server_cmd)


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

        self.doip_client = Doip_Client_Sim_Odx(ecu="BGM", server_doip_id=0x1001, server_ip="169.254.1.200", server_port=13400, auto_flag=False)

    def after_each_func(self, ecu):
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        self.doip_client.close()
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
        

    @allure.title("UdsServer_ECU重启服务_01")
    @pytest.mark.smoke
    def test_caseid_001(self):
        # int setup_ecu_reset_cb1(uint16_t server_addr, uint16_t client_addr, uint8_t reset_type,uint8_t ret_nrc)
        self.cpp_case_lib.setup_ecu_reset_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        result = self.cpp_case_lib.setup_ecu_reset_cb1(
            0x1001, 0x0E80, 0x1, 0x0
        )  # 这个参数的传参

        # 诊断仪发送诊断请求
        
        self.doip_client.run()  #  建立TCP链接
        self.doip_client.routing_act()  # 请求路由激活
        self.doip_client.send_data([0x11, 0x01])
        sleep(1)
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 == result
        result1, result2 = self.doip_client.retrun_udsdata_and_check_response() # 判断diagd的处理结果
        assert result2 == [0x51, 0x01]

  