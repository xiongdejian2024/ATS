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
        
    @allure.title("27服务_NRC35/36/37_lv11延时时效未到重新发送27服务")
    @pytest.mark.full
    def test_caseid_1986266(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x35)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 10服务
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
        assert result == [0x7F, 0x27, 0x35]  # 对比key错误
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x36]  # 超过错误最大次数
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x37]  # 未到密码重置时间
        sleep(7)#未到错误时效时间
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x11])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x37]  # 未到密码重置时间
        sleep(3)#到了错误时效时间
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x11])  # 第四次重启
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x11,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        
    @allure.title("27服务_NRC24_未发送请求种子直接发送key")
    @pytest.mark.sanity
    def test_caseid_1986264(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1( 0x1001, 0x0E80, 0x02, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x27, 0x24]
        
    @allure.title("27服务_正响应_解锁成功后再次解锁seed返回000000")
    @pytest.mark.smoke
    def test_caseid_1986230(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
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
        assert result == [0x67, 0x02]
        assert 0 == self.cpp_case_lib.check_security_access_cb_result()
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x00,0x00,0x00]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x24]
        
    @allure.title("27服务_NRC12_请求配置表不存在的子服务")
    @pytest.mark.full
    def test_caseid_1985816(self):
        data_ret = b"\x03\x01\x02"
        result = self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0x0)  # 10服务
        sleep(0.2)
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x09, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4,]
        self.sd_tester.send_data([0x27, 0x09])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x27,0x12]
        assert -1 == self.cpp_case_lib.check_security_access_cb_result()

    @allure.title("27服务_NRC35/36/37_lv5错误次数超过配置表范围")
    @pytest.mark.full
    def test_caseid_1986009(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x35)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 10服务
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
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x35]  # 对比key错误
        self.sd_tester.send_data([0x27, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x05,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x36]  # 超过错误最大次数
        self.sd_tester.send_data([0x27, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x27, 0x37]  # 未到密码重置时间
        sleep(11)
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x05])  # 第四次重启
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x05,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x06]
        
    @allure.title("27服务_正响应_lv1keysize与seedsize和配置表中匹配")
    @pytest.mark.smoke
    def test_caseid_1988336(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
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
        assert result == [0x67, 0x02]
        assert 0 == self.cpp_case_lib.check_security_access_cb_result()
        
    @allure.title("27服务_NRC35/36/37_lv1错误次数和延时时效修改配置表范围校验")
    @pytest.mark.sanity
    def test_caseid_1988404(self):
        self.json_obj.update_json_data('$.dcm.SecurityLevel[0].num_failed', 3)
        self.json_obj.update_json_data('$.dcm.SecurityLevel[0].security_delay_time', 7)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        sleep(2)
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0x35)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
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
        assert result == [0x7f,0x27,0x35]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x35]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x36]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x37]
        assert 0 == self.cpp_case_lib.check_security_access_cb_result()
        sleep(7)
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.json_obj.recover_json_data()
        self.restart_diagserver()  
        
        
    @allure.title("27服务_NRC13_lv1seedsize和配置表中不匹配")
    @pytest.mark.sanity
    def test_caseid_1988365(self):
        data_ret = b"\x03\x04" 
        out_seed = b"\x01\x02"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]  
        data_ret = b"\x03\x04\x03\x04" 
        out_seed = b"\x01\x02\x03\x04"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]  
        
    @allure.title("27服务_NRC13_lv1keysize和配置表中不匹配")
    @pytest.mark.full
    def test_caseid_1988371(self):
        data_ret = b"\x03\x04" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x27, 0x13]
        assert -1 == self.cpp_case_lib.check_security_access_cb_result()
        data_ret = b"\x03\x04\x01\x02" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x04, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x27, 0x13]
        assert -1 == self.cpp_case_lib.check_security_access_cb_result()
        
    @allure.title("27服务_正响应_lv7keysize与seedsize和配置表中匹配")
    @pytest.mark.smoke
    def test_caseid_1988358(self):
        data_ret = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07" 
        out_seed = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x07,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.sd_tester.send_data([0x27, 0x08, 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06,0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x08]
        assert 0 == self.cpp_case_lib.check_security_access_cb_result()
        
    @allure.title("27服务_NRC13_lv7seedsize和配置表中不匹配")
    @pytest.mark.sanity
    def test_caseid_1988402(self):
        data_ret = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07" 
        out_seed = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]
        data_ret = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07" 
        out_seed = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]
        
    @allure.title("27服务_NRC13_lv7keysize和配置表中不匹配")
    @pytest.mark.full
    def test_caseid_1988401(self):
        data_ret = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06" 
        out_seed = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x27, 0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x07,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.sd_tester.send_data([0x27, 0x08, 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]
        assert -1 == self.cpp_case_lib.check_security_access_cb_result()
        data_ret = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08" 
        out_seed = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x07, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x07])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x07,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.sd_tester.send_data([0x27, 0x08, 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f,0x27,0x13]
        assert -1 == self.cpp_case_lib.check_security_access_cb_result()
        
    @allure.title("27服务_正响应_同时只能有一个安全等级处于解锁状态")
    @pytest.mark.smoke
    def test_caseid_1988340(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1( 0x1001, 0x0E80, 0x03, 0)  # 10服务
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
        self.sd_tester.send_data([0x27, 0x12, 0x03, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x12]
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0x40, 0x8f, 0x03]
        data_ret = b"\x03\x04\x05" #相同会话下解锁05后看11是否保持解锁状态
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.sd_tester.send_data([0x27, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x05,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x06, 0x03, 0x04, 0x05])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x06]
        self.sd_tester.send_data([0x22, 0x40, 0x8f])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7f, 0x22, 0x33]