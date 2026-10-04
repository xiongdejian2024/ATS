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
from xat_ecu.legacy.protocol.ProtocolClientKeywords import ProtocolClientKeywords
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords


def start_diagd():
    diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/mock_config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
    return start_process(diagd_cmd)


def stop_diagd(diagd_id):
    stop_process(diagd_id)

def start_obt():
    obt_server_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/mock_config/;export UDSDOIP_DATA_PATH=../../sotest/juds_demo/obt_server/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/juds_obt_server"
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
        self.dm_config_json_path = r'/root/wjj1/sat/sotest/juds_demo/mock_config/dm_config.json'
        self.json_obj = JsonModification(self.dm_config_json_path)
        # 启动diag
        self.diagd = start_diagd()
        # 启动obt server
        self.obt_server = start_obt()
        self.doip_client = None
        self.mock_server_obj = ProtocolServerKeywords(uds_host="172.18.1.27", remote_mock_server=True) #模拟服务端

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
        # self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        # self.sd_tester.send_data([0x10, 0x01])
        # self.sd_tester.session_ctrl_and_check()
        
        self.doip_client = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)
        sleep(0.2)

    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
        self.doip_client.doip_sock_obj.tcp_client_sock.stop()
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
        
        
    @allure.title("22服务_功能寻址_多客户端_请求单个did")
    @pytest.mark.full
    def test_caseid_aaa(self):
        # self.json_obj.update_json_data('$.ReadDataByIdentifier[0].access_permision[0]', 'AP_Comb_E')
        # logger.info("改完了重启diagserver")
        # self.restart_diagserver()
        self.mock_server_obj1 = ProtocolServerKeywords(uds_host="172.18.1.27", remote_mock_server=True) #模拟服务端
        self.mock_server_obj2 = ProtocolServerKeywords(uds_host="172.18.128.231", remote_mock_server=True) #模拟服务端
        self.mock_server_obj3 = ProtocolServerKeywords(uds_host="172.18.128.184", remote_mock_server=True) #模拟服务端
        self.mock_server_obj4 = ProtocolServerKeywords(uds_host="172.18.128.80", remote_mock_server=True) #模拟服务端
        self.mock_server_obj5 = ProtocolServerKeywords(uds_host="172.18.128.176", remote_mock_server=True) #模拟服务端
        self.doip_client.start_tcp_connect()
        mock_data = {
                0x1fff: {
                    0x10: {
                        0x01: ['7F78', '5001'],
                        0X02: ['7F11'],
                        0X03: ['500300000000'],
                        0X04: []
                    }
                    },
        #         0x1003: {
        #             0x10: {
        #                 0x01: ['7F78', '5001'],
        #                 0X02: ['7F11'],
        #                 0X03: ['500300000000'],
        #                 0X04: []
        #         }
        # },
            
        #         0x1023: {
        #             0x10: {
        #                 0x01: ['7F78', '5001'],
        #                 0X02: ['7F11'],
        #                 0X03: ['500300000000'],
        #                 0X04: []
        #         }
        # },
        #         0x1030: {
        #             0x10: {
        #                 0x01: ['7F78', '5001'],
        #                 0X02: ['7F11'],
        #                 0X03: ['500300000000'],
        #                 0X04: []
        #         }
        # },
        #         0x1031: {
        #             0x10: {
        #                 0x01: ['7F78', '5001'],
        #                 0X02: ['7F11'],
        #                 0X03: ['500300000000'],
        #                 0X04: []
        #         }
        # }
        }
        self.mock_server_obj1.doip_update_service_data_0x8001(mock_data)
        # self.mock_server_obj2.doip_update_service_data_0x8001(mock_data)
        # self.mock_server_obj3.doip_update_service_data_0x8001(mock_data)
        # self.mock_server_obj4.doip_update_service_data_0x8001(mock_data)
        # self.mock_server_obj5.doip_update_service_data_0x8001(mock_data)
        # data_ret = b"\x03"
        # did_num = (ctypes.c_short * 2)(0xF186, 0xf186)#把数据放入数组中,单个放入和校验
        # self.cpp_case_lib.max_read_did_cb1(0x1FFF, 0x0E80, did_num, 2, data_ret, len(data_ret), 0)
        # self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.doip_client.doip_generate_service_0x8001(target_address=0x1FFF, source_address=0x0e80, diag_data=[0x10, 0x03])
        time.sleep(20)
        # self.sd_tester.send_data([0x22, 0xf1, 0x86, 0xf1, 0x86])
        # sleep(0.2)
        # result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        # assert result == [0x62, 0xf1, 0x86,0x03, 0xf1, 0x86,0x03]
        # assert 0 == self.cpp_case_lib.check_read_did_max_result()