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
import ssl
import socket

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_cases.legacy.jetsoa.case_helper.json_modification import *
from xat_ecu.legacy.protocol.ProtocolClientKeywords import ProtocolClientKeywords
from xat_ecu.legacy.socket.SocketData import SocketData


def start_diagd():
    diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/tls_config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
    return start_process(diagd_cmd)


def stop_diagd(diagd_id):
    stop_process(diagd_id)

def start_obt():
    obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/tls_config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
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
        self.dm_config_json_path = r'/root/wjj1/sat/sotest/juds_demo/tls_config/dm_config.json'
        self.json_obj = JsonModification(self.dm_config_json_path)
        # 启动diag
        self.diagd = start_diagd()
        # 启动obt server
        self.obt_server = start_obt()
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        assert 0 == self.cpp_case_lib.start_uds_server()
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        assert self.cpp_case_lib != None
        flags = 4  # bit2  doip网关tls功能开关：1表示启用，0表示关闭
        assert 0 == self.cpp_case_lib.get_set_jidu_flags(flags)
        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=3496)#初始化client端的teser
        logger.info(f"function before run finished.")
        self.doip_client.start_tcp_connect(auto_activate_route=False, after_connect=True)  # 稍后建链
        self.doip_client.doip_sock_obj.tcp_client_sock.ssl_communication = True #开启tls通信
        self.doip_client.doip_sock_obj.tcp_client_sock.set_ca_cert_file(certfile='/root/wjj1/sat/certs/client-cert.pem', 
                                                                        keyfile='/root/wjj1/sat/certs/client-key.pem', 
                                                                        ca_cert_file='/root/wjj1/sat/certs/ca-cert.pem')
        logger.info(f"开启tls通信")
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接
        # self.doip_client.start_udp_connect()  # 建立UDP链接

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)
        #  load c++ library
        # self.cpp_case_lib = ctypes.cdll.LoadLibrary("/root/wjj1/sat/sotest/juds_demo/build/libtest_uds_app.so")
        # self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # # call c++ function
        # result = self.cpp_case_lib.start_uds_server()
        # # check result
        # assert 0 == result



    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        self.json_obj.recover_json_data()
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        try:
            self.doip_client.doip_sock_obj.tcp_client_sock.stop()#关闭tcp链接
        except Exception as e:
            print(f"error:{e}")
        # self.doip_client.stop_udp_connect()  # 关闭UDP链接
        if self.diagd:
            stop_process(self.diagd)
        if self.obt_server:
            stop_process(self.obt_server)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.json_obj.recover_json_data()
        super().after_class(self, ecu)

    @allure.title("TLS_0x8002诊断请求肯定响应_0x00")
    @pytest.mark.full
    def test_caseid_1988713(self):
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1001, diag_data = [0x10, 0x01], check_ack_code = 0x00)
        
    @allure.title("TLS_UDP_0x0000首部否定_0x00格式错误_0x0001车辆识别请求")
    @pytest.mark.full
    def test_caseid_1988721(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FF000100000000", send_type='udp', need_expect_type = [0x0000])
        
    @allure.title("TLS_TCP_0x0000首部否定_0x00格式错误_0x0005路由激活请求_关闭socket")
    @pytest.mark.full
    def test_caseid_1988733(self):
        self.doip_client.doip_sock_obj.tcp_client_sock.stop()
        self.doip_client.start_tcp_connect(auto_activate_route= False)
        self.doip_client.doip_send_raw_data(raw_data = "02FF0005000000050E8000", send_type='tcp',need_expect_type = [0x00])
        self.doip_client.check_tcp_client_connect_status(0)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x00格式错误_0x8001诊断指令_关闭socket")
    @pytest.mark.full
    def test_caseid_1988735(self):
        SocketData.RECONNECT_TIME = 5
        self.doip_client.doip_send_raw_data(raw_data = "02008001000000060E8010111001", send_type='tcp',need_expect_type = [0x0000])
        print("等待1秒")
        time.sleep(1)
        self.doip_client.check_tcp_client_connect_status(0)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x00格式错误_0x0008在线检测响应_关闭socket")
    @pytest.mark.full
    def test_caseid_1988771(self):
        self.doip_client.doip_send_raw_data(raw_data = "02008001000000020E80", send_type='tcp',need_expect_type = [0x0000])
        self.doip_client.check_tcp_client_connect_status(0)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x00格式错误_DoIP实体忽略接收到的首部否定响应报文")
    @pytest.mark.full
    def test_caseid_1988737(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD00000000000100", send_type='tcp',except_relay_none=True)
        self.doip_client.check_tcp_client_connect_status(1)
    
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x8001诊断指令_错误发送0x8004_忽略报文")
    @pytest.mark.full
    def test_caseid_1988743(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd8004000000060e8010011001", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x0001车辆识别请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988745(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd000100000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x0002车辆识别请求(带EID)_忽略报文")
    @pytest.mark.full
    def test_caseid_1988747(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd000200000006020000001011", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x0003车辆识别请求(带VIN)_忽略报文")
    @pytest.mark.full
    def test_caseid_1988749(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd0003000000113030303030303030303030303030303030", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x4001DoIP实体状态请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988751(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd400100000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x4003诊断电源模式请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988753(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd400300000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x8002诊断正响应_忽略报文")
    @pytest.mark.full
    def test_caseid_1988755(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd80020000000510010e8000", send_type='tcp', except_relay_none=True)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x01未知负载类型_0x8003诊断负响应_忽略报文")
    @pytest.mark.full
    def test_caseid_1988757(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd80030000000510010e8002", send_type='tcp', except_relay_none=True)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x04无效的负载长度_0x0005路由激活请求_关闭socket")
    @pytest.mark.full
    def test_caseid_1988767(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD0005000000060E8000FFFFFF", send_type='tcp', need_expect_type = [0x0000], check_na_code=0x04)
        self.doip_client.check_tcp_client_connect_status(False)
        
    @allure.title("TLS_TCP_0x0000首部否定_0x04无效的负载长度_0x0008在线检测响应_关闭socket")
    @pytest.mark.full
    def test_caseid_1988769(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD0008000000030E8000", send_type='tcp', need_expect_type = [0x0000], check_na_code=0x04)
        self.doip_client.check_tcp_client_connect_status(False)