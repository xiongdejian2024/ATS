"""
@filename     : test_78service.py
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
from xat_ecu.legacy.protocol.ProtocolClientKeywords import ProtocolClientKeywords


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
        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        logger.info(f"function before run finished.")
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并自动激活路由
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x01], 
                                                      check_return_data=['5001003201F4'])

    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
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
        self.json_obj.recover_json_data()
        super().after_class(self, ecu)
    
    @allure.title("10服务_正响应_正响应抑制位78后回复负响应")
    @pytest.mark.full
    def test_caseid_1988500(self):
        # self.json_obj.update_json_data('$.dcm.Sessions[0].p2', 0)
        # logger.info("改完了重启diagserver")
        # self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.timeout_read_did_cb1(0x1001, 0x0E80, 0xd03a, data_ret, len(data_ret), 1, 0)#22服务
        self.cpp_case_lib.setup_session_ctrl_cb2(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x02], 
                                                      check_return_data=['500200190064'])
        # assert 0 == self.cpp_case_lib.check_session_ctrl_timeout_cb_result()
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0xd0, 0x3a], 
                                                      check_return_data=['7f2278','7f2231'])
        
    @allure.title("NRC78_超过配置表规定次数回复负响应")
    @pytest.mark.full
    def test_caseid_1988042(self):
        self.json_obj.update_json_data('$.Common.max_number_of_request_correctly_received_resp_pending', 4)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.timeout_read_did_cb1(0x1001, 0x0E80, 0xd005, data_ret, len(data_ret), 6, 0)#22服务
        self.cpp_case_lib.setup_session_ctrl_cb2(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x02], 
                                                      check_return_data=['500200190064'])
        # assert 0 == self.cpp_case_lib.check_session_ctrl_timeout_cb_result()
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0xd0, 0x05], 
                                                      check_return_data=['7f2278','7f2278','7f2278','7f2278','7f2210'])
        
    @allure.title("NRC78_01会话下超时回复78后回复正响应")
    @pytest.mark.full
    def test_caseid_1987774(self):
        data_ret = b"\x03"
        self.cpp_case_lib.timeout_read_did_cb1(0x1001, 0x0E80, 0x9003, data_ret, len(data_ret), 1, 0)
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0x90, 0x03], 
                                                      check_return_data=['7f2278','62900303'])#向1001发送22 90 03拿到78再拿到正响应
        assert 0 == self.cpp_case_lib.check_read_did_timeout_result()
        
    @allure.title("NRC78_02会话下超时回复78后回复正响应")
    @pytest.mark.full
    def test_caseid_1988031(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[4].access_permision', 'AP_Comb_P')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.timeout_read_did_cb1(0x1001, 0x0E80, 0xd005, data_ret, len(data_ret), 1, 0)
        self.cpp_case_lib.setup_session_ctrl_cb2(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x02], 
                                                      check_return_data=['500200190064'])
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0xd0, 0x05], 
                                                      check_return_data=['7f2278','62d00503'])#向1001发送22 90 03拿到78再拿到正响应
        assert 0 == self.cpp_case_lib.check_read_did_timeout_result()
        
    @allure.title("NRC78_02会话下超时回复78后回复负响应")
    @pytest.mark.full
    def test_caseid_1988038(self):
        self.json_obj.update_json_data('$.ReadDataByIdentifier[6].access_permision', 'AP_Comb_E')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        data_ret = b"\x03"
        self.cpp_case_lib.timeout_read_did_cb1(0x1001, 0x0E80, 0xd03a, data_ret, len(data_ret), 1, 0)
        self.cpp_case_lib.setup_session_ctrl_cb2(0x1001, 0x0E80, 0x02, 0)  # 10服务
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x10, 0x02], 
                                                      check_return_data=['500200190064'])
        self.doip_client.doip_generate_service_0x8001(target_address=0x1001,diag_data=[0x22, 0xd0, 0x3a], 
                                                      check_return_data=['7f2278','7f2231'])#向1001发送22 90 03拿到78再拿到正响应
        assert 0 == self.cpp_case_lib.check_read_did_timeout_result()
