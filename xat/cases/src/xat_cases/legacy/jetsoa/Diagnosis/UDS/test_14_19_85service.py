"""
@filename     : test_14_19_85service.py
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
    diagd_cmd = "JUDS_OUT_DIR=../../CarinaX86_64;UDS_LOG_DIR=../../sotest/juds_demo/log/;export UDSDOIP_CONFIG_PATH=../../sotest/juds_demo/config/;export JUDS_LOG_DIR=$UDS_LOG_DIR;export ENV_CONFIG_PATH=/root/wjj1/sat/sotest/juds_demo/config/;export LD_LIBRARY_PATH=$JUDS_OUT_DIR/lib;$JUDS_OUT_DIR/bin/jetdiagd"
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
        time.sleep(5)
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
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x3, 0x0)  # 10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x01])  # uds指令
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x54]
        
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
        
    @allure.title("85服务_正响应_控制DTC控制使能")
    @pytest.mark.smoke
    def test_caseid_1987131(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])  # uds指令进入编程回话
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50,0x03,0x00,0x32,0x01,0xF4]
        self.sd_tester.send_data([0x85, 0x02])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x02]
        assert 0 == self.cpp_case_lib.getdtc_ctrl_enable(0)#获取DTC控制使能为关
        self.sd_tester.send_data([0x85, 0x01])  # uds指令设置使能on
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x01]
        assert 0 == self.cpp_case_lib.getdtc_ctrl_enable(1)#获取DTC控制使能为开
        
    @allure.title("85服务_NRC7F_会话模式不满足当前不为03会话")
    @pytest.mark.full
    def test_caseid_1988451(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x85, 0x02])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x7F]
        self.sd_tester.send_data([0x85, 0x01])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x7F]
        self.json_obj.update_json_data('$.ControlDtcSetting[0].access_permision[0]', 'AP_Comb_DE')
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.sd_tester.send_data([0x85, 0x02])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x02]
        assert 0 == self.cpp_case_lib.getdtc_ctrl_enable(0)#获取DTC控制使能为关
        self.json_obj.recover_json_data()
        self.restart_diagserver()
        
    @allure.title("85服务_NRC12_不支持子服务")
    @pytest.mark.full
    def test_caseid_1988452(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x85, 0x00])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x12] 
        
    @allure.title("85服务_NRC13_消息长度不符合")
    @pytest.mark.full
    def test_caseid_1988453(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x85])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x13]
        
    @allure.title("19服务_NRC13_消息长度不匹配")#最大长度校验未做限制
    @pytest.mark.sanity
    def test_caseid_1988465(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x19, 0x02])  # uds指令清除DTC
        sleep(0.2)
        assert [0x7F, 0x19, 0x13] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("85服务_NRC31_DTCSettingControlOptionRecord数据错误_不满足3个byte")#三个ff是代表dtc的状态是全部关闭
    @pytest.mark.sanity
    def test_caseid_1988454(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x85, 0x02, 0xFF])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x31]
        self.sd_tester.send_data([0x85, 0x02, 0xFF, 0xFF, 0xFF, 0xFF])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x31]
        
    @allure.title("85服务_正响应_DTCSettingControlOptionRecord满足3个byte且任意值为FF")#三个ff是代表dtc的状态是全部关闭
    @pytest.mark.sanity
    def test_caseid_1988455(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x85, 0x02, 0xFF, 0xFF, 0xFF])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x02]
        self.sd_tester.send_data([0x85, 0x01, 0xFF, 0x00, 0x00])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x01]
        self.sd_tester.send_data([0x85, 0x02, 0x00, 0xFF, 0xFF])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0xc5,0x02]
        
    @allure.title("85服务_NRC31_DTCSettingControlOptionRecord数据错误_不满足3个byte都不为FF")#三个任意值为f即可
    @pytest.mark.full
    def test_caseid_1988456(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x10, 0x03])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4]
        self.sd_tester.send_data([0x85, 0x02, 0x00, 0x00, 0x00])  # uds指令设置使能off
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F, 0x85, 0x31]
        
    @allure.title("14服务_正响应_当前无储存DTC服务器应当发送肯定响应")
    @pytest.mark.smoke
    def test_caseid_1988461(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x19, 0x02, 0x09])  # 前面已经清过dtc了,再发送190209查关于09子网掩码的dtc
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x02, 0x09]#什么都没有的情况下后面就跟只跟上我的子网掩码
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x54]
        
    @allure.title("14服务_NRC13_消息长度不符合")
    @pytest.mark.sanity
    def test_caseid_1988462(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x14, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x14,0x13]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x14,0x13]
        self.sd_tester.send_data([0x14])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x14,0x13]
        
    @allure.title("14服务_NRC31_不支持指定的groupOfDTC参数")# todo
    @pytest.mark.full
    def test_caseid_1988463(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0x01])  # uds指令清除DTC
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x7F,0x14,0x31]
        
    @allure.title("UdsServer_诊断事件上报dtc存在自然老化")
    @pytest.mark.smoke
    def test_caseid_1986117(self):
        self.cpp_case_lib.setup_session_ctrl_cb1()#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        result = self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能 
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为   
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        assert 0 == self.cpp_case_lib.check_readdtc_did_cb_result()  # 检测冻结帧的值
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭    
        sleep(2)
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        for i in range(8):
            logger.info(f"循环第: {i}次")
            result = self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
            sleep(0.1)
            assert 0 == result
        result = self.cpp_case_lib.get_event_staus(Name, 8)  # 00001000置位
        assert 0 == result
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭
        self.sd_tester.send_data([0x19, 0x01, 0x09])  # uds指令根据DTC状态掩码查找匹配的DTC数量
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59,0x01,0x09,0x01,0x00,0x01]
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        assert 0 == result
        for i in range(8):
            logger.info(f"循环第: {i}次")
            result = self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
            sleep(0.1)
            assert 0 == result
        result = self.cpp_case_lib.get_event_staus(Name, 8)  # 00001000置位
        assert 0 == result
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭
        assert 0 == result
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        assert 0 == result
        for i in range(8):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 0)  # 00001000置位
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 1)  # 循环关闭
        assert 0 == result
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)  # 循环开启
        assert 0 == result
        self.sd_tester.send_data([0x19, 0x01, 0x09])  # uds指令根据DTC状态掩码查找匹配的DTC数量
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59,0x01,0x09,0x01,0x00,0x00]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("UdsServer_诊断事件上报dtc开启一次循环超过老化阈值也只能上报一次老化")
    @pytest.mark.smoke
    def test_caseid_1986126(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        sleep(2)
        assert 0 == self.cpp_case_lib.check_readdtc_did_cb_result()  # 检测冻结帧的值
        for i in range(8):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 8)  # 00001000置位
        self.sd_tester.send_data([0x19, 0x01, 0x09])  # uds指令根据DTC状态掩码查找匹配的DTC数量
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59,0x01,0x09,0x01,0x00,0x01]
        for i in range(8):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 2)  # JUPrepassed = 0x02
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 8)  # 00001000置位
        self.sd_tester.send_data([0x19, 0x01, 0x09])  # uds指令根据DTC状态掩码查找匹配的DTC数量
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59,0x01,0x09,0x01,0x00,0x01]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 0)

    @allure.title("UdsServer_诊断事件上报dtc存在查看扩展帧")
    @pytest.mark.smoke
    def test_caseid_1986127(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        Name = b"Dtc_0x051511_Properties"
        data_ret = b"\x03"
        self.cpp_case_lib.read_data_element_cb1(Name, data_ret, len(data_ret), 0)#扩展帧的回调函数
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        self.sd_tester.send_data([0x19, 0x06, 0x05, 0x15, 0x11, 0xff])  # 19服务06查看扩展帧data
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x06, 0x05, 0x15, 0x11, 0x09, 0x01, 0x12, 0x34, 0x03, 0x12, 0x12, 0x34]  # 051511是dtc,09状态位,01是record_number位置,1234是我给的值,
                                                                                                        #03是record_number位置,12是第一个data_element1,1234
                                                                                                        #是后面的1234是第二个data_element2,因为他的bit是8开始那么就是00 12 34,前面的00由第一次的12补,后面的被覆盖
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("19服务_正响应_06子服务查看单个扩展帧")
    @pytest.mark.full
    def test_caseid_1988701(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        Name = b"Dtc_0x051511_Properties"
        data_ret = b"\x03"
        self.cpp_case_lib.read_data_element_cb1(Name, data_ret, len(data_ret), 0)#扩展帧的回调函数
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        self.sd_tester.send_data([0x19, 0x06, 0x05, 0x15, 0x11, 0x03])  # 19服务06查看扩展帧data
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x06, 0x05, 0x15, 0x11, 0x09, 0x03, 0x12, 0x12, 0x34]  # 051511是dtc,09状态位,01是record_number位置,1234是我给的值,
                                                                                                        #03是record_number位置,12是第一个data_element1,1234
                                                                                                        #是后面的1234是第二个data_element2,因为他的bit是8开始那么就是00 12 34,前面的00由第一次的12补,后面的被覆盖
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())

    @allure.title("UdsServer_诊断事件上报dtc冻结帧data是否正确")
    @pytest.mark.smoke
    def test_caseid_1987108(self):
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        Name = b"Dtc_0x051511_Properties"
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        self.sd_tester.send_data([0x19, 0x02, 0x08])  # 19服务02查看DTC,08看的是那7个bit
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x02, 0x09, 0x05, 0x15, 0x11, 0x09]  # 检测到051511的dtc子网掩码是09
        self.sd_tester.send_data([0x19, 0x04, 0x05, 0x15, 0x11, 0xFF])  # 19服务04查看冻结帧data
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x04, 0x05, 0x15, 0x11, 0x09,0x20, 0x05, 0xDD, 0x00, 0xDD, 0x01, 0xDD, 0x02, 0xDD, 0x0A, 0xDD, 0x0c]#051511状态位是09FreezeFram为0x20后面是冻结帧data
        # self.sd_tester.send_data([0x19, 0x0A])  # 19服务04查看冻结帧data
        # sleep(0.2)
        # result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        # assert result == [0x59, 0x0A,  0x09, 0x05, 0x15, 0x11, 0x01, 0x12, 0x34, 0x03, 0x12, 0x12, 0x34]
        #59 0A 09 05 15 11 09 05 15 12 00 05 15 13 00 45 46 00 00 91 6F 2F 00 92 EA 04 00 97 8B 11 00 97 8B 12 00 97 8B 13 00 97 8D 11 00 97 8D 12 
        # 00 97 8D 95 00 9D 79 11 00 9D 79 12 00 9D 79 13 00 D0 02 00 00 D0 2A 88 00 D0 36 00 00 D0 61 11 00 D0 61 12 00 D0 61 13 00 D0 62 11 00 D0 
        # 62 12 00 D0 62 13 00 D0 63 11 00 D0 63 12 00 D0 63 13 00 D0 64 11 00 D0 64 12 00 D0 64 13 00 D0 70 11 00 D0 70 12 00 D0 70 13 00 D0 B0 00 00 D0 
        # B1 51 00 D0 B2 11 00 D0 B2 15 00 D0 B2 86 00 E1 09 12 00 E1 09 14 00 E1 09 62 00 E3 00 55 00 E3 00 56 00 E4 00 57 00 EE 03 68 00 EE 04 68 00 EF 87 4A 00
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("UdsServer_诊断事件上报dtc存在查看冻结帧")
    @pytest.mark.smoke
    def test_caseid_1985984(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event" 
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
            sleep(0.2)
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_readdtc_did_cb_result()#校验冻结帧数据值
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())

    @allure.title("UdsServer_诊断事件上报且去抖确认dtc存在流程")
    @pytest.mark.smoke
    def test_caseid_1985979(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        Name = b"Dtc_0x051511_Event"
        result = self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == result
        for i in range(16):  # 配置表里面写到每次上报+8直到计数为127故障
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("19服务_NRC12_不支持子服务")
    @pytest.mark.full
    def test_caseid_1988464(self):
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x19, 0x03])  # uds指令清除DTC
        sleep(0.2)
        assert [0x7F, 0x19, 0x12] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("19服务_正响应_04子服务查看全部冻结帧data")
    @pytest.mark.full
    def test_caseid_1988699(self):
        raw_data = self.json_obj.init_json_data()
        raw_data['DtcProperties'][0]['freeze_frame'].append("FreezeFrame0x21")
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        Name = b"Dtc_0x051511_Properties"
        data_ret = b"\x03"
        self.cpp_case_lib.read_data_element_cb1(Name, data_ret, len(data_ret), 0)#扩展帧的回调函数
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        assert 0 == self.cpp_case_lib.check_readdtc_did_cb_result()#校验冻结帧数据值
        self.sd_tester.send_data([0x19, 0x02, 0x08])  # 19服务04查看冻结帧data,08看的是那7个bit
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x02, 0x09, 0x05, 0x15, 0x11, 0x09]  # 检测到051511的dtc子网掩码是09
        self.sd_tester.send_data([0x19, 0x04, 0x05, 0x15, 0x11, 0xFF])  # 19服务04查看冻结帧data
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x04, 0x05, 0x15, 0x11, 0x09,0x20, 0x05, 0xDD, 0x00, 0xDD, 0x01, 0xDD, 0x02, 0xDD, 0x0A, 0xDD, 0x0c,
                                                            0x21, 0x05, 0xDD, 0x00, 0xDD, 0x01, 0xDD, 0x02, 0xDD, 0x0A, 0xDD, 0x0c]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        
    @allure.title("19服务_正响应_04子服务查看单组冻结帧data")
    @pytest.mark.full
    def test_caseid_1988700(self):
        self.json_obj.update_json_data('$.FreezeFrame[1].short_name', 'FreezeFrame0x24')
        self.json_obj.update_json_data('$.FreezeFrame[1].record_number', 36)
        raw_data = self.json_obj.init_json_data()
        raw_data['DtcProperties'][0]['freeze_frame'].append("FreezeFrame0x24")
        self.json_obj.update_json_data(own_data=raw_data)
        logger.info("改完了重启diagserver")
        self.restart_diagserver()
        self.cpp_case_lib.setup_session_ctrl_cb1(0x1001, 0x0E80, 0x01, 0)#10服务
        Name = b"Dtc_0x051511_Properties"
        data_ret = b"\x03"
        self.cpp_case_lib.read_data_element_cb1(Name, data_ret, len(data_ret), 0)#扩展帧的回调函数
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        data_ret = b"\x03"
        self.cpp_case_lib.setup_readDTC_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)#冻结帧的DID回调
        Name = b"Dtc_0x051511_Event"
        assert 0 == self.cpp_case_lib.setup_cycle(b"DEM_STRESS_TEST_000000", 0)#设置诊断事件操作循环类别
        assert 0 == self.cpp_case_lib.dtc_ctrl_enable(1)#设置/获取DTC控制使能
        for i in range(16):
            logger.info(f"循环第: {i}次")
            assert 0 == self.cpp_case_lib.report_monitor_action(Name, 3)#上报诊断事件监控行为
        assert 0 == self.cpp_case_lib.get_event_staus(Name, 9)#获取诊断事件状态
        assert 0 == self.cpp_case_lib.check_readdtc_did_cb_result()#校验冻结帧数据值
        self.sd_tester.send_data([0x19, 0x02, 0x08])  # 19服务04查看冻结帧data,08看的是那7个bit
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x02, 0x09, 0x05, 0x15, 0x11, 0x09]  # 检测到051511的dtc子网掩码是09
        self.sd_tester.send_data([0x19, 0x04, 0x05, 0x15, 0x11, 0x24])  # 19服务04查看冻结帧data
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x59, 0x04, 0x05, 0x15, 0x11, 0x09, 0x24, 0x05, 0xDD, 0x00, 0xDD, 0x01, 0xDD, 0x02, 0xDD, 0x0A, 0xDD, 0x0c]
        self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])  # uds指令清除DTC
        sleep(0.2)
        assert [0x54] == (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        self.json_obj.recover_json_data()
        self.restart_diagserver()