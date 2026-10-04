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
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并自动激活路由
        self.doip_client.start_udp_connect()  # 建立UDP链接

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



    def after_each_func(self, ecu):
        sleep(3)#等待日志落盘
        self.doip_client.stop_udp_broadcast_connect()  # 关闭广播车辆公告
        self.cpp_case_lib.stop_uds_server()  # TODO 待优化点：如果不调用stop, 测试程序会一直等待或coredump
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        self.doip_client.doip_sock_obj.tcp_client_sock.stop()#关闭tcp链接
        self.doip_client.stop_udp_connect()  # 关闭UDP链接
        if self.diagd:
            stop_process(self.diagd)
        if self.obt_server:
            stop_process(self.obt_server)
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        self.json_obj.recover_json_data()
        super().after_class(self, ecu)

    @allure.title("doip_车辆vin码相关接口")
    @pytest.mark.full
    def test_caseid_1985740(self):
        vin = b"123456789ABCDEFGH"
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin)
        self.doip_client.doip_generate_service_0x0001(check_vin = vin.decode("utf-8"))#pythoy是str类型，c是char*把这个转成str
        
    @allure.title("doip_车辆vin码相关_少于17个字节补0")
    @pytest.mark.full
    def test_caseid_1988510(self):
        vin0 = b"123456789ABCDEFG"#少1个字节
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin0)
        self.doip_client.doip_generate_service_0x0001(check_vin = "123456789ABCDEFG0")
        vin2 = b"123456789"#少7个字节
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin2)
        self.doip_client.doip_generate_service_0x0001(check_vin = "12345678900000000")

    @allure.title("doip_车辆vin码相关_大于17个字节截断后面的")
    @pytest.mark.full
    def test_caseid_1988511(self):
        vin0 = b"123456789ABCDEFGHI"#多1个字节
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin0)
        self.doip_client.doip_generate_service_0x0001(check_vin = "123456789ABCDEFGH")
        vin2 = b"123456789ABCDEFGHIJK"#多3个字节
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin2)
        self.doip_client.doip_generate_service_0x0001(check_vin = "123456789ABCDEFGH")
        
    @allure.title("doip-电源power相关接口")
    @pytest.mark.full
    def test_caseid_1985738(self):
        self.cpp_case_lib.check_doip_power.argtypes = [ctypes.c_int]
        for i in range(3):
            assert 0 == self.cpp_case_lib.check_doip_power(i)
            self.doip_client.doip_generate_service_0x4003(check_mode = i)
            
    @allure.title("doip-电源power相关_设置超范围值")
    @pytest.mark.full
    def test_caseid_1988514(self):
        self.cpp_case_lib.check_doip_power.argtypes = [ctypes.c_int]
        assert 0 == self.cpp_case_lib.check_doip_power(2)
        sleep(0.5)
        assert -1 == self.cpp_case_lib.check_doip_power(4)
        self.doip_client.doip_generate_service_0x4003(check_mode = 2)
        
    @allure.title("0x4003&0x4004诊断电源模式_默认值0x00not_Ready")
    @pytest.mark.full
    def test_caseid_aaa(self):
        self.doip_client.doip_generate_service_0x4003(check_mode = 0)
        
    @allure.title("0x0002车辆识别请求(带EID)_EID匹配返回响应")
    @pytest.mark.full
    def test_caseid_1988515(self):
        self.doip_client.doip_generate_service_0x0002(eid = "020000001011", check_eid = "020000001011")
        
    @allure.title("0x0002车辆识别请求(带EID)_EID不匹配无响应")
    @pytest.mark.full
    def test_caseid_1988516(self):
        self.doip_client.doip_generate_service_0x0002(eid = "000000000000", check_eid = None)
        
    @allure.title("0x0003车辆识别请求(带VIN)_VIN不匹配无响应")
    @pytest.mark.full
    def test_caseid_1988518(self):
        self.doip_client.doip_generate_service_0x0003(vin = "123456789ABCDEFGH", check_eid = None)
        
    @allure.title("0x0003车辆识别请求(带VIN)_VIN匹配返回响应")
    @pytest.mark.full
    def test_caseid_1988520(self):
        self.doip_client.doip_generate_service_0x0003(vin = "00000000000000000", check_vin = "00000000000000000")
        
    @allure.title("0x0001车辆识别请求_正响应")
    @pytest.mark.full
    def test_caseid_1988523(self):
        self.doip_client.doip_generate_service_0x0001(check_logical_address=0x1001,
                                                      check_vin = "00000000000000000", 
                                                      check_eid = "020000001011", 
                                                      check_gid = "000000000001",
                                                      check_further_action_required = 00)
        
    @allure.title("0x8002诊断请求肯定响应_0x00")
    @pytest.mark.full
    def test_caseid_1988610(self):
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1001, diag_data = [0x10, 0x01], check_ack_code = 0x00)
        
    @allure.title("0x8003诊断请求负响应_0x02无效SA_关闭socket")
    @pytest.mark.full
    def test_caseid_1988611(self):
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0eA0, target_address = 0x1001, diag_data = [0x10, 0x01], check_nrc_code = 0x2)
        assert 0 == self.cpp_case_lib.get_connect_count(0)

    @allure.title("0x8003诊断请求负响应_0x03无效TA_TA不在路由表内_忽略报文")
    @pytest.mark.full
    def test_caseid_1988613(self):
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1006, diag_data = [0x10, 0x01], check_nrc_code = 0x3)
        assert 0 == self.cpp_case_lib.get_connect_count(1)
        
    @allure.title("0x8003诊断请求负响应_0x04诊断报文长度过长_超出target网段传输层协议最大支持长度_忽略报文")
    @pytest.mark.full
    def test_caseid_1988615(self):
        self.json_obj.update_json_data('$.DoIp[0].max_request_bytes', 2)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1006, diag_data = [0x10, 0x01], check_nrc_code = 0x4)
        assert 0 == self.cpp_case_lib.get_connect_count(1)
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x8003诊断请求负响应_0x06Target不可达")
    @pytest.mark.full
    def test_caseid_1988616(self):
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0eA0, target_address = 0x1001, diag_data = [0x10, 0x01], check_nrc_code = 0x6)#制造让1001不在线状态就可以
        assert 0 == self.cpp_case_lib.get_connect_count(1)
        
    @allure.title("UUdsServer_doip-诊断激活线相关_设置/获取诊断激活线状态")
    @pytest.mark.full
    def test_caseid_1985734(self):
        self.cpp_case_lib.set_get_activation_line.restype = ctypes.c_int
        assert 0 == self.cpp_case_lib.set_get_activation_line(0)
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1001, diag_data = [0x10, 0x01], except_relay_none =True)
        sleep(0.5)
        assert 0 == self.cpp_case_lib.set_get_activation_line(1)
        self.doip_client.doip_generate_service_0x8001(source_address = 0x0e80, target_address = 0x1001, diag_data = [0x10, 0x01], check_ack_code=0x00)
        
    @allure.title("0x4001&0x4002DoIP实体状态_edge_gateway网关")
    @pytest.mark.full
    def test_caseid_1988645(self):
        self.doip_client.doip_generate_service_0x4001(check_node_type=0,check_tcp_data_max_numer=10,check_now_tcp_data_open_number=1)
        
    @allure.title("0x4001&0x4002DoIP实体状态_gateway网关")
    @pytest.mark.full
    def test_caseid_1988646(self):
        self.json_obj.update_json_data('$.DoIp.doip_entity_type', 'gateway')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.doip_generate_service_0x4001(check_node_type=0,check_tcp_data_max_numer=10,check_now_tcp_data_open_number=1)
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x4001&0x4002DoIP实体状态_node节点")
    @pytest.mark.full
    def test_caseid_1988647(self):
        self.json_obj.update_json_data('$.DoIp.doip_entity_type', 'node')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.doip_generate_service_0x4001(check_node_type=1,check_tcp_data_max_numer=10,check_now_tcp_data_open_number=1)
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_0x0001车辆识别请求")
    @pytest.mark.full
    def test_caseid_1988720(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FF000100000000", send_type='udp', need_expect_type = [0x00], check_na_code=0x00)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_0x0002车辆识别请求(带EID)")
    @pytest.mark.full
    def test_caseid_1988722(self):
        self.doip_client.doip_send_raw_data(raw_data = "01FE000200000006020000001011", send_type='udp', need_expect_type = [0x00], check_na_code=0x00)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_0x0003车辆识别请求(带VIN)")
    @pytest.mark.full
    def test_caseid_1988724(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FF0003000000110102030405060708090A0B0C0D0E0F1011", send_type='udp', need_expect_type = [0x00], check_na_code=0x00)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_DoIP实体忽略接收到的首部否定响应报文")
    @pytest.mark.full
    def test_caseid_1988730(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD00000000000100", send_type='udp',except_relay_none=True)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_0x4001DoIP实体状态请求")
    @pytest.mark.full
    def test_caseid_1988726(self):
        self.doip_client.doip_send_raw_data(raw_data = "00FF0100000000", send_type='udp', need_expect_type = [0x00], check_na_code=0x00)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_0x4003诊断电源模式请求")
    @pytest.mark.full
    def test_caseid_aaa(self):
        self.doip_client.doip_send_raw_data(raw_data = "FF000300000000", send_type='udp', need_expect_type = [0x00], check_na_code=0x00)
        
    @allure.title("UDP_0x0000首部否定_0x00格式错误_DoIP实体忽略接收到的首部否定响应报文")
    @pytest.mark.full
    def test_caseid_1988730(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD00000000000100", send_type='udp', except_relay_none=True)
        
    @allure.title("TCP_0x0000首部否定_0x00格式错误_0x8001诊断指令_关闭socket")
    @pytest.mark.full
    def test_caseid_1988734(self):
        self.doip_client.doip_send_raw_data(raw_data = "02008001000000060E8010111001", send_type='tcp',except_relay_none=True)
        self.doip_client.check_tcp_client_connect_status(0)
        
    @allure.title("TCP_0x0000首部否定_0x00格式错误_0x0008在线检测响应_关闭socket")
    @pytest.mark.full
    def test_caseid_1988770(self):
        self.doip_client.doip_send_raw_data(raw_data = "02008001000000020E80", send_type='tcp',except_relay_none=True)
        self.doip_client.check_tcp_client_connect_status(0)
        
    @allure.title("TCP_0x0000首部否定_0x00格式错误_DoIP实体忽略接收到的首部否定响应报文")
    @pytest.mark.full
    def test_caseid_1988736(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD00000000000100", send_type='tcp',except_relay_none=True)
        self.doip_client.check_tcp_client_connect_status(1)
        
    @allure.title("UDP_0x0000首部否定_0x01未知负载类型_0x0001车辆识别请求_错误发送0x0009_忽略报文")
    @pytest.mark.full
    def test_caseid_1988738(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD00000000000900", send_type='udp', check_na_code=0x04, need_expect_type=[0x0000])
        
    @allure.title("UDP_0x0000首部否定_0x01未知负载类型_0x8001诊断指令_忽略报文")
    @pytest.mark.full
    def test_caseid_1988739(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd8001000000070e8010011001", send_type='udp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("UDP_0x0000首部否定_0x01未知负载类型_0x0005路由激活请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988740(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd0005000000070e800000000000", send_type='udp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("UDP_0x0000首部否定_0x01未知负载类型_0x0008在线检测响应")
    @pytest.mark.full
    def test_caseid_1988741(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd0008000000021001", send_type='udp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x8001诊断指令_错误发送0x8004_忽略报文")
    @pytest.mark.full
    def test_caseid_1988742(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd8004000000060e8010011001", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x0001车辆识别请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988746(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd000100000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x0002车辆识别请求(带EID)_忽略报文")
    @pytest.mark.full
    def test_caseid_1988748(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd000200000006020000001011", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
    
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x4001DoIP实体状态请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988752(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd400100000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x4003诊断电源模式请求_忽略报文")
    @pytest.mark.full
    def test_caseid_1988754(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd400300000000", send_type='tcp', need_expect_type = [0x0000],check_na_code=0x01)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x8002诊断正响应_忽略报文")
    @pytest.mark.full
    def test_caseid_1988756(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd80020000000510010e8000", send_type='tcp', except_relay_none=True)
        
    @allure.title("TCP_0x0000首部否定_0x01未知负载类型_0x8003诊断负响应_忽略报文")
    @pytest.mark.full
    def test_caseid_1988758(self):
        self.doip_client.doip_send_raw_data(raw_data = "02fd80030000000510010e8002", send_type='tcp', except_relay_none=True)
        
    @allure.title("0x0000首部否定_0x02报文过长_忽略报文")
    @pytest.mark.full
    def test_caseid_1988760(self):
        self.json_obj.update_json_data('$.DoIp.max_request_bytes', 3)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.doip_send_raw_data(raw_data = "02FD8001000003E9100210112E123400000000", send_type='tcp', need_expect_type = [0x0000], check_na_code=0x02)
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("UDP_0x0000首部否定_0x04无效的负载长度_0x0001车辆识别请求")
    @pytest.mark.full
    def test_caseid_1988761(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD000100000001", send_type='udp', need_expect_type = [0x0000], check_na_code=0x04)
        
    @allure.title("UDP_0x0000首部否定_0x04无效的负载长度_0x0002车辆识别请求(带EID)")
    @pytest.mark.full
    def test_caseid_1988762(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD000200000005020000001011", send_type='udp', need_expect_type = [0x0000], check_na_code=0x04)
        
    @allure.title("UDP_0x0000首部否定_0x04无效的负载长度_0x0003车辆识别请求(带VIN)")
    @pytest.mark.full
    def test_caseid_1988763(self):
        self.doip_client.doip_send_raw_data(raw_data= "02FD0003000000060102030405060708090A0B0C0D0E0F1011", send_type='udp', need_expect_type = [0x0000], check_na_code=0x04)
        
    @allure.title("UDP_0x0000首部否定_0x04无效的负载长度_0x4001DoIP实体状态请求")
    @pytest.mark.full
    def test_caseid_1988764(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD400100000001", send_type='udp', need_expect_type = [0x0000], check_na_code=0x04)
        
    @allure.title("UDP_0x0000首部否定_0x04无效的负载长度_0x4003诊断电源模式请求")
    @pytest.mark.full
    def test_caseid_1988765(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD400300000001", send_type='udp', need_expect_type = [0x0000], check_na_code=0x04)
        
    @allure.title("TCP_0x0000首部否定_0x04无效的负载长度_0x0005路由激活请求_关闭socket")
    @pytest.mark.full
    def test_caseid_1988766(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD0005000000060E8000FFFFFF", send_type='tcp', need_expect_type = [0x0000], check_na_code=0x04)
        self.doip_client.check_tcp_client_connect_status(False)
        
    @allure.title("TCP_0x0000首部否定_0x04无效的负载长度_0x0008在线检测响应_关闭socket")
    @pytest.mark.full
    def test_caseid_1988768(self):
        self.doip_client.doip_send_raw_data(raw_data = "02FD0008000000030E8000", send_type='tcp', need_expect_type = [0x0000], check_na_code=0x04)
        self.doip_client.check_tcp_client_connect_status(False)
        
    @allure.title("0x0007在线检测请求_全部为TCP_DATA达上限_新增TCP_DATA_原诊断仪均在线")#todo 超过max_tester_connections的值还是可以建链
    @pytest.mark.full
    def test_caseid_1988556(self):
        # self.json_obj.update_json_data('$.DoIp.max_tester_connections', 3)
        # self.json_obj.update_json_data('$.DoIp.tcp_general_inactivity_time', 30)
        add_data1 = {
            "addr": 3744,
            "link_type": "DOIP"
            }
        add_data2 = {
            "addr": 3760,
            "link_type": "DOIP"
            }
        add_data3 = {
            "addr": 3776,
            "link_type": "DOIP"
            }
        add_data4 = {
            "addr": 3745,
            "link_type": "DOIP"
            }
        raw_data = self.json_obj.init_json_data()
        raw_data['DiagConnection'][0]['connection'].append(add_data1)
        raw_data['DiagConnection'][0]['connection'].append(add_data2)
        raw_data['DiagConnection'][0]['connection'].append(add_data3)
        raw_data['DiagConnection'][0]['connection'].append(add_data4)
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.mock_relay_data_0x0008(0x0E80)
        self.doip_client.auto_handle_tcp_data()
        # time.sleep(2)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        # assert 1 == self.cpp_case_lib.get_connect_count()
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client1.mock_relay_data_0x0008(0x0EA0)
        self.doip_client1.auto_handle_tcp_data()
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0EA0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 1 == self.cpp_case_lib.get_connect_count()
        
        self.doip_client2 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client2.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client2.mock_relay_data_0x0008(0x0EB0)
        self.doip_client2.auto_handle_tcp_data()
        self.doip_client2.doip_generate_service_0x0005(source_address=0x0EB0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 2 == self.cpp_case_lib.get_connect_count()
        
        self.doip_client3 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client3.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client3.mock_relay_data_0x0008(0x0EC0)
        self.doip_client3.auto_handle_tcp_data()
        self.doip_client3.doip_generate_service_0x0005(source_address=0x0EC0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 3 == self.cpp_case_lib.get_connect_count()
        
        self.doip_client4 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client4.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client4.mock_relay_data_0x0008(0x0EA1)
        self.doip_client4.auto_handle_tcp_data()
        self.doip_client4.doip_generate_service_0x0005(source_address=0x0EA1, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 4 == self.cpp_case_lib.get_connect_count()
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x0007在线检测请求_不会给未路由激活的socket发送在线检测")
    @pytest.mark.full
    def test_caseid_1988558(self):
        self.json_obj.update_json_data('$.DoIp.max_tester_connections', 3)
        add_data1 = {
            "addr": 3744,
            "link_type": "DOIP"
            }
        add_data2 = {
            "addr": 3760,
            "link_type": "DOIP"
            }
        add_data3 = {
            "addr": 3776,
            "link_type": "DOIP"
            }
        raw_data = self.json_obj.init_json_data()
        raw_data['DiagConnection'][0]['connection'].append(add_data1)
        raw_data['DiagConnection'][0]['connection'].append(add_data2)
        raw_data['DiagConnection'][0]['connection'].append(add_data3)
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        time.sleep(1)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        assert 1 == self.cpp_case_lib.get_connect_count()
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0EA0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 2 == self.cpp_case_lib.get_connect_count()
        
        self.doip_client2 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client2.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client2.doip_generate_service_0x0005(source_address=0x0EB0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 3 == self.cpp_case_lib.get_connect_count()
        sleep(1)#未回复0008响应断连
        self.doip_client3 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client3.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client3.doip_generate_service_0x0005(source_address=0x0EC0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 3 == self.cpp_case_lib.get_connect_count()
        
    @allure.title("0x0007在线检测请求_不会给未路由激活的socket发送在线检测")
    @pytest.mark.full
    def test_caseid_1988560(self):
        time.sleep(1)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        assert 1 == self.cpp_case_lib.get_connect_count()
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0E80, check_res_code=0x10)#新的逻辑地址
        #中间看下怎么校验socket断连又重新连接的
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 1 == self.cpp_case_lib.get_connect_count()
        
    @allure.title("0x0008在线检测响应报文_主动发送重置tcp_general_inactivity_time")#后面可以在加一步重置了以后8s以后socket断连
    @pytest.mark.full
    def test_caseid_1988567(self):
        self.json_obj.update_json_data('$.DoIp.tcp_general_inactivity_time', 8)
        add_data = {
            "addr": 3744,
            "link_type": "DOIP"
            }
        raw_data = self.json_obj.init_json_data()
        raw_data['DiagConnection'][0]['connection'].append(add_data)
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        
        time.sleep(1)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        assert 1 == self.cpp_case_lib.get_connect_count()
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0EA0, check_res_code=0x10)#新的逻辑地址
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        time.sleep(1)
        assert 2 == self.cpp_case_lib.get_connect_count()
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        assert 0 == self.cpp_case_lib.setup_tcp_connect_count_cb(2)
        sleep(2)
        self.doip_client1.doip_send_raw_data(raw_data = "02FD0008000000030EA000", send_type='tcp')#0ea0发送0008在线响应报文
        sleep(4)
        self.doip_client1.doip_send_raw_data(raw_data = "02FD0008000000030EA000", send_type='tcp')#0ea0发送0008在线响应报文
        time.sleep(1)
        assert 2 == self.cpp_case_lib.get_connect_count()
        sleep(1)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        assert 0 == self.cpp_case_lib.setup_tcp_connect_count_cb(1)
        time.sleep(1)
        assert 1 == self.cpp_case_lib.get_connect_count()
        
    @allure.title("0x0008在线检测响应报文_主动发送重置tcp_general_inactivity_time")#后面可以在加一步重置了以后8s以后socket断连
    @pytest.mark.full
    def test_caseid_1988830(self):
        add_data1 = {
            "addr": 3744,
            "link_type": "DOIP"
            }
        add_data2 = {
            "addr": 3776,
            "link_type": "DOIP"
            }
        raw_data = self.json_obj.init_json_data()
        raw_data['DiagConnection'][0]['connection'].append(add_data1)
        raw_data['DiagConnection'][0]['connection'].append(add_data2)
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        # time.sleep(1)
        # self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        # assert 1 == self.cpp_case_lib.get_connect_count()
        self.doip_client.stop_3e_80_data()  
        self.doip_client.doip_generate_service_0x4001(check_now_tcp_data_open_number=1)
        self.doip_client1 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client1.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client1.doip_generate_service_0x0005(source_address=0x0EA0, check_res_code=0x10)#新的逻辑地址
        self.doip_client1.stop_3e_80_data()
        self.doip_client.doip_generate_service_0x4001(check_now_tcp_data_open_number=2)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        # time.sleep(1)
        # assert 1 == self.cpp_case_lib.get_connect_count()
        
        self.doip_client2 = ProtocolClientKeywords(uds_host="169.254.1.200", uds_port=13400)#初始化client端的teser
        self.doip_client2.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接并自动激活路由
        self.doip_client2.doip_generate_service_0x0005(source_address=0x0EB0, check_res_code=0x10)#新的逻辑地址
        self.doip_client.doip_generate_service_0x4001(check_now_tcp_data_open_number=3)
        self.cpp_case_lib.get_connect_count.restype = ctypes.c_int
        # time.sleep(1)
        # assert 2 == self.cpp_case_lib.get_connect_count()
        self.doip_client1.doip_sock_obj.tcp_client_sock.stop()#关闭tcp链接
        sleep(2)
        self.doip_client.doip_generate_service_0x4001(check_now_tcp_data_open_number=2)
        # self.doip_client2.stop_3e_80_data()
        # self.doip_client2.doip_send_raw_data(raw_data = "02fd0008000000020eb0", send_type='tcp')
        
        sleep(9)#等待0E80的socket的inactive_time超时10s
        self.doip_client2.stop_3e_80_data()
        self.doip_client2.doip_generate_service_0x4001(check_now_tcp_data_open_number=1)
        sleep(2)
        self.doip_client.doip_sock_obj.tcp_client_sock.stop()#关闭tcp链接
        sleep(11)#等待0E80的socket的inactive_time超时10s
        self.doip_client.check_tcp_client_connect_status(False)
        self.doip_client1.check_tcp_client_connect_status(False)
        self.doip_client2.check_tcp_client_connect_status(False)
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("未初始化调用set接口")#后面可以在加一步重置了以后8s以后socket断连
    @pytest.mark.full
    def test_caseid_1988829(self):
        self.cpp_case_lib.stop_uds_server()
        sleep(2)
        self.cpp_case_lib.get_set_jidu_flags.argtypes = [ctypes.c_uint8]
        self.cpp_case_lib.get_set_jidu_flags.restype = ctypes.c_int
        assert self.cpp_case_lib != None
        flags = 4  # bit2  doip网关tls功能开关：1表示启用，0表示关闭
        assert -1 == self.cpp_case_lib.get_set_jidu_flags(flags)
        vin = b"123456789ABCDEFGH"
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert -1 == self.cpp_case_lib.check_write_doip_vin(vin)