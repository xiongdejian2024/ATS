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
    
    @allure.title("Doip_建链后路由未激活等待5s后自动断链") 
    @pytest.mark.full
    def test_caseid_1985965(self):
        self.json_obj.update_json_data('$.DoIp.tcp_initial_inactivity_time', 5)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接
        logger.info("建链开始")
        sleep(5)
        self.doip_client.check_tcp_sock_start_to_close_time(check_time=5, offset=1)
        self.json_obj.recover_json_data()
        self.restart_diagserver()   

    @allure.title("UdsServer_建链后激活路由等待10s自动断链")  
    @pytest.mark.full
    def test_caseid_1985966(self):#激活后有3e80一直在发送导致无法断链
        self.doip_client.start_tcp_connect(auto_activate_route=True)  # 建立TCP链接并路由激活
        sleep(2)
        self.doip_client.keep_session_flag = False
        sleep(15)
        logger.info("等待15s")
        self.doip_client.check_tcp_sock_start_to_close_time(check_time=15, offset=1) 
        
    @allure.title("Doip_车辆公告下发次数以及间隔时间")
    @pytest.mark.full
    def test_caseid_1986190(self):
        self.json_obj.update_json_data('$.DoIp.vehicle_announcement_count', 10)
        self.json_obj.update_json_data('$.DoIp.vehicle_announcement_interval', 2)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(25)
        self.doip_client.check_vehicle_broadcast_interval_and_times(check_time_interval=2, check_times=10, specify_time=25, times_offset=1)#我检测的时间是25s，间隔时间是2s，总共检测10次,日志打印了9次,校验失败显示收到了0次
        self.doip_client.stop_udp_broadcast_connect()  # 关闭广播车辆公告
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x0004车辆信息声明_路由激活后不再发送车辆声明")
    @pytest.mark.full
    def test_caseid_1988533(self):
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        self.doip_client.start_tcp_connect(auto_activate_route=False)  # 建立TCP链接
        sleep(5)
        self.doip_client.check_vehicle_broadcast_interval_and_times(check_time_interval=1, check_times=4, specify_time=4, times_offset=1)
        self.doip_client.doip_generate_service_0x0005(check_res_code=0x10)#激活路由
        sleep(2)
        self.doip_client.check_vehicle_broadcast_interval_and_times(check_time_interval=0, check_times=0, specify_time=2)#校验当前无车辆公告
        sleep(2)
        
    @allure.title("0x0004车辆信息声明_EID未配置")
    @pytest.mark.full
    def test_caseid_1988532(self):
        raw_data1 = self.json_obj.init_json_data()#获取原始数据
        del raw_data1['DoIp']['eid']#删除eid配置
        self.json_obj.update_json_data(own_data=raw_data1)#更新配置文件
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_eid = "000000000000")
        self.doip_client.stop_udp_broadcast_connect()  # 关闭广播车辆公告
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x0004车辆信息声明_GID未配置")
    @pytest.mark.full
    def test_caseid_1988531(self):
        raw_data1 = self.json_obj.init_json_data()#获取原始数据
        del raw_data1['DoIp']['gid']#删除eid配置
        self.json_obj.update_json_data(own_data=raw_data1)#更新配置文件
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_gid = "000000000000")
        self.doip_client.stop_udp_broadcast_connect()  # 关闭广播车辆公告
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("0x0004车辆信息声明_周期发送过程中配置VIN")
    @pytest.mark.full
    def test_caseid_1988530(self):
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_vin = "00000000000000000")#校验vin
        sleep(2)
        vin = b"123456789ABCDEFGH"
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin)
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_vin = "123456789ABCDEFGH")#设置完后校验新的vin
        
    @allure.title("0x0004车辆信息声明_启动后以vehicle_announcement_interval发送vehicle_announcement_count次_已配置VIN")
    @pytest.mark.full
    def test_caseid_1988529(self):
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        vin = b"123456789ABCDEFGH"
        self.cpp_case_lib.check_write_doip_vin.argtypes = [ctypes.c_char_p]#传进来的vin码是什么类型
        assert 0 == self.cpp_case_lib.check_write_doip_vin(vin)
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_vin = "123456789ABCDEFGH")
        
    @allure.title("0x0004车辆信息声明_启动后以vehicle_announcement_interval发送vehicle_announcement_count次_未配置VIN")
    @pytest.mark.full
    def test_caseid_1988527(self):
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_vin = "00000000000000000")
        
    @allure.title("0x0004车辆信息声明_启动后以vehicle_announcement_interval发送vehicle_announcement_count次_未配置VIN")
    @pytest.mark.full
    def test_caseid_1988527(self):
        self.doip_client.start_udp_broadcast_connect()  # 建立广播车辆公告链接
        sleep(2)
        self.doip_client.check_current_udp_broadcast_data(check_vin = "00000000000000000")
        
