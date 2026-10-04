"""
@filename     : test_10service.py
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

cur_path = os.path.join(os.getcwd().split('sat')[0], 'sat')
sys.path.append(cur_path)
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
        #self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        time.sleep(5)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.diagd = start_diagd()
        self.obt_server = start_obt()
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(os.path.join(cur_path, "sotest/juds_demo/build/libtest_uds_app.so"))
        # self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # # call c++ function
        # assert 0 == self.cpp_case_lib.start_uds_server()
        time.sleep(5)
        
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.obt_server = None
        super().before_class(self, ecu)
        self.dm_config_json_path = os.path.join(cur_path, "sotest/juds_demo/config/dm_config.json")
        self.json_obj = JsonModification(self.dm_config_json_path)
        # 启动diag
        self.diagd = start_diagd()
        # 启动obt server
        self.obt_server = start_obt()
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary(os.path.join(cur_path, "sotest/juds_demo/build/libtest_uds_app.so"))
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        assert 0 == self.cpp_case_lib.start_uds_server()

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        if self.diagd:
            stop_process(self.diagd)
        if self.obt_server:
            stop_process(self.obt_server)
        sleep(3)#等待日志落盘
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.json_obj.recover_json_data()
        super().after_class(self, ecu)
        
    @allure.title("10服务_正响应_多次注册回调函数")
    @pytest.mark.sanity
    def test_caseid_1985668(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 第一次注册回调函数
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 第二次注册回调函数
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 第二次注册回调函数
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_session_ctrl_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]

    @allure.title("10服务_正响应_再次进入当前会话重置成功")
    @pytest.mark.sanity
    def test_caseid_1987652(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]  
        
    @allure.title("10服务_NRC13_消息长度错误")
    @pytest.mark.full
    def test_caseid_1987647(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01 ,0x01])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_session_ctrl_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x10, 0x13]
        
    @allure.title("10服务_NRC12_配置表中未规定的子服务")
    @pytest.mark.full
    def test_caseid_1987648(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x04, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x04])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_session_ctrl_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x10, 0x12]
        
    @allure.title("10服务_正响应_解锁后退出当前会话再次进入之前会话需要重新解锁")
    @pytest.mark.full
    def test_caseid_1987654(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0x408f, data_ret, len(data_ret), 0)#22服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0 )  # 注册编程回话
        
        data = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(
            0x1001, 0x0E80, 0x11, 0, data, len(data),out_seed,len(out_seed), 0
        )  # 27服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0x40, 0x8f, 0x03]
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x33]
        
    @allure.title("10服务_NRC7E_黑名单1002禁止1003")
    @pytest.mark.sanity
    def test_caseid_1987196(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 这个参数的传参
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x10,  0x7E]
        assert -1 == self.cpp_case_lib.check_session_ctrl_cb_result()
        
    @allure.title("10服务_正响应_会话超时")
    @pytest.mark.smoke
    def test_caseid_1986212(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.stop_tester_present()
        assert 0 ==self.cpp_case_lib.get_session(0x1001, 0x0E80, 0x03)
        sleep(3)
        assert 0 ==self.cpp_case_lib.get_session(0x1001, 0x0E80, 0x01)
        
    @allure.title("10服务_正响应_保持发送3e80不自动退出会话")
    @pytest.mark.full
    def test_caseid_1988502(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.stop_tester_present()
        sleep(1)
        assert 0 ==self.cpp_case_lib.get_session(0x1001, 0x0E80, 0x03)
        self.sd_tester.send_data([0x3E, 0x80])
        sleep(3)
        assert 0 ==self.cpp_case_lib.get_session(0x1001, 0x0E80, 0x03)
        
    @allure.title("10服务_正响应_初始值在01会话下_读只允许在03会话下的did")
    @pytest.mark.sanity
    def test_caseid_1988418(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[0].access_permision[0]', 'AP_Comb_E')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0x408f, data_ret, len(data_ret), 0)#普通22读did
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("10服务_正响应_初始值在01会话下_读只允许在02会话下的did")
    @pytest.mark.full
    def test_caseid_1988419(self):
        self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xd10c, data_ret, len(data_ret), 0)#普通22读did
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xd1, 0x0c])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x22, 0x41, 0xae])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0x41, 0xae, 0x03]
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("10服务_正响应_正响应抑制位2s不回复")
    @pytest.mark.full
    def test_caseid_1988487(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x82])
        self.sd_tester.stop_tester_present()
        result = (self.sd_tester.sd_tester.check_and_print_response_result())#当前已经在02会话下,看的就是02下面的p2*值
        assert result == None
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        
    @allure.title("10服务_正响应_正响应抑制位回复负响应")
    @pytest.mark.full
    def test_caseid_1988488(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x82])
        result = (self.sd_tester.sd_tester.check_and_print_response_result())#当前已经在02会话下,看的就是02下面的p2*值
        assert result == None
        self.sd_tester.send_data([0x10, 0x83])
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x10, 0x7E]
        assert -1 == self.cpp_case_lib.check_session_ctrl_cb_result()
        
    @allure.title("3E服务_正响应_正响应抑制位无回复")
    @pytest.mark.full
    def test_caseid_1988489(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.stop_tester_present()
        self.sd_tester.send_data([0x3e, 0x80])
        result = (self.sd_tester.sd_tester.check_and_print_response_result())#3e 80 不回复
        assert result == None