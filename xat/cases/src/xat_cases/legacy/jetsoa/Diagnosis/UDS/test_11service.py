"""
@filename     : test_11service.py
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
        self.cpp_case_lib.setup_session_ctrl_cb1(
            0x1001, 0x0E80, 0x3, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
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

    @allure.title("11服务_正响应_会话和安全密钥匹配")
    @pytest.mark.smoke
    def test_caseid_1985786(self):
        self.json_obj.update_json_data('$.EcuReset[1].access_permision[0]', 'AP_Comb_DE_UL11')
        self.restart_diagserver()
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1( 0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed),0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 注册拓展回话
        sleep(0.2)
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 这个参数的传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x11])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67,0x11,0x01,0x02,0x03]  # 检测到请求报文中包含的参数值超出了授权范围
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x12]  # 检测到请求报文中包含的参数值超出了授权范围
        self.sd_tester.send_data([0x11, 0x03])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = self.cpp_case_lib.check_ecu_reset_cb_result()
        assert 0 == result
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x51, 0x03]
        self.json_obj.recover_json_data()
        logger.info("恢复json数据")
        self.restart_diagserver()
        
    @allure.title("11服务_NRC33_解锁等级不匹配")
    @pytest.mark.full
    def test_caseid_1988053(self):
        self.json_obj.update_json_data('$.EcuReset[1].access_permision[0]', 'AP_Comb_DE_UL11')
        self.restart_diagserver()
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1( 0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed),0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 注册拓展回话
        sleep(0.2)
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 11服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x05])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67,0x05,0x01,0x02,0x03]  # 检测到请求报文中包含的参数值超出了授权范围
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x04, 0x05])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x67, 0x06]  # 检测到请求报文中包含的参数值超出了授权范围
        self.sd_tester.send_data([0x11, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x11, 0x33]
        assert -1 == self.cpp_case_lib.check_ecu_reset_cb_result()
        self.json_obj.recover_json_data()
        logger.info("恢复json数据")
        self.restart_diagserver()
        
    @allure.title("11服务_正响应_1101在不同会话下可执行")
    @pytest.mark.sanity
    def test_caseid_1988052(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 注册拓展回话
        sleep(0.2)
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 这个参数的传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x51, 0x01]
        assert 0 == self.cpp_case_lib.check_ecu_reset_cb_result()
        self.sd_tester.send_data([0x10, 0x02])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_ecu_reset_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x51, 0x01]
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50,0x01,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x11, 0x01])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_ecu_reset_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x51, 0x01]
        
    @allure.title("11服务_NRC33_未解锁")
    @pytest.mark.full
    @pytest.mark.bbb
    def test_caseid_1987646(self):
        self.json_obj.update_json_data('$.EcuReset[1].access_permision[0]', 'AP_Comb_DE_UL11')
        self.restart_diagserver()
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 11服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        sleep(0.2)
        self.sd_tester.send_data([0x11, 0x03])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x11, 0x33]
        self.json_obj.recover_json_data()
        logger.info("恢复json数据")
        self.restart_diagserver()

    @allure.title("11服务_NRC13_消息长度错误")
    @pytest.mark.sanity
    def test_caseid_1987644(self):
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 11服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x11, 0x01, 0x01])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x11, 0x13]
        
    @allure.title("11服务_NRC12_配置表中未规定的子服务")
    @pytest.mark.smoke
    def test_caseid_1985787(self):
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 11服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x11, 0x02])  # uds指令
        sleep(0.2)  # 如果有返回值建议等待超过500ms
        assert -1 == self.cpp_case_lib.check_ecu_reset_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7F, 0x11, 0x12]
        
    @allure.title("11服务_正响应_正响应抑制位5s不回复")
    @pytest.mark.smoke
    def test_caseid_1988494(self):
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 11服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x11, 0x81])  # uds指令
        self.sd_tester.stop_tester_present()
        sleep(3)
        assert 0 == self.cpp_case_lib.check_ecu_reset_cb_result()
        result = (self.sd_tester.sd_tester.check_and_print_response_result())#当前已经在02会话下,看的就是02下面的p2*值
        assert result == None
        
    @allure.title("11服务_正响应_正响应抑制位负响应立即回复")
    @pytest.mark.sanity
    @pytest.mark.bbb
    def test_caseid_1988497(self):
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 11服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x11, 0x83])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())  # 判断diagd的处理结果
        assert result == [0x7f, 0x11, 0x7E]
        assert -1 == self.cpp_case_lib.check_ecu_reset_cb_result()