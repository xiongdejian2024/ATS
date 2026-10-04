"""
@filename     : test_22service.py
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
        
    @allure.title("22服务_NRC31_did仅支持02会话_当前为03,01会话")
    @pytest.mark.full
    def test_caseid_1987951(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0) # 10服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xd01c, data_ret, len(data_ret), 0)# 22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x22, 0xd0, 0X1c])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x01,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x22, 0xd0, 0X1c])
        sleep(0.2)
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        
    @allure.title("22服务_正响应_读多个DID")
    @pytest.mark.smoke
    def test_caseid_1987740(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 10)(0x41ae, 0x9003,0xcf05,0xd005,0xd03a,0xd09a,0xd0b5,0xd110,0xd134,0xd230)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 10, data_ret, len(data_ret), 0)#22读多个did
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x41, 0xae, 0x90,0x03,0xcf,0x05,0xd0,0x05,0xd0,0x3a,0xd0,0x9a,0xd0,0xb5,0xd1,0x10,0xd1,0x34,0xd2,0x30])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_read_did_max_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0x41, 0xae,0x03, 0x90,0x03,0x03,0xcf,0x05,0x03,0xd0,0x05,0x03,0xd0,0x3a,0x03,0xd0,0x9a,0x03,0xd0,0xb5,0x03,0xd1,0x10,0x03,0xd1,0x34,0x03,0xd2,0x30,0x03,]
    
    @allure.title("22服务_正响应_发送两个相同did")
    @pytest.mark.sanity
    def test_caseid_1987893(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 2)(0xF186, 0xf186)#把数据放入数组中,单个放入和校验
        result = self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 2, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xf1, 0x86, 0xf1, 0x86])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xf1, 0x86, 0x03, 0xf1, 0x86,0x03]
        assert 0 == self.cpp_case_lib.check_read_did_max_result()
        
    @allure.title("22服务_功能寻址_多客户端_请求单个did")
    @pytest.mark.full
    def test_caseid_1987966(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 2)(0xF186, 0xf186)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1FFF, 0x0E80, did_num, 2, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1FFF, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xf1, 0x86, 0xf1, 0x86])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xf1, 0x86,0x03, 0xf1, 0x86,0x03]
        assert 0 == self.cpp_case_lib.check_read_did_max_result()
        
    @allure.title("22服务_NRC13_超出配置表规定的最大did个数")
    @pytest.mark.sanity
    def test_caseid_1987892(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 11)(0x41ae, 0x9003,0xcf05,0xd005,0xd03a,0xd09a,0xd0b5,0xd110,0xd134,0xd230,0xf186)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.Exc_read_did_cb1(0x1001, 0x0E80, did_num, 11, data_ret, len(data_ret), 0)#22读多个did
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x41, 0xae, 0x90,0x03,0xcf,0x05,0xd0,0x05,0xd0,0x3a,0xd0,0x9a,0xd0,0xb5,0xd1,0x10,0xd1,0x34,0xd2,0x30,0xf1,0x86])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x13]
        assert 0 == self.cpp_case_lib.check_read_did_exc_result()
        
    @allure.title("22服务_NRC13_+无效did超出配置表规定的最大did个数")
    @pytest.mark.full
    def test_caseid_1987976(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 11)(0x41ae, 0x1234,0xcf05,0xd005,0xd03a,0xd09a,0xd0b5,0xd110,0xd134,0xd230,0xf186)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.Exc_read_did_cb1(0x1001, 0x0E80, did_num, 11, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x41, 0xae, 0x12,0x34,0xcf,0x05,0xd0,0x05,0xd0,0x3a,0xd0,0x9a,0xd0,0xb5,0xd1,0x10,0xd1,0x34,0xd2,0x30,0xf1,0x86])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x13]
        assert 0 == self.cpp_case_lib.check_read_did_exc_result()
        
    @allure.title("22服务_NRC31_多个did均为无效did")
    @pytest.mark.full
    def test_caseid_1987975(self):
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 3)(0x1234, 0x2234,0x3234)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 3, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x12, 0x34, 0x22, 0x34, 0x32, 0x34])
        sleep(0.2)
        assert -2 == self.cpp_case_lib.check_read_did_max_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x31] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        
    @allure.title("22服务_NRC13_少于3个byte")
    @pytest.mark.full
    def test_caseid_1987957(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xD1, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xD1])
        sleep(0.2)
        result = self.cpp_case_lib.check_read_did_cb_result()
        assert -1 == result  # 校验输入和输出是否是一致的
        result = (
            self.sd_tester.return_udsdata_and_check_and_print_response_result()
        )
        assert result == [
            0x7F,0x22,0x13,
        ]  # 该响应码表示由于诊断工具未能满足 ECU 的安全策略,所以请求的动作不能被执行
    
    @allure.title("22服务_NRC01_应用层给负响应")
    @pytest.mark.sanity
    def test_caseid_1987960(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xea41, data_ret, len(data_ret), 1)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xea, 0x41])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x22,0x01]
        assert 0 == self.cpp_case_lib.check_read_did_cb_result()
            
    @allure.title("22服务_正响应_多个did其中有无效did")
    @pytest.mark.sanity
    def test_caseid_1987961(self):
        data_ret = b"\x03"
        did_num_true = (ctypes.c_short * 2)(0x41ae, 0xfe80)#把数据放入数组中,单个放入和校验
        did_num_false= (ctypes.c_short * 2)(0x1234,0x2234)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.two_read_did_cb1(0x1001, 0x0E80, did_num_true, 2,did_num_false, 2, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0x41, 0xae, 0x12,0x34,0x22,0x34,0xfe,0x80])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_read_did_two_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0x41, 0xae,0x03,0xfe,0x80,0x03] 
        
    @allure.title("22服务_NRC33_多个did其中包含安全等级不通过")
    @pytest.mark.full
    def test_caseid_1987963(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 3)(0xd12f, 0xb163,0xf1ab)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 3, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x22, 0xd1, 0x2f, 0xb1,0x63, 0xf1,0xab])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x33] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        assert -2 == self.cpp_case_lib.check_read_did_max_result()
        
    @allure.title("22服务_NRC33_did解锁等级不匹配")
    @pytest.mark.full
    def test_caseid_1987986(self):
        data_ret = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  #10服务
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xb163, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x22, 0xb1, 0x63])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x33] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        
    @allure.title("22服务_正响应_did安全等级满足lv11")
    @pytest.mark.sanity
    def test_caseid_1987987(self):
        data_ret = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  #10服务
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0x408f, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
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
        assert 0 == self.cpp_case_lib.check_read_did_cb_result()
        
    @allure.title("22服务_正响应_did会话满足")
    @pytest.mark.smoke
    def test_caseid_1987988(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  #10服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xd911, data_ret, len(data_ret), 0)# 22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x22, 0xd9, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xd9, 0x11, 0x03]
        assert 0 == self.cpp_case_lib.check_read_did_cb_result()
            
    @allure.title("22服务_NRC13_did byte不为2的倍数")
    @pytest.mark.full
    def test_caseid_1987736(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xD12F, data_ret, len(data_ret), 0)#22服务did
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xD1, 0x2F, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x22,0x13]
        
    @allure.title("22服务_NRC33_did未满足解锁")
    @pytest.mark.full
    def test_caseid_1985813(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xD12F, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xD1, 0x2F])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x22,0x33]
        
    @allure.title("22服务_NRC31_读配置表中只写的did")
    @pytest.mark.full
    def test_caseid_1988203(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0x0)  #10服务
        data_ret = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xf102, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x02,0x00,0x19,0x00,0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.sd_tester.send_data([0x22, 0xf1, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x22,0x31]
        
    @allure.title("22服务_NRC31_did既不满足会话也不满足解密")
    @pytest.mark.full
    def test_caseid_1988226(self):
        data_ret = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0x0)  #10服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0x408f, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x02,0x00,0x19,0x00,0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x22,0x31]
        
    @allure.title("22服务_NRC31_did仅支持03会话_当前为02,01会话")
    @pytest.mark.full
    @pytest.mark.aaa
    def test_caseid_1987738(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[24].access_permision[0]', 'AP_Comb_E')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0x0)  #10服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0x408f, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xd9, 0X07])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xd9, 0X07])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("22服务_正响应_多个did其中有会话不相同")
    @pytest.mark.full
    @pytest.mark.aaa
    def test_caseid_1987962(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[3].access_permision[0]', 'AP_Comb_P')
        self.json_obj.update_json_data('$.ReadDataByIdentifier[4].access_permision[0]', 'AP_Comb_P')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 4)(0xcf05, 0xd005, 0xd134, 0xf186)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 4, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02, 0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xcf, 0x05, 0xd0,0x05,0xd1,0x34,0xf1,0x86])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xcf, 0x05, 0x03, 0xd0, 0x05, 0x03, 0xf1, 0x86, 0x03]
        assert 0 == self.cpp_case_lib.check_read_did_max_result()
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("22服务_NRC31_多个did不满足会话+无效did")
    @pytest.mark.full
    @pytest.mark.aaa
    def test_caseid_1987964(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[7].access_permision[0]', 'AP_Comb_E')
        self.json_obj.update_json_data('$.ReadDataByIdentifier[4].access_permision[0]', 'AP_Comb_P')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 4)(0xd09a, 0xd005,0x1234,0x2234)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 4, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x22, 0xd0, 0x9a, 0x22, 0x34, 0x12, 0x23, 0xd0, 0x05])
        sleep(0.2)
        assert -2 == self.cpp_case_lib.check_read_did_max_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x31] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("22服务_NRC31_多个did不满足会话")
    @pytest.mark.full
    @pytest.mark.aaa
    def test_caseid_1987965(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[7].access_permision[0]', 'AP_Comb_E')
        self.json_obj.update_json_data('$.ReadDataByIdentifier[6].access_permision[0]', 'AP_Comb_E')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        did_num = (ctypes.c_short * 3)(0xd09a, 0xd03a,0xd01c)#把数据放入数组中,单个放入和校验
        self.cpp_case_lib.max_read_did_cb1(0x1001, 0x0E80, did_num, 3, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x22, 0xd0, 0x9a, 0xd0, 0x3a, 0xd0, 0x1c])
        sleep(0.2)
        assert -2 == self.cpp_case_lib.check_read_did_max_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x31] #多个did中如果满足密码的需要,是所有的关于密码的did都需要满足条件
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("22服务_NRC31_did仅支持01会话_当前为03,02会话")
    @pytest.mark.full
    @pytest.mark.aaa
    def test_caseid_1987984(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[27].access_permision[0]', 'AP_Comb_D')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x1, 0x0)  #10服务
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xd916, data_ret, len(data_ret), 0)#22服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x22, 0xd9, 0X16])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x22, 0xd9, 0X16])
        sleep(0.2)
        assert -1 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x22, 0x31]
        self.json_obj.recover_json_data()
        self.restart_diagserver()