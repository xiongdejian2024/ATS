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


@allure.story("UdsServer_22")
class TestExampleAbstract(TestABCBase):
    def restart_diagserver(self):
        stop_process(self.obt_server)
        stop_process(self.diagd)
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        time.sleep(5)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.diagd = start_diagd()
        self.obt_server = start_obt()
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        time.sleep(5)
        
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
        # 启动obt server
        self.obt_server = start_obt()

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令

    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
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
        
    @allure.title("UdsServer_读写DID服务_2E22")
    @pytest.mark.full
    def test_caseid_1987758(self):
        data_exp = b"\x01\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD902, data_exp, len(data_exp), 0)#2e服务
        data_ret = b"\x01\x02"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xD902, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0x02, 0x01, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x6E, 0xd9, 0x02]
        self.sd_tester.send_data([0x22, 0xD9, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x62, 0xD9, 0x02, 0x01, 0x02]

    @allure.title("2E服务_NRC13_写入data少于一个字节")
    @pytest.mark.full
    def test_caseid_1987759(self):
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD904, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0x04])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x2E, 0x13]
        assert -1 == self.cpp_case_lib.check_write_did_cb_result()
        
    @allure.title("2E服务_NRC31_执行写入一个不存在的did")
    @pytest.mark.full
    def test_caseid_1987760(self):
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD922, data_exp, len(data_exp), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0x22, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x2E, 0x31]
        
    @allure.title("2E服务_正响应_写配置表中支持读写的did")
    @pytest.mark.sanity
    def test_caseid_1988209(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD903, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x01,0x00,0x32,0x01,0xf4]
        self.sd_tester.send_data([0x2E, 0xd9, 0x03, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x6E, 0xd9, 0x03]
        
    @allure.title("2E服务_NRC31_配置表中只读类型did进行写入")
    @pytest.mark.full
    def test_caseid_1988215(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xd9c0, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x01,0x00,0x32,0x01,0xf4]
        self.sd_tester.send_data([0x2E, 0xd9, 0xC0, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x2E, 0x31]
        
    @allure.title("2E服务_正响应_解锁等级匹配")
    @pytest.mark.sanity
    def test_caseid_1987762(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x00)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0x408f, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x27, 0x11])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x11, 0x01, 0x02, 0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x2E, 0x40, 0x8f, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x6E, 0x40, 0x8f]
        
    @allure.title("2E服务_NRC33_未解密")
    @pytest.mark.full
    def test_caseid_1988220(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0x408f, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x2E, 0x40, 0x8f, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x2e, 0x33]
        
    @allure.title("2E服务_NRC33_解密失败")
    @pytest.mark.full
    def test_caseid_1988221(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x00)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0x408f, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x27, 0x11])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x11, 0x01, 0x02, 0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x27, 0x13]
        self.sd_tester.send_data([0x2E, 0x40, 0x8f, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x2e, 0x33]
        
    @allure.title("2E服务_NRC33_解密等级不匹配")
    @pytest.mark.full
    def test_caseid_1988290(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x00)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xd916, data_exp, len(data_exp), 0)#2E服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x11])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x11, 0x01, 0x02, 0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x2E, 0xd9, 0x16, 0x02, 0x02, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x2e, 0x33]