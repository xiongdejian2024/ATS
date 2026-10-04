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
        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        logger.info(f"function before run finished.")


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
        self.doip_client.start_tcp_connect(auto_activate_route=True, wait_start_time=0)  # 建立TCP链接并自动激活路由
        self.doip_client.start_udp_connect()  # 建立UDP链接



    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
        self.doip_client.stop_udp_broadcast_connect()  # 关闭广播车辆公告
        self.doip_client.stop_tcp_connect()#关闭tcp链接
        self.doip_client.stop_udp_connect()  # 关闭UDP链接
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
           
    @allure.title("0x0005路由激活请求_正响应_类型0x00")
    @pytest.mark.full
    def test_caseid_1988536(self):
        self.doip_client.stop_tcp_connect()#关闭tcp链接
        self.json_obj.update_json_data('$.DoIp.tcp_initial_inactivity_time', 5)
        self.restart_diagserver()
        logger.info("重启diagserver")
        self.doip_client.start_tcp_connect(auto_activate_route=False,wait_start_time=0) # 建立TCP链接
        logger.info("建链")
        sleep(4.9)
        logger.info("发指令")
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#激活路由
        #校验当前没有车辆公告
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x0005路由激活请求_正响应_类型0x01")
    @pytest.mark.full
    def test_caseid_1988537(self):
        self.doip_client.stop_tcp_connect()#关闭tcp链接
        self.doip_client.start_tcp_connect(auto_activate_route=False,wait_start_time=0) # 建立TCP链接
        logger.info("建链")
        sleep(9.9)
        logger.info("发指令")
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#需要给类型传参0x01
        
    @allure.title("0x0005路由激活请求_正响应_类型0xE0")
    @pytest.mark.full
    def test_caseid_1988538(self):
        self.doip_client.stop_tcp_connect()#关闭tcp链接
        self.doip_client.start_tcp_connect(auto_activate_route=False,wait_start_time=0) # 建立TCP链接
        logger.info("建链")
        sleep(9.9)
        logger.info("发指令")
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#需要给类型传参0xE0
        
    @allure.title("0x0005路由激活请求_正响应_重复路由激活")
    @pytest.mark.full
    def test_caseid_1988539(self):
        self.doip_client.stop_tcp_connect()#关闭tcp链接
        self.doip_client.start_tcp_connect(auto_activate_route=False,wait_start_time=0) # 建立TCP链接
        logger.info("建链")
        sleep(9.9)
        logger.info("发指令")
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#激活类型0x00
        logger.info("第一次激活类型为0x00")
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#需要给类型传参0x01
        logger.info("第一次激活类型为0x01")
        
    @allure.title("0x0005路由激活请求_负响应_0x00SA错误_关闭socket")
    @pytest.mark.full
    def test_caseid_1988540(self):
        self.doip_client.doip_generate_service_0x0005(source_address=0x0E81, check_res_code=0x00)#sa传参为错误地址
        self.doip_client.doip_generate_service_0x0005(except_relay_none=True)#再次发送路由激活无响应
        
    @allure.title("0x0005路由激活请求_负响应_0x01Socket达上限_关闭socket")
    @pytest.mark.full
    def test_caseid_1988544(self):
        self.json_obj.update_json_data('$.DoIp.max_tester_connections', 3)
        self.restart_diagserver()
        logger.info("重启diagserver")
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        logger.info("新的逻辑地址激活")
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0EA0, check_res_code=0x10)#新的逻辑地址
        self.doip_client1.stop_tcp_connect()#关闭tcp链接
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("TCP_0x0000首部否定_0x00格式错误_0x0005路由激活请求_关闭socket")
    @pytest.mark.full
    def test_caseid_1988732(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FF0005000000050E8000", send_type='tcp',need_expect_type = [0x00])
        self.doip_client.check_tcp_client_connect_status(0)