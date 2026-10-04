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
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并自动激活路由
        sleep(5)
        # int setup_session_ctrl_cb1(uint16_t server_addr_exp, uint16_t client_addr_exp, uint8_t session_exp, uint8_t ret_nrc);
        self.cpp_case_lib.setup_session_ctrl_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.setup_session_ctrl_cb1.restype = ctypes.c_int
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x01, 0
        )  # 这个参数的传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x10, 0x01])
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果("p2_star": 十进制6500=16进制的1964,6500x10ms(单位)=65000ms)
        assert result == [0x7F, 0x10, 0x78]
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果("p2_star": 十进制6500=16进制的1964,6500x10ms(单位)=65000ms)
        assert result == [0x50, 0x01, 0x00, 0x00, 0x19, 0x64]
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x01], 
                                                      check_return_data=['7f2278','500100001964'])#向1001发送22 90 03拿到78再拿到正响应
        
    @allure.title("UdsServer_78延时保持_默认回话下0x22超时78")
    @pytest.mark.full
    def test_caseid_1987774(self):
        # int setup_read_did_cb1(uint16_t server_addr_exp, uint16_t client_addr_exp, uint16_t did_exp,
        # const unsigned char* data_ret, int data_ret_len, uint8_t ret_nrc)
        
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并自动激活路由
        sleep(5)
        self.cpp_case_lib.timeout_read_did_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.timeout_read_did_cb1.restype = ctypes.c_int
        data_ret = b"\x03"
        result = self.cpp_case_lib.timeout_read_did_cb1(
            0x1001, 0x0E80, 0x9003, data_ret, len(data_ret), 0,1)
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0x90, 0x03], 
                                                      check_return_data=['7f2278','62900303'])#向1001发送22 90 03拿到78再拿到正响应
        result = self.cpp_case_lib.check_read_did_timeout_result()
        assert 0 == result  # 校验python中输入和c++中输出是否是一致的
        
    @allure.title("22服务_正响应_多个did其中有会话不相同")# todo c++那边判断条件写的不对
    @pytest.mark.full
    def test_caseid_1987962(self):
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x2, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 4)(0xcf05, 0xd005,0xd134,0xf186)#把数据放入数组中,单个放入和校验
        result = self.cpp_case_lib.max_read_did_cb1(
            0x1001, 0x0E80, did_num, 4, data_ret, len(data_ret), 0
        )#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xcf, 0x05, 0xd0,0x05,0xd1,0x34,0xf1,0x86])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        # result = self.cpp_case_lib.check_read_did_max_result()
        # assert 0 == result  # 校验输入和输出是否是一致的

        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x62, 0xcf, 0x05,0x03,0xd0,0x05,0x03,0xf1,0x86,0x03]
        
    @allure.title("22服务_NRC31_多个did不满足会话+无效did")
    @pytest.mark.full
    def test_caseid_1987964(self):
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 4)(0xd09a, 0xd005,0x1234,0x2234)#把数据放入数组中,单个放入和校验
        result = self.cpp_case_lib.max_read_did_cb1(
            0x1001, 0x0E80, did_num, 4, data_ret, len(data_ret), 0
        )
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50, 0x01, 0x00, 0x00, 0x19, 0x64]
        self.sd_tester.send_data([0x22, 0xd0, 0x9a, 0x22, 0x34, 0x12, 0x23, 0xd0, 0x05])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_max_result()
        assert -2 == result  # 校验输入和输出是否是一致的
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7f, 0x22, 0x31] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        
    @allure.title("22服务_NRC31_多个did不满足会话")
    @pytest.mark.full
    def test_caseid_1987965(self):
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 3)(0xd09a, 0xd03a,0xd01c)#把数据放入数组中,单个放入和校验
        result = self.cpp_case_lib.max_read_did_cb1(
            0x1001, 0x0E80, did_num, 3, data_ret, len(data_ret), 0
        )
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50, 0x01, 0x00, 0x00, 0x19, 0x64]
        self.sd_tester.send_data([0x22, 0xd0, 0x9a, 0xd0, 0x3a, 0xd0, 0x1c])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_max_result()
        assert -2 == result  # 校验输入和输出是否是一致的
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7f, 0x22, 0x31] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        
    @allure.title("22服务_NRC31_did仅支持03会话_当前为02,01会话")
    @pytest.mark.full
    def test_caseid_1987738(self):
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(
            0x1001, 0x0E80, 0xd907, data_ret, len(data_ret), 0
        )#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x01], 
                                                      check_return_data=['7f2278','5001003201f4'])#向1001发送22 90 03拿到78再拿到正响应
        self.sd_tester.send_data([0x22, 0xd9, 0X07])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == result  # 校验输入和输出是否是一致的

        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x10, 0x02])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xd9, 0X07])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == result  # 校验输入和输出是否是一致的

        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7F, 0x22, 0x31]
        
    @allure.title("22服务_NRC31_did仅支持01会话_当前为03,02会话")
    @pytest.mark.full
    def test_caseid_1987984(self):
        result = self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(
            0x1001, 0x0E80, 0xd916, data_ret, len(data_ret), 0
        )#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x22, 0xd9, 0X16])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == result  # 校验输入和输出是否是一致的

        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x10, 0x02])  # uds指令
        sleep(0.2)
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xd9, 0X16])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == result  # 校验输入和输出是否是一致的
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7F, 0x22, 0x31]