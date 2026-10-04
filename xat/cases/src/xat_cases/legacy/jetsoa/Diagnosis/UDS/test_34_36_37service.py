"""
@filename     : test_31service.py
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
    diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export ENV_CONFIG_PATH=../../sotest/juds_demo/config/;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
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
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        sleep(0.2)

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
        
    @allure.title("37服务_NRC24_未发送34/36服务直接发送37服务")
    @pytest.mark.full
    def test_caseid_1987817(self):
        req_param_record_exp = b""
        resp_param_record_exp = b""
        self.cpp_case_lib.transfer_exit_cb1(
            0x1001,0x0E80,req_param_record_exp,len(req_param_record_exp),resp_param_record_exp,len(resp_param_record_exp),0)  # 37服务传参
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x37])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x37,0x24]
        assert -1 == self.cpp_case_lib.check_transfer_exit_cb_result()
        
    @allure.title("34服务_NRC7F_会话不满足要求") 
    @pytest.mark.sanity
    def test_caseid_1987920(self):
        memory_addr = b"\x00\xFF\x02\x02"
        memory_size = b"\x10\x00\x00\x00"
        self.cpp_case_lib.setup_request_download_cb1(0x1001, 0x0E80,0x00,0x44,
                                memory_addr,len(memory_addr),memory_size,len(memory_size),0,)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00, 0xff, 0x02, 0x02, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x34, 0x7F]
        assert -1 == self.cpp_case_lib.check_request_download_cb_result()
        
    @allure.title("34服务_NRC31_memoryAddress无效") 
    @pytest.mark.full
    def test_caseid_1987787(self):
        memory_addr = b"\xFF\xFF\x01\x01"
        memory_size = b"\x10\x00\x00\x00"
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001, 0x0E80,0x00,0x44,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0xFF, 0xFF, 0x01, 0x01, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = ( self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x34, 0x31]
        assert -1 == self.cpp_case_lib.check_request_download_cb_result()
        
    @allure.title("34服务_NRC33_未解密") 
    @pytest.mark.full
    def test_caseid_1987798(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        memory_addr = b"\x00\xFF\x02\x01"
        memory_size = b"\x10\x00\x00\x00"
        sleep(0.2)
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x44,memory_addr,len(memory_addr),memory_size,len(memory_size),0,)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00,0xFF, 0x02, 0x01, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x34, 0x33]
        
    @allure.title("34服务_NRC33_解密失败") 
    @pytest.mark.full
    def test_caseid_1988441(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x35)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        memory_addr = b"\x00\xFF\x02\x01"
        memory_size = b"\x10\x00\x00\x00"
        sleep(0.2)
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x44,memory_addr,len(memory_addr),memory_size,len(memory_size),0,)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x35]
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00,0xFF, 0x02, 0x01, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x34, 0x33]
        
    @allure.title("34服务_NRC13_消息长度小于5个字节") 
    @pytest.mark.full
    def test_caseid_1987781(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务传参
        sleep(0.2)
        memory_addr = b"\x00"
        memory_size = b"\x10"
        sleep(0.2)
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x12, memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x34, 0x00, 0x12, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result() )
        assert result == [0x7F, 0x34, 0x13]
        
    @allure.title("36服务_NRC13_请求下载小于3个byte") 
    @pytest.mark.full
    def test_caseid_1987860(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        sleep(0.2)
        memory_addr = b"\x00\x00\x00\x00"
        memory_size = b"\x10\x00\x00\x00"
        req_param_record = b""
        resp_param_record = b""
        sleep(0.2)
        result = self.cpp_case_lib.setup_transfer_data_cb1(0x1001,0x0E80,0x01,
            req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        data_ret = b"\x01\x02\x03"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        result = self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x44,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x01, 0x02, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x30, 0x08, 0x00, 0x00]
        self.sd_tester.send_data([0x36])  
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x36,0x13]
        self.sd_tester.send_data([0x36, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x36,0x13]
        
    @allure.title("36服务_NRC73_传输未按照01-FF顺序传输") 
    @pytest.mark.sanity
    def test_caseid_1987850(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        req_param_record = b"\x00"
        resp_param_record = b""
        result = self.cpp_case_lib.setup_transfer_data_cb1(0x1001,0x0E80,0x03,
            req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        data_ret = b"\x01\x02\x03"  
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        memory_addr = b"\x00\x00\x00\x00"
        memory_size = b"\x10\x00\x00\x00"
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x48,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x01, 0x02, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x30, 0x08, 0x00, 0x00]
        self.sd_tester.send_data([0x36, 0x03, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x36, 0x73]
        assert -1 == self.cpp_case_lib.check_transfer_data_cb_result()
           
    @allure.title("36服务_NRC31_transferRequestParameterRecord与requestDownload不匹配") 
    @pytest.mark.full
    def test_caseid_1988443(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        req_param_record = b"\x00\x00"
        resp_param_record = b""
        self.cpp_case_lib.setup_transfer_data_cb1(0x1001,0x0E80,0x01,
            req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        memory_addr = b"\xFF\x02\x03"#3-0bit
        memory_size = b"\x10\x00\x00"#7-4bit
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x33,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x34, 0x00, 0x33, 0xFF, 0x02, 0x03, 0x10, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x10, 0x03]
        self.sd_tester.send_data([0x36, 0x01, 0x00, 0x00])  
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x36,0x31]
        
    @allure.title("36服务_NRC24_未发送34服务直接发送36服务") 
    @pytest.mark.full
    def test_caseid_1987763(self):
        req_param_record = b"\x00\x00"
        resp_param_record = b"\x00\x00"
        self.cpp_case_lib.setup_transfer_data_cb1(
            0x1001,0x0E80,0x01,req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x36,0x01,0x00,0x00,0x00,0x00])  
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x36, 0x24]
        
    @allure.title("36服务_正响应_单次能够传输最大字节") 
    @pytest.mark.sanity
    def test_caseid_1988449(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        sleep(0.2)
        memory_addr = b"\xFF\x02\x03"#3-0bit
        memory_size = b"\x10\x00\x00"#7-4bit
        req_param_record = b"\x00"
        resp_param_record = b""
        sleep(0.2)
        result = self.cpp_case_lib.setup_transfer_data_cb1(0x1001,0x0E80,0x01,
            req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        result = self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x33,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x34, 0x00, 0x33, 0xFF, 0x02, 0x03, 0x10, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x10, 0x03]
        self.sd_tester.send_data([0x36, 0x01, 0x00])  
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x76,0x01]
        self.sd_tester.send_data([0x37])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x77]
        
    @allure.title("34服务_正响应_addressAndLengthFormatIdentifier参数匹配") 
    @pytest.mark.sanity
    def test_caseid_1988448(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        memory_addr = b"\x00\xFF\x02\x03"#3-0bit
        memory_size = b"\x10\x00\x00"#7-4bit
        req_param_record = b"\x00"
        resp_param_record = b""
        sleep(0.2)
        result = self.cpp_case_lib.setup_transfer_data_cb1(0x1001,0x0E80,0x01,
            req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        result = self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x34,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x34, 0x00, 0x34, 0x00, 0xFF, 0x02, 0x03, 0x10, 0x00, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x10, 0x03]