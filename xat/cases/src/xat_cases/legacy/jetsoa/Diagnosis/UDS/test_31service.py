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
        
    @allure.title("31服务_正响应_有routineStatusRecord值")
    @pytest.mark.sanity
    def test_caseid_1985670(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x02\x03"
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0206,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x06, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0x02, 0x06, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)
        
    @allure.title("31服务_NRC12_Rid仅支持01子服务")
    @pytest.mark.full
    def test_caseid_1987743(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b""
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0xa100,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0xa1, 0x00, 0x01, 0x02])
        sleep(0.2) 
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0xa1, 0x00]
        self.sd_tester.send_data([0x31, 0x03, 0xa1, 0x00])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result() )
        assert result == [0x7F, 0x31, 0x12]
        assert -1 == self.cpp_case_lib.check_routine_ctrl_cb_result(3)

    @allure.title("31服务_NRC13_数据长度不匹配")
    @pytest.mark.sanity
    def test_caseid_1987755(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x01\x02"
        result = self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0205,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x13]
        
    @allure.title("31服务_NRC31_会话与解锁等级都不匹配先判断会话")
    @pytest.mark.full
    def test_caseid_1988420(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x01\x02"
        result = self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x02,0x0208,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x08])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x31]
        assert -1 == self.cpp_case_lib.check_routine_ctrl_cb_result(2)
        
    @allure.title("31服务_NRC33_未解锁状态")
    @pytest.mark.sanity
    def test_caseid_1987756(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x01\x02"
        result = self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0208,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x08, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x33]
        
    @allure.title("31服务_NRC33_解锁等级不匹配")
    @pytest.mark.sanity
    def test_caseid_1988421(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x01\x02"
        result = self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x2044,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x05,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x06]
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0x44])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x33]

    @allure.title("31服务_正响应_无routineStatusRecord值")
    @pytest.mark.full
    def test_caseid_1985803(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b""
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0206,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x06, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0x02, 0x06]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)

    @allure.title("31服务_NRC31_Rid支持在01和03会话模式_当前在02会话")
    @pytest.mark.full
    def test_caseid_1985814(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b""
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0205,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x05, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x31]
        assert -1 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)
        
    @allure.title("31服务_NRC31_无效子服务")
    @pytest.mark.full
    def test_caseid_1988423(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b""
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0x0203,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x31,0x31]
        assert -1 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)