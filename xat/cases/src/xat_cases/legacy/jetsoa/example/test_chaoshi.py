#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : test_protocol.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/12 13:12
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
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
        diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
        self.diagd = start_process(diagd_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_diagd.sh &")
        # 启动obt server
        obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        self.obt_server = start_process(obt_server_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_obt_server.sh &")
        self.doip_client = None

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

        #  load c++ library
        # self.cpp_case_lib = ctypes.cdll.LoadLibrary(
        #     "../../sotest/juds_demo/build/libtest_uds_app.so"
        # )
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(
            "/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so"
        )
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        result = self.cpp_case_lib.start_uds_server()
        assert 0 == result

        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        logger.info(f"function before run finished.")

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

    @allure.title("UdsServer_建链后激活路由发送诊断1101，期望往返5101")
    @pytest.mark.full
    def test_caseid_00001(self):
        self.doip_client.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)  # 请求路由激活,检查返回肯定响应
        sleep(5)

        # 发送0x8001 后，检查积极响应0x8002的响应码和 返回数据0x51
        self.doip_client.doip_generate_service_0x8001(diag_data=[0x11, 0x01], check_return_data=['5101'])
        sleep(30)

        # 发送0x8001 后，检查否定响应0x8003的响应码
        self.doip_client.doip_generate_service_0x8001(diag_data=[0x11, 0x01], check_nrc_code=0x2)
        sleep(11)
    
    @allure.title("doip_建链后激活路由等待10s自动断链")
    @pytest.mark.full
    def test_caseid_1985966(self):
        self.doip_client.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接不自动激活路由
        self.doip_client.reset_tcp_sock_start_time()  #重新计算socket没断开开始的时间
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)  # 请求路由激活,检查返回肯定响应
        time.sleep(12)   #等待12秒等着服务端断开连接
        self.doip_client.check_tcp_sock_start_to_close_time(10) #检查socket从发送05路由激活到服务断开的时间为10秒
        sleep(2)