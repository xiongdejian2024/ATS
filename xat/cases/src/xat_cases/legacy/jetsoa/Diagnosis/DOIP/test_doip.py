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

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_cases.legacy.jetsoa.case_helper.json_modification import *


def start_diagd():
    diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
    return start_process(diagd_cmd)


def stop_diagd(diagd_id):
    stop_process(diagd_id)


def start_obt():
    obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
    return start_process(obt_server_cmd)    


def stop_obt(obt_id):
    stop_process(obt_id)


@allure.feature("Demon")
@allure.story("UdsServer")
class TestExampleAbstract(TestABCBase):
    def restart_diagserver(self):
        stop_process(self.obt_server)
        stop_process(self.diagd)
        self.diagd = start_diagd()
        self.obt_server = start_obt()
        
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.obt_server = None
        super().before_class(self, ecu)
        self.dm_config_json_path = r'/root/wjj1/sat/sotest/juds_demo/config/dm_config.json'
        self.json_obj = JsonModification(self.dm_config_json_path)
        # 启动diag
        self.diagd = start_diagd()
        # diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
        # self.diagd = start_process(diagd_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_diagd.sh &")
        # 启动obt server
        self.obt_server = start_obt()
        # obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        # self.obt_server = start_process(obt_server_cmd)
        # os.system("/root/wjj1/sat/sotest/juds_demo/start_obt_server.sh &")

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(
            "/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so"
        )
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result

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
        self.json_obj.recover_json_data()
        super().after_class(self, ecu)

@allure.story("doip")
class Testdoip(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.obt_server = None
        super().before_class(self, ecu)
        self.nucapp = NucApp(self.tb_config)
        # 启动diag
        # diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
        # self.diagd = start_process(diagd_cmd)
        os.system("/root/wjj1/sat/sotest/juds_demo/start_diagd.sh &")
        # 启动obt server
        # obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
        # self.obt_server = start_process(obt_server_cmd)
        os.system("/root/wjj1/sat/sotest/juds_demo/start_obt_server.sh &")

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

    @allure.title("UdsServer_doip-电源power相关")
    @pytest.mark.full
    def test_caseid_1985738(self):
        self.cpp_case_lib.check_doip_power.argtypes = [ctypes.c_int]
        self.cpp_case_lib.check_doip_power.restype = ctypes.c_int
        result = self.cpp_case_lib.check_doip_power(1)
        assert 0 == result

    @allure.title("UdsServer_doip-车辆公告相关")
    @pytest.mark.full
    # "is_activation_line_dependent": false配置文件中这个值设置成false,不然车辆公告只能通过设置诊断激活线相关的接口才能获取
    def test_caseid_1985739(self):
        try:
            self.nucapp.start_nuc_tcpdump(interface="enp114s0")
            self.cpp_case_lib.check_doip_announcement.restype = ctypes.c_int
            result = self.cpp_case_lib.check_doip_announcement()
            assert 0 == result
            sleep(5)
        except Exception as e:
            logger.error(e)
        self.nucapp.stop_nuc_tcpdump()

    @allure.title("UdsServer_doip_集度标志位_obt防火墙关闭")
    @pytest.mark.full
    def test_caseid_1985952(self):
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
        flags = 0
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result

        # 诊断仪发送诊断请求
        # self.test_obt_app()
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 == result
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x51, 0x01]

    @allure.title("UdsServer_doip_集度标志位_obt防火墙打开")
    @pytest.mark.full
    def test_caseid_1985742(self):
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
        flags = 2
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result

        # 诊断仪发送诊断请求
        # self.test_obt_app()
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 != result
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x7F, 0x11, 0x22]
        flags = 0
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result

    @allure.title("UdsServer_doip_集度标志位_bit2tls功能开启")
    @pytest.mark.full
    def test_caseid_1985954(self):
        # int setup_ecu_reset_cb1(uint16_t server_addr, uint16_t client_addr, uint8_t reset_type,uint8_t ret_nrc)
        self.cpp_case_lib.setup_ecu_reset_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.cpp_case_lib.setup_ecu_reset_cb1(
            0x1001, 0x0E80, 0x1, 0x0 )  # 这个参数的传参
        flags = 4  # bit2  doip网关tls功能开关：1表示启用，0表示关闭
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result
        # 诊断仪发送诊断请求
        # self.test_obt_app()
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 == result
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x51, 0x01]
        flags = 0  # bit2  doip网关tls功能开关：1表示启用，0表示关闭
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result
        sleep(5)

    @allure.title("UdsServer_doip_集度标志位_未建链时bit2和3都置位")
    @pytest.mark.full
    def test_caseid_1985957(self):
        try:
            self.nucapp.start_nuc_tcpdump(interface="enp114s0")
            sleep(10)
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
            flags = 12  # bit2和3  doip网关tls功能开关：1表示启用，0表示关闭
            self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
            self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
            result = self.cpp_case_lib.get_set_jidu_flags(flags)
            assert 0 == result
            # 诊断仪发送诊断请求
            # self.test_obt_app()
            self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
            self.sd_tester.send_data([0x11, 0x01])
            sleep(0.2)
            result = self.cpp_case_lib.check_ecu_reset_cb_result()
            assert 0 != result
            flags = 0
            self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
            self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
            result = self.cpp_case_lib.get_set_jidu_flags(flags)
            assert 0 == result
            sleep(2)
        except Exception as e:
            logger.error(e)
        self.nucapp.stop_nuc_tcpdump()

    @allure.title("UdsServer_doip_集度标志位_bit3置位")
    @pytest.mark.full
    def test_caseid_1985958(self):
        # int setup_ecu_reset_cb1(uint16_t server_addr, uint16_t client_addr, uint8_t reset_type,uint8_t ret_nrc)
        self.cpp_case_lib.setup_ecu_reset_cb1.argtypes = [
            ctypes.c_uint16,
            ctypes.c_uint16,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        result = self.cpp_case_lib.setup_ecu_reset_cb1(
            0x1001, 0x0E80, 0x1, 0x0)  # 这个参数的传参
        flags = 8  # bit2和3  doip网关tls功能开关：1表示启用，0表示关闭
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result
        # 诊断仪发送诊断请求
        # self.test_obt_app()
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  #
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 == result
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )  # 判断diagd的处理结果
        assert result == [0x51, 0x01]
        flags = 0
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        result = self.cpp_case_lib.get_set_jidu_flags(flags)
        assert 0 == result

    @allure.title("UdsServer_doip-诊断激活线相关_获取doip层的tcp连接数量")
    @pytest.mark.full
    def test_caseid_1985733(self):
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        result = self.cpp_case_lib.get_connect_count(1)
        assert 0 == result
        sleep(5)

    @allure.title("UdsServer_doip-诊断激活线相关_设置TCP连接状态接口")
    @pytest.mark.full
    def test_caseid_1985735(self):
        status = 0
        self.cpp_case_lib.set_doip_tcp.argtypes = [ctypes.c_int]
        self.cpp_case_lib.set_doip_tcp.restype = ctypes.c_int
        result = self.cpp_case_lib.set_doip_tcp(status)
        assert 0 == result
        status = 1
        result = self.cpp_case_lib.set_doip_tcp(status)
        assert 0 == result
        