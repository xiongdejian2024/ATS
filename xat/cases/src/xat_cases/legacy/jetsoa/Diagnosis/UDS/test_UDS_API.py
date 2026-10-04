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
from xat_cases.legacy.jetsoa.case_helper.test_abc_base import TestABCBase
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
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
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
        self.dm_config_json_path = r'../../sotest/juds_demo/config/dm_config.json'
        self.json_obj = JsonModification(self.dm_config_json_path)
        # 启动diag
        self.diagd = start_diagd()
        # 启动obt server
        self.obt_server = start_obt()
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x54]

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
        
    @allure.title("读写DID服务_22接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1985676(self):
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xF1, 0x86])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xF1, 0x86, 0x03]
        
    @allure.title("读写DID服务_2E接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1985677(self):
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD904, data_exp, len(data_exp), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0x04, 0x02, 0x02, 0x02])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_write_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x6E, 0xd9, 0x04]
        
    @allure.title("UdsServer_自定义诊断服务_接口")
    @pytest.mark.smoke
    def test_caseid_1985731(self):
        data_ret = b"\x03\x01\x02"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1( 0x1001, 0x0E80, 0x05, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
        req_ret = b"\x03"
        resp_ret = b"\x03"
        sleep(0.2)
        self.cpp_case_lib.setup_custom_uds_cb1(0x1001, 0x0E80, 0x2F, req_ret, len(req_ret), resp_ret, len(resp_ret), 0)  # 自定义服务
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
        assert result == [0x67, 0x06]
        self.sd_tester.send_data([0x2F, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x6f]
        assert 0 == self.cpp_case_lib.check_custom_uds_cb_result()
        
    @allure.title("UdsServer_同进程同地址重复初始化")
    @pytest.mark.smoke
    def test_caseid_1985776(self):
        # int start_uds_server()
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        # check result
        assert 0 == self.cpp_case_lib.start_uds_server()
        self.cpp_case_lib.stop_uds_server()   
        
    @allure.title("会话控制服务_接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1985794(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x02, 0)  # 这个参数的传参
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02, 0x00, 0x19, 0x00, 0x64]
        assert 0 ==self.cpp_case_lib.get_session(0x1001, 0x0E80, 0x02)
        assert 0 == self.cpp_case_lib.check_session_ctrl_cb_result()
        
    @allure.title("ECU重启服务_接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1985650(self):
        self.cpp_case_lib.setup_ecu_reset_cb1(0x1001, 0x0E80, 0x1, 0x0)  # 注册11服务的回调函数可以注册多次,都是已最后一个为主
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")# 注明给谁发数据
        self.sd_tester.send_data([0x11, 0x01])#发送诊断指令
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_ecu_reset_cb_result()# 检测实际回调函数中的值和前期我预设的值是否是一致的
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x51, 0x01]#检测diagd的值
        
    @allure.title("安全等级解锁服务_27接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1988298(self):
        data_ret = b"\x03\x04\x05" 
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x11, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x03, 0)  # 10服务
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
        assert 0 == self.cpp_case_lib.check_security_access_cb_result()
        
    @allure.title("例程控制服务_接口_正响应")
    @pytest.mark.smoke
    def test_caseid_1987741(self):
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x02\x03"
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0xea, 0x29, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x03,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        self.sd_tester.send_data([0x31, 0x03, 0xea, 0x29])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x03, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(3)
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x02,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        self.sd_tester.send_data([0x31, 0x02, 0xea, 0x29])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x02, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(2)
        
    @allure.title("上传下载服务_接口_正响应")  # 暂时只会用34,36,37
    @pytest.mark.smoke
    def test_caseid_1985717(self):
        req_param_record_exp = b""
        resp_param_record_exp = b""
        self.cpp_case_lib.transfer_exit_cb1(0x1001,0x0E80,req_param_record_exp,len(req_param_record_exp),
                                            resp_param_record_exp,len(resp_param_record_exp),0 )  # 37服务传参
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x2, 0x0)  # 10服务传参
        data_ret = b"\x03\x04\x05"
        out_seed = b"\x01\x02\x03"
        self.cpp_case_lib.setup_security_access_cb1(0x1001, 0x0E80, 0x01, 0, data_ret, len(data_ret),out_seed,len(out_seed), 0)  # 27服务
        memory_addr = b"\x00\x00\x00\x00"
        memory_size = b"\x10\x00\x00\x00"
        self.cpp_case_lib.setup_request_download_cb1(
            0x1001,0x0E80,0x00,0x44,memory_addr,len(memory_addr),memory_size,len(memory_size),0)  # 34服务传参
        req_param_record = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        resp_param_record = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.cpp_case_lib.setup_transfer_data_cb1(
            0x1001,0x0E80,0x01,req_param_record,len(req_param_record),resp_param_record,len(resp_param_record),0)  # 36服务传参
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x02,  0x00, 0x19, 0x00, 0x64]
        self.sd_tester.send_data([0x27, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67,0x01,0x01,0x02,0x03]
        self.sd_tester.send_data([0x27, 0x02, 0x03, 0x02, 0x01])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x67, 0x02]
        self.sd_tester.send_data([0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_request_download_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x74, 0x30, 0x08, 0x00, 0x00]#一次可以传输多少数据对应是十进制524288也就是36可以接收这么多字节
        self.sd_tester.send_data(
            [0x36,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])  # 接收多少字节,字节中FF也可以,从01开始的
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_transfer_data_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x76, 0x01]
        self.sd_tester.send_data([0x37])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_transfer_exit_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x77]
        
    @allure.title("诊断事件相关_设置诊断事件状态回调_正响应")
    @pytest.mark.full
    def test_caseid_1985921(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.notify_event_status_cb1(Name, 0, 0)  # 这个参数的传参
        assert 0 == result
        
    @allure.title("诊断事件相关_获取诊断事件检测到故障的次数_正响应")
    @pytest.mark.full
    def test_caseid_1985919(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.get_fault_detection_counter(Name, 0)
        assert 0 == result
        
    @allure.title("诊断事件相关_获取诊断事件是否完成检查_正响应")
    @pytest.mark.full
    def test_caseid_1985918(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.get_test_complete(Name, 0)
        assert 0 == result
        
    @allure.title("诊断事件相关_获取诊断事件去抖动状态_正响应")
    @pytest.mark.full
    def test_caseid_1985913(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.get_debounce_status(Name, 0)
        assert 0 == result
        
    @allure.title("诊断事件相关_获取诊断事件关联的DTC编号_正响应")
    @pytest.mark.full
    def test_caseid_1985912(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.get_dtc_number(Name, 0, 333073)
        assert 0 == result
        
    @allure.title("诊断事件相关_获取诊断事件状态_正响应")
    @pytest.mark.full
    def test_caseid_1985753(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.get_event_staus(Name, 0)  # 这个参数的传参
        assert 0 == result

    @allure.title("诊断事件相关_设置/获取诊断事件警告指示器状态_正响应")
    @pytest.mark.full
    def test_caseid_1985899(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.wir_staus(Name)
        assert 0 == result
        
    @allure.title("诊断事件相关_注册/获取诊断事件警示指示器_正响应")
    @pytest.mark.full
    def test_caseid_1985922(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_notify_indicator_cb1(b"Warningindicator", 0)  # 注册警示指示器
        assert 0 == self.cpp_case_lib.setup_cycle( b"DEM_STRESS_TEST_000000", 0)  # 设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)  # 设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            sleep(0.1)
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)  # 上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)  # 7个bit的置位只检测bit0和3/获取诊断事件状态
        assert 0 == self.cpp_case_lib.get_indicator_type(b"Warningindicator", 2)  # 获取警示指示器
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        for i in range(8):
            logger.info(f"循环第: {i}次")#第一轮启动老化,警示器关闭
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        assert 0 == self.cpp_case_lib.get_indicator_type(b"Warningindicator", 0)  # 获取警示指示器
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        
    @allure.title("诊断事件上报_注册/上报诊断事件上报_正响应")
    @pytest.mark.full
    def test_caseid_1985924(self):
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.setup_init_monitor_reason_cb1(Name, 0)  # 注册诊断事件初始化监控原因回调
        assert 0 == result
        result = self.cpp_case_lib.report_monitor_action(Name, 0)  # 上报诊断事件监控行为
        assert 0 == result
        
    @allure.title("诊断事件条件控制_注册/上报诊断事件上报_正响应")
    @pytest.mark.full
    def test_caseid_1985762(self):
        self.cpp_case_lib.setup_get_condition.restype = ctypes.c_int
        Name = b"test_enable_condition_dtc_000000"
        result = self.cpp_case_lib.setup_get_condition(Name, 1)  # 这个参数的传参
        assert 0 == result
        result = self.cpp_case_lib.setup_get_condition(Name, 0)  # 这个参数的传参
        assert 0 == result
        
    @allure.title("诊断事件操作循环_设置/获取事件操作循环_正响应")
    @pytest.mark.full
    def test_caseid_1985761(self):
        Name = b"DEM_STRESS_TEST_000000"
        assert 0 == self.cpp_case_lib.setup_cycle(Name, 0)  # 设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.get_operation_cycle(Name, 0)  # 获取诊断事件操作循环类别
        
    @allure.title("诊断DTC相关接口_清除目标内存存储的DTC组_正响应")
    @pytest.mark.full
    def test_caseid_1985763(self):
        Name = b"TestMemory"
        result = self.cpp_case_lib.clear_dtc(Name, 7)  # 清除目标内存存储的DTC组
        assert 0 == result
        
    @allure.title("诊断DTC相关接口_获取目标内存存储的DTC数量_正响应")
    @pytest.mark.full
    def test_caseid_1985925(self):
        Name = b"PrimaryMemory"
        result = self.cpp_case_lib.get_num_of_stored_dtc_entry(Name, 0)  # 获取目标内存存储的DTC数量
        assert 0 == result
        
    @allure.title("诊断DTC相关接口_获取DTC当前状态_正响应")
    @pytest.mark.full
    def test_caseid_1985927(self):
        DTC = 333073
        result = self.cpp_case_lib.get_current_dtc_status(DTC, 0)  # 获取DTC当前状态
        assert 0 == result
        
    @allure.title("诊断DTC相关接口_设置/获取DTC控制使能_正响应")
    @pytest.mark.full
    def test_caseid_1985929(self):
        result = self.cpp_case_lib.dtc_ctrl_enable(0)  # 设置/获取DTC控制使能
        assert 0 == result