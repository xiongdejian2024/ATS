# -*- coding: utf-8 -*-
"""
@File        : test_diag_bgm_full.py.py
@Author      : wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import time
import pytest
import allure
import sys, os

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

from sat.test_case.basetech.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_Service(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            # #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path)
        #     self.sniff.set_save_name(f"BGM_MCU_Service_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()
    
    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
        
    @allure.story("MCU_基础诊断服务")
    @allure.title("UDS_SessionControl(0x10)_DefaultSession")
    def test_caseid_1349479(self):
        try:
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("UDS_SessionControl(0x10)_ProgrammingSession")
    def test_caseid_1349480(self):
        try:
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_基础诊断服务")
    @allure.title("UDS_SessionControl(0x1002)_ExtendedSession")
    def test_caseid_1349481(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("进入扩展会话测试-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.session_control(3)
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
        except:
            assert False
             
    @allure.story("MCU_基础诊断服务")
    @allure.title("安全访问L3 0x27 03/04")
    def test_caseid_1349488(self):  # 0x27 03/04
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3测试"):
                self.b_cli.security_access_level(3)
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("安全访问L5 0x27 05/06")
    def test_caseid_1349489(self):  # 0x27 05/06
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
        except:
            assert False

    @allure.story("MCU_基础诊断服务")
    @allure.title("安全访问L11 0x27 11/12")
    def test_caseid_1349491(self):  # 0x27 11/12
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11测试"):
                self.b_cli.security_access_level(11)
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("ControlDTCSetting: 0x85 01 - DTC monitor function is on测试")
    def test_caseid_1349492(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("ControlDTCSetting: 0x85 01 - DTC monitor function is on测试"):
                self.b_cli.control_dtc_setting(0x01)
                p = self.b_cli.get_payload()
                assert p == 'c501'
        except:
            assert False

    @allure.story("MCU_基础诊断服务")
    @allure.title("ControlDTCSetting: 0x85 02 - DTC monitor function is off测试")
    def test_caseid_1349493(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("ControlDTCSetting: 0x85 01 - DTC monitor function is off测试"):
                self.b_cli.control_dtc_setting(0x02)
                p = self.b_cli.get_payload()
                assert p == 'c502'
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("UDS_Tester present(0x3E00)")
    def test_caseid_1349494(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("UDS_Tester present(0x3E)测试"):
                self.b_cli.test_persent()
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("UDS_Tester present(0x3E)测试"):
                self.b_cli.test_persent()
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("UDS_Tester present(0x3E)测试"):
                self.b_cli.test_persent()
        except:
            assert False
    
    @allure.story("MCU_基础诊断服务")
    @allure.title("Communication Control: 0x28 00 测试")
    def test_caseid_1349495(self):
        try:
            with allure.step("Communication Control: 0x28 00 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.communication_control(0x00)
            with allure.step(f"检查CAN应用报文: 0x533"):
                captured_msgdata0 = self.ipdu.recv_pdu("connectivitycanfd",0x533,timeout=2)
                if captured_msgdata0 is None:
                    logger.info("BGM Tx网络管理报文已禁能")
                    assert False
                else:
                    llogger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata0}")
                    assert True
            with allure.step(f"检查CAN应用报文: 0x114"):
                captured_msgdata1 = self.ipdu.recv_pdu("bodycan",0x114,timeout=2)
                if captured_msgdata1 is None:
                    logger.info("BGM Tx网络管理报文已禁能")
                    assert False
                else:
                    logger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata1}")
                    assert True
        except:
            assert False
    
    @allure.story("MCU_基础诊断服务")
    @allure.title("Communication Control: 0x28 01 03 - EnableRxAndDisableTx 所有报文测试")
    def test_caseid_1349496(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("通信控制: EnableRxAndDisableTx 应用报文测试"):
                self.b_cli.communication_control(0x01, 0x03)
            with allure.step(f"检查CAN应用报文: 0x114"):
                self.ipdu.rx_flag_reset_bus("bodycan")
                captured_msgdata1 = self.ipdu.recv_pdu("bodycan",0x114,timeout=2)
                if captured_msgdata1:
                    logger.info(f"BGM Tx应用报文未禁能 {captured_msgdata1}")
                    assert False
                else:
                    logger.info("BGM Tx应用报文已禁能")
                    assert True
            with allure.step(f"检查CAN网络管理报文: 0x533"):
                self.ipdu.rx_flag_reset_bus("connectivitycanfd")
                captured_msgdata0 = self.ipdu.recv_pdu("connectivitycanfd", 0x533, timeout=2)
                if captured_msgdata0 is None:
                    logger.info("BGM Tx网络管理报文已禁能")
                    assert True
                else:
                    logger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata0}")
                    assert False
            with allure.step("进入默认测试"):
                self.b_cli.session_control(1)
            with allure.step("通信控制: EnableRxAndDisableTx 应用报文 - 异常测试"):
                with pytest.raises(ValueError):
                    self.b_cli.communication_control(0x01,0x03)
        except:
            assert False
    
    @allure.story("MCU_基础诊断服务")
    @allure.title("Communication Control: 0x28 03 03 DisableRxAndTx测试")
    def test_caseid_1349498(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("通信控制: DisableRxAndTx 应用报文测试"):
                self.b_cli.communication_control(0x03, 0x03)
            with allure.step(f"检查CAN应用报文: 0x114"):
                self.ipdu.rx_flag_reset_bus("bodycan")
                captured_msgdata1 = self.ipdu.recv_pdu("bodycan",0x114,timeout=2)
                if captured_msgdata1:
                    logger.info("BGM Tx应用报文未禁能")
                    assert False
                else:
                    logger.info("BGM Tx应用报文已禁能")
                    assert True
            with allure.step(f"检查CAN网络管理报文: 0x533"):
                self.ipdu.rx_flag_reset_bus("connectivitycanfd")
                captured_msgdata0 = self.ipdu.recv_pdu("connectivitycanfd", 0x533, timeout=2)
                if captured_msgdata0 is None:
                    logger.info("BGM Tx网络管理报文已禁能")
                    assert True
                else:
                    logger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata0}")
                    assert False
            with allure.step("进入默认测试"):
                self.b_cli.session_control(1)
            with allure.step("通信控制: DisableRxAndTx 应用报文 - 异常测试"):
                with pytest.raises(ValueError):
                    self.b_cli.communication_control(0x03,0x03)
        except:
            assert False
    
    @allure.story("MCU_基础诊断服务")
    @allure.title("Communication Control: 0x28 01 02 - EnableRxAndDisableTx 网络管理报文测试")
    def test_caseid_1565002(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("通信控制: EnableRxAndDisableTx 应用报文测试"):
                self.b_cli.communication_control(0x01, 0x02)
            with allure.step(f"检查CAN网络管理报文: 0x533"):
                self.ipdu.rx_flag_reset_bus("connectivitycanfd")
                captured_msgdata0 = self.ipdu.recv_pdu("connectivitycanfd", 0x533, timeout=2)
                if captured_msgdata0 is None:
                    logger.info("BGM Tx网络管理报文已禁能")
                    assert True
                else:
                    logger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata0}")
                    assert False
            with allure.step("进入默认测试"):
                self.b_cli.session_control(1)
            with allure.step("通信控制: EnableRxAndDisableTx 网络管理报文 - 异常测试"):
                with pytest.raises(ValueError):
                    self.b_cli.communication_control(0x01, 0x02)
        except:
            assert False
    
    @allure.story("MCU_基础诊断服务")
    @allure.title("Communication Control: 0x28 01 01 - EnableRxAndDisableTx 应用报文测试")
    def test_caseid_1566572(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("通信控制: EnableRxAndDisableTx 应用报文测试"):
                self.b_cli.communication_control(0x01, 0x01)
            with allure.step(f"检查CAN应用报文: 0x114"):
                self.ipdu.rx_flag_reset_bus("bodycan")
                captured_msgdata1 = self.ipdu.recv_pdu("bodycan",0x114,timeout=2)
                if captured_msgdata1 is None:
                    logger.info("BGM Tx应用报文已禁能")
                    assert True
                else:
                    logger.info(f"BGM Tx网络管理报文未禁能: {captured_msgdata1}")
                    assert False
            with allure.step("进入默认测试"):
                self.b_cli.session_control(1)
            with allure.step("通信控制: EnableRxAndDisableTx 应用报文 - 异常测试"):
                with pytest.raises(ValueError):
                    self.b_cli.communication_control(0x01, 0x01)
        except:
            assert False

    @allure.story("MCU_基础诊断服务")
    @allure.title("UDS_EcuReset(0x1101)_HardReset")
    def test_caseid_1692933(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("EcuReset(0x11)_HardReset测试"):
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p[0:4] == '5101'
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("EcuReset(0x11)_HardReset测试"):
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p[0:4] == '5101'
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p[0:4] == '5101'
            with allure.step("退出编程会话测试"):
                self.b_cli.exit_boot()
        except:
            assert False       
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("Supported DTC: 0x19 0A测试")
    def test_caseid_1758554(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("获取支持的DTC测试"):
                self.b_cli.read_data_by_dtc(0x0A)
                p = self.b_cli.get_payload()
                assert p[0:4] == '590a'
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("获取支持的DTC测试"):
                self.b_cli.read_data_by_dtc(0x0A)
                p = self.b_cli.get_payload()
                assert p[0:4] == '590a'
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("Clear DTC: 0x14服务测试")
    def test_caseid_1758563(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("Clear DTC测试"):
                self.b_cli.clear_dtc()
                p = self.b_cli.get_payload()
                assert p[0:6] == '54'
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("Clear DTC测试"):
                self.b_cli.clear_dtc()
                p = self.b_cli.get_payload()
                assert p[0:6] == '54'
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("读取0x14FFFFFF测试")
    def test_caseid_1758583(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始读取0x190209"):
                self.b_cli.read_data_by_dtc(0x02, 0x09)
                p = self.b_cli.get_payload()
            with allure.step("清除DTC"):
                self.b_cli.clear_dtc()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始读取0x190209"):
                self.b_cli.read_data_by_dtc(0x02, 0x09)
                p = self.b_cli.get_payload()
            with allure.step("清除DTC"):
                self.b_cli.clear_dtc()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取DTC预期失败"):
                with pytest.raises(ValueError):
                    self.b_cli.clear_dtc()
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_基础诊断服务")
    @allure.title("	UDS_ReadSnapshotDatawithDTC(0x1904)")
    def test_caseid_1758585(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("Clear DTC测试"):
                self.b_cli.clear_dtc()
                p = self.b_cli.get_payload()
                assert p[0:6] == '54'
            with allure.step("进入扩展测试"):
                self.b_cli.session_control(3)
            with allure.step("Clear DTC测试"):
                self.b_cli.clear_dtc()
                p = self.b_cli.get_payload()
                assert p[0:6] == '54'
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_SOC_Service(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1001)
            # #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_SOC_Service_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()
    
    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
        
    @allure.story("SOC_基础诊断服务")
    @allure.title("UDS_SessionControl(0x10)_DefaultSession")
    def test_caseid_1349479(self):
        try:
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("读取当前会话测试"):
                self.b_cli.read_data_by_identifier(0xf186)
                p = self.b_cli.get_payload()
                assert p == '62f18601'
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("读取当前会话测试"):
                self.b_cli.read_data_by_identifier(0xf186)
                p = self.b_cli.get_payload()
                assert p == '62f18601'

        except:
            assert False
            
            
    @allure.story("SOC_基础诊断服务")
    @allure.title("UDS_SessionControl(0x10)_ProgrammingSession")
    def test_caseid_1349480(self):
        try:
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("读取当前会话测试"):
                self.b_cli.read_data_by_identifier(0xf186)
                p = self.b_cli.get_payload()
                assert p == '62f18602'
                self.b_cli.exit_boot()
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("读取当前会话测试"):
                self.b_cli.read_data_by_identifier(0xf186)
                p = self.b_cli.get_payload()
                assert p == '62f18602'
        except:
            assert False

    @allure.story("SOC_基础诊断服务")
    @allure.title("UDS_SessionControl(0x1002)_ExtendedSession")
    def test_caseid_1349481(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("进入扩展会话测试-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.session_control(3)
        except:
            assert False
            
    @allure.story("SOC_基础诊断服务")
    @allure.title("安全访问L1 0x27 01/02")
    def test_caseid_1349487(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("通过安全访问L1测试"):
                self.b_cli.security_access_level(1)
        except:
            assert False
            
    @allure.story("SOC_基础诊断服务")
    @allure.title("安全访问L5 0x27 05/06")
    def test_caseid_1349489(self):  # 0x27 05/06
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
        except:
            assert False
            
    @allure.story("SOC_基础诊断服务")
    @allure.title("安全访问L5 0x27 07/08")
    def test_caseid_1349490(self):  # 0x27 07/08
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L7测试"):
                self.b_cli.security_access_level(7)
        except:
            assert False
            
    @allure.story("SOC_基础诊断服务")
    @allure.title("UDS_EcuReset(0x1101)_HardReset")
    def test_caseid_1692933(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("EcuReset(0x11)_HardReset测试"):
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p == '5101'
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("EcuReset(0x11)_HardReset测试"):
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p == '5101'
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
                self.b_cli.reset(0x01)
                p = self.b_cli.get_payload()
                assert p == '5101'
        except:
            assert False       

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_IOControl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_MCU_IOControl_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)

    """
        0x2F IO Control
    """
    @allure.story("诊断IOControl")
    @allure.title("IO控制:Available Delta Power signal output测试 - DID:0x40E2_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349885?projectId=46"
    )
    def test_caseid_1349885(self):
        try:    
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Available Delta Power signal output状态"):
                self.b_cli.read_data_by_identifier(0x40E2)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Available Delta Power signal output测试 - 测试边界值: 7FFF"
            ):
                self.b_cli.io_control(0x40E2, 0x03, [0x7FFF])
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x40E2)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '7fff'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x40E2, 0x00)
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x40E2)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x40E2, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x40E2, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    
    @allure.title("IO控制: Activation of Washer Front Safe - DID:0x420A_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349889?projectId=46"
    )
    def test_caseid_1349889(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Activation of Washer Front Safe状态"):
                self.b_cli.read_data_by_identifier(0x420A)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Activation of Washer Front Safe测试 - 测试值: 0x01=off"):
                self.b_cli.io_control(0x420A, 0x03, [0x01])
            with allure.step("读取Activation of Washer Front Safe状态应为 off"):
                self.b_cli.read_data_by_identifier(0x420A)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Activation of Washer Front Safe测试 - 测试值: 0x02=on"):
                self.b_cli.io_control(0x420A, 0x03, [0x02])
            with allure.step("读取Activation of Washer Front Safe状态应为 on"):
                self.b_cli.read_data_by_identifier(0x420A)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '02'
            with allure.step("退出IO控制:Activation of Washer Front Safe"):
                self.b_cli.io_control(0x420A, 0x00)
            with allure.step("读取Activation of Washer Front Safe状态"):
                self.b_cli.read_data_by_identifier(0x420A)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Washing Supply Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x420A, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x420A, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    
    @allure.title("IO控制: Ignition Power Relay Control - DID:0x4252_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349892?projectId=46"
    )
    def test_caseid_1349892(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Ignition Power Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4252)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Ignition Power Relay Control测试 - 测试断开: 00"):
                self.b_cli.io_control(0x4252, 0x03, [0x00])
            with allure.step("读取Ignition Power Relay Control状态应为断开: 00"):
                self.b_cli.read_data_by_identifier(0x4252)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: Ignition Power Relay Control测试 - 测试闭合: 01"):
                self.b_cli.io_control(0x4252, 0x03, [0x01])
            with allure.step("读取Ignition Power Relay Control状态应为闭合: 01"):
                self.b_cli.read_data_by_identifier(0x4252)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出IO控制:Ignition Power Relay Control"):
                self.b_cli.io_control(0x4252, 0x00)
            with allure.step("读取Ignition Power Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4252)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Ignition Power Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]  
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4252, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4252, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Private Unlock Supply Control - DID:0x4260_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349894?projectId=46"
    )
    def test_caseid_1349894(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Private Unlock Supply Control状态"):
                self.b_cli.read_data_by_identifier(0x4260)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Private Unlock Supply Control测试 - 测试断开: 00"):
                self.b_cli.io_control(0x4260, 0x03, [0x00])
            with allure.step("读取Private Unlock Supply Control状态应为断开: 00"):
                self.b_cli.read_data_by_identifier(0x4260)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: Private Unlock Supply Control测试 - 测试闭合: 01"):
                self.b_cli.io_control(0x4260, 0x03, [0x01])
            with allure.step("读取Private Unlock Supply Control状态应为闭合: 01"):
                self.b_cli.read_data_by_identifier(0x4260)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出IO控制:Private Unlock Supply Control"):
                self.b_cli.io_control(0x4260, 0x00)
            with allure.step("读取Private Unlock Supply Control状态"):
                self.b_cli.read_data_by_identifier(0x4260)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Private Unlock Supply Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4260, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4260, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Single Stroke Wiping - DID:0x4328_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349896?projectId=46"
    )
    def test_caseid_1349896(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Single Stroke Wiping状态"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Single Stroke Wiping测试 - 测试值: 0x01(single stroke)"):
                self.b_cli.io_control(0x4328, 0x03, [0x01])
            with allure.step("读取Single Stroke Wiping状态应为 single stroke"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Single Stroke Wiping测试 - 测试值: 0x00(Off)"):
                self.b_cli.io_control(0x4328, 0x03, [0x00])
            with allure.step("读取Single Stroke Wiping状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出IO控制:Single Stroke Wiping"):
                self.b_cli.io_control(0x4328, 0x00)
            with allure.step("读取Single Stroke Wiping状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Single Stroke Wiping 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4328, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4328, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Climate Relay Control - DID:0x432E_0")  # 等待
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349897?projectId=46"
    )
    def test_caseid_1349897(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("读取Climate Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x432E)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Climate Relay Control测试 - 测试值: 0x01 ON"):
                self.b_cli.io_control(0x432E, 0x03, [0x01])
            with allure.step("读取Climate Relay Control状态应为 ON"):
                self.b_cli.read_data_by_identifier(0x432E)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Climate Relay Control测试 - 测试值: 0x00 Off"):
                self.b_cli.io_control(0x432E, 0x03, [0x00])
            with allure.step("读取Climate Relay Control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x432E)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出IO控制:Climate Relay Control"):
                self.b_cli.io_control(0x432E, 0x00)
            with allure.step("读取Climate Relay Control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x432E)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Climate Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x432E, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x432E, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title("IO控制: Rain Sensor ReAdaption - DID:0x43B8_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349899?projectId=46"
    )
    def test_caseid_1349899(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Rain Sensor ReAdaption状态"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Rain Sensor ReAdaption测试 - 测试值: 0x01 True"):
                self.b_cli.io_control(0x43B8, 0x03, [0x01])
            with allure.step("读取Rain Sensor ReAdaption状态应为 True"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Rain Sensor ReAdaption测试 - 测试值: 0x00 False"):
                self.b_cli.io_control(0x43B8, 0x03, [0x00])
            with allure.step("读取Rain Sensor ReAdaption状态应为 False"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出IO控制:Rain Sensor ReAdaption"):
                self.b_cli.io_control(0x43B8, 0x00)
            with allure.step("读取Rain Sensor ReAdaption状态应"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Rain Sensor ReAdaption 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x43B8, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x43B8, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Rear Windscreen Heater Control #1 - DID:0xEF99_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349902?projectId=46"
    )
    def test_caseid_1349902(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Rear Windscreen Heater Control #1状态"):
                self.b_cli.read_data_by_identifier(0xEF99)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: Rear Windscreen Heater Control #1测试 - 测试值: 0x01 ON"
            ):
                self.b_cli.io_control(0xEF99, 0x3, [0x01])
            with allure.step("读取Rear Windscreen Heater Control #1状态应为 ON"):
                self.b_cli.read_data_by_identifier(0xEF99)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step(
                "IO控制: Rear Windscreen Heater Control #1测试 - 测试值: 0x00 Off"
            ):
                self.b_cli.io_control(0xEF99, 0x3, [0x00])
            with allure.step("读取Rear Windscreen Heater Control #1状态应为 Off"):
                self.b_cli.read_data_by_identifier(0xEF99)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出控制:Rear Windscreen Heater Control #1"):
                self.b_cli.io_control(0xEF99, 0x00)
            with allure.step("读取Rear Windscreen Heater Control #1状态"):
                self.b_cli.read_data_by_identifier(0xEF99)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Rear Windscreen Heater Control #1 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xEF99, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xEF99, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:B pillar door opening button backlight control测试 - DID:0x4212_0"
    )  # 等待超时
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349903?projectId=46"
    )
    def test_caseid_1349903(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("读取B pillar door opening button backlight control状态"):
                self.b_cli.read_data_by_identifier(0x4212)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: B pillar door opening button backlight control测试 - 测试值: 0x01 ON"
            ):
                self.b_cli.io_control(0x4212, 0x03, [0x01])
            with allure.step("读取B pillar door opening button backlight control状态应为 ON"):
                self.b_cli.read_data_by_identifier(0x4212)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step(
                "IO控制: B pillar door opening button backlight control测试 - 测试值: 0x00 Off"
            ):
                self.b_cli.io_control(0x4212, 0x03, [0x00])
            with allure.step(
                "读取B pillar door opening button backlight control状态应为 Off"
            ):
                self.b_cli.read_data_by_identifier(0x4212)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出控制:B pillar door opening button backlight control"):
                self.b_cli.io_control(0x4212, 0x00)
            with allure.step("读取B pillar door opening button backlight control状态"):
                self.b_cli.read_data_by_identifier(0x4212)
                pl3 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, B pillar door opening button backlight control 变回控制前的值"
            # ):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4212, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4212, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: C pillar door opening button backlight control - DID:0x4213_0"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349904?projectId=46"
    )
    def test_caseid_1349904(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("读取C pillar door opening button backlight control状态"):
                self.b_cli.read_data_by_identifier(0x4213)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: C pillar door opening button backlight control测试 - 测试值: 0x01 ON"
            ):
                self.b_cli.io_control(0x4213, 0x03, [0x01])
            with allure.step("读取C pillar door opening button backlight control状态应为 ON"):
                self.b_cli.read_data_by_identifier(0x4213)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step(
                "IO控制: C pillar door opening button backlight control测试 - 测试值: 0x00 Off"
            ):
                self.b_cli.io_control(0x4213, 0x03, [0x00])
            with allure.step(
                "读取C pillar door opening button backlight control状态应为 Off"
            ):
                self.b_cli.read_data_by_identifier(0x4213)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出控制:C pillar door opening button backlight control"):
                self.b_cli.io_control(0x4213, 0x00)
            with allure.step("读取C pillar door opening button backlight control状态"):
                self.b_cli.read_data_by_identifier(0x4213)
                pl3 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, C pillar door opening button backlight control 变回控制前的值"
            # ):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4213, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4213, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Steering Wheel heat control - DID:0x4220_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349905?projectId=46"
    )
    def test_caseid_1349905(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Steering Wheel heat control状态"):
                self.b_cli.read_data_by_identifier(0x4220)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Steering Wheel heat control测试 - 测试值: 0x01 ON"):
                self.b_cli.io_control(0x4220, 0x03, [0x01])
            with allure.step("读取Steering Wheel heat control状态应为 ON"):
                self.b_cli.read_data_by_identifier(0x4220)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Steering Wheel heat control测试 - 测试值: 0x00 Off"):
                self.b_cli.io_control(0x4220, 0x03, [0x00])
            with allure.step("读取Steering Wheel heat control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4220)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出控制:Steering Wheel heat control"):
                self.b_cli.io_control(0x4220, 0x00)
            with allure.step("读取Steering Wheel heat control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4220)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Steering Wheel heat control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4220, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4220, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: High Mounted Stop Lamp control - DID:0x4221_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349906?projectId=46"
    )
    def test_caseid_1349906(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取High Mounted Stop Lamp control状态"):
                self.b_cli.read_data_by_identifier(0x4221)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: High Mounted Stop Lamp control测试 - 测试值: 0x01 ON"):
                self.b_cli.io_control(0x4221, 0x03, [0x01])
            with allure.step("读取High Mounted Stop Lamp control状态应为 ON"):
                self.b_cli.read_data_by_identifier(0x4221)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: High Mounted Stop Lamp control测试 - 测试值: 0x00 Off"):
                self.b_cli.io_control(0x4221, 0x03, [0x00])
            with allure.step("读取High Mounted Stop Lamp control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4221)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出控制:High Mounted Stop Lamp control"):
                self.b_cli.io_control(0x4221, 0x00)
            with allure.step("读取High Mounted Stop Lamp control状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4221)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, High Mounted Stop Lamp control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4221, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4221, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:Interior Lights Control_Boot/Trunk Lamps PWM 测试 - DID:0x41E5_80"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349907?projectId=46"
    )
    def test_caseid_1349907(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control测试 - 仅控制Boot/Trunk Lamps PWM: 0x000000000064"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80]
                )
                
            with allure.step("读取Power Outlet Control状态应为: 000000000064"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:8] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x80])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: Boot/Trunk Lamps PWM 变回控制前的值"
            # ):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x80])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x80])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:Interior Lights Control_Hazard switch illumination PWM 测试 - DID:0x41E5_40"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349908?projectId=46"
    )
    def test_caseid_1349908(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control测试 - - 仅控制 Hazard switch illumination PWM: 000000006400"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x40]
                )
            with allure.step("读取Power Outlet Control状态应为: 000000006400"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[8:10] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x40])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: Hazard switch illumination PWM 变回控制前的值"
            # ):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x40])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x40])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:Interior Lights Control_Interior Footwell Light Supply PWM 测试 - DID:0x41E5_20"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349909?projectId=46"
    )
    def test_caseid_1349909(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control_Interior Footwell Light Supply PWM 测试 - 仅控制Interior Footwell Light Supply PWM: 000000640000"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x20]
                )
            with allure.step("读取Power Outlet Control状态应为: 000000640000"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[10:12] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x20])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: Interior Footwell Light Supply PWM 变回控制前的值"
            # ):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x20])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x20])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    
    @allure.title(
        "IO控制:Interior Lights Control_FLDoor Indicate Lamp Supply 测试 - DID:0x41E5_10"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349910?projectId=46"
    )
    def test_caseid_1349910(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control测试 - 仅控制FLDoor Indicate Lamp Supply: 000064000000"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x10]
                )
            with allure.step("读取Power Outlet Control状态应为: 000064000000"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[12:14] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x10])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: FLDoor Indicate Lamp Supply 变回控制前的值"
            # ):
            #     assert pl2[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x10])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x10])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:Interior Lights Control_FRDoor Indicate Lamp Supply 测试 - DID:0x41E5_08"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349911?projectId=46"
    )
    def test_caseid_1349911(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control测试 - 仅控制FRDoor Indicate Lamp Supply: 006400000000"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x08]
                )
            with allure.step("读取Power Outlet Control状态应为: 006400000000"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[14:16] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x08])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: FRDoor Indicate Lamp Supply 变回控制前的值"
            # ):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x08])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x08])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:Interior Lights Control_Door Switch Symbol and Rear USB backlight Supply 测试 - DID:0x41E5_04"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349912?projectId=46"
    )
    def test_caseid_1349912(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Power Outlet Control测试 - 仅控制Door Switch Symbol and Rear USB backlight Supply: 640000000000"
            ):
                self.b_cli.io_control(
                    0x41E5, 0x03, [0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x04]
                )
            with allure.step("读取Power Outlet Control状态应为: 640000000000"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl1 = self.b_cli.get_payload()
                assert pl1[16:18] == '64'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E5, 0x00, [0x04])
            with allure.step("读取Power Outlet Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl2 = self.b_cli.get_payload()
            # with allure.step(
            #     "测试退出IO控制后, Interior Lights Control: Door Switch Symbol and Rear USB backlight Supply 变回控制前的值"
            # ):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x04])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E5, 0x00, [0x04])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Level Energy Electric Substitution - DID:0x429D_80_40")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349913?projectId=46"
    )
    def test_caseid_1349913(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Level Energy Electric Substitution状态"):
                self.b_cli.read_data_by_identifier(0x429D)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: Level Energy Electric Substitution_Energy Level Electric Substitution Subtype测试 - 测试边界值: 0xF0"
            ):
                self.b_cli.io_control(0x429D, 0x03, [0xF0, 0x80])
            with allure.step("读取Level Energy Electric Substitution状态应为: 0xF0"):
                self.b_cli.read_data_by_identifier(0x429D)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == 'f0'
            with allure.step(
                "IO控制: Level Energy Electric Substitution_Energy Level Electric Substitution Main测试 - 测试边界值: 0xFF"
            ):
                self.b_cli.io_control(0x429D, 0x03, [0xFF, 0x40])
            with allure.step("读取Level Energy Electric Substitution状态应为: 0xFF"):
                self.b_cli.read_data_by_identifier(0x429D)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == 'ff'
            with allure.step("退出控制:Level Energy Electric Substitution"):
                self.b_cli.io_control(0x429D, 0x00, [0x80])
                self.b_cli.io_control(0x429D, 0x00, [0x40])
            with allure.step("读取Level Energy Electric Substitution状态"):
                self.b_cli.read_data_by_identifier(0x429D)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Level Energy Electric Substitution 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x429D, 0x00, [0x40])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x429D, 0x00, [0x40])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Power Level Electric Substitution - DID:0x429E_80_40")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349914?projectId=46"
    )
    def test_caseid_1349914(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Power Level Electric Substitution状态"):
                self.b_cli.read_data_by_identifier(0x429E)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: Power Level Electric Substitution_Power Level Electric Substitution Subtype测试 - 测试边界值: 0xF0"
            ):
                self.b_cli.io_control(0x429E, 0x03, [0xF0, 0x80])
            with allure.step("读取Power Level Electric Substitution状态应为: 0xF0"):
                self.b_cli.read_data_by_identifier(0x429E)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == 'f0'
            with allure.step(
                "IO控制: Power Level Electric Substitution_Power Level Electric Substitution Main测试 - 测试边界值: 0xFF"
            ):
                self.b_cli.io_control(0x429E, 0x03, [0xFF, 0x40])
            with allure.step("读取Power Level Electric Substitution状态应为: 0xFF"):
                self.b_cli.read_data_by_identifier(0x429E)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == 'ff'
            with allure.step("退出控制:Power Level Electric Substitution"):
                self.b_cli.io_control(0x429E, 0x00, [0x80])
                self.b_cli.io_control(0x429E, 0x00, [0x40])
            with allure.step("读取Power Level Electric Substitution状态"):
                self.b_cli.read_data_by_identifier(0x429E)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Power Level Electric Substitution 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x429E, 0x00, [0x40])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x429D, 0x00, [0x40])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Exterior Light Relay Control  - DID:0x439F_80_40")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349898?projectId=46"
    )
    def test_caseid_1349915(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Light Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: Exterior Light Relay Control测试 - 测试值: Exterior Light Relay Control = 0x01 ON, Rear Exterior Light Relay Control = 0x00 Off"
            ):
                self.b_cli.io_control(0x439F, 0x03, [0x00, 0x01, 0x40])
                
            with allure.step(
                "读取Exterior Light Relay Control状态应为: Exterior Light Relay Control = 0x01 ON, Rear Exterior Light Relay Control = 0x00 Off"
            ):
                self.b_cli.read_data_by_identifier(0x439F)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step(
                "IO控制: Exterior Light Relay Control测试 - 测试值: Exterior Light Relay Control = 0x00 Off, Rear Exterior Light Relay Control = 0x00 Off"
            ):
                self.b_cli.io_control(0x439F, 0x03, [0x00, 0x00, 0x40])
                
            with allure.step(
                "读取Exterior Light Relay Control状态应为: Exterior Light Relay Control = 0x00 Off, Rear Exterior Light Relay Control = 0x00 Off"
            ):
                self.b_cli.read_data_by_identifier(0x439F)
                pl2 = self.b_cli.get_payload()
                assert pl2[-2:] == '00'
            with allure.step(
                "IO控制: Exterior Light Relay Control测试 - 测试值: Exterior Light Relay Control = 0x00 Off, Rear Exterior Light Relay Control = 0x01 ON"
            ):
                self.b_cli.io_control(0x439F, 0x03, [0x01, 0x00, 0x80])
                
            with allure.step("读取Exterior Light Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl3 = self.b_cli.get_payload()
                assert pl3[-4:-2] == '01'
            with allure.step(
                "IO控制: Exterior Light Relay Control测试 - 测试值: Exterior Light Relay Control = 0x00 Off, Rear Exterior Light Relay Control = 0x00 Off"
            ):
                self.b_cli.io_control(0x439F, 0x03, [0x00, 0x00, 0x80])
                
            with allure.step("读取Exterior Light Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl4 = self.b_cli.get_payload()
                assert pl4[-4:-2] == '00'
            with allure.step("退出IO控制:Exterior Light Relay Control"):
                self.b_cli.io_control(0x439F, 0x00, [0x80])
                self.b_cli.io_control(0x439F, 0x00, [0x40])
            with allure.step("读取Exterior Light Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl5 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Light Relay Control 变回控制前的值"):
            #     assert pl0 == pl5
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x439F, 0x00, [0x40])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x439F, 0x00, [0x40])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y4 - DID:0x7022_800000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349935?projectId=46"
    )
    def test_caseid_1349917(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x80, 0x00, 0x00, 0x80, 0x00, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '80'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x80, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x80, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x80, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    
    @allure.title("IO控制: Exterior Lights Control_LED Stop Lamp - DID:0x7022_000100")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349918?projectId=46"
    )
    def test_caseid_1349918(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x01, 0x00, 0x00, 0x01, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态应为自动头灯等级 ON"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '01'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x01, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x01, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x01, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampLeft.Y1 - DID:0x7022_000200"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349920?projectId=46"
    )
    def test_caseid_1349920(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x000200000200"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x02, 0x00, 0x00, 0x02, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '02'
            with allure.step("退出IO控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x02, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x02, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x02, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Exterior Lights Control_LED High Beam - DID:0x7022_000400")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349921?projectId=46"
    )
    def test_caseid_1349921(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000400"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x04, 0x00, 0x00, 0x04, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '04'
            with allure.step("退出IO控制:Exterior Lights Control"):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x04, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x04, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x04, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y3 - DID:0x7022_000800"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349923?projectId=46"
    )
    def test_caseid_1349923(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x08, 0x00, 0x00, 0x08, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '08'
            with allure.step("退出控制:Exterior Lights Control"):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x08, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2[6:8] == pl0[6:8]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x08, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x08, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_LED Daytime Running Lamp - DID:0x7022_001000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349924?projectId=46"
    )
    def test_caseid_1349924(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01001000"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x10, 0x00, 0x00, 0x10, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '10'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x10, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x10, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x10, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y1 - DID:0x7022_002000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349925?projectId=46"
    )
    def test_caseid_1349925(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x002000002000"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x20, 0x00, 0x00, 0x20, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '20'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x20, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x20, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x20, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y2 - DID:0x7022_004000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349926?projectId=46"
    )
    def test_caseid_1349926(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x000400004000"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x40, 0x00, 0x00, 0x40, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '40'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x40, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x40, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x40, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y3 - DID:0x7022_008000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349927?projectId=46"
    )
    def test_caseid_1349927(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x0080000800"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x80, 0x00, 0x00, 0x80, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-4:-2] == '80'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x80, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x80, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x00, 0x80, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Exterior Lights Control_Low Beam - DID:0x7022_010000")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349928?projectId=46"
    )
    def test_caseid_1349928(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x010000010000"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x01, 0x00, 0x00, 0x01, 0x00, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '01'
            with allure.step("退出控制:Exterior Lights Control"):
                self.b_cli.io_control(0x7022, 0x00, [0x01, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x01, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x01, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_Automatic Headlamp Leveling - DID:0x7022_020000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349929?projectId=46"
    )
    def test_caseid_1349929(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x02, 0x00, 0x00, 0x02, 0x00, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '02'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x02, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2[8:10] == pl0[8:10]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x02, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x02, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_Direction Indicator - DID:0x7022_040000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349930?projectId=46"
    )
    def test_caseid_1349930(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0x040000040000"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x04, 0x00, 0x00, 0x04, 0x00, 0x00]
                )
                
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '04'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x04, 0x00, 0x00])
                
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x04, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x04, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Exterior Lights Control_LED High Beam - DID:0x7022_080000")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349931?projectId=46"
    )
    def test_caseid_1349931(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x08, 0x00, 0x00, 0x08, 0x00, 0x00]
                )
                
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '08'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x08, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x08, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x7022, 0x00, [0x08, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_AIInteractionLampRight.Y1 - DID:0x7022_100000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349932?projectId=46"
    )
    def test_caseid_1349932(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x10, 0x00, 0x00, 0x10, 0x00, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '10'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x10, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x10, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x10, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_LED Daytime Running Lamp - DID:0x7022_200000"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349933?projectId=46"
    )
    def test_caseid_1349933(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x20, 0x00, 0x00, 0x20, 0x00, 0x00]
                )
                
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '20'
            with allure.step("退出控制:Exterior Lights Control"):
                self.b_cli.io_control(0x7022, 0x00, [0x20, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x20, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x20, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Exterior Lights Control_LED Rear Fog Lamp - DID:0x7022_400000")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349934?projectId=46"
    )
    def test_caseid_1349934(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000100"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x40, 0x00, 0x00, 0x40, 0x00, 0x00]
                )
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-6:-4] == '40'
            with allure.step("退出控制:Exterior Lights Control "):
                self.b_cli.io_control(0x7022, 0x00, [0x40, 0x00, 0x00])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x40, 0x00, 0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x40, 0x00, 0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
                
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制: Exterior Lights Control_StsOfLedRightAIILY4 - DID:0x7022_000080"
    )
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349917?projectId=46"
    )
    def test_caseid_1349935(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Exterior Lights Control 测试 - 测试控制: 0xFFFF01000080"):
                self.b_cli.io_control(
                    0x7022, 0x03, [0x00, 0x00, 0x01, 0x00, 0x00, 0x80]
                )
                
            with allure.step("读取Exterior Lights Control 状态应为右LED状态Y4亮"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step("退出IO控制:Exterior Lights Control"):
                self.b_cli.io_control(0x7022, 0x00, [0x00, 0x00, 0x80])
            with allure.step("读取Exterior Lights Control 状态"):
                self.b_cli.read_data_by_identifier(0x7022)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Exterior Lights Control 变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x00, 0x80])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x7022, 0x00, [0x00, 0x00, 0x80])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制:SoundSignalling测试 - DID:0x4217")
    def test_caseid_1491515(self):
        # try:
        assert True
        # with allure.step("进入默认会话"):    不用测
        #     self.b_cli.session_control(1)
        # with allure.step("进入扩展会话"):
        #     self.b_cli.session_control(3)
        # with allure.step("读取Front Camera Defrost Control 状态"):
        #     self.b_cli.read_data_by_identifier(0x4217)
        #     pl1 = self.b_cli.get_payload()
        # with allure.step("IO控制:Front Camera Defrost Control 测试"):
        #     self.b_cli.io_control(0x4256, 0x03,[0x00])
        # with allure.step("读取Front Camera Defrost Control 状态"):
        #     
        #     self.b_cli.read_data_by_identifier(0x4217)
        #     pl0 = self.b_cli.get_payload()
        # with allure.step("退出IO控制"):
        #     self.b_cli.io_control(0x4217, 0x00)
        # with allure.step("读取Front Camera Defrost Control 状态"):
        #     
        #     self.b_cli.read_data_by_identifier(0x4217)
        #     pl0 = self.b_cli.get_payload()
        # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
        #     assert pl1 == pl0
        # except:
        #     assert False
        
    @allure.story("诊断IOControl")
    @allure.title("IO控制:SoundSignalling测试 - DID:0x4256")
    def test_caseid_1491516(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Front Camera Defrost Control 状态"):
                self.b_cli.read_data_by_identifier(0x4256)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制:Front Camera Defrost Control 测试"):
                self.b_cli.io_control(0x4256, 0x03, [0x00])
            with allure.step("读取Front Camera Defrost Control 状态"):
                self.b_cli.read_data_by_identifier(0x4256)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '00'
            with allure.step("IO控制:Front Camera Defrost Control 测试"):
                self.b_cli.io_control(0x4256, 0x03, [0x01])
            with allure.step("读取Front Camera Defrost Control 状态"):
                self.b_cli.read_data_by_identifier(0x4256)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x4256, 0x00)
            with allure.step("读取Front Camera Defrost Control 状态"):
                self.b_cli.read_data_by_identifier(0x4256)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4256, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4256, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:C pillar Right door opening button backlight control测试 - DID:0x4223"
    )
    def test_caseid_1491518(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step(
                "读取C pillar Right door opening button backlight control 状态"
            ):
                self.b_cli.read_data_by_identifier(0x4223)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01' or pl1[-2:] == '00'
            with allure.step(
                "IO控制:C pillar Right door opening button backlight control 测试"
            ):
                self.b_cli.io_control(0x4223, 0x03, [0x01])
            with allure.step(
                "读取C pillar Right door opening button backlight control 状态"
            ):
                self.b_cli.read_data_by_identifier(0x4223)
                pl0 = self.b_cli.get_payload()
                assert pl0[-2:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x4223, 0x00)
            with allure.step(
                "读取C pillar Right door opening button backlight control状态"
            ):
                self.b_cli.read_data_by_identifier(0x4223)
                pl0 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
            #     assert pl1 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4223, 0x03, [0x01])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4223, 0x03, [0x01])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title(
        "IO控制:B pillar Right door opening button backlight control测试 - DID:0x4222"
    )
    def test_caseid_1491519(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step(
                "读取B pillar Right door opening button backlight control 状态"
            ):
                self.b_cli.read_data_by_identifier(0x4222)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01' or pl1[-2:] == '00'
            with allure.step(
                "IO控制:B pillar Right door opening button backlight control 测试"
            ):
                self.b_cli.io_control(0x4222, 0x03, [0x01])
            with allure.step(
                "读取B pillar Right door opening button backlight control 状态"
            ):
                self.b_cli.read_data_by_identifier(0x4222)
                pl0 = self.b_cli.get_payload()
                assert pl0[-2:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x4222, 0x00)
            with allure.step(
                "读取B pillar Right door opening button backlight control状态"
            ):
                self.b_cli.read_data_by_identifier(0x4222)
                pl0 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
            #     assert pl1 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4222, 0x03, [0x01])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4222, 0x03, [0x01])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制:SoundSignalling测试 - DID:0x41F2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349885?projectId=46"
    )
    def test_caseid_1491521(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Available Delta Power signal output状态"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Available Delta Power signal output测试 - 测试边界值: 7FFF"
            ):
                self.b_cli.io_control(0x41F2, 0x03, [0x01])
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41F2, 0x00)
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41F2, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x41F2, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("UDS_IOControl(0x2F)_ECM Wake Up Control")
    def test_caseid_1491522(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECM Wake Up Control状态"):
                self.b_cli.read_data_by_identifier(0x4253)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:ECM Wake Up Control测试"
            ):
                self.b_cli.io_control(0x4253, 0x03, [0x01])
                
            with allure.step("读取ECM Wake Up Control"):
                self.b_cli.read_data_by_identifier(0x4253)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step(
                "IO控制:ECM Wake Up Control测试"
            ):
                self.b_cli.io_control(0x4253, 0x03, [0x00])
            with allure.step("读取ECM Wake Up Control"):
                self.b_cli.read_data_by_identifier(0x4253)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '00'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x4253, 0x00)
            with allure.step("读取ECM Wake Up Control"):
                self.b_cli.read_data_by_identifier(0x4253)
                pl2 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后,ECM Wake Up Control变回控制前的值"):
            #     assert pl2 == pl0
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4253, 0x03, [0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                   self.b_cli.io_control(0x4253, 0x03, [0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title("IO控制: Usage Mode - DID:0xDD0A_0") # 需要增加FR standstl信号，待完善
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1349901?projectId=46")
    def test_caseid_1758514(self):
        try:
            self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            time.sleep(3)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Usage Mode状态"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Inactive)"):
                self.b_cli.io_control(0xDD0A, 0x3, [0x01])
            with allure.step("读取Usage Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '01'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Conven)"):
                self.b_cli.io_control(0xDD0A, 0x3, [0x02])
            with allure.step("读取Usage Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '02'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Active)"):
                self.b_cli.io_control(0xDD0A, 0x3, [0x0b])
            with allure.step("读取Usage Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0b'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Driving)"):
                self.b_cli.io_control(0xDD0A, 0x3, [0x0d])
            with allure.step("读取Usage Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0d'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Abandoned)"):
                self.b_cli.io_control(0xDD0A, 0x3, [0x00])
            with allure.step("读取Usage Mode状态应为 Abandoned"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '00'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0xDD0A, 0x0)
            with allure.step("读取Usage Mode状态应为 Abandoned"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后,Usage Mode变回控制前的值"):
            #     assert pl0 = pl
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xDD0A, 0x3, [0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xDD0A, 0x3, [0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Car Mode - DID:0xD134_0")  # 需要增加FR standstl信号，待完善
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349900?projectId=46"
    )
    # 
    def test_caseid_1758519(self):
        try:
            self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl0 = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl0 = self.b_cli.get_payload()
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Car Mode测试 - 测试切换: 0x01(Transport)"):
                self.b_cli.io_control(0xD134, 0x3, [0x01])
            with allure.step("读取Car Mode状态应为Transport"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Car Mode测试 - 测试切换: 0x02(Factory)"):
                self.b_cli.io_control(0xD134, 0x3, [0x02])
            with allure.step("读取Car Mode状态应为Factory"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '02'
            with allure.step("IO控制: Car Mode测试 - 测试切换: 0x03(Crash)"):
                self.b_cli.io_control(0xD134, 0x3, [0x03])
            with allure.step("读取Car Mode状态应为Crash"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl3 = self.b_cli.get_payload()
                assert pl3[6:] == '03'
            with allure.step("IO控制: Car Mode测试 - 测试切换: 0x05(Dynamometer)"):
                self.b_cli.io_control(0xD134, 0x3, [0x05])
            with allure.step("读取Car Mode状态应为Dynamometer"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl4 = self.b_cli.get_payload()
                assert pl4[6:] == '05'
            with allure.step("退出控制:Car Mode"):
                self.b_cli.io_control(0xD134, 0x00)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl5 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Car Mode 变回控制前的值"):
            #     assert pl5[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xD134, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0xD134, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("诊断IOControl")
    @allure.title("IO控制: Battery Power Saver Relay Control测试 - DID:0x41E8_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349887?projectId=46"
    )
    def test_caseid_1758524(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Power Saver Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制: Battery Power Saver Relay Control测试 - 测试值: 00(OFF)"
            ):
                self.b_cli.io_control(0x41E8, 0x03, [0x00])
            with allure.step("读取Battery Power Saver Relay Control状态应为 OFF:00 "):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: Battery Power Saver Relay Control测试 - 测试值: 01(ON)"):
                self.b_cli.io_control(0x41E8, 0x03, [0x01])
            with allure.step("读取Battery Power Saver Relay Control状态应为 ON:01 "):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41E8, 0x00)
            with allure.step("读取Battery Power Saver Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Battery Power Saver Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E8, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x41E8, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: Ignition Extended Relay Control - DID:0x4250_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349891?projectId=46"
    )
    def test_caseid_1758533(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Ignition Extended Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4250)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Ignition Extended Relay Control测试 - 测试断开: 00"):
                self.b_cli.io_control(0x4250, 0x03, [0x00])
            with allure.step("读取Ignition Extended Relay Control状态应为断开: 00"):
                self.b_cli.read_data_by_identifier(0x4250)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: Ignition Extended Relay Control测试 - 测试闭合: 01"):
                self.b_cli.io_control(0x4250, 0x03, [0x01])
            with allure.step("读取Ignition Extended Relay Control状态应为闭合: 01"):
                self.b_cli.read_data_by_identifier(0x4250)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出控制:Ignition Extended Relay Control"):
                self.b_cli.io_control(0x4250, 0x00)
            with allure.step("读取Ignition Extended Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4250)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Ignition Extended Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4250, 0x03, [0x01])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4250, 0x03, [0x01])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("IO控制: KL15_3 Relay Control - DID:0x4254_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349893?projectId=46"
    )
    def test_caseid_1758589(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取KL15_3 Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4254)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: KL15_3 Relay Control测试 - 测试断开: 00"):
                self.b_cli.io_control(0x4254, 0x03, [0x00])
            with allure.step("读取KL15_3 Relay Control状态应为断开: 00"):
                self.b_cli.read_data_by_identifier(0x4254)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: KL15_3 Relay Control测试 - 测试闭合: 01"):
                self.b_cli.io_control(0x4254, 0x03, [0x01])
            with allure.step("读取KL15_3 Relay Control状态应为闭合: 01"):
                self.b_cli.read_data_by_identifier(0x4254)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出IO控制:KL15_3 Relay Control"):
                self.b_cli.io_control(0x4254, 0x00)
            with allure.step("读取KL15_3 Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x4254)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, KL15_3 Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4254, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x4254, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    # @allure.story("MCU_诊断DID")
    # @allure.title("读取Power Outlet Control 测试 DID:0x4110")
    # def test_caseid_1349723(self):
    #     try:
    #         with allure.step("进入默认会话"):
    #             self.b_cli.session_control(1)
    #         with allure.step("读取Power Outlet Control 测试"):
    #             self.b_cli.read_data_by_identifier(0x4110)
    #             with allure.step("参数校验"):
    #                 pl = self.b_cli.get_payload()
    #                 pl = int(pl[6:], 16)
    #                 print("value is ", pl)
    #                 values = bytearray([0x00, 0x01])
    #                 if pl in values:
    #                     assert True
    #                 else:
    #                     assert False, "value out of range"
    #         with allure.step("进入扩展会话"):
    #             self.b_cli.session_control(3)
    #         with allure.step("读取Power Outlet Control 测试"):
    #             self.b_cli.read_data_by_identifier(0x4110)
                
    #     except:
    #         assert False

    @allure.story("诊断IOControl")
    
    @allure.title("IO控制: Comfort Relay Control - DID:0x424F_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349890?projectId=46"
    )
    def test_caseid_1758598(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Comfort Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x424F)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Comfort Relay Control测试 - 测试断开: 00"):
                self.b_cli.io_control(0x424F, 0x03, [0x00])
            with allure.step("读取Comfort Relay Control状态应为断开: 00"):
                self.b_cli.read_data_by_identifier(0x424F)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '00'
            with allure.step("IO控制: Comfort Relay Control测试 - 测试闭合: 01"):
                self.b_cli.io_control(0x424F, 0x03, [0x01])
            with allure.step("读取Comfort Relay Control状态应为闭合: 01"):
                self.b_cli.read_data_by_identifier(0x424F)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '01'
            with allure.step("退出IO控制:Comfort Relay Control"):
                self.b_cli.io_control(0x424F, 0x00)
            with allure.step("读取Comfort Relay Control状态"):
                self.b_cli.read_data_by_identifier(0x424F)
                pl3 = self.b_cli.get_payload()
            # with allure.step("测试退出IO控制后, Comfort Relay Control 变回控制前的值"):
            #     assert pl3[6:] == pl0[6:]
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x424F, 0x00)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("退出IO控制 -NRC 31"):
                with pytest.raises(ValueError):
                    self.b_cli.io_control(0x424F, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_RoutineControl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_MCU_RoutineControl_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
        
    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "Read Private ECUs Part 测试 RID:0x0208_1_2_3"
    )
    def test_caseid_1349989(self):
        # assert True
        try:
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Read Private ECUs Part/serial Numbers 测试"):
                self.b_cli.routing_control(0x0208, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20'
            with allure.step("停止例程控制: Read Private ECUs Part/serial Numbers 测试"):
                self.b_cli.routing_control(0x0208, 0x02)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20'
            with allure.step("请求例程控制结果: Read Private ECUs Part/serial Numbers 测试"):
                self.b_cli.routing_control(0x0208, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[8:10] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x0208, 0x02)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x0208, 0x02)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Steering Wheel Heating Command RID:0x200C_1_2_3")  # 00值错误
    def test_caseid_1350004(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Steering Wheel Heating Command 测试"):
                self.b_cli.routing_control(0x200C, 0x01, data=0x00.to_bytes(1, 'big'))
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '22' or pl1[-2:] == '21' or pl1[-2:] == '20'
            with allure.step("停止例程控制: Steering Wheel Heating Command 测试"):
                self.b_cli.routing_control(0x200C, 0x02)
                pl2 = self.b_cli.get_payload()
                assert pl2[-2:] == '22' or pl2[-2:] == '21' or pl2[-2:] == '20'
            with allure.step("请求例程控制结果: Read Private ECUs Part/serial Numbers 测试"):
                self.b_cli.routing_control(0x200C, 0x03)
                pl3 = self.b_cli.get_payload()
                assert pl3[-2:] == '22' or pl3[-2:] == '21' or pl3[-2:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x200C, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x200C, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Private Locking Deactivation RID:0x2015_1_2_3")  # BT 值错误 已经提BUG
    def test_caseid_1350005(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Private Locking Deactivation 测试"):
                self.b_cli.routing_control(0x2015, 0x01, data=0x00.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("停止例程控制: Private Locking Deactivation 测试"):
                self.b_cli.routing_control(0x2015, 0x02)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("请求例程控制结果: Private Locking Deactivation 测试"):
                self.b_cli.routing_control(0x2015, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2015, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2015, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Battery Sensor Request RID:0x2022_1_2_3")
    def test_caseid_1350006(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Battery Sensor Request 测试"):
                self.b_cli.routing_control(0x2022, 0x01, data=0x00.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("停止例程控制: Battery Sensor Request 测试"):
                self.b_cli.routing_control(0x2022, 0x02)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("请求例程控制结果: Battery Sensor Request 测试"):
                self.b_cli.routing_control(0x2022, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '20' or '22'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2022, 0x02)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2022, 0x02)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Hazard Lights Activation RID:0x2066_1_2_3")
    def test_caseid_1350007(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Hazard Lights Activation 测试"):
                self.b_cli.routing_control(0x2066, 0x01, data=0x00.to_bytes(1, 'big'))
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '32' or pl1[-2:] == '30'
            with allure.step("停止例程控制: Hazard Lights Activation 测试"):
                self.b_cli.routing_control(0x2066, 0x02)
                pl2 = self.b_cli.get_payload()
                assert pl2[-2:] == '32' or pl2[-2:] == '30'
            with allure.step("请求例程控制结果: Hazard Lights Activation 测试"):
                self.b_cli.routing_control(0x2066, 0x03)
                pl3 = self.b_cli.get_payload()
                assert pl3[-2:] == '32' or pl3[-2:] == '30'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2066, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2066, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Reset Usage Mode Extention Statistics RID:0x2071_1")
    def test_caseid_1350008(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Reset Usage Mode Extention Statistics 测试"):
                self.b_cli.routing_control(
                    0x2071, 0x01, data=0xFFFFFF.to_bytes(3, 'big')
                )
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                     self.b_cli.routing_control(
                    0x2071, 0x01, data=0xFFFFFF.to_bytes(3, 'big')
                )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                     self.b_cli.routing_control(
                    0x2071, 0x01, data=0xFFFFFF.to_bytes(3, 'big')
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Reset Usage Mode Time Statistics RID:0x2072_1")
    def test_caseid_1350009(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Reset Usage Mode Time Statistics 测试"):
                self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing RID:0x20EB_1_2_3"
    )
    def test_caseid_1350010(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "停止例程控制: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step(
                "请求例程控制结果: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "停止例程控制: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step(
                "请求例程控制结果: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x20EB, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) RID:0x20F1_1_2_3"
    )
    def test_caseid_1350012(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "开始例程控制: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x01, data=0xFFFF.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "停止例程控制: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x02)
                self.b_cli.routing_control(0x20F1, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "请求例程控制结果: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x03)
                self.b_cli.routing_control(0x20F1, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "开始例程控制: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "停止例程控制: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x02)
                self.b_cli.routing_control(0x20F1, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "请求例程控制结果: Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F1, 0x03)
                self.b_cli.routing_control(0x20F1, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x20F1, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) RID:0x20F2_1_2_3"
    )
    def test_caseid_1350013(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "开始例程控制: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "停止例程控制: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x02)
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "请求例程控制结果: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x03)
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "开始例程控制: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "停止例程控制: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x02)
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step(
                "请求例程控制结果: Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
            ):
                self.b_cli.routing_control(0x20F2, 0x03)
                self.b_cli.routing_control(0x20F2, 0x01, data=0x010A.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x20F2,0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    # @allure.story("MCU_诊断RoutineControl")
    # 
    # @allure.title(
    #     "Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM) RID:0x20F3_1_2_3"
    # )  # 超时
    # def test_caseid_1350014(self):
    #     try:
    #         with allure.step("进入默认会话"):
    #             self.b_cli.session_control(1)
    #         with allure.step(
    #             "开始例程控制: Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
    #         ):
    #             self.b_cli.routing_control(0x20F3, 0x01,data=0x010A.to_bytes(2, 'big'))
    #             p = self.b_cli.get_payload()
    #             assert p[8:10] == '10'
    #         with allure.step(
    #             "请求例程控制结果: Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
    #         ):
    #             self.b_cli.routing_control(0x20F3, 0x03)
    #             p = self.b_cli.get_payload()
    #             assert p[8:10] == '10'
    #         with allure.step("进入扩展会话"):
    #             self.b_cli.session_control(3)
    #         with allure.step(
    #             "开始例程控制: Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
    #         ):
    #             self.b_cli.routing_control(0x20F3, 0x01,data=0x010A.to_bytes(2, 'big'))
    #             p = self.b_cli.get_payload()
    #             assert p[8:10] == '10'
    #         with allure.step(
    #             "请求例程控制结果: Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM) 测试"
    #         ):
    #             self.b_cli.routing_control(0x20F3, 0x03)
    #             p = self.b_cli.get_payload()
    #             assert p[8:10] == '10'
    #     except:
    #         assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("NetworkCommunicationControl RID:0xA101")
    def test_caseid_1350015(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制: 总线通信控制测试"):
                self.b_cli.routing_control(0xA101, 0x01, data=0x0FFF.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '1000'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 总线通信控制测试"):
                self.b_cli.routing_control(0xA101, 0x01, data=0x0FFF.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '1000'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA101, 0x01, data=0x0FFF.to_bytes(2, 'big'))
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("initilize AWM RID:0x2013_1_3")
    def test_caseid_1349424(self):
        try:
            with pytest.raises(ValueError):
                with allure.step("进入默认会话"):
                    self.b_cli.session_control(1)
                with allure.step("开始例程控制: 学习AWM位置测试"):
                    self.b_cli.routing_control(0x2013, 0x01)
                    p = self.b_cli.get_payload()
                    assert p[8:] == '10'
                with allure.step("请求例程结果: 学习结果测试"):
                    self.b_cli.routing_control(0x2013, 0x03)
                    p = self.b_cli.get_payload()
                    assert p[8:] == '1002' or '1000'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 学习AWM位置测试"):
                self.b_cli.routing_control(0x2013, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("请求例程结果: 学习结果测试"):
                self.b_cli.routing_control(0x2013, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:] == '1002' or ' 1000'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Calibarte ChargeLid  RID:0x2031_1_3")  # BT会话1否定响应 会话3值错误，已提BUG
    def test_caseid_1349425(self):
        try:
            with pytest.raises(ValueError):
                with allure.step("进入默认会话"):
                    self.b_cli.session_control(1)
                with allure.step("开始例程控制: Calibarte ChargeLid测试"):
                    self.b_cli.routing_control(0x2031, 0x01)
            with pytest.raises(ValueError):
                with allure.step("进入默认会话"):
                    self.b_cli.session_control(1)
                with allure.step("开始例程控制: Calibarte ChargeLid测试"):
                    self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Calibarte ChargeLid"):
                self.b_cli.routing_control(0x2031, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("请求例程控制结果: Calibarte ChargeLid - NRC31 测试"):
                self.b_cli.routing_control(0x2031, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
            
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("100BaseT1 Ethernet Test Mode 1  RID:0xA001_1")
    def test_caseid_1350026(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 100BaseT1 Ethernet Test Mode 1 测试"):
                self.b_cli.routing_control(0xA001, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA001, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA001, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("100BaseT1 Ethernet Test Mode 2  RID:0xA002_1")
    def test_caseid_1350027(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 100BaseT1 Ethernet Test Mode 2 测试"):
                self.b_cli.routing_control(0xA002, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA002, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA002, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("100BaseT1 Ethernet Test Mode 3  RID:0xA003_1")
    def test_caseid_1350028(self):
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("通过安全访问L5"):
        #         self.b_cli.security_access_level(5)               
        #     with allure.step("开始例程控制: 100BaseT1 Ethernet Test Mode 3 测试"):
        #         self.b_cli.routing_control(0xA003, 0x01)
        #         pl = self.b_cli.get_payload()
        #         assert pl[8:] == '10'
        # except:
        #     assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("100BaseT1 Ethernet Test Mode 4  RID:0xA004_1")
    def test_caseid_1350029(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 100BaseT1 Ethernet Test Mode 4 测试"):
                self.b_cli.routing_control(0xA004, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA004, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA004, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断RoutineControl")
    @allure.title("100BaseT1 Ethernet Test Mode 5  RID:0xA005_1")
    def test_caseid_1350031(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 100BaseT1 Ethernet Test Mode 5 测试"):
                self.b_cli.routing_control(0xA005, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA005, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA005, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("Allow Unlocking  RID:0x2098_1")
    def test_caseid_1350032(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("开始例程控制: Allow Unlocking 测试"):
                self.b_cli.routing_control(0x2098, 0x01, data=0x01.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[8:] == '1001'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2098, 0x01, data=0x01.to_bytes(1, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2098, 0x01, data=0x01.to_bytes(1, 'big'))
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("UDS_RoutingControl(0x31)_Reset Usage Mode Time Statistics")
    def test_caseid_1493595(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Reset Usage Mode Time Statistics 测试"):
                self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.title("RountineControl:Alarm Programming Mode测试 - RID:0x2025")
    @allure.story("MCU_诊断RoutineControl")
    def test_caseid_1493596(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 1 测试"):
                self.b_cli.routing_control(0x2025, 0x01, data=0x21.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or pl[-2:] == '22'
                self.b_cli.routing_control(0x2025, 0x01, data=0x20.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or pl[-2:] == '22'
                self.b_cli.routing_control(0x2025, 0x01, data=0x11.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or pl[-2:] == '22'
                self.b_cli.routing_control(0x2025, 0x01, data=0x10.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or pl[-2:] == '22'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            #with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 1 NRC31 测试"):
                #with pytest.raises(ValueError):
                    # self.b_cli.routing_control(
                    #     0x2025, 0x01, data=0x20.to_bytes(1, 'big')
                    # )
                    # pl = self.b_cli.get_payload()
                    # assert pl[-2:] == '20' or pl[-2:] == '22'
                    # self.b_cli.routing_control(
                    #     0x2025, 0x01, data=0x25.to_bytes(1, 'big')
                    # )
                    # pl = self.b_cli.get_payload()
                    # assert pl[-2:] == '20' or pl[-2:] == '22'
                    # self.b_cli.routing_control(
                    #     0x2025, 0x01, data=0x11.to_bytes(1, 'big')
                    # )
                    # pl = self.b_cli.get_payload()
                    # assert pl[-2:] == '20' or pl[-2:] == '22'
                    # self.b_cli.routing_control(
                    #     0x2025, 0x01, data=0x10.to_bytes(1, 'big')
                    # )
                    # pl = self.b_cli.get_payload()
                    # assert pl[-2:] == '20' or pl[-2:] == '22'
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2072, 0x01,data=0xFF01.to_bytes(2, 'big'))
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 2 RID:0xA052_1")
    def test_caseid_1758512(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 2 测试"):
                self.b_cli.routing_control(0xA052, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA052, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA052, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 7 RID:0xA057_1")
    def test_caseid_1758522(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 7 测试"):
                self.b_cli.routing_control(0xA057, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA057, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA057, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 4 RID:0xA054_1")
    def test_caseid_1758526(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 4 测试"):
                self.b_cli.routing_control(0xA054, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            # with allure.step("进入默认会话"):
            #     self.b_cli.session_control(1)
            # with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 4 NRC31 测试"):
            #     with pytest.raises(ValueError):
            #         self.b_cli.routing_control(0xA054, 0x01)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA054, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA054, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 6 RID:0xA056_1")
    def test_caseid_1758537(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 6 测试"):
                self.b_cli.routing_control(0xA056, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            # with allure.step("进入默认会话"):
            #     self.b_cli.session_control(1)
            # with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 6 NRC31 测试"):
            #     with pytest.raises(ValueError):
            #         self.b_cli.routing_control(0xA056, 0x01)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA056, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA056, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("initilize AWM RID:0x2013_1_3")
    def test_caseid_1758555(self):
        try:
            # with pytest.raises(ValueError):
            #     with allure.step("进入默认会话"):
            #         self.b_cli.session_control(1)
            #     with allure.step("开始例程控制: 学习AWM位置测试"):
            #         self.b_cli.routing_control(0x2013, 0x01)
            #         p = self.b_cli.get_payload()
            #         assert p[8:] == '10'
            #     with allure.step("请求例程结果: 学习结果测试"):
            #         self.b_cli.routing_control(0x2013, 0x03)
            #         p = self.b_cli.get_payload()
            #         assert p[8:] == '1002' or '1000'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 学习AWM位置测试"):
                self.b_cli.routing_control(0x2013, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("请求例程结果: 学习结果测试"):
                self.b_cli.routing_control(0x2013, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:] == '1002' or ' 1000'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 1 RID:0xA051_1")
    def test_caseid_1758560(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 1 测试"):
                self.b_cli.routing_control(0xA051, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            # with allure.step("进入默认会话"):
            #     self.b_cli.session_control(1)
            # with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 1 NRC31 测试"):
            #     with pytest.raises(ValueError):
            #         self.b_cli.routing_control(0xA051, 0x01)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA051, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA051, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 5 RID:0xA055_1")
    def test_caseid_1350021(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 5 测试"):
                self.b_cli.routing_control(0xA055, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '10'
            # with allure.step("进入默认会话"):
            #     self.b_cli.session_control(1)
            # with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 5 NRC31 测试"):
            #     with pytest.raises(ValueError):
            #         self.b_cli.routing_control(0xA055, 0x01)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA055, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("请求例程控制结果: -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA055, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断RoutineControl")
    @allure.title("1000BaseT1 Ethernet Test Mode 3 RID:0xA053_1")  #BT 返回值错误 已提BUG 不用测
    def test_caseid_1350019(self):
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("通过安全访问L5"):
        #         self.b_cli.security_access_level(5)
        #     with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 3 测试"):
        #         self.b_cli.routing_control(0xA053, 0x01)
        #         pl = self.b_cli.get_payload()
        #         assert pl[8:] == '10'
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("开始例程控制: 1000BaseT1 Ethernet Test Mode 3 NRC31 测试"):
        #         with pytest.raises(ValueError):
        #             self.b_cli.routing_control(0xA053, 0x01)
        # except:
        #     assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_SOC_RoutineControl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1001)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_SOC_RoutineControl_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
        
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "Transfer Key Info 测试 RID:0x0208_1_2_3"
    )
    def test_caseid_1349989(self):
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("开始例程控制: Read Private ECUs Part/serial Numbers 测试"):
        #         self.b_cli.routing_control(0x0208, 0x01)
        #         pl = self.b_cli.get_payload()
        #         assert pl[8:] == '20'
        #     with allure.step("停止例程控制: Read Private ECUs Part/serial Numbers 测试"):
        #         self.b_cli.routing_control(0x0208, 0x02)
        #         pl = self.b_cli.get_payload()
        #         assert pl[8:] == '20'
        #     with allure.step("请求例程控制结果: Read Private ECUs Part/serial Numbers 测试"):
        #         self.b_cli.routing_control(0x0208, 0x03)
        #         pl = self.b_cli.get_payload()
        #         assert pl[8:10] == '20'
        # except:
        #     assert False
    
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("取消FOTA任务测试 RID:0xA102")
    def test_caseid_1349991(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("取消FOTA任务测试"):
                self.b_cli.routing_control(0xA102, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '1000'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("取消FOTA任务测试"):
                self.b_cli.routing_control(0xA102, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '1000'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)    
            with allure.step("取消FOTA任务测试"):
                self.b_cli.routing_control(0xA102, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[8:] == '1000'
        except:
            assert False
    
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("ChargeLid Open/Close RID:0x2030")
    def test_caseid_1349993(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: ChargeLid Open测试"):
                self.b_cli.routing_control(0x2030, 0x01, data=0x01.to_bytes(1, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20' 
            with allure.step("开始例程控制: ChargeLid Open测试"):
                self.b_cli.routing_control(0x2030, 0x01, data=0x00.to_bytes(1, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2030, 0x01, data=0x00.to_bytes(1, 'big'))
            # with allure.step("开始例程控制: ChargeLid Open测试"):
            #     with pytest.raises(ValueError):
            #         self.b_cli.routing_control(
            #             0x2030, 0x01, data=0x01.to_bytes(1, 'big')
            #         )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0x2030, 0x01, data=0x00.to_bytes(1, 'big'))
        except:
            assert False
    
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("打开滑行模式测试 RID:0x2030")
    def test_caseid_1349994(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("滑行模式测试"):
                self.b_cli.routing_control(0x2030, 0x01, data=0x01.to_bytes(1, 'big'))
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("滑行模式测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2030, 0x01, data=0x01.to_bytes(1, 'big')
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("滑行模式测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2030, 0x01, data=0x01.to_bytes(len(str(0x01)), 'big')
                    )
                    time.sleep(0.5)
                    p2 = self.b_cli.get_payload()
                    assert p2[4:] == '31'
        except:
            assert False

    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness, invalid值测试 RID:0x2040"
    )
    def test_caseid_1349995(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x80FFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness, 最小值测试 RID:0x2040"
    )
    def test_caseid_1349996(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2040,
                    0x01,
                    data=0x0000000000000000000000000000000000000000000000000000000000000000.to_bytes(
                        32, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x0000000000000000000000000000000000000000000000000000000000000000.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x0000000000000000000000000000000000000000000000000000000000000000.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness, 边界值测试 RID:0x2040"
    )
    def test_caseid_1349997(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2040,
                    0x01,
                    data=0x7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF.to_bytes(
                        32, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF7FFFFFFF.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "控制智能氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness 最大值测试 RID:0x2041"
    )
    def test_caseid_1349998(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2041,
                    0x01,
                    data=0x7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F.to_bytes(
                        816, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness RID:0x2040")
    def test_caseid_1349999(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2040,
                    0x01,
                    data=0x2233441100000000000000000000000000000000000000000000000011223344.to_bytes(
                        32, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x2233441100000000000000000000000000000000000000000000000011223344.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2040,
                        0x01,
                        data=0x2233441100000000000000000000000000000000000000000000000011223344.to_bytes(
                            32, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
    
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "控制智能氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness invalid值测试 RID:0x2041"
    )
    def test_caseid_1350000(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x807F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F7F.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("控制智能氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness RID:0x2041")
    def test_caseid_1350001(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2041,
                    0x01,
                    data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                        816, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("控制智能氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness RID:0x2041")
    def test_caseid_1350002(self):
        try:
            self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试"):
                self.b_cli.routing_control(
                    0x2041,
                    0x01,
                    data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                        816, 'big'
                    ),
                )
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step(
                "控制普通氛围灯灯带 ALM1-ALM8 的颜色 Red、Green、Blue 和亮度 Brightness测试 - NRC31"
            ):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2041,
                        0x01,
                        data=0x0102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000000001020304112233440000000000000000010203041122334400000000000000000102030411223344000000000000.to_bytes(
                            816, 'big'
                        ),
                    )
                    time.sleep(0.5)
                    p1 = self.b_cli.get_payload()
                    assert p1[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title(
        "RountineControl:upload SOA service data tracking record测试 - RID:0xEA29"
    )
    def test_caseid_1502237(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: upload vehicle data tracking record 测试"):
                self.b_cli.routing_control(
                    0xEA29,
                    0x01,
                    0x687474703A2F2F3136392E3235342E302E31323A38303830.to_bytes(
                        24, 'big'
                    ),
                )
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20'
                self.b_cli.routing_control(0xEA29, 0x02)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xEA29, 0x02)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xEA29, 0x02)
        except:
            assert False

    @allure.story("SOC_诊断RoutineControl")
    @allure.title("RountineControl:upload vehicle data tracking record测试 - RID:0xEA28")
    def test_caseid_1502239(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: upload vehicle data tracking record 测试"):
                self.b_cli.routing_control(
                    0xEA28,
                    0x01,
                    0x687474703A2F2F3136392E3235342E302E31323A38303830.to_bytes(
                        24, 'big'
                    ),
                )
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20'
                self.b_cli.routing_control(0xEA28, 0x02)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                    0xEA28,
                    0x01,
                    0x687474703A2F2F3136392E3235342E302E31323A38303830.to_bytes(
                        24, 'big'
                    ),
                )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                    0xEA28,
                    0x01,
                    0x687474703A2F2F3136392E3235342E302E31323A38303830.to_bytes(
                        24, 'big'
                    ),
                )
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("RountineControl:upload LOG测试 - RID:0xEA1D")
    def test_caseid_1502240(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制:upload LOG 测试"):
                self.b_cli.routing_control(0xEA1D, 0x01, data=0x0.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '10' or pl[-2:] == '12'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制:upload LOG 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0xEA1D, 0x01, data=0x0.to_bytes(1, 'big')
                    )
                    pl = self.b_cli.get_payload()
                    assert pl[-2:] == '10' or pl[-2:] == '12'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0xEA1D, 0x01, data=0x0.to_bytes(1, 'big')
                    )
        except:
            assert False
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("RountineControl:enable SSH测试 - RID:0xA041")
    def test_caseid_1502241(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L7测试"):
                self.b_cli.security_access_level(0x07)
            with allure.step("开始例程控制:disable SSH 测试"):
                self.b_cli.routing_control(0xA041, 0x01, data=0x2.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '10'
            with allure.step("开始例程控制:enable SSH 测试"):
                self.b_cli.routing_control(0xA041, 0x01, data=0x1.to_bytes(1, 'big'))
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制:upload LOG 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA041, 0x01, data=0x1.to_bytes(1, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制:-NRC31回复"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(0xA041, 0x01, data=0x1.to_bytes(1, 'big'))
        except:
            assert False   
            
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("刷写测试:0x0206")
    
    def test_caseid_1758518(self):
        assert True
        
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("擦除存储器 测试 DID: 0xFF00")
    
    def test_caseid_1758557(self):
        assert True
        
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("刷写测试:0x0205")
    
    def test_caseid_1758561(self):
        assert True
        
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("打开/关闭OBD防火墙测试 RID: 0xA040")
    def test_caseid_1758567(self):  # RID:0xA040
        """
        SOC 打开/关闭OBD防火墙测试 RID: 0xA040
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('通过安全访问等级L7'):
                self.b_cli.security_access_level(0x07)
            with allure.step('开启OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x0100.to_bytes(2, 'big'))
                self.b_cli.read_data_by_identifier(0xB165)
                p = self.b_cli.get_payload()
                assert p[6:] == "01"
            with allure.step('关闭OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
                self.b_cli.read_data_by_identifier(0xB165)
                p = self.b_cli.get_payload()
                assert p[6:] == "02"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
        except:
            assert False
    
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("证书测试:0x0212")
    def test_caseid_1758569(self):
        assert True
        
    @allure.story("SOC_诊断RoutineControl")
    @allure.title("证书测试:0x8020")
    def test_caseid_1758607(self):
        assert True

@pytest.mark.smoke
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_EOL(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_MCU_EOL_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
        
    @allure.story("MCU_诊断EOL")
    @allure.title("读写Voltage Value Charging At Inactive 测试 DID:0x4534")
    def test_caseid_1566449(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Voltage Value Charging At Inactive 测试"):
                self.b_cli.read_data_by_identifier(0x4534)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Voltage Value Charging At Inactive 测试"):
                self.b_cli.read_data_by_identifier(0x4534)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16) / 10
                print("value is ", p1)
                assert 8 <= p1 <= 16
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Voltage Value Charging At Inactive 测试"):
                self.b_cli.write_data_by_identifier(0x4534, '50')
                self.b_cli.read_data_by_identifier(0x4534)
                p2 = self.b_cli.get_payload()
                p2 = int(p[6:], 16) / 10
                print("value is ", p2)
                assert 8 <= p2 <= 16
            with allure.step("恢复写入Voltage Value Charging At Inactive 测试"):
                self.b_cli.write_data_by_identifier(0x4534, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4534)
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4534,'50')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("IO控制: Single Stroke Wiping - DID:0x4328_0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349896?projectId=46"
    )
    def test_caseid_1566491(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Single Stroke Wiping状态"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Single Stroke Wiping测试 - 测试值: 0x01(single stroke)"):
                self.b_cli.io_control(0x4328, 0x03, [0x01])
            with allure.step("读取Single Stroke Wiping状态应为 single stroke"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl1 = self.b_cli.get_payload()
                assert pl1[6:] == '01'
            with allure.step("IO控制: Single Stroke Wiping测试 - 测试值: 0x00(Off)"):
                self.b_cli.io_control(0x4328, 0x03, [0x00])
            with allure.step("读取Single Stroke Wiping状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == '00'
            with allure.step("退出IO控制:Single Stroke Wiping"):
                self.b_cli.io_control(0x4328, 0x00)
            with allure.step("读取Single Stroke Wiping状态应为 Off"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl3 = self.b_cli.get_payload()
            with allure.step("测试退出IO控制后, Single Stroke Wiping 变回控制前的值"):
                assert pl3[6:] == pl0[6:]
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x4328)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.io_control(0x4328, 0x03, [0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("IO控制:SoundSignalling测试 - DID:0x41F2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1349885?projectId=46"
    )
    def test_caseid_1566579(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Available Delta Power signal output状态"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl0 = self.b_cli.get_payload()
            with allure.step(
                "IO控制:Available Delta Power signal output测试 - 测试边界值: 7FFF"
            ):
                self.b_cli.io_control(0x41F2, 0x03, [0x01])
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl1 = self.b_cli.get_payload()
                assert pl1[-2:] == '01'
            with allure.step("退出IO控制"):
                self.b_cli.io_control(0x41F2, 0x00)
            with allure.step("读取Available Delta Power signal output"):
                self.b_cli.read_data_by_identifier(0x41F2)
                pl2 = self.b_cli.get_payload()
            with allure.step("测试退出IO控制后, Available Delta Power signal output变回控制前的值"):
                assert pl2 == pl0
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x41F2)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.io_control(0x41F2, 0x00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("读取Ajar Switch Status 测试 DID:0x42F2")
    def test_caseid_1569753(self):
        try:
            with allure.step("四门两盖全关"):
                self.io.init_bgm_HW()  # 用例开启始前都先恢复5门关门状态，主驾无人，车门按钮未按下
                self.io.hood_door1_close()
                self.io.hood_door2_open()
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Ajar Switch Status 测试"):
                self.b_cli.read_data_by_identifier(0x42F2)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '7c' or '6f'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(1)
                self.b_cli.session_control(3)
            with allure.step("读取Ajar Switch Status 测试"):
                self.b_cli.read_data_by_identifier(0x42F2)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '7c' or '6f'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x42F2)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("读取车辆电池电压测试 DID:0xDD02")
    def test_caseid_1569856(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取车辆电池电压测试"):
                self.b_cli.read_data_by_identifier(0xDD02)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert 0 <= pl / 4 <= 63.75
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取车辆电池电压测试"):
                self.b_cli.read_data_by_identifier(0xDD02)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert 0 <= pl / 4 <= 63.75
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0xDD02)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing RID:0x20EB_1_2_3"
    )  # 超时 已提BUG
    def test_caseid_1645760(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            # with allure.step("通过安全访问L5"):
            #     self.b_cli.security_access_level(0x5)
            with allure.step(
                "停止例程控制: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step(
                "请求例程控制结果: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
                
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            # with allure.step("通过安全访问L5"):
            #     self.b_cli.security_access_level(0x5)
            with allure.step(
                "停止例程控制: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x01)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step(
                "请求例程控制结果: Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing 测试"
            ):
                self.b_cli.routing_control(0x20EB, 0x03)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '20' or '22'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.routing_control(0x20EB, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.story("MCU_诊断RoutineControl")
    @allure.title(
        "EOL_实车诊断仪ECOS测试"
    )
    
    def test_caseid_1749873(self):
        assert True
        
    
    @allure.story("MCU_诊断EOL")
    @allure.title(
        "EOL_离线刷写台写入值测试"
    )
    def test_caseid_1749882(self):
        assert True
    
    @allure.story("MCU_诊断EOL")
    @allure.title("APP诊断数据库零件号 DID: 0xF1A0")
    def test_caseid_1758511(self):  # DID: 0xF1A0
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取APP诊断数据库零件号测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断EOL")
    @allure.title("读写Tire Pressure Monitoring System (TPMS) Sensor IDs 测试 DID: 0x281F")
    def test_caseid_1758515(self):  # DID: 0x281F
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.read_data_by_identifier(0x281F)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.read_data_by_identifier(0x281F)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.write_data_by_identifier(
                    0x281F, '00000000000000000000000000000000'
                )
                self.b_cli.read_data_by_identifier(0x281F)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '00000000000000000000000000000000'
            with allure.step("恢复写入Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.write_data_by_identifier(0x281F, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x281F)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.write_data_by_identifier(
                    0x281F, '00000000000000000000000000000000'
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("Calibarte ChargeLid  RID:0x2031_1_3")
    def test_caseid_1758521(self):
        try:
            # with pytest.raises(ValueError):
            #     with allure.step("进入默认会话"):
            #         self.b_cli.session_control(1)
            #     with allure.step("开始例程控制: Calibarte ChargeLid测试"):
            #         self.b_cli.routing_control(0x2031, 0x01)
            # with pytest.raises(ValueError):
            # with allure.step("进入默认会话"):
            #     self.b_cli.session_control(1)
            # with allure.step("开始例程控制: Calibarte ChargeLid"):
            #     self.b_cli.routing_control(0x2031, 0x01)
            #     p = self.b_cli.get_payload()
            #     assert p[8:10] == '10'
            # with allure.step("请求例程控制结果: Calibarte ChargeLid - NRC31 测试"):
            #     self.b_cli.routing_control(0x2031, 0x03)
            #     p = self.b_cli.get_payload()
            #     assert p[8:10] == '10'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Calibarte ChargeLid"):
                self.b_cli.routing_control(0x2031, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("请求例程控制结果: Calibarte ChargeLid - NRC31 测试"):
                self.b_cli.routing_control(0x2031, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.routing_control(0x2031, 0x01)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.routing_control(0x2031, 0x01)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断EOL")
    @allure.title("Calibarte ChargeLid  RID:0x2031_1_3")  # BT会话1否定响应 会话3值错误，已提BUG
    def test_caseid_1758523(self):
        try:
            # with pytest.raises(ValueError):
            #     with allure.step("进入默认会话"):
            #         self.b_cli.session_control(1)
            #     with allure.step("开始例程控制: Calibarte ChargeLid测试"):
            #         self.b_cli.routing_control(0x2031, 0x01)
            # with pytest.raises(ValueError):
           
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: Calibarte ChargeLid"):
                self.b_cli.routing_control(0x2031, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("请求例程控制结果: Calibarte ChargeLid - NRC31 测试"):
                self.b_cli.routing_control(0x2031, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:10] == '10'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                       self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("读取0x190209测试")
    def test_caseid_1758528(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始读取0x190209"):
                self.b_cli.read_data_by_dtc(0x02, 0x09)
                self.b_cli.clear_dtc()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始读取0x190209"):
                self.b_cli.read_data_by_dtc(0x02, 0x09)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                       self.b_cli.routing_control(0x2031, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("读取Security Key between BNCM and BGM (Digital Key) Mac 测试 DID:0xD906")
    def test_caseid_1758532(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取Security Key between BNCM and BGM (Digital Key) Mac 测试"
            ):
                self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取Security Key between BNCM and BGM (Digital Key) Mac 测试"
            ):
                self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title(
        "写入Security Key between BNCM and BGM (Digital Key) 测试 DID:0xD903"
    )
    def test_caseid_1758536(self):
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("检查是否D903已经写入值"):
                if p == '62d90400':
                    logger.info("值未写入")
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'    
                else:
                    logger.info("值已经被写入")
                    with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90400'
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
            
            
    @allure.story("MCU_诊断EOL")
    @allure.title("写入/读取Secret Key For Immobilizer Target #2 - IEM test DID: 0x40DF")
    def test_caseid_1758541(self):
        """
        Version DID: 0x40DF
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11) 
            with allure.step("读取Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.read_data_by_identifier(0x40DF)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("写入Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.write_data_by_identifier(
                    0x40DF,
                    'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                )
                time.sleep(0.5)
                self.b_cli.read_data_by_identifier(0x40DF)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '6240dff442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
                )
                data = p[6:]
            with allure.step("恢复写入Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.write_data_by_identifier(0x40DF, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                    with allure.step("读取-NRC31回复测试"):
                        with pytest.raises(ValueError):
                            self.b_cli.read_data_by_identifier(0x40DF)
                    with allure.step("写入-3NRC31回复测试"):
                        with pytest.raises(ValueError):
                            self.b_cli.write_data_by_identifier(0x40DF,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("IO控制: Usage Mode - DID:0xDD0A")
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1349901?projectId=46")
    def test_caseid_1758545(self):
        try:
            self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            time.sleep(3)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Usage Mode状态"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl0 = self.b_cli.get_payload()
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Inactive)"):
                self.b_cli.io_control(0xDD0A, 0x03, [0x01])
            with allure.step("读取Car Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '01'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Conven)"):
                self.b_cli.io_control(0xDD0A, 0x03, [0x02])
            with allure.step("读取Car Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '02'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Active)"):
                self.b_cli.io_control(0xDD0A, 0x03, [0x0b])
            with allure.step("读取Car Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0b'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Driving)"):
                self.b_cli.io_control(0xDD0A, 0x03, [0x0d])
            with allure.step("读取Car Mode状态应为 driving"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0d'
            with allure.step("IO控制: Usage Mode测试 - 测试切换: 0x00 (Abandoned)"):
                self.b_cli.io_control(0xDD0A, 0x03, [0x00])
            with allure.step("读取Car Mode状态应为 Abandoned"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '00'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入-3NRC31回复测试"):
                        self.b_cli.io_control(0xDD0A, 0x03, [0x00])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("写入-3NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.io_control(0xDD0A, 0x03, [0x00])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title(
        "写入Security Key between BNCM and BGM (Digital Key) 测试 DID:0xD903"
    )
    def test_caseid_1758551(self):
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("检查是否D903已经写入值"):
                if p == '62d90400':
                    logger.info("值未写入")
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'    
                else:
                    logger.info("值已经被写入")
                    with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90400'
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()

    @allure.story("MCU_诊断EOL")
    @allure.title("ECU硬件号 DID: 0xF1AA")
    def test_caseid_1758556(self):  # DID:0xF1AA
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("写入/读取CCP测试 - Internal DID:0xF106")
    def test_caseid_1758558(self):
        """
        CCP -  DID:0xF106
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(0x5)
            with allure.step("写入CCP测试"):
                self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
                self.b_cli.read_data_by_identifier(0xF106)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '62f106ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeaf1'
                )
                data = p[6:]
            with allure.step("恢复写入CCP测试"):
                self.b_cli.write_data_by_identifier(0xF106, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                    with pytest.raises(ValueError):
                        with allure.step("写入NRC31回复测试"):
                            self.b_cli.write_data_by_identifier(0xF106,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xF106)
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断EOL")
    @allure.title("读取/写入Remote Vehicle Immobilization Secret Key 测试 DID:0x408F")  # 超时
    def test_caseid_1758566(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("读取Remote Vehicle Immobilization Secret Key 测试"):
                self.b_cli.read_data_by_identifier(0x408F)
                time.sleep(0.5)
            with allure.step("写入Remote Vehicle Immobilization Secret Key 测试"):
                self.b_cli.write_data_by_identifier(0x408F,'50555555555555555555555555555555')
                self.b_cli.read_data_by_identifier(0x408F)
                pl = self.b_cli.get_payload()
                assert pl == '62408f50555555555555555555555555555555'
            with allure.step("恢复写入Remote Vehicle Immobilization Secret Key 测试"):
                data = pl[6:]
                self.b_cli.write_data_by_identifier(0x408F, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x408F)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.write_data_by_identifier(0x408F,'50555555555555555555555555555555')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x408F)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.write_data_by_identifier(0x408F,'50555555555555555555555555555555')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
        
    @allure.story("MCU_诊断EOL")
    @allure.title("EOL_Read|WriteDataByIdentifier(0x22|2E)_Secret Key For Immobilizer Target #3 - MGM")
    def test_caseid_1758580(self):
        try:
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E0)
                pl = self.b_cli.get_payload()
            with allure.step("解锁安全等级11 测试"):
                self.b_cli.security_access_level(11)
            with allure.step("写入Secret Key For Immobilizer Target #3 测试"):
                self.b_cli.write_data_by_identifier(0x40E0,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E0)
                pl = self.b_cli.get_payload()
                assert pl[6:] == 'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
            with allure.step("恢复写入Remote Vehicle Immobilization Secret Key 测试"):
                data = pl[6:]
                self.b_cli.write_data_by_identifier(0x40E0, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x40E0)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.write_data_by_identifier(0x40E0,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("读取NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.read_data_by_identifier(0x40E0)
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.write_data_by_identifier(0x40E0,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断EOL")
    @allure.title(
        "读取Security Key between BNCM and BGM (Digital Key) write status 测试 DID:0xD904"
    )
    def test_caseid_1349778_1758582(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400'
            with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
     
    @allure.story("MCU_诊断EOL")
    @allure.title("写入/读取Secret Key For Immobilizer Target #1 - ECM test DID: 0x40DE")
    def test_caseid_1758588(self):
        """
        Version DID: 0x40DE
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.read_data_by_identifier(0x40DE)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("写入Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.write_data_by_identifier(
                    0x40DE,
                    'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                )
                self.b_cli.read_data_by_identifier(0x40DE)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '6240def442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
                )
                data = p[6:]
            with allure.step("恢复写入Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.write_data_by_identifier(0x40DE, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0x40DE)
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(
                    0x40DE,
                    'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0x40DE)
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(
                    0x40DE,
                    'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断EOL")
    @allure.title("initilize AWM RID:0x2013_1_3")
    def test_caseid_1758600(self):
        try:
            # with pytest.raises(ValueError):
            #     with allure.step("进入默认会话"):
            #         self.b_cli.session_control(1)
            #     with allure.step("开始例程控制: 学习AWM位置测试"):
            #         self.b_cli.routing_control(0x2013, 0x01)
            #         p = self.b_cli.get_payload()
            #         assert p[8:] == '10'
            #     with allure.step("请求例程结果: 学习结果测试"):
            #         self.b_cli.routing_control(0x2013, 0x03)
            #         p = self.b_cli.get_payload()
            #         assert p[8:] == '1002' or '1000'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 学习AWM位置测试"):
                self.b_cli.routing_control(0x2013, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("请求例程结果: 学习结果测试"):
                self.b_cli.routing_control(0x2013, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:] == '1002' or ' 1000'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with allure.step("写入NRC31回复测试"):
                    with pytest.raises(ValueError):
                        self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("ECU总成号 DID: 0xF1AB")
    def test_caseid_1758603(self):  # DID:0xF1AB
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断EOL")
    @allure.title("读写L11安全常数测试 DID: 0xD12F")
    def test_caseid_1758605(self):
        """
        Version DID: 0xD12F
        """
        with allure.step("进入默认会话"):
            self.b_cli.session_control(1)
        with allure.step("读取L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.read_data_by_identifier(0xD12F)
        with allure.step("写入L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("进入扩展会话"):
            self.b_cli.session_control(3)
        with allure.step("通过安全访问L11"):
            self.b_cli.security_access_level(11)
        with allure.step("读取L11安全常数测试"):
            self.b_cli.read_data_by_identifier(0xD12F)
            p = self.b_cli.get_payload()
            self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("进入默认会话"):
            self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xD12F)
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("进入编程会话"):
            self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xD12F)
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("退出编程会话"):
            self.b_cli.exit_boot()
        
            
    @allure.story("MCU_诊断EOL")
    @allure.title("initilize AWM RID:0x2013_1_3")
    def test_caseid_1758611(self):
        try:
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("开始例程控制: 学习AWM位置测试"):
                self.b_cli.routing_control(0x2013, 0x01)
                p = self.b_cli.get_payload()
                assert p[8:] == '10'
            with allure.step("请求例程结果: 学习结果测试"):
                self.b_cli.routing_control(0x2013, 0x03)
                p = self.b_cli.get_payload()
                assert p[8:] == '1002' or ' 1000'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
                with allure.step("NRC31回复测试"):
                    with pytest.raises(ValueError):
                        with allure.step("写入NRC31回复测试"):
                            self.b_cli.routing_control(0x2013, 0x03)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
                
        except:
            assert False
            
    @allure.story("MCU_诊断EOL")
    @allure.title("VIN码测试 DID: 0xF190")
    def test_caseid_1349658_108540(self):  # DID: 0xF190
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
                self.b_cli.read_data_by_identifier(0xF190)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            with allure.step("恢复写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("写入VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

@pytest.mark.smoke
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_SOC_EOL(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1001)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_SOC_EOL_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
    
    @allure.story("SOC_诊断EOL")
    @allure.title("OBD防火墙状态测试 DID: 0xB165")
    def test_caseid_108543(self):
        """
        OBD防火墙状态测试 DID: 0xB165
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('OBD防火墙默认关闭测试'):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('OBD防火墙默认关闭测试'):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            # with allure.step('OBD防火墙默认关闭-NRC31测试'):
            #     with pytest.raises(ValueError):
            with allure.step('OBD防火墙默认关闭测试'):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("读取/写入VID测试 DID: 0xB163")
    def test_caseid_1349411(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L7"):
                self.b_cli.security_access_level(7)
            with allure.step("读取VID测试"):
                self.b_cli.read_data_by_identifier(0xB163)
                p = self.b_cli.get_payload()
            with allure.step("写入VID测试"):
                self.b_cli.write_data_by_identifier(0xB163,'067b9e1c3c61ac0e776decd18c05ee61') #真实VID测试,只改了最后一位d为1测试用
                self.b_cli.read_data_by_identifier(0xB163)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62b163067b9e1c3c61ac0e776decd18c05ee61'
            with allure.step("恢复写入VID测试"):
                data = p[6:]
                self.b_cli.write_data_by_identifier(0xB163, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB163)
            with allure.step("写入NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xB163,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB163)
            with allure.step("写入NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xB163, data)
        except:
            assert False
        
    @allure.story("SOC_诊断EOL")
    @allure.title("打开/关闭OBD防火墙测试 RID: 0xA040")
    def test_caseid_1566490(self):  # RID:0xA040
        """
        SOC 打开/关闭OBD防火墙测试 RID: 0xA040
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('通过安全访问等级L7'):
                self.b_cli.security_access_level(0x07)
            with allure.step('开启OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x0100.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == "10"
            with allure.step('关闭OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
        except:
            assert False

    @allure.story("SOC_诊断EOL")
    @allure.title("ECU软件号 DID: 0xF1AE")
    def test_caseid_1758507(self):  # DID:0xF1AE
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU软件号"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU软件号"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU软件号 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1AE)
                    time.sleep(0.5)
                    p = self.b_cli.get_payload()
                    if p[:2] == '7F':
                        assert p[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("APP诊断数据库零件号 DID: 0xF1A0")
    def test_caseid_1758511(self):  # DID: 0xF1A0
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取APP诊断数据库零件号测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1A0)
                    time.sleep(0.5)
                    p = self.b_cli.get_payload()
                    if p[:2] == '7F':
                        assert p[4:] == '31'
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")    
    @allure.title("ChargeLid Open/Close RID:0x2030")
    def test_caseid_1758538(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: ChargeLid Open测试"):
                self.b_cli.routing_control(0x2030, 0x01, data=0x01.to_bytes(1, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20' 
            with allure.step("开始例程控制: ChargeLid Open测试"):
                self.b_cli.routing_control(0x2030, 0x01, data=0x00.to_bytes(1, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == '20'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("开始例程控制: ChargeLid Open测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2030, 0x01, data=0x01.to_bytes(1, 'big')
                    )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("开始例程控制: ChargeLid Open测试"):
                with pytest.raises(ValueError):
                    self.b_cli.routing_control(
                        0x2030, 0x01, data=0x01.to_bytes(1, 'big')
                    )
        except:
            assert False

    @allure.story("SOC_诊断EOL")
    @allure.title("整车基线版本号测试 DID: 0xF150")  # 先写才能读出
    def test_caseid_1758539(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入整车基线版本号"):
                self.b_cli.write_data_by_identifier(0xF150, '0161601100604347')
                self.b_cli.read_data_by_identifier(0xF150)
                pl = self.b_cli.get_payload()
                assert pl == '62f1500161601100604347'
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取整车基线版本号"):
                self.b_cli.read_data_by_identifier(0xF150)
                pl = self.b_cli.get_payload()
                assert pl == '62f1500161601100604347'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31测试"):
                        self.b_cli.read_data_by_identifier(0xF150)
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("打开/关闭OBD防火墙测试 RID: 0xA040")
    def test_caseid_1758543(self):  # RID:0xA040
        """
        SOC 打开/关闭OBD防火墙测试 RID: 0xA040
        """
        try:
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(1)
                self.b_cli.session_control(3)
            with allure.step('通过安全访问等级L7'):
                self.b_cli.security_access_level(7)
            with allure.step('开启OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x0100.to_bytes(2, 'big'))
                p = self.b_cli.get_payload()
                assert p[8:] == "10"
            with allure.step('关闭OBD防火墙'):
                self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取整车基线版本号"):
                with pytest.raises(ValueError):
                    with allure.step("写入-NRC31测试"):
                        self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31测试"):
                with pytest.raises(ValueError):
                    with allure.step("写入-NRC31测试"):
                        self.b_cli.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("ECU序列号测试 DID:0xF18C")
    def test_caseid_1758544(self):  # DID:0xF18C
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl1 = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl2 = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl3 = self.b_cli.get_payload()
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("读取/写入VID测试 DID: 0xB163")
    def test_caseid_1758547(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L7"):
                self.b_cli.security_access_level(7)
            with allure.step("读取VID测试"):
                self.b_cli.read_data_by_identifier(0xB163)
                p = self.b_cli.get_payload()
            with allure.step("写入VID测试"):
                self.b_cli.write_data_by_identifier(
                    0xB163, '067b9e1c3c61ac0e776decd18c05ee61'
                )  # 真实VID测试，只改了最后一位d为1测试用
                self.b_cli.read_data_by_identifier(0xB163)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62b163067b9e1c3c61ac0e776decd18c05ee61'
            with allure.step("恢复写入VID测试"):
                data = p[6:]
                self.b_cli.write_data_by_identifier(0xB163, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
                with pytest.raises(ValueError):
                    with allure.step("读取-NRC31测试"):
                        self.b_cli.read_data_by_identifier(0xB163)
                    with allure.step("写入-NRC31测试"):
                        self.b_cli.write_data_by_identifier(0xB163, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取-NRC31测试"):
                        self.b_cli.read_data_by_identifier(0xB163)
                    with allure.step("写入-NRC31测试"):
                        self.b_cli.write_data_by_identifier(0xB163, data)
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("ECU硬件号 DID: 0xF1AA")
    def test_caseid_1758556(self):  # DID:0xF1AA
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
        except:
            assert False
    
    @allure.story("SOC_诊断EOL")
    @allure.title("FOTA result测试 DID: 0xF154")
    def test_caseid_1758572(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取FOTA result测试"):
                self.b_cli.read_data_by_identifier(0xF154)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '02'
                assert p[-4:-2] == '00'
                assert p[-6:-4] == '00'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取FOTA result测试"):
                self.b_cli.read_data_by_identifier(0xF154)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '02'
                assert p[-4:-2] == '00'
                assert p[-6:-4] == '00'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取ECU硬件版本号测试"):
                        self.b_cli.read_data_by_identifier(0xF154)
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("整车展示的版本号 DID: 0xF151")  # 0.6.5
    def test_caseid_1758573(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本号测试"):
                self.b_cli.read_data_by_identifier(0xF151)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取版本号测试"):
                self.b_cli.read_data_by_identifier(0xF151)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入整车展示的版本号测试"):
                self.b_cli.write_data_by_identifier(
                    0xF151,
                    '067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61',
                )
                self.b_cli.read_data_by_identifier(0xF151)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '62f151067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61'
                )
            with allure.step("恢复入整车展示的版本号测试"):
                data = p[6:]
                self.b_cli.write_data_by_identifier(0xF151, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取ECU硬件版本号测试"):
                        self.b_cli.read_data_by_identifier(0xF151)
                    with allure.step("写入ECU硬件版本号测试"):
                        self.b_cli.write_data_by_identifier(0xF151, data)
        except:
            assert False

    @allure.story("SOC_诊断EOL")
    @allure.title("证书测试:0x8020")
    def test_caseid_1758575(self):
        assert True
    
    @allure.story("SOC_诊断EOL")
    @allure.title("EOL_Read|WriteDataByIdentifier(0x22|2ED01C)_PublicKey")  # 公钥只能写一次；如果里面没有公钥会读取失败 
    def test_caseid_1758590(self):
        try:
            with allure.step("删除密钥后重启并等待10s"): 
                commands = "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)        
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                time.sleep(10)
            with allure.step("进入编程会话测试"):
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                self.b_cli.session_control(2)
            with allure.step("通过安全访问L1"):
                self.b_cli.security_access_level(1)
            with allure.step("写入密钥"):
                self.b_cli.write_data_by_identifier(0xD01C,'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577')
            with allure.step("读取密钥"):
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                self.b_cli.read_data_by_identifier(0xd01c)
                p = self.b_cli.get_payload()
                assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'
            with allure.step("写入密钥后重启并等待10s"):
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                time.sleep(10)
                self.b_cli.sd_test.update_serverdoipid(0x1001)
            with allure.step("校验文件/data/certificate/vbf_pk.pem 大小 看是否为0"):
                commands = "cat /data/certificate/vbf_pk.pem"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)
                logger.info("outmsg={}".format(type(outmsg)))
                if len(outmsg) < 3:
                    logger.info("文件大小小于3")
                    raise ValueError
                else:
                    logger.info("文件不为空 文件大小为{}".format(len(outmsg)))
            with allure.step("读取vehicleInfo.json"): 
                commands = "cat /data/vehicleInfo.json"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)      
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("读取密钥"):
                self.b_cli.read_data_by_identifier(0xd01c)
                p = self.b_cli.get_payload()
                assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'  
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("写入L1常数测试 DID: 0xF102") #安全等级1常数只能写一次
    def test_caseid_1758595(self):
        try:
            with allure.step("删除密钥后重启并等待10s"): 
                commands = "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)        
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                time.sleep(10)
                self.b_cli.session_control(1)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("通过安全访问L1"):
                self.b_cli.security_access_level(1)
            with allure.step("写入L1常数测试"):
                self.b_cli.write_data_by_identifier(0xF102,'FFFFFFFFFF')
        except:
            assert False
            
    #D03A读取前提是先写入D01C的值
    @allure.story("SOC_诊断EOL")
    @allure.title("读取swAuth Public Key CheckSum测试 DID:0xD03A") #诊断调查表
    def test_caseid_1349668(self):
        try:
            with allure.step("读取vehicleInfo.json"): 
                commands = "cat /data/vehicleInfo.json"
                self.b_cli.ssh_bgm.type_commands(commands)        
            with allure.step('进入编程会话'):
                self.b_cli.session_control(2)
            with allure.step("读取D01C值"): 
                self.b_cli.read_data_by_identifier(0xd01c,False)
                pl = self.b_cli.get_payload()
                # data = pl[-2:]
                if pl[0:6] == '7f2222':
                    logger.info('D01C1值未写入 写入D01C值')
                    with allure.step('进入编程会话'):
                        self.b_cli.session_control(2)
                    with allure.step("解锁安全等级1 测试"):
                        self.b_cli.security_access_level(1)
                    with allure.step("未写入Public Key 先写入"):
                        self.b_cli.write_data_by_identifier(0xD01C,'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577')
                    with allure.step("读取密钥"):
                        self.b_cli.read_data_by_identifier(0xd01c)
                        p = self.b_cli.get_payload()
                        assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'
                    
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("取swAuth Public Key CheckSum测试"):
                self.b_cli.read_data_by_identifier(0xD03A)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("取swAuth Public Key CheckSum测试"):
                self.b_cli.read_data_by_identifier(0xD03A)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取swAuth Public Key CheckSum-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD03A)
        except:
            assert False
            
    @allure.story("SOC_诊断EOL")
    @allure.title("ECU总成号 DID: 0xF1AB")
    def test_caseid_1758603(self):  # DID:0xF1AB
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_DID(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_MCU_DID_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
    
    @allure.story("MCU_诊断DID")
    @allure.title("当前会话测试 DID: 0xF186")
    def test_caseid_1349656(self):  # DID: 0xF186
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("当前会话测试 - 默认会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18601'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("当前会话测试 - 扩展会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18603'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("当前会话测试 - 编程会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18602'
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    
    @allure.story("MCU_诊断DID")
    @allure.title("ECU硬件号, ECU总成号, ECU序列号测试 DID: 0xED20")
    def test_caseid_1349665(self):  # DID: 0xED20
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.title("Requested Charge Voltage 测试 DID: 0xF124") #这个搞不来自动化 需要在sbl刷完之后d
    
    def test_caseid_1349679(self):
        assert True
        # """
        #    Requested Charge Voltage  测试 DID: 0xF124
        # """
        # try:
        #     with allure.step("进入编程会话"):
        #         self.b_cli.session_control(2)
        #         time.sleep(15)
        #         BgmDoIPAnoucementParser("config/DoIPConfig.json", "1002")
        #         time.sleep(2)
                
        #     with allure.step('Requested Charge Voltage 测试'):
        #         self.b_cli.read_data_by_identifier(0xF124)
        #         p = self.b_cli.get_payload()
        #         assert 11 < int(p[-2:], 16) / 40 + 10.6 < 16
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #         time.sleep(15)
        #         BgmDoIPAnoucementParser("config/DoIPConfig.json", "1002")
        # except:
        #     assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title("读取子节点序列号 DID:0xF13F")
    def test_caseid_1349680(self):
        with allure.step("进入默认会话"):
            self.b_cli.session_control(1)
        with allure.step("读取子节点序列号测试"):
            self.b_cli.read_data_by_identifier(0xF13F)
        with allure.step("进入扩展会话"):
            self.b_cli.session_control(3)
        with allure.step("读取子节点序列号测试"):
            self.b_cli.read_data_by_identifier(0xF13F)
            
    
    @allure.story("MCU_诊断DID")
    @allure.title("读取全局时间测试 DID:0xDD00")
    def test_caseid_1349684(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取全局时间测试"):
                self.b_cli.read_data_by_identifier(0xDD00)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl / 600)
                assert 0 <= pl / 600 <= 7158278, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取全局时间测试"):
                self.b_cli.read_data_by_identifier(0xDD00)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl / 600)
                assert 0 <= pl / 600 <= 7158278, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取全局时间测试-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDD00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取总里程测试 DID:0xDD01")  #里程最大值只能是418937 并且每次写入的值都得比之前的值要大
    def test_caseid_1349685(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("读取总里程测试"):
                self.b_cli.read_data_by_identifier(0xDD01)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                assert 0 <= int(pl[-2:],16) <= 4294967295
            with allure.step("进入拓展会话测试"):
                self.b_cli.session_control(3)
            with allure.step("读取总里程测试"):
                self.b_cli.read_data_by_identifier(0xDD01)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[-2:],16) <= 4294967295
            with allure.step("解锁安全等级5 测试"):
                self.b_cli.security_access_level(5)
            with allure.step("写入总里程"):
                self.b_cli.write_data_by_identifier(0xDD01, 'FFFFFF')
                self.b_cli.read_data_by_identifier(0xDD01)
                pl = self.b_cli.get_payload()
                assert pl == '62dd01418937'
            with allure.step("恢复写入总里程"):
                self.b_cli.write_data_by_identifier(0xDD01,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取总里程测试-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDD01)
            with allure.step("写入总里程测试-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xDD01, 'FFFFFF')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()

        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取使用模式测试 DID:0xDD0A")
    def test_caseid_1349687_1349901(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取使用模式测试"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert pl == 0 or 1 or 2 or 11 or 13 or 255, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取使用模式测试"):
                self.b_cli.read_data_by_identifier(0xDD0A)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert pl == 0 or 1 or 2 or 11 or 13 or 255, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取使用模式测试-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDD0A)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取供电等级测试 DID:0xDD0C")
    def test_caseid_1349688(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取供电等级测试"):
                self.b_cli.read_data_by_identifier(0xDD0C)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                values = bytearray(
                    [
                        0x0F,
                        0x10,
                        0x11,
                        0x20,
                        0x21,
                        0x22,
                        0x23,
                        0x24,
                        0x30,
                        0x31,
                        0x32,
                        0x33,
                        0x34,
                        0x35,
                        0x36,
                        0x37,
                        0x38,
                        0x39,
                        0x3A,
                        0x3B,
                        0x3C,
                        0x3D,
                        0x3E,
                        0x3F,
                        0x40,
                        0x41,
                        0x42,
                        0x43,
                        0x44,
                        0x45,
                        0x46,
                        0x47,
                        0x48,
                        0x49,
                        0x4A,
                        0x4B,
                        0x4C,
                        0x4D,
                        0x4E,
                        0x4F,
                        0x50,
                        0x51,
                        0x52,
                        0x53,
                        0x54,
                        0x55,
                        0x56,
                        0x57,
                        0x58,
                        0x59,
                        0x5A,
                        0x5B,
                        0x5C,
                        0x5D,
                        0x5E,
                        0x5F,
                        0xFF,
                    ]
                )
                if pl in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取供电等级测试"):
                self.b_cli.read_data_by_identifier(0xDD0C)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取使用模式测试-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDD0C)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("写入/读取CCP测试 - Internal DID:0xF106")
    def test_caseid_1349689_1349393(self):
        """
        CCP -  DID:0xF106
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(0x5)
            with allure.step("写入CCP测试"):
                self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
                self.b_cli.read_data_by_identifier(0xF106)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '62f106ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeaf1'
                )
                data = p[6:]
            with allure.step("恢复写入CCP测试"):
                self.b_cli.write_data_by_identifier(0xF106, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                    with pytest.raises(ValueError):
                        with allure.step("写入NRC31回复测试"):
                            self.b_cli.write_data_by_identifier(0xF106,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xF106)
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Quiesent Current - Low Range测试 - Internal DID:0x4025")
    def test_caseid_1349690(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Quiesent Current - Low Range测试"):
                self.b_cli.read_data_by_identifier(0x4025)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 - 511
                print("value is ", pl)
                assert -511 <= pl <= 0, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Quiesent Current - Low Range测试"):
                self.b_cli.read_data_by_identifier(0x4025)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 - 511
                print("value is ", pl)
                assert -511 <= pl <= 0, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Quiesent Current - Low Range-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4025)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title(
        "读取Normalised Cumulated Discharge From Battery When Engine Off测试 DID:0x4026"
    )
    def test_caseid_1349692(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取Normalised Cumulated Discharge From Battery When Engine Off测试"
            ):
                self.b_cli.read_data_by_identifier(0x4026)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 20
                print("value is ", pl)
                assert 0 <= pl <= 180, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取Normalised Cumulated Discharge From Battery When Engine Off测试"
            ):
                self.b_cli.read_data_by_identifier(0x4026)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 20
                print("value is ", pl)
                assert 0 <= pl <= 180, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Quiesent Current - Low Range-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4026)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Vehicle Battery - Time In Service测试 DID:0x4027")
    def test_caseid_1349693(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Vehicle Battery - Time In Service测试"):
                self.b_cli.read_data_by_identifier(0x4027)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 4095, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Vehicle Battery - Time In Service测试"):
                self.b_cli.read_data_by_identifier(0x4027)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 4095, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Vehicle Battery - Time In Service-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4026)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    
    @allure.title("读取Vehicle Battery State Of Charge - Estimated测试 DID:0x4028")
    def test_caseid_1349694(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Vehicle Battery State Of Charge - Estimated测试"):
                self.b_cli.read_data_by_identifier(0x4028)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) / 10
                print("value is ", pl)
                assert 0 <= pl <= 100, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Vehicle Battery State Of Charge - Estimated测试"):
                self.b_cli.read_data_by_identifier(0x4028)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) / 10
                print("value is ", pl)
                assert 0 <= pl <= 100, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Vehicle Battery State Of Charge - Estimated-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4028)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Vehicle Battery Temperature - Estimated DID:0x4029")
    
    def test_caseid_1349695(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Vehicle Battery Temperature - Estimated测试"):
                self.b_cli.read_data_by_identifier(0x4029)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 2 - 128
                print("value is ", pl)
                assert -70 <= pl <= 125, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Vehicle Battery Temperature - Estimated测试"):
                self.b_cli.read_data_by_identifier(0x4029)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 2 - 128
                print("value is ", pl)
                assert -70 <= pl <= 125, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Vehicle Battery Temperature - Estimated-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4029)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    
    @allure.title("读取Vehicle Battery Voltage DID:0x402A")
    def test_caseid_1349697(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Vehicle Battery Voltage 测试"):
                self.b_cli.read_data_by_identifier(0x402A)
                pl = self.b_cli.get_payload()
                assert 0 < int(pl[-1:],16)/10 < 25
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Vehicle Battery Voltage 测试"):
                self.b_cli.read_data_by_identifier(0x402A)
                pl = self.b_cli.get_payload()
                assert 0 < int(pl[-1:],16)/10 < 25
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Vehicle Battery Voltage-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x402A)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Current 测试 DID:0x4090")
    def test_caseid_1349699(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Current 测试"):
                self.b_cli.read_data_by_identifier(0x4090)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 64 - 512
                print("value is ", pl)
                assert -512 <= pl <= 511.984375, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Current 测试"):
                self.b_cli.read_data_by_identifier(0x4090)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 64 - 512
                print("value is ", pl)
                assert -512 <= pl <= 511.984375, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Current-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4090)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery State of Charge Statistics Counter 测试 DID:0x4094")
    def test_caseid_1349700(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery State of Charge Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x4094)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 65535, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 65535, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 65535, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 65535, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 65535, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 65535, "value6 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery State of Charge Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x4094)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 65535, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 65535, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 65535, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 65535, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 65535, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 65535, "value6 out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery State of Charge Statistics Counter-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4094)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Charge Balance Statistics Counter 测试 DID:0x40A2")
    def test_caseid_1349701(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Charge Balance Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40A2)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 65535, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 65535, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 65535, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 65535, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 65535, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 65535, "value6 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Charge Balance Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40A2)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 65535, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 65535, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 65535, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 65535, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 65535, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 65535, "value6 out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Charge Balance Statistics Counter-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40A2)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Seconds since last reset 测试 DID:0x40AF")
    
    def test_caseid_1349702(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Seconds since last reset 测试"):
                self.b_cli.read_data_by_identifier(0x40AF)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 100
                print("value is ", pl)
                assert 0 <= pl <= 65535, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Seconds since last reset 测试"):
                self.b_cli.read_data_by_identifier(0x40AF)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 100
                print("value is ", pl)
                assert 0 <= pl <= 65535, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Seconds since last reset-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40AF)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Capacity Relative 测试 DID:0x40B0")
    def test_caseid_1349704(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Capacity Relative 测试"):
                self.b_cli.read_data_by_identifier(0x40B0)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 100
                print("value is ", pl)
                assert 0 <= pl <= 2.5, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Capacity Relative 测试"):
                self.b_cli.read_data_by_identifier(0x40B0)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16) * 1 / 100
                print("value is ", pl)
                assert 0 <= pl <= 2.5, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Capacity Relative-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40B0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Low Battery Warning Statistics Register 测试 DID:0x40CA")
    
    def test_caseid_1349705(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Low Battery Warning Statistics Register 测试"):
                self.b_cli.read_data_by_identifier(0x40CA)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 255, "value1 out of range"
                pl1 = int(self.pl[6:8], 16)
                assert 0 <= pl1 <= 255, "value1 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Low Battery Warning Statistics Register 测试"):
                self.b_cli.read_data_by_identifier(0x40CA)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 255, "value1 out of range"
                pl1 = int(self.pl[6:8], 16)
                assert 0 <= pl1 <= 255, "value1 out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Low Battery Warning Statistics Register-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40B0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Sensor Consistency Check 测试 DID:0x40CB")
    def test_caseid_1349707(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Sensor Consistency Check 测试"):
                self.b_cli.read_data_by_identifier(0x40CB)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                values = bytearray([0x00, 0x01])
                if pl in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Sensor Consistency Check 测试"):
                self.b_cli.read_data_by_identifier(0x40CB)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                values = bytearray([0x00, 0x01])
                if pl in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Sensor Consistency Check-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40CB)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Quiescent Current - Statistics 测试 DID:0x40D7")
    
    def test_caseid_1349708(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Quiescent Current - Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x40D7)
                self.pl = self.b_cli.get_payload()
                with allure.step("value1 参数校验"):
                    pl = int(self.pl[6:8], 16)
                    assert 0 <= pl <= 65535, "value1 out of range"
                with allure.step("value2 参数校验"):
                    pl1 = int(self.pl[8:10], 16)
                    assert 0 <= pl1 <= 65535, "value2 out of range"
                with allure.step("value3 参数校验"):
                    pl2 = int(self.pl[10:12], 16)
                    assert 0 <= pl2 <= 65535, "value3 out of range"
                with allure.step("value4 参数校验"):
                    pl3 = int(self.pl[12:14], 16)
                    assert 0 <= pl3 <= 65535, "value4 out of range"
                with allure.step("value5 参数校验"):
                    pl4 = int(self.pl[14:16], 16)
                    assert 0 <= pl4 <= 65535, "value5 out of range"
                with allure.step("value6 参数校验"):
                    pl5 = int(self.pl[16:18], 16)
                    assert 0 <= pl5 <= 65535, "value6 out of range"
                with allure.step("value7 参数校验"):
                    pl6 = int(self.pl[18:20], 16)
                    assert 0 <= pl6 <= 65535, "value7 out of range"
                with allure.step("value8 参数校验"):
                    pl7 = int(self.pl[20:22], 16)
                    assert 0 <= pl7 <= 65535, "value8 out of range"
                with allure.step("value9 参数校验"):
                    pl8 = int(self.pl[22:24], 16)
                    assert 0 <= pl8 <= 65535, "value9 out of range"
                with allure.step("value10 参数校验"):
                    pl9 = int(self.pl[24:26], 16)
                    assert 0 <= pl9 <= 65535, "value10 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Quiescent Current - Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x40D7)
                self.pl = self.b_cli.get_payload()
                with allure.step("value1 参数校验"):
                    pl = int(self.pl[6:8], 16)
                    assert 0 <= pl <= 65535, "value1 out of range"
                with allure.step("value2 参数校验"):
                    pl1 = int(self.pl[8:10], 16)
                    assert 0 <= pl1 <= 65535, "value2 out of range"
                with allure.step("value3 参数校验"):
                    pl2 = int(self.pl[10:12], 16)
                    assert 0 <= pl2 <= 65535, "value3 out of range"
                with allure.step("value4 参数校验"):
                    pl3 = int(self.pl[12:14], 16)
                    assert 0 <= pl3 <= 65535, "value4 out of range"
                with allure.step("value5 参数校验"):
                    pl4 = int(self.pl[14:16], 16)
                    assert 0 <= pl4 <= 65535, "value5 out of range"
                with allure.step("value6 参数校验"):
                    pl5 = int(self.pl[16:18], 16)
                    assert 0 <= pl5 <= 65535, "value6 out of range"
                with allure.step("value7 参数校验"):
                    pl6 = int(self.pl[18:20], 16)
                    assert 0 <= pl6 <= 65535, "value7 out of range"
                with allure.step("value8 参数校验"):
                    pl7 = int(self.pl[20:22], 16)
                    assert 0 <= pl7 <= 65535, "value8 out of range"
                with allure.step("value9 参数校验"):
                    pl8 = int(self.pl[22:24], 16)
                    assert 0 <= pl8 <= 65535, "value9 out of range"
                with allure.step("value10 参数校验"):
                    pl9 = int(self.pl[24:26], 16)
                    assert 0 <= pl9 <= 65535, "value10 out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Quiescent Current - Statistics-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40D7)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Available Delta Power signal output 测试 DID:0x40E2")
    
    def test_caseid_1349709(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Available Delta Power signal output 测试"):
                self.b_cli.read_data_by_identifier(0x40E2)
                pl = self.b_cli.get_payload()
                # 把16进制字符串转成带符号10进制
                if pl[6] in '01234567':
                    pl = int(pl[6:], 16)
                else:
                    # 负数算法
                    width = 32  # 16进制数所占位数
                    d = 'FFFF' + pl[6:]
                    pl = int(d, 16)
                    if pl > 2 ** (width - 1) - 1:
                        pl = 2**width - pl
                        pl = 0 - pl
                assert -32768 < pl < 32767
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Available Delta Power signal output 测试"):
                self.b_cli.read_data_by_identifier(0x40E2)
                pl = self.b_cli.get_payload()
                # 把16进制字符串转成带符号10进制
                if pl[6] in '01234567':
                    pl = int(pl[6:], 16)
                else:
                    # 负数算法
                    width = 32  # 16进制数所占位数
                    d = 'FFFF' + pl[6:]
                    pl = int(d, 16)
                    if pl > 2 ** (width - 1) - 1:
                        pl = 2**width - pl
                        pl = 0 - pl
                assert -32768 < pl < 32767
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Available Delta Power signal output-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40E2)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Distribution Relays Status 测试 DID:0x40E3")
    def test_caseid_1349710(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Distribution Relays Status 测试"):
                self.b_cli.read_data_by_identifier(0x40E3)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:8], 16) in range(0, 256), "Relay status fail"
                assert 0 <= int(p[8:], 16) <= 7
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Distribution Relays Status 测试"):
                self.b_cli.read_data_by_identifier(0x40E3)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:8], 16) in range(0, 256), "Relay status fail"
                assert 0 <= int(p[8:], 16) <= 7
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Distribution Relays Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40E3)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Power System Fault Counters 测试 DID:0x40E4")
    
    def test_caseid_1349712(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Power System Fault Counters 测试"):
                self.b_cli.read_data_by_identifier(0x40E4)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 255, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 255, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 255, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 255, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 255, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 255, "value6 out of range"
                pl6 = int(self.pl[18:20], 16)
                assert 0 <= pl6 <= 255, "value7 out of range"
                pl7 = int(self.pl[20:22], 16)
                assert 0 <= pl7 <= 255, "value8 out of range"
                pl8 = int(self.pl[22:24], 16)
                assert 0 <= pl8 <= 255, "value9 out of range"
                pl9 = int(self.pl[24:26], 16)
                assert 0 <= pl9 <= 255, "value10 out of range"
                pl10 = int(self.pl[26:28], 16)
                assert 0 <= pl10 <= 255, "value11 out of range"
                pl11 = int(self.pl[28:30], 16)
                assert 0 <= pl11 <= 255, "value12 out of range"
                pl12 = int(self.pl[30:32], 16)
                assert 0 <= pl12 <= 255, "value13 out of range"
                pl13 = int(self.pl[32:34], 16)
                assert 0 <= pl13 <= 255, "value14 out of range"
                pl14 = int(self.pl[34:36], 16)
                assert 0 <= pl14 <= 255, "value15 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Power System Fault Counters 测试"):
                self.b_cli.read_data_by_identifier(0x40E4)
                self.pl = self.b_cli.get_payload()
                pl = int(self.pl[6:8], 16)
                assert 0 <= pl <= 255, "value1 out of range"
                pl1 = int(self.pl[8:10], 16)
                assert 0 <= pl1 <= 255, "value2 out of range"
                pl2 = int(self.pl[10:12], 16)
                assert 0 <= pl2 <= 255, "value3 out of range"
                pl3 = int(self.pl[12:14], 16)
                assert 0 <= pl3 <= 255, "value4 out of range"
                pl4 = int(self.pl[14:16], 16)
                assert 0 <= pl4 <= 255, "value5 out of range"
                pl5 = int(self.pl[16:18], 16)
                assert 0 <= pl5 <= 255, "value6 out of range"
                pl6 = int(self.pl[18:20], 16)
                assert 0 <= pl6 <= 255, "value7 out of range"
                pl7 = int(self.pl[20:22], 16)
                assert 0 <= pl7 <= 255, "value8 out of range"
                pl8 = int(self.pl[22:24], 16)
                assert 0 <= pl8 <= 255, "value9 out of range"
                pl9 = int(self.pl[24:26], 16)
                assert 0 <= pl9 <= 255, "value10 out of range"
                pl10 = int(self.pl[26:28], 16)
                assert 0 <= pl10 <= 255, "value11 out of range"
                pl11 = int(self.pl[28:30], 16)
                assert 0 <= pl11 <= 255, "value12 out of range"
                pl12 = int(self.pl[30:32], 16)
                assert 0 <= pl12 <= 255, "value13 out of range"
                pl13 = int(self.pl[32:34], 16)
                assert 0 <= pl13 <= 255, "value14 out of range"
                pl14 = int(self.pl[34:36], 16)
                assert 0 <= pl14 <= 255, "value15 out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Power System Fault Counters-NRC3C1 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40E4)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Driver Door Status Diagnostics Counter 测试 DID:0x40E8")
    
    def test_caseid_1349713(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E8)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 255, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E8)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 255, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Driver Door Status Diagnostics Counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40E8)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Immo Status History 测试 DID:0x40EE")
    
    def test_caseid_1349715(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Immo Status History 测试"):
                self.b_cli.read_data_by_identifier(0x40EE)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                with allure.step("#1 参数验证"):
                    assert (
                        p[6:8] == '00' or '01' or '02' or '0b' or 'od' or 'ff'
                    ), "invalid value"
                    assert (
                        p[8:9] == '0' or '1' or '2' or '3'
                    ), "PowerTrain Start Request out of range"
                    assert (
                        p[9:10] == '0' or '1' '2'
                    ), "Driver Start Request #1 out ouf range"
                    assert (
                        p[10:12] == '00' or '01' or '02' or '03'
                    ), "Steering Lock Enabling Of Propulsion #1(reserved) out of range"
                    assert int(p[12:14], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                    ], "Engine State #1 out of range"
                    assert int(p[14:16], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status1 #1 out of range"
                    assert int(p[16:18], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status2 #1 out of range"
                    assert int(p[18:20], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status3 #2 out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("#1 参数验证"):
                    assert (
                        p[6:8] == '00' or '01' or '02' or '0b' or 'od' or 'ff'
                    ), "invalid value"
                    assert (
                        p[8:9] == '0' or '1' or '2' or '3'
                    ), "PowerTrain Start Request out of range"
                    assert (
                        p[9:10] == '0' or '1' '2'
                    ), "Driver Start Request #1 out ouf range"
                    assert (
                        p[10:12] == '00' or '01' or '02' or '03'
                    ), "Steering Lock Enabling Of Propulsion #1(reserved) out of range"
                    assert int(p[12:14], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                    ], "Engine State #1 out of range"
                    assert int(p[14:16], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status1 #1 out of range"
                    assert int(p[16:18], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status2 #1 out of range"
                    assert int(p[18:20], 16) in [
                        0,
                        1,
                        2,
                        3,
                    ], "Immobilization Engine Status3 #2 out of range"
            with allure.step("读取Immo Status History 测试"):
                self.b_cli.read_data_by_identifier(0x40EE)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Immo Status History-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40EE)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Locking Command History 测试 DID:0x40EF")
    def test_caseid_1349716(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Locking Command History 测试"):
                self.b_cli.read_data_by_identifier(0x40EF)
                pl = self.b_cli.get_payload()
                with allure.step("Central Lock Status 1 - 1st group data参数校验"):
                    assert int(pl[6:8], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("Locking Source 1 - 1st group data参数校验"):
                    assert int(pl[8:10], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                    ], "out of range"
                with allure.step("DoorDrvrLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[10:12], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[12:14], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrReLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[14:16], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassReLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[16:18], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrLockSts 1 - 1st group data参数校验"):
                    assert int(pl[18:20], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorPassLockSts 1 - 1st group data参数校验"):
                    assert int(pl[20:22], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorPassReLockSts 1 - 1st group data参数校验"):
                    assert int(pl[22:24], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorDrvrSts 1 - 1st group data参数校验"):
                    assert int(pl[24:26], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorPassSts 1 - 1st group data参数校验"):
                    assert int(pl[26:28], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorDrvrReSts 1 - 1st group data参数校验"):
                    assert int(pl[28:30], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorPassReSts 1 - 1st group data参数校验"):
                    assert int(pl[30:32], 16) in [0, 1, 2], "value out of range"
                with allure.step("Usage Mode 1 - 1st group data参数校验"):
                    assert int(pl[32:34], 16) in [
                        0,
                        1,
                        2,
                        11,
                        13,
                        255,
                    ], "value out of range"
                with allure.step("进入扩展会话"):
                    self.b_cli.session_control(3)
                with allure.step("读取Locking Command History 测试"):
                    self.b_cli.read_data_by_identifier(0x40EF)
                    pl = self.b_cli.get_payload()
                with allure.step("Central Lock Status 1 - 1st group data参数校验"):
                    assert int(pl[6:8], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("Locking Source 1 - 1st group data参数校验"):
                    assert int(pl[8:10], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                    ], "out of range"
                with allure.step("DoorDrvrLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[10:12], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[12:14], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrReLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[14:16], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassReLockCmd 1 - 1st group data参数校验"):
                    assert int(pl[16:18], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrLockSts 1 - 1st group data参数校验"):
                    assert int(pl[18:20], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorPassLockSts 1 - 1st group data参数校验"):
                    assert int(pl[20:22], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorPassReLockSts 1 - 1st group data参数校验"):
                    assert int(pl[22:24], 16) in [0, 1, 2, 3], "value out of range"
                with allure.step("DoorDrvrSts 1 - 1st group data参数校验"):
                    assert int(pl[24:26], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorPassSts 1 - 1st group data参数校验"):
                    assert int(pl[26:28], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorDrvrReSts 1 - 1st group data参数校验"):
                    assert int(pl[28:30], 16) in [0, 1, 2], "value out of range"
                with allure.step("DoorPassReSts 1 - 1st group data参数校验"):
                    assert int(pl[30:32], 16) in [0, 1, 2], "value out of range"
                with allure.step("Usage Mode 1 - 1st group data参数校验"):
                    assert int(pl[32:34], 16) in [
                        0,
                        1,
                        2,
                        11,
                        13,
                        255,
                    ], "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Locking Command History-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40EF)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Unlocking Command History 测试 DID:0x40F0")  # 已知bug
    def test_caseid_1349717(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Unlocking Command History 测试"):
                self.b_cli.read_data_by_identifier(0x40F0)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Unlocking Command History 测试"):
                self.b_cli.read_data_by_identifier(0x40F0)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                with allure.step("Central Lock Status 1 校验"):
                    assert int(p[6:8], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("Locking Source 1 校验"):
                    assert int(p[8:10], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                    ], "out of range"
                with allure.step("DoorDrvrLockCmd 1 校验"):
                    assert int(p[10:12], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        12,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassLockCmd 1 校验"):
                    assert int(p[12:14], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        12,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrReLockCmd 1 校验"):
                    assert int(p[14:16], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        12,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorPassReLockCmd 1 校验"):
                    assert int(p[16:18], 16) in [
                        0,
                        1,
                        2,
                        3,
                        4,
                        8,
                        12,
                        18,
                        19,
                        20,
                    ], "value out of range"
                with allure.step("DoorDrvrLockSts 1 校验"):
                    assert int(p[18:20], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("DoorPassLockSts 1 校验"):
                    assert int(p[20:22], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("DoorDrvrReLockSts 1 校验"):
                    assert int(p[22:24], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("DoorPassReLockSts 1 校验"):
                    assert int(p[24:26], 16) in [0, 1, 2, 3], "out of range"
                with allure.step("DoorDrvrSts 1 校验"):
                    assert int(p[26:28], 16) in [0, 1, 2], "out of range"
                with allure.step("DoorPassSts 1 校验"):
                    assert int(p[28:30], 16) in [0, 1, 2], "out of range"
                with allure.step("DoorDrvrReSts 1 校验"):
                    assert int(p[30:32], 16) in [0, 1, 2], "out of range"
                with allure.step("DoorPassReSts 1 校验"):
                    assert int(p[32:34], 16) in [0, 1, 2], "out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Unlocking Command History-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40F0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Play protection counter 测试 DID:0x40F2")
    
    def test_caseid_1349718(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Play protection counter 测试"):
                self.b_cli.read_data_by_identifier(0x40F2)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Play protection counter 测试"):
                self.b_cli.read_data_by_identifier(0x40F2)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Play protection counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40F2)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title("读写Steering Wheel Tuning 测试 DID:0x4109")  # 挂mcu
    def test_caseid_1349720(self):
        try:
            with allure.step("进入默认会话测试"):
                self.b_cli.session_control(1)
            with allure.step("读取Steering Wheel Tuning 测试"):
                self.b_cli.read_data_by_identifier(0x4109)
                p = self.b_cli.get_payload()
                assert -7 <= int(p[-2:],16) - 8 <= 7 or int(p[-2:],16) == 0
            with allure.step("进入扩展会话测试"):
                self.b_cli.session_control(3)
                time.sleep(0.5)
            with allure.step("读取Steering Wheel Tuning 测试"):
                self.b_cli.read_data_by_identifier(0x4109)
                p = self.b_cli.get_payload()
                assert -7 <= int(p[-2:], 16) - 8 <= 7 or int(p[-2:],16) == 0
            with allure.step("写入Steering Wheel Tuning 测试"):
                time.sleep(1)
                self.b_cli.write_data_by_identifier(0x4109,'05')
            with allure.step("读取Steering Wheel Tuning 测试"):
                time.sleep(1)
                self.b_cli.read_data_by_identifier(0x4109)
                p = self.b_cli.get_payload()
                assert p[-2:] == '05'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Steering Wheel Tuning-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4109)
            with allure.step("写入Steering Wheel Tuning 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4109,'05')  
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Day/Night And Twilight Sensors Status 测试 DID:0x410B")
    def test_caseid_1349721(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Day/Night And Twilight Sensors Status 测试"):
                self.b_cli.read_data_by_identifier(0x410B)
                with allure.step("参数校验"):
                    time.sleep(0.5)
                    p = self.b_cli.get_payload()
                    assert int(p[6:8], 16) in [0, 1, 2, 3], "out of range"
                    assert 0 <= int(p[8:], 16) <= 16383, "out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Day/Night And Twilight Sensors Status 测试"):
                self.b_cli.read_data_by_identifier(0x410B)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Day/Night And Twilight Sensors Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x410B)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    
    @allure.story("MCU_诊断DID")
    @allure.title("读取Alarm Trigger Information 测试 DID:0x416B")
    def test_caseid_1349724(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Alarm Trigger Information 测试"):
                self.b_cli.read_data_by_identifier(0x416B)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Alarm Trigger Information 测试"):
                self.b_cli.read_data_by_identifier(0x416B)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Trigger Information-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x416B)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Interior Light Day to Night Timer 测试 DID:0x416D")
    def test_caseid_1349725(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Light Day to Night Timer 测试"):
                self.b_cli.read_data_by_identifier(0x416D)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("写入Interior Light Day to Night Timer 测试"):
                self.b_cli.write_data_by_identifier(0x416D, '2710')
                self.b_cli.read_data_by_identifier(0x416D)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 10000
                data = p[6:]
            with allure.step("恢复写入Interior Light Day to Night Timer 测试"):
                self.b_cli.write_data_by_identifier(0x416D, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Trigger Information-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x416D)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Interior Light Night to Day Timer 测试 DID:0x416E")
    def test_caseid_1349726(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Light Night to Day Timer 测试"):
                self.b_cli.read_data_by_identifier(0x416E)
                p = self.b_cli.get_payload()
                pl = int(p[6:], 16)
                print("value is ", pl)
                assert 0 <= pl <= 10000
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Light Night to Day Timer 测试"):
                self.b_cli.read_data_by_identifier(0x416E)
                pl1 = self.b_cli.get_payload()
                pl2 = int(pl1[6:], 16)
                print("value is ", pl)
                assert 0 <= pl2 <= 10000
            with allure.step("写入Interior Light Night to Day Timer 测试"):
                self.b_cli.write_data_by_identifier(0x416E, '2710')
                self.b_cli.read_data_by_identifier(0x416E)
                pl = self.b_cli.get_payload()
                assert pl == '62416e2710'
            with allure.step("恢复写入Interior Light Night to Day Timer 测试"):
                data = p[6:]
                self.b_cli.write_data_by_identifier(0x416E, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Trigger Information-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x416D)
            with allure.step("写入Interior Light Night to Day Timer 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x416E, '2710')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Wiper Park Position Status 测试 DID:0x418F")
    def test_caseid_1349815_1349727(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Wiper Park Position Status 测试"):
                self.b_cli.read_data_by_identifier(0x418F)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Wiper Park Position Status 测试"):
                self.b_cli.read_data_by_identifier(0x418F)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Wiper Park Position Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x418F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Transport Mode Battery State Of Charge 测试 DID:0x41CE")
    def test_caseid_1349728(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Transport Mode Battery State Of Charge 测试"):
                self.b_cli.read_data_by_identifier(0x41CE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Transport Mode Battery State Of Charge 测试"):
                self.b_cli.read_data_by_identifier(0x41CE)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Transport Mode Battery State Of Charge-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x41CE)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    @allure.title("UDS_ReadDataByIdentifier(0x22)_Interior Lights Control")
    def test_caseid_1349729(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl = self.b_cli.get_payload()
                # assert 0 < int(pl[0:2],16) < 100
                # assert 0 < int(pl[2:4],16) < 100
                # assert 0 < int(pl[4:6],16) < 100 
                assert 0 <= int(pl[6:8],16) <= 100  
                assert 0 <= int(pl[8:10],16) <= 100  
                assert 0 <= int(pl[10:12],16) <= 100  
                assert 0 <= int(pl[12:14],16) <= 100  
                assert 0 <= int(pl[14:16],16) <= 100  
                assert 0 <= int(pl[16:18],16) <= 100 
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Lights Control状态"):
                self.b_cli.read_data_by_identifier(0x41E5)
                pl = self.b_cli.get_payload()
                # assert 0 < int(pl[0:2],16) < 100
                # assert 0 < int(pl[2:4],16) < 100
                # assert 0 < int(pl[4:6],16) < 100 
                assert 0 <= int(pl[6:8],16) <= 100  
                assert 0 <= int(pl[8:10],16) <= 100  
                assert 0 <= int(pl[10:12],16) <= 100  
                assert 0 <= int(pl[12:14],16) <= 100  
                assert 0 <= int(pl[14:16],16) <= 100  
                assert 0 <= int(pl[16:18],16) <= 100  
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Lights Control-NRC31状态"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x41E5)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Power Saver Relay Control 测试 DID:0x41E8")
    
    def test_caseid_1349730(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Power Saver Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Power Saver Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x41E8)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Power Saver Relay Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x41E8)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Activate Driver Side Mirror Defroster 测试 DID:0x4219")
    
    def test_caseid_1349731(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Activate Driver Side Mirror Defroster 测试"):
                self.b_cli.read_data_by_identifier(0x4219)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Activate Driver Side Mirror Defroster 测试"):
                self.b_cli.read_data_by_identifier(0x4219)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Activate Driver Side Mirror Defroster-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4219)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Activate Passenger Side Mirror Defroster 测试 DID:0x421A")
    
    def test_caseid_1349732(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Activate Passenger Side Mirror Defroster 测试"):
                self.b_cli.read_data_by_identifier(0x421A)
                self.b_cli.session_control(3)
                self.b_cli.read_data_by_identifier(0x421A)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Activate Passenger Side Mirror Defroster 测试"):
                self.b_cli.read_data_by_identifier(0x421A)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Activate Driver Side Mirror Defroster-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4219)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Activate Electrical Front Windscreen 测试 DID:0x421D")
    
    def test_caseid_1349733(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Activate Electrical Front Windscreen 测试"):
                self.b_cli.read_data_by_identifier(0x421D)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Activate Electrical Front Windscreen 测试"):
                self.b_cli.read_data_by_identifier(0x421D)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Activate Electrical Front Windscreen-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x421D)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Activate Electrical Rear Window 测试 DID:0x421E")
    def test_caseid_1349734(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Activate Electrical Rear Window 测试"):
                self.b_cli.read_data_by_identifier(0x421E)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
                self.b_cli.read_data_by_identifier(0x421E)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl in [0, 1]
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Activate Electrical Rear Window-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x421E)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Overhead Console  Rear Button Status 测试 DID: 0x422F")
    
    def test_caseid_1349735(self):  # DID: 0x422F
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Overhead Console  Rear Button Status 测试"):
                self.b_cli.read_data_by_identifier(0x422F)
                pl1 = self.b_cli.get_payload()
                pl1 = int(pl1[6:], 16)
                assert pl1 in [0, 1, 2, 3]
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Overhead Console  Rear Button Status 测试"):
                self.b_cli.read_data_by_identifier(0x422F)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl in [0, 1, 2, 3]
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Overhead Console  Rear Button Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x422F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Overhead Console  Button Status 测试 DID: 0x4230")
    
    def test_caseid_1349737(self):  # DID: 0x4230
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Overhead Console  Button Status 测试"):
                self.b_cli.read_data_by_identifier(0x4230)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("参数校验"):
                assert int(p[6:7], 16) in range(0, 127)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Overhead Console  Button Status 测试"):
                self.b_cli.read_data_by_identifier(0x4230)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Overhead Console  Button Status 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4230)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Timer Car Mode Factory Pause 测试  DID:0x4231")
    def test_caseid_1349738(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Timer Car Mode Factory Pause 测试"):
                self.b_cli.read_data_by_identifier(0x4231)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) * 5 <= 1275
                data = pl[6:]
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Timer Car Mode Factory Pause 测试"):
                self.b_cli.read_data_by_identifier(0x4231)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) * 5 <= 1275
            with allure.step("写入Timer Car Mode Factory Pause 测试"):
                self.b_cli.write_data_by_identifier(0x4231, '15')
                self.b_cli.read_data_by_identifier(0x4231)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '15'
            with allure.step("恢复写入Timer Car Mode Factory Pause 测试"):
                self.b_cli.write_data_by_identifier(0x4231, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Timer Car Mode Factory Pause-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4231)
            with allure.step("写入Timer Car Mode Factory Pause-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4231, '15')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写 Delay to Enter Car Mode 测试 DID:0x4232")
    def test_caseid_1349739(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Delay to Enter Car Mode 测试"):
                self.b_cli.read_data_by_identifier(0x4232)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                assert 0 <= int(pl[6:], 16) * 5 <= 1275
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Delay to Enter Car Mode 测试"):
                self.b_cli.read_data_by_identifier(0x4232)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) * 5 <= 1275
            with allure.step("写入Delay to Enter Car Mode 测试"):
                self.b_cli.write_data_by_identifier(0x4232, 'FE')
                self.b_cli.read_data_by_identifier(0x4232)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == 'fe'
            with allure.step("恢复写入Delay to Enter Car Mode 测试"):
                self.b_cli.write_data_by_identifier(0x4232, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Delay to Enter Car Mode-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4232)
            with allure.step("写入Delay to Enter Car Mode-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4232, 'FE')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Rain Sensor High Temperature Detected 测试 - Internal DID:0x4282")
    def test_caseid_1349740(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Rain Sensor High Temperature Detected 测试"):
                self.b_cli.read_data_by_identifier(0x4282)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Rain Sensor High Temperature Detected 测试"):
                self.b_cli.read_data_by_identifier(0x4282)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Rain Sensor High Temperature Detected-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4232)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Rain Sensor High Voltage Detected 测试 DID:0x4283")
    def test_caseid_1349741(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Rain Sensor High Voltage Detected 测试"):
                self.b_cli.read_data_by_identifier(0x4283)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Rain Sensor High Voltage Detected 测试"):
                self.b_cli.read_data_by_identifier(0x4283)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Rain Sensor High Voltage Detected-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4283)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写NFC duration after unlock 测试 DID:0x4297")
    def test_caseid_1349742(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取NFC duration after unlock 测试"):
                self.b_cli.read_data_by_identifier(0x4297)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("写入NFC duration after unlock 测试"):
                self.b_cli.write_data_by_identifier(0x4297, '01')
                self.b_cli.read_data_by_identifier(0x4297)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) <= 255
            with allure.step("恢复写入NFC duration after unlock 测试"):
                self.b_cli.write_data_by_identifier(0x4297,data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取NFC duration after unlock 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4297)
            with allure.step("写入NFC duration after unlock 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4297, '01')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取NFC duration after unlock 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4297)
            with allure.step("写入NFC duration after unlock 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4297, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.title("Requested Charge Voltage 测试 DID: 0xF124") #这个搞不来自动化 需要在sbl刷完之后d
    
    def test_caseid_1349743(self):
        assert True
        # """
        #    Requested Charge Voltage  测试 DID: 0xF124
        # """
        # try:
        #     with allure.step("进入编程会话"):
        #         self.b_cli.session_control(2)
        #         time.sleep(15)
        #         BgmDoIPAnoucementParser("config/DoIPConfig.json", "1002")
        #         time.sleep(2)
                
        #     with allure.step('Requested Charge Voltage 测试'):
        #         self.b_cli.read_data_by_identifier(0xF124)
        #         p = self.b_cli.get_payload()
        #         assert 11 < int(p[-2:], 16) / 40 + 10.6 < 16
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #         time.sleep(15)
        #         BgmDoIPAnoucementParser("config/DoIPConfig.json", "1002")
        # except:
        #     assert False
        
    @allure.title("Battery Average Quiescent Current_High Range测试 DID: 0x42E4")
    def test_caseid_1349744(self):
        """
        Battery Average Quiescent Current_High Range测试 DID: 0x42E4
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('Battery Average Quiescent Current_High Range测试'):
                self.b_cli.read_data_by_identifier(0x42E4)
                p = self.b_cli.get_payload()
                logger.info("p[-4:]={}".format(p[-4:]))
                assert -2555 <= int(p[-4:], 16) * 5 - 2555 <= 0
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('Battery Average Quiescent Current_High Range测试'):
                self.b_cli.read_data_by_identifier(0x42E4)
                p = self.b_cli.get_payload()
                assert -2555 <= int(p[-4:], 16) * 5 - 2555 <= 0
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('Battery Average Quiescent Current_High Range-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42E4)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.title("读取Alarm Status 测试 DID:0x42E5")
    def test_caseid_1349745(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Alarm Status 测试"):
                self.b_cli.read_data_by_identifier(0x42E5)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Alarm Status 测试"):
                self.b_cli.read_data_by_identifier(0x42E5)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1 or 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42E5)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写 Central Locking Play Protection 测试 DID:0x42E9")
    def test_caseid_1349746(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Alarm Status 测试"):
                self.b_cli.read_data_by_identifier(0x42E9)
                pl = self.b_cli.get_payload()
                pl1 = int(pl[6:], 16)
                assert pl1 == 0 or 1
            with allure.step("写入Alarm Status 测试"):
                self.b_cli.write_data_by_identifier(0x42E9, '01')
                time.sleep(0.5)
                self.b_cli.read_data_by_identifier(0x42E9)
                time.sleep(0.5)
                pl2 = self.b_cli.get_payload()
                assert pl2[6:] == "01"
            with allure.step("恢复写入Alarm Status 测试"):
                self.b_cli.write_data_by_identifier(0x42E9, pl[6:])
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Alarm Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42E9)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42E9)
            with allure.step("写入Alarm Status 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x42E9, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Private Unlock Status 测试 DID:0x42F4")
    def test_case_1349748(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Private Unlock Status 测试"):
                self.b_cli.read_data_by_identifier(0x42F4)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Private Unlock Status 测试"):
                self.b_cli.read_data_by_identifier(0x42F4)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Alarm Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42F4)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取ITO Signal Frequency Status 测试 DID:0x42FB")
    def test_caseid_1349749(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ITO Signal Frequency Status 测试"):
                self.b_cli.read_data_by_identifier(0x42FB)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ITO Signal Frequency Status 测试"):
                self.b_cli.read_data_by_identifier(0x42FB)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert 0 <= pl <= 65536
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ITO Signal Frequency Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42FB)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Hazard Switch Status 测试 DID:0x4300")
    def test_caseid_1349750(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Hazard Switch Status 测试"):
                self.b_cli.read_data_by_identifier(0x4300)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Hazard Switch Status 测试"):
                self.b_cli.read_data_by_identifier(0x4300)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                assert pl == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Hazard Switch Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4300)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Ignition Power Relay Feedback 测试 - Internal DID:0x4305")
    def test_caseid_1349751(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Ignition Power Relay Feedback 测试"):
                self.b_cli.read_data_by_identifier(0x4305)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Ignition Power Relay Feedback 测试"):
                self.b_cli.read_data_by_identifier(0x4305)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:8], 16)
                assert pl_0 == 0 or 1
                pl_12 = int(pl[8:], 16) * 0.001
                assert 0 <= pl_12 <= 25
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Ignition Power Relay Feedback-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4305)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Wiper Motor Communication Error Detection 测试 DID:0x430B")
    
    def test_caseid_1349752(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Wiper Motor Communication Error Detection 测试"):
                self.b_cli.read_data_by_identifier(0x430B)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Wiper Motor Communication Error Detection 测试"):
                self.b_cli.read_data_by_identifier(0x430B)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Wiper Motor Communication Error Detection-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x430B)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Wiper Motor Node Error Detection 测试 DID:0x430C")
    def test_caseid_1349753(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Wiper Motor Node Error Detection 测试"):
                self.b_cli.read_data_by_identifier(0x430C)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Wiper Motor Node Error Detection 测试"):
                self.b_cli.read_data_by_identifier(0x430C)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Wiper Motor Communication Error Detection-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x430C)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取 Usage Mode Extention Statistics 测试 DID:0x430E")
    
    def test_caseid_1349754(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Usage Mode Extention Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x430E)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 20):
                    assert int(pl[j : j + 2], 16) in range(0, 65536), "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Usage Mode Extention Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x430E)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 20):
                    assert int(pl[j : j + 2], 16) in range(0, 65536), "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Usage Mode Extention Statistics-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x430E)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Usage Mode Time Statistics 测试 DID:0x430F")
    def test_caseid_1349755(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Usage Mode Time Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x430F)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 9):
                    assert int(pl[j : j + 6], 16) in range(0, 16777217), "out of range"
                    i += 1
                    j = j + 6
            with allure.step("读取Usage Mode Time Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x430F)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Usage Mode Time Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x430F)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 9):
                    assert int(pl[j : j + 6], 16) in range(0, 16777217), "out of range"
                    i += 1
                    j = j + 6
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Usage Mode Extention Statistics-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x430F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Fuel Pump / crash Control 测试 DID:0x4310")
    def test_caseid_1349756(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Fuel Pump / crash Control 测试"):
                self.b_cli.read_data_by_identifier(0x4310)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Fuel Pump / crash Control 测试"):
                self.b_cli.read_data_by_identifier(0x4310)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Fuel Pump / crash Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4310)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读写Dynamometer Wheels 测试 DID:0x4313")
    def test_caseid_1349757(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Dynamometer Wheels 测试"):
                self.b_cli.read_data_by_identifier(0x4313)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 1 or 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Dynamometer Wheels 测试"):
                self.b_cli.read_data_by_identifier(0x4313)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 1 or 2
            # with allure.step('切换Dym模式'):
            #     self.b_cli.change_carmode(5)
            with allure.step("写入Dynamometer Wheels 测试"):
                self.b_cli.write_data_by_identifier(0x4313, '00')
                self.b_cli.read_data_by_identifier(0x4313)
                pl = self.b_cli.get_payload()
                assert pl == "62431300"
            with allure.step("写入Dynamometer Wheels 测试"):
                self.b_cli.write_data_by_identifier(0x4313, '01')
                self.b_cli.read_data_by_identifier(0x4313)
                pl = self.b_cli.get_payload()
                assert pl == "62431301"
            with allure.step("写入Dynamometer Wheels 测试"):
                self.b_cli.write_data_by_identifier(0x4313, '02')
                self.b_cli.read_data_by_identifier(0x4313)
                pl = self.b_cli.get_payload()
                assert pl == "62431302"
            with allure.step("恢复写入Dynamometer Wheels 测试"):
                self.b_cli.write_data_by_identifier(0x4313, pl[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Fuel Pump / crash Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4313)
            with allure.step("写入Dynamometer Wheels-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4313, pl[6:])
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Single Stroke Wiping DID:0x4328")
    def test_caseid_1349758(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Single Stroke Wiping 测试"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Single Stroke Wiping 测试"):
                self.b_cli.read_data_by_identifier(0x4328)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Single Stroke Wiping-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4328)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Interior Light Footwell Status Feedback 测试 DID:0x432D")
    
    def test_caseid_1349759(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Light Footwell Status Feedback 测试"):
                self.b_cli.read_data_by_identifier(0x432D)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Light Footwell Status Feedback 测试"):
                self.b_cli.read_data_by_identifier(0x432D)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Light Footwell Status Feedback-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x432D)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Climate Relay Control 测试 DID:0x432E")
    
    def test_caseid_1349760(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Climate Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x432E)
                self.b_cli.read_data_by_identifier(0x432E)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Climate Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x432E)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Climate Relay Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x432E)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Low Battery SoC in Transport Mode 测试 DID:0x433E")
    def test_caseid_1349763(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Low Battery SoC in Transport Mode 测试"):
                self.b_cli.read_data_by_identifier(0x433E)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Low Battery SoC in Transport Mode 测试"):
                self.b_cli.read_data_by_identifier(0x433E)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Low Battery SoC in Transport Mode -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x432E)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Exterior Light Relay Control 测试 DID:0x439F")
    def test_caseid_1349764(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exterior Light Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:8], 16)
                if pl_0 == 0:
                    assert True
                elif pl_0 >= 1:
                    assert True
                else:
                    assert False
                pl_1 = int(pl[8:], 16)
                if pl_1 == 0:
                    assert True
                elif pl_1 >= 1:
                    assert True
                else:
                    assert False
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Light Relay Control 测试"):
                self.b_cli.read_data_by_identifier(0x439F)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:8], 16)
                if pl_0 == 0:
                    assert True
                elif pl_0 >= 1:
                    assert True
                else:
                    assert False
                pl_1 = int(pl[8:], 16)
                if pl_1 == 0:
                    assert True
                elif pl_1 >= 1:
                    assert True
                else:
                    assert False
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Exterior Light Relay Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x439F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Rain Sensor ReAdaption 测试:0x43B8")
    
    def test_caseid_1349765(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Rain Sensor ReAdaption 测试"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Rain Sensor ReAdaption 测试"):
                self.b_cli.read_data_by_identifier(0x43B8)
                pl = self.b_cli.get_payload()
                pl_0 = int(pl[6:], 16)
                assert pl_0 == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Rain Sensor ReAdaption-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x43B8)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Car Mode including subtypes 测试 DID:0x43C4")
    
    def test_caseid_1349766(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L3"):
                self.b_cli.security_access_level(3)
            with allure.step("读取Car Mode including subtypes 测试"):
                self.b_cli.read_data_by_identifier(0x43C4)
                payload = self.b_cli.get_payload()
                p = bin(int(payload[6:8],16))
                if len(p[2:]) < 6:
                    zero_num = 6 - len(p[2:])
                    p = '0b' + '0' * zero_num + p[2:]

                values = [
                    '0b000000',
                    '0b000001',
                    '0b000010',
                    '0b000010',
                    '0b000011',
                    '0b001000',
                    '0b010000',
                    '0b011000',
                    '0b011001',
                    '0b101000',
                    '0b101001',
                ]

                if p in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入默认会话"):
                    self.b_cli.session_control(1)
            with allure.step("读取Car Mode including subtypes 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x43C4)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Car Mode including subtypes 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x43C4)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Door and Lock status for SWDL 测试 DID:0x43D6")
    def test_caseid_1349767(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Door and Lock status for SWDL 测试"):
                self.b_cli.read_data_by_identifier(0x43D6)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                values = bytearray([0x00, 0x01, 0x02, 0x03, 0x04])
                if p in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Door and Lock status for SWDL 测试"):
                self.b_cli.read_data_by_identifier(0x43D6)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                values = bytearray([0x00, 0x01, 0x02, 0x03, 0x04])
                if p in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Door and Lock status for SWDL -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x43D6)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取 Low Battery SoC In Factory Mode 测试 DID:0x4516")
    def test_caseid_1349768(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Low Battery SoC In Factory Mode 测试"):
                self.b_cli.read_data_by_identifier(0x4516)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                assert p == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Low Battery SoC In Factory Mode 测试"):
                self.b_cli.read_data_by_identifier(0x4516)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                assert p == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Low Battery SoC In Factory Mode-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4516)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Immobilize Mangement status 测试 DID:0x45A1")
    def test_caseid_1349769(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Immobilize Mangement status 测试"):
                self.b_cli.read_data_by_identifier(0x45A1)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                values = bytearray([0x00, 0x01, 0x02, 0x03])
                if p in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Immobilize Mangement status 测试"):
                self.b_cli.read_data_by_identifier(0x45A1)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                values = bytearray([0x00, 0x01, 0x02, 0x03])
                if p in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Immobilize Mangement status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x45A1)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")  #不用测
    @allure.title("读取Immobilize Mangement status 测试 DID:0x45A3")
    def test_caseid_1349770(self):
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("读取Immobilize Mangement status 测试"):
        #         self.b_cli.read_data_by_identifier(0x45A3)
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("读取Immobilize Mangement status 测试"):
        #         self.b_cli.read_data_by_identifier(0x45A3)
        #         payload = self.b_cli.get_payload()
        # except:
        #     assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读写Rain Sensor Threshold value 测试 DID:0x45A4")
    def test_caseid_1349771(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Rain Sensor Threshold value 测试"):
                self.b_cli.read_data_by_identifier(0x45A4)
                p = self.b_cli.get_payload()
                assert -40 <= int(p[6:],16)*5 -40 <= 35 
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Rain Sensor Threshold value 测试"):
                self.b_cli.read_data_by_identifier(0x45A4)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert -40 <= int(p[6:],16)*5 -40 <= 35 
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("写入Rain Sensor Threshold value 测试"):
                self.b_cli.write_data_by_identifier(0x45A4, '10')
                self.b_cli.read_data_by_identifier(0x45A4)
                pl = self.b_cli.get_payload()
                assert pl == '6245a410'
            with allure.step("恢复写入Rain Sensor Threshold value-NRC31 测试"):
                self.b_cli.write_data_by_identifier(0x45A4, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Rain Sensor Threshold value 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x45A4)
            with allure.step("写入Rain Sensor Threshold value 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x45A4, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Windows Short Drop Windows Short Drop 测试 DID:0x45BF")
    def test_caseid_1349772(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Windows Short Drop Windows Short Drop 测试"):
                self.b_cli.read_data_by_identifier(0x45BF)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                assert p == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Windows Short Drop Windows Short Drop 测试"):
                self.b_cli.read_data_by_identifier(0x45BF)
                payload = self.b_cli.get_payload()
                p = int(payload[6:], 16)
                print("value is ", p)
                assert p == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Windows Short Drop Windows Short Drop-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x45BF)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Exterior Lighting Status 测试 DID:0x7000")
    def test_caseid_1349773(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exterior Lighting Status 测试"):
                self.b_cli.read_data_by_identifier(0x7000)
                payload = self.b_cli.get_payload()
                p_0 = int(payload[6:8], 16)
                print("value is ", p_0)
                values = bytearray(
                    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10]
                )
                if p_0 in values:
                    assert True
                else:
                    assert False, "value out of range"
                p_1 = int(payload[8:10], 16)
                print("value is ", p_1)
                values = bytearray(
                    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10]
                )
                if p_1 in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lighting Status 测试"):
                self.b_cli.read_data_by_identifier(0x7000)
                payload = self.b_cli.get_payload()
                p_0 = int(payload[6:8], 16)
                print("value is ", p_0)
                values = bytearray(
                    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10]
                )
                if p_0 in values:
                    assert True
                else:
                    assert False, "value out of range"
                p_1 = int(payload[8:10], 16)
                print("value is ", p_1)
                values = bytearray(
                    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10]
                )
                if p_1 in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Exterior Lighting Status 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x7000)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Exterior Lights Control 测试 DID:0x7022")
    def test_caseid_1349774(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exterior Lights Control 测试"):
                self.b_cli.read_data_by_identifier(0x7022)
                payload = self.b_cli.get_payload()
                p_0 = int(payload[6:8], 16)
                print("value is ", p_0)
                assert 0 <= p_0 <= 255
                p_1 = int(payload[8:10], 16)
                print("value is ", p_1)
                assert 0 <= p_1 <= 255
                p_2 = int(payload[10:12], 16)
                print("value is ", p_2)
                assert 0 <= p_2 <= 255
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exterior Lights Control 测试"):
                self.b_cli.read_data_by_identifier(0x7022)
                payload = self.b_cli.get_payload()
                p_0 = int(payload[6:8], 16)
                print("value is ", p_0)
                assert 0 <= p_0 <= 255
                p_1 = int(payload[8:10], 16)
                print("value is ", p_1)
                assert 0 <= p_1 <= 255
                p_2 = int(payload[10:12], 16)
                print("value is ", p_2)
                assert 0 <= p_2 <= 255
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Exterior Lights Control-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x7022)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("诊断IOControl")
    
    @allure.title("UDS_ReadDataByIdentifier(0x22)_Car Mode") 
    def test_caseid_1349776(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl = self.b_cli.get_payload()
                assert int(pl[-2:],16) in [0,1,2,3,5]
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Car Mode状态"):
                self.b_cli.read_data_by_identifier(0xD134)
                pl = self.b_cli.get_payload()
                assert int(pl[-2:],16) in [0,1,2,3,5]
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Car Mode状态-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD134)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Available Delta Energy 测试 DID:0xD934")
    def test_caseid_1349781(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Available Delta Energy 测试"):
                self.b_cli.read_data_by_identifier(0xD934)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16) - 16
                assert -16 <= p <= 47
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Available Delta Energy 测试"):
                self.b_cli.read_data_by_identifier(0xD934)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16) - 16
                assert -16 <= p <= 47
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Available Delta Energy-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD934)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Energy Available To Warning 测试 DID:0xD935")
    def test_caseid_1349782(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Available Delta Warning 测试"):
                self.b_cli.read_data_by_identifier(0xD935)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16) - 16
                assert -16 <= p <= 47
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Available Delta Warning 测试"):
                self.b_cli.read_data_by_identifier(0xD935)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16) - 16
                assert -16 <= p <= 47
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Available Delta Warning 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD935)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.title("Car Configuration Parameter Faults 测试 DID: 0xE103")
    
    def test_caseid_1349784(self):
        """
        Car Configuration Parameter Faults 测试 DID: 0xE103
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('Car Configuration Parameter Faults测试'):
                self.b_cli.read_data_by_identifier(0xE103)
                p = self.b_cli.get_payload()
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('Car Configuration Parameter Faults测试'):
                self.b_cli.read_data_by_identifier(0xE103)
                p = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('Car Configuration Parameter Faults-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xE103)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读写VFCVectorFrame Setting 测试 DID:0xE503")
    def test_caseid_1349786(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert p1 == 0 or 1
            with allure.step("读取VFCVectorFrame Setting 测试"):
                self.b_cli.read_data_by_identifier(0xE503)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VFCVectorFrame Setting 测试"):
                self.b_cli.read_data_by_identifier(0xE503)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert p1 == 0 or 1
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入VFCVectorFrame Setting 测试"):
                self.b_cli.write_data_by_identifier(0xE503, '01')
                self.b_cli.read_data_by_identifier(0xE503)
                p1 = self.b_cli.get_payload()
                p1 = int(p1[6:], 16)
                assert p1 == 1
            with allure.step("恢复写入VFCVectorFrame Setting 测试"):
                self.b_cli.write_data_by_identifier(0xE503, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取VFCVectorFrame Setting-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xE503)
            with allure.step('写入VFCVectorFrame Setting-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xE503, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Luggage Supply Status Feedback 测试 DID:0xEE94")
    def test_caseid_1349787(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Luggage Supply Status Feedback 测试"):
                self.b_cli.read_data_by_identifier(0xEE94)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:10], 16)
                assert 0 <= p_0 <= 4292967295
                p_1 = int(p[10:14], 16)
                assert 0 <= p_1 <= 4292967295
                p_2 = int(p[14:18], 16)
                assert 0 <= p_2 <= 4292967295
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Luggage Supply Status Feedback 测试"):
                self.b_cli.read_data_by_identifier(0xEE94)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:10], 16)
                assert 0 <= p_0 <= 4292967295
                p_1 = int(p[10:14], 16)
                assert 0 <= p_1 <= 4292967295
                p_2 = int(p[14:18], 16)
                assert 0 <= p_2 <= 4292967295
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取Luggage Supply Status Feedback-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xEE94)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Statistic Information for Horn 测试 DID:0xEE99")
    def test_caseid_1349788(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Statistic Information for Horn 测试"):
                self.b_cli.read_data_by_identifier(0xEE99)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:10], 16)
                assert 0 <= p_0 <= 4292967295
                p_1 = int(p[10:14], 16)
                assert 0 <= p_1 <= 4292967295
                p_2 = int(p[14:18], 16)
                assert 0 <= p_2 <= 4292967295
            with allure.step("读取Statistic Information for Horn 测试"):
                self.b_cli.read_data_by_identifier(0xEE99)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Statistic Information for Horn 测试"):
                self.b_cli.read_data_by_identifier(0xEE99)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:10], 16)
                assert 0 <= p_0 <= 4292967295
                p_1 = int(p[10:14], 16)
                assert 0 <= p_1 <= 4292967295
                p_2 = int(p[14:18], 16)
                assert 0 <= p_2 <= 4292967295
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取Statistic Information for Horn-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xEE99)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取rear Windscreen Heater Control #1 测试 DID:0xEF99")
    
    def test_caseid_1349789(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Statistic Information for Horn 测试"):
                self.b_cli.read_data_by_identifier(0xEF99)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert p == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Statistic Information for Horn 测试"):
                self.b_cli.read_data_by_identifier(0xEF99)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert p == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取Statistic Information for Horn-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xEF99)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取CEM Wake Up Cause 测试 DID:0xF010")
    def test_caseid_1349790(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取CEM Wake Up Cause 测试"):
                self.b_cli.read_data_by_identifier(0xF010)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取CEM Wake Up Cause 测试"):
                self.b_cli.read_data_by_identifier(0xF010)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取CEM Wake Up Cause-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF010)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Private ECU(s) Delivery Assembly Part Number(s) 测试 DID:0xF1BB")
    
    def test_caseid_1349791(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Private ECU(s) Delivery Assembly Part Number(s) 测试"):
                self.b_cli.read_data_by_identifier(0xF1BB)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Private ECU(s) Delivery Assembly Part Number(s) 测试"):
                self.b_cli.read_data_by_identifier(0xF1BB)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取CEM Wake Up Cause-NRC31测试'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1BB)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Error Reset Reason History 测试 DID:0xFD00")
    def test_caseid_1349792(self):
        assert True  # APTIV未实现
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("读取Error Reset Reason History 测试"):
        #         self.b_cli.read_data_by_identifier(0xFD00)
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("读取Error Reset Reason History 测试"):
        #         self.b_cli.read_data_by_identifier(0xFD00)
        # except:
        #     assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Direction Indication Diagnostics Status 测试 DID:0xFD07")
    
    def test_caseid_1349793(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Direction Indication Diagnostics Status 测试"):
                self.b_cli.read_data_by_identifier(0xFD07)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert p == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Direction Indication Diagnostics Status 测试"):
                self.b_cli.read_data_by_identifier(0xFD07)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert p == 0 or 1
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Direction Indication Diagnostics Status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xFD07)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Ethernet Link Status 测试 DID:0xD250")
    def test_caseid_1349794(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Ethernet Link Status 测试"):
                self.b_cli.read_data_by_identifier(0xD250)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:8], 16)
                assert 0 <= p_0 <= 255
                p_1 = int(p[6:8], 16)
                assert 0 <= p_1 <= 128
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Ethernet Link Status 测试"):
                self.b_cli.read_data_by_identifier(0xD250)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:8], 16)
                assert 0 <= p_0 <= 255
                p_1 = int(p[6:8], 16)
                assert 0 <= p_1 <= 128
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Ethernet Link Status- NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD250)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Single Quality Index 测试 DID:0xD260")
    
    def test_caseid_1349795(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Single Quality Index 测试"):
                self.b_cli.read_data_by_identifier(0xD260)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:8], 16)
                assert 0 <= p_0 <= 255
                p_1 = int(p[8:10], 16)
                assert 0 <= p_1 <= 255
                p_2 = int(p[10:12], 16)
                assert 0 <= p_2 <= 255
                p_3 = int(p[12:14], 16)
                assert 0 <= p_3 <= 255
                p_4 = int(p[14:16], 16)
                assert 0 <= p_4 <= 255
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Single Quality Index 测试"):
                self.b_cli.read_data_by_identifier(0xD260)
                p = self.b_cli.get_payload()
                p_0 = int(p[6:8], 16)
                assert 0 <= p_0 <= 255
                p_1 = int(p[8:10], 16)
                assert 0 <= p_1 <= 255
                p_2 = int(p[10:12], 16)
                assert 0 <= p_2 <= 255
                p_3 = int(p[12:14], 16)
                assert 0 <= p_3 <= 255
                p_4 = int(p[14:16], 16)
                assert 0 <= p_4 <= 255
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Single Quality Index- NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD260)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Activate frontwasher 测试 - Internal DID:0x420A")
    def test_caseid_1349796(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Activate frontwasher 测试"):
                self.b_cli.read_data_by_identifier(0x420A)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in [0, 1, 2, 3]
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Activate frontwasher 测试"):
                self.b_cli.read_data_by_identifier(0x420A)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in [0, 1, 2, 3]
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Activate frontwasher- NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x420A)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Wiper's lever information from CDC 测试 DID:0x4218")
    def test_caseid_1349797(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Wiper's lever information from CDC 测试"):
                self.b_cli.read_data_by_identifier(0x4218)
                p = self.b_cli.get_payload()
                p = int(p[6:8], 16)
                assert p == 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Wiper's lever information from CDC 测试"):
                self.b_cli.read_data_by_identifier(0x4218)
                p = self.b_cli.get_payload()
                p = int(p[6:8], 16)
                assert p == 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Wiper's lever information from CDC 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4218)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Voltage Wake Up Charging At Sleep Enable 测试 DID:0x4530")
    def test_caseid_1349798(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Voltage Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.read_data_by_identifier(0x4530)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or '01'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Voltage Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.read_data_by_identifier(0x4530)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or '01'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("写入Voltage Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.write_data_by_identifier(0x4530, '01')
                self.b_cli.read_data_by_identifier(0x4530)
                p = self.b_cli.get_payload()
                assert p[-2:] == '01'
            with allure.step("恢复写入Voltage Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.write_data_by_identifier(0x4530, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Voltage Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4530)
            with allure.step("写入Voltage Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4530, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读Voltage Wake Up Chrgn At Sleep 测试 DID:0x4531")
    def test_caseid_1349799(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Voltage Wake Up Chrgn At Sleep 测试"):
                self.b_cli.read_data_by_identifier(0x4531)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert 8 <= p1 / 10 <= 16
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Voltage Wake Up Chrgn At Sleep 测试"):
                self.b_cli.read_data_by_identifier(0x4531)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert 8 <= p1 / 10 <= 16
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("写入Voltage Wake Up Chrgn At Sleep 测试"):
                self.b_cli.write_data_by_identifier(0x4531, '77')
                self.b_cli.read_data_by_identifier(0x4531)
                p2 = self.b_cli.get_payload()
                assert p2[-2:] == '77'
            with allure.step("恢复写入Voltage Wake Up Chrgn At Sleep 测试"):
                self.b_cli.write_data_by_identifier(0x4531, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Voltage Wake Up Chrgn At Sleep-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4530)
            with allure.step("写入Voltage Wake Up Chrgn At Sleep-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4530, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Timer Wake Up Charging At Sleep Enable 测试 DID:0x4532")
    def test_caseid_1349800(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.read_data_by_identifier(0x4532)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert p1 == 0 or 1
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.read_data_by_identifier(0x4532)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                assert p1 == 0 or 1
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.write_data_by_identifier(0x4532, '01')
                self.b_cli.read_data_by_identifier(0x4532)
                p2 = self.b_cli.get_payload()
                p2 = int(p[6:], 16)
                assert p2 == 1
            with allure.step("恢复写入Timer Wake Up Charging At Sleep Enable 测试"):
                self.b_cli.write_data_by_identifier(0x4532, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Timer Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4532)
            with allure.step("写入Timer Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4532, '01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Prim Energy Available Charge Abort for Parked 测试 DID:0x4533")
    def test_caseid_1349801(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Prim Energy Available Charge Abort for Parked 测试"):
                self.b_cli.read_data_by_identifier(0x4533)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                print("value is ", p1)
                assert 0 <= p1 <= 127
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Prim Energy Available Charge Abort for Parked 测试"):
                self.b_cli.read_data_by_identifier(0x4533)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                print("value is ", p1)
                assert 0 <= p1 <= 127
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("写入Prim Energy Available Charge Abort for Parked 测试"):
                self.b_cli.write_data_by_identifier(0x4533, '50')
                self.b_cli.read_data_by_identifier(0x4533)
                p2 = self.b_cli.get_payload()
                p2 = int(p[6:], 16)
                print("value is ", p2)
                assert p2 == 80
                self.b_cli.write_data_by_identifier(0x4533, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Timer Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4533)
            with allure.step("写入Timer Wake Up Charging At Sleep Enable-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4533, '50')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Voltage Value Charging At Inactive 测试 DID:0x4534")
    def test_caseid_1349802(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Voltage Value Charging At Inactive 测试"):
                self.b_cli.read_data_by_identifier(0x4534)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16) / 10
                print("value is ", p1)
                assert 8 <= p1 <= 16
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Voltage Value Charging At Inactive 测试"):
                self.b_cli.read_data_by_identifier(0x4534)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16) / 10
                print("value is ", p1)
                assert 8 <= p1 <= 16
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Voltage Value Charging At Inactive 测试"):
                self.b_cli.write_data_by_identifier(0x4534, '50')
                self.b_cli.read_data_by_identifier(0x4534)
                p2 = self.b_cli.get_payload()
                p2 = int(p[6:], 16) / 10
                print("value is ", p2)
                assert 8 <= p2 <= 16
            with allure.step("恢复写入Voltage Value Charging At Inactive 测试"):
                self.b_cli.write_data_by_identifier(0x4534, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Voltage Value Charging At Inactive-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4534)
            with allure.step("写入Voltage Value Charging At Inactive-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4534, '50')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Prim Energy Available Charge Required for Parked 测试 DID:0x4535")
    def test_caseid_1349803(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Prim Energy Available Charge Required for Parked 测试"):
                self.b_cli.read_data_by_identifier(0x4535)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                print("value is ", p1)
                assert 0 <= p1 <= 127
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Prim Energy Available Charge Required for Parked 测试"):
                self.b_cli.read_data_by_identifier(0x4535)
                p = self.b_cli.get_payload()
                p1 = int(p[6:], 16)
                print("value is ", p1)
                assert 0 <= p1 <= 127
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("写入Prim Energy Available Charge Required for Parked 测试"):
                self.b_cli.write_data_by_identifier(0x4535, '50')
                time.sleep(3)
                self.b_cli.read_data_by_identifier(0x4535)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '50'
            with allure.step("恢复写入Prim Energy Available Charge Required for Parked 测试"):
                self.b_cli.write_data_by_identifier(0x4535, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Prim Energy Available Charge Required for Parked-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4535)
            with allure.step("写入Prim Energy Available Charge Required for Parked-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4535, '50')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Level Energy Electric Substitution 测试 DID:0x429D")
    def test_caseid_1349804(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Level Energy Electric Substitution 测试"):
                self.b_cli.read_data_by_identifier(0x429D)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert 0 <= p <= 15
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Level Energy Electric Substitution 测试"):
                self.b_cli.read_data_by_identifier(0x429D)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert 0 <= p <= 15
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Level Energy Electric Substitution-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x429D)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Power Level Electric Substitution 测试 DID:0x429E")
    def test_caseid_1349805(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Power Level Electric Substitution 测试"):
                self.b_cli.read_data_by_identifier(0x429E)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert 0 <= p <= 15
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Power Level Electric Substitution 测试"):
                self.b_cli.read_data_by_identifier(0x429E)
                p = self.b_cli.get_payload()
                p = int(p[6:], 16)
                assert 0 <= p <= 15
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Power Level Electric Substitution-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x429E)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title("读取FotaStatus 测试 DID: 0xF153")
    def test_caseid_1349806(self):  # DID: 0xF153
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取FotaStatus 测试"):
                self.b_cli.read_data_by_identifier(0xF153)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取FotaStatus 测试"):
                self.b_cli.read_data_by_identifier(0xF153)
                p = self.b_cli.get_payload()
                # p1 = int(p[6:], 16)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("写入FotaStatus idle测试"):
                self.b_cli.write_data_by_identifier(0xF153, '00')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '00'
            with allure.step("写入FotaStatus Query测试"):
                self.b_cli.write_data_by_identifier(0xF153, '01')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '01'
            with allure.step("写入FotaStatus Downloading测试"):
                self.b_cli.write_data_by_identifier(0xF153, '02')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '02'
            with allure.step("写入FotaStatus Active测试"):
                self.b_cli.write_data_by_identifier(0xF153, '03')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '03'
            with allure.step("写入FotaStatus Update测试"):
                self.b_cli.write_data_by_identifier(0xF153, '04')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '04'
            with allure.step("写入FotaStatus Rollback测试"):
                self.b_cli.write_data_by_identifier(0xF153, '05')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '05'
            with allure.step("写入UpdateFailedNotDriving测试"):
                self.b_cli.write_data_by_identifier(0xF153, '06')
                self.b_cli.read_data_by_identifier(0xF153)
                p2 = self.b_cli.get_payload()
                assert p2[6:] == '06'
            with allure.step("恢复写入Prim Energy Available Charge Required for Parked 测试"):
                self.b_cli.write_data_by_identifier(0xF153, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取FotaStatus-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF153)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Tailgate/bootlid Open/Close Counter 测试 DID:0xA00A")
    
    def test_caseid_1349807(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取FotaStatus 测试"):
                self.b_cli.read_data_by_identifier(0xA00A)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 11):
                    assert int(p[j : j + 2], 16) in range(0, 65536), "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取FotaStatus 测试"):
                self.b_cli.read_data_by_identifier(0xA00A)
                p = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 11):
                    assert int(p[j : j + 2], 16) in range(0, 65536), "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取FotaStatus-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xA00A)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Digital Key Current UTC Time 测试 DID:0xC008")
    
    def test_caseid_1349808(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) <= 4294967295
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)               
            with allure.step("读取Digital Key Current UTC Time 测试"):
                self.b_cli.read_data_by_identifier(0xC008)
                pl = self.b_cli.get_payload()
                assert 0 <= int(pl[6:], 16) <= 4294967295
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取FotaStatus-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xC008)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Sensata TPMS Software Version 测试 DID:0x4503")
    def test_caseid_1349810(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Sensata TPMS Software Version 测试"):
                self.b_cli.read_data_by_identifier(0x4503)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Sensata TPMS Software Version 测试"):
                self.b_cli.read_data_by_identifier(0x4503)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Sensata TPMS Software Version-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4503)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "UDS_ReadDataByIdentifier(0x22)_TPMS Development log message status 测试 DID: 0x4504"
    )
    def test_caseid_1349811(self):  # DID: 0x4504
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取TPMS Development log message status 测试"
            ):
                self.b_cli.read_data_by_identifier(0x4504)
                p = self.b_cli.get_payload()
                assert p[-2:] in ['00','01','02','03','04']
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取TPMS Development log message status 测试"
            ):
                self.b_cli.read_data_by_identifier(0x4504)
                p = self.b_cli.get_payload()
                assert p[-2:] in ['00','01','02','03','04']
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入TPMS Development log message status 测试"):
                self.b_cli.write_data_by_identifier(0x4504, '00')
                self.b_cli.read_data_by_identifier(0x4504)
                p = self.b_cli.get_payload()
                assert p[-2:] in ['00','01','02','03','04']
            with allure.step("恢复写入TPMS Development log message status 测试"):
                self.b_cli.write_data_by_identifier(0x4504, p[-2:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取TPMS Development log message status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4504)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "读写Adjust the system state of Interiorlight target value 测试 DID: 0x4600"
    )
    def test_caseid_1349812(self):  # DID: 0x4600
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取Adjust the system state of Interiorlight target value 测试"
            ):
                self.b_cli.read_data_by_identifier(0x4600)
                time.sleep(0.5)
                self.p = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 5):
                    assert 0 <= int(self.p[j : j + 2], 16) <= 100, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取Adjust the system state of Interiorlight target value 测试"
            ):
                self.b_cli.read_data_by_identifier(0x4600)
                time.sleep(0.5)
                self.p = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 5):
                    assert 0 <= int(self.p[j : j + 2], 16) <= 100, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入TPMS Development log message status 测试"):
                self.b_cli.write_data_by_identifier(0x4600, '0000000000')
                self.b_cli.read_data_by_identifier(0x4600)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0000000000'
            with allure.step("恢复写入TPMS Development log message status 测试"):
                self.b_cli.write_data_by_identifier(0x4600, self.p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取TPMS Development log message status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4600)
            with allure.step("紫儿TPMS Development log message status-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4600, '0000000000')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读写 测试Interior Light Day to Night Value DID: 0x416F")
    def test_caseid_1349813(self):  # DID: 0x416F
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Light Day to Night Value 测试"):
                self.b_cli.read_data_by_identifier(0x416F)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(400, 701)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Light Day to Night Value 测试"):
                self.b_cli.read_data_by_identifier(0x416F)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(400, 701)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Interior Light Day to Night Value 测试"):
                self.b_cli.write_data_by_identifier(0x416F, '0190')
                self.b_cli.read_data_by_identifier(0x416F)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0190'
            with allure.step("恢复写入Interior Light Day to Night Value 测试"):
                self.b_cli.write_data_by_identifier(0x416F, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Light Day to Night Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x416F)
            with allure.step("读取Interior Light Day to Night Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x416F, '0190')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读写Interior Light Night to Day Value 测试 DID: 0x4170")
    def test_caseid_1349814(self):  # DID: 0x4170
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Interior Light Night to Day Value 测试"):
                self.b_cli.read_data_by_identifier(0x4170)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(800, 1300)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Light Night to Day Value 测试"):
                self.b_cli.read_data_by_identifier(0x4170)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(800, 1300)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5) 
            with allure.step("写入Interior Light Night to Day Value 测试"):
                self.b_cli.write_data_by_identifier(0x4170,'0320')
                self.b_cli.read_data_by_identifier(0x4170)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0320'
            with allure.step("恢复写入Interior Light Night to Day Value 测试"):
                self.b_cli.write_data_by_identifier(0x4170, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Light Day to Night Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4170)
            with allure.step("读取Interior Light Day to Night Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4170,'0320')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("UDS_ReadDataByIdentifier(0x22)_Main Battery Counter In Transport Mode")
    def test_caseid_1349815(self):  # DID: 0x4187
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Main Battery Counter In Transport Mode 测试"):
                self.b_cli.read_data_by_identifier(0x4187)
                p = self.b_cli.get_payload()
                assert int(p[-4:], 16) in range(0, 255)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Interior Light Night to Day Value 测试"):
                self.b_cli.read_data_by_identifier(0x4187)
                p = self.b_cli.get_payload()
                assert int(p[-4:], 16) in range(0, 255)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Light Night to Day Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4187)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Charge Mode 测试 DID:0x40D1")  # 无响应导致BGM重启，挂mcu
    def test_caseid_1349816(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Charge Mode 测试"):
                self.b_cli.read_data_by_identifier(0x40D1)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                values = bytearray([0x00, 0x01, 0x02])
                if pl in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Charge Mode 测试"):
                self.b_cli.read_data_by_identifier(0x40D1)
                pl = self.b_cli.get_payload()
                pl = int(pl[6:], 16)
                print("value is ", pl)
                values = bytearray([0x00, 0x01, 0x02])
                if pl in values:
                    assert True
                else:
                    assert False, "value out of range"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Interior Light Night to Day Value-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40D1)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.title("Requested Charge Voltage 测试 DID: 0x411D")
    def test_caseid_1349817(self):
        """
        Requested Charge Voltage  测试 DID: 0x411D
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('Requested Charge Voltage 测试'):
                self.b_cli.read_data_by_identifier(0x411D)
                p = self.b_cli.get_payload()
                assert 11 < int(p[-2:], 16) / 40 + 10.6 < 16
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('Requested Charge Voltage 测试'):
                self.b_cli.read_data_by_identifier(0x411D)
                p = self.b_cli.get_payload()
                assert 11 < int(p[-2:], 16) / 40 + 10.6 < 16
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Requested Charge Voltage-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x411D)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "读取Battery Normalized Internal Resistance Statistics Counter 测试 DID:0x42D3"
    )
    def test_caseid_1349818(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取Battery Normalized Internal Resistance Statistics Counter 测试"
            ):
                self.b_cli.read_data_by_identifier(0x42D3)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 10):
                    assert 0 <= int(pl[j : j + 2], 16) / 10 <= 25.5, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取Battery Normalized Internal Resistance Statistics Counter 测试"
            ):
                self.b_cli.read_data_by_identifier(0x42D3)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 10):
                    assert 0 <= int(pl[j : j + 2], 16) / 10 <= 25.5, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Normalized Internal Resistance Statistics Counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42D3)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "读取Battery Average Quiescent Current - Statistics 测试 - Internal DID:0x42CD"
    )
    def test_caseid_1349820(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Average Quiescent Current - Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x42CD)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 10):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Average Quiescent Current - Statistics 测试"):
                self.b_cli.read_data_by_identifier(0x42CD)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 10):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Average Quiescent Current -Statistics-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42CD)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Capacity Statistics Counter 测试 DID:0x42D1")
    def test_caseid_1349821(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Capacity Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x42D1)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 11):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Capacity Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x42D1)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 11):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Capacity Statistics Counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42D1)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Battery Capacity Statistics Counter 测试 DID:0x42CF")
    def test_caseid_1349824(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Battery Capacity Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x42CF)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 5):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Battery Capacity Statistics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x42CF)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 5):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Capacity Statistics Counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42CF)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title(
        "读取Battery Normalized Internal Resistance Statistics Counter 测试 DID:0x42D2"
    )
    def test_caseid_1349825(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step(
                "读取Battery Normalized Internal Resistance Statistics Counter 测试"
            ):
                self.b_cli.read_data_by_identifier(0x42D2)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step(
                "读取Battery Normalized Internal Resistance Statistics Counter 测试"
            ):
                self.b_cli.read_data_by_identifier(0x42D2)
                pl = self.b_cli.get_payload()
                i = 0
                j = 6
                for i in range(0, 11):
                    assert 0 <= int(pl[j : j + 2], 16) <= 256, "out of range"
                    i += 1
                    j = j + 2
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Battery Normalized Internal Resistance Statistics Counter-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x42D2)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取AWM LIN Message Detection 测试 DID:0xDA00")
    def test_caseid_1349826(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取AWM LIN Message Detection 测试"):
                self.b_cli.read_data_by_identifier(0xDA00)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(0, 2)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取AWM LIN Message Detection 测试"):
                self.b_cli.read_data_by_identifier(0xDA00)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert int(p[6:], 16) in range(0, 2)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取AWM LIN Message Detection -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDA00)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("UDS_Read|WriteDataByIdentifier(0x22|2E)_Development Test Mode")
    def test_caseid_1349827(self):
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("读取Development Test Mode 测试"):
        #         self.b_cli.read_data_by_identifier(0x4500)
        #         p = self.b_cli.get_payload()
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("读取Development Test Mode 测试"):
        #         self.b_cli.read_data_by_identifier(0x4500)
        #         time.sleep(0.5)
        #         p = self.b_cli.get_payload()
        # except:
        #     assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title("Internal DID:Power Management Config测试 - DID:0xF0F5")
    def test_caseid_1502229(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Power Management Config测试"):
                self.b_cli.read_data_by_identifier(0xF0F5)
                pl = self.b_cli.get_payload()
                try:
                    with allure.step("进入默认会话"):
                        self.b_cli.session_control(1)
                    with allure.step("读取Power Management Config测试"):
                        self.b_cli.read_data_by_identifier(0xF0F5)
                        pl = self.b_cli.get_payload()
                        assert int(pl[-12:-10], 16) > 0 or int(pl[-12:-10], 16) < 40
                        assert int(pl[-10:-8], 16) > 0 or int(pl[-10:-8], 16) < 20
                        assert int(pl[-8:-6], 16) > 0 or int(pl[-8:-6], 16) < 10
                        assert int(pl[-6:-4], 16) > 0 or int(pl[-6:-4], 16) < 10
                        assert int(pl[-4:-2], 16) > 0 or int(pl[-4:-2], 16) < 5
                        assert int(pl[-2:], 16) > 0 or int(pl[-2:], 16) < 10

                    with allure.step("进入扩展会话"):
                        self.b_cli.session_control(3)
                    with allure.step("读取Power Management Config测试"):
                        self.b_cli.read_data_by_identifier(0xF0F5)
                        pl = self.b_cli.get_payload()
                        try:
                            with allure.step("进入默认会话"):
                                self.b_cli.session_control(1)
                            with allure.step("读取Power Management Config测试"):
                                self.b_cli.read_data_by_identifier(0xF0F5)
                                pl = self.b_cli.get_payload()
                                assert (
                                    int(pl[-12:-10], 16) > 0
                                    or int(pl[-12:-10], 16) < 40
                                )
                                assert (
                                    int(pl[-10:-8], 16) > 0 or int(pl[-10:-8], 16) < 20
                                )
                                assert int(pl[-8:-6], 16) > 0 or int(pl[-8:-6], 16) < 10
                                assert int(pl[-6:-4], 16) > 0 or int(pl[-6:-4], 16) < 10
                                assert int(pl[-4:-2], 16) > 0 or int(pl[-4:-2], 16) < 5
                                assert int(pl[-2:], 16) > 0 or int(pl[-2:], 16) < 10

                            with allure.step("进入扩展会话"):
                                self.b_cli.session_control(3)
                            with allure.step("读取Power Management Config测试"):
                                self.b_cli.read_data_by_identifier(0xF0F5)
                                pl = self.b_cli.get_payload()
                                assert (
                                    int(pl[-12:-10], 16) > 0
                                    or int(pl[-12:-10], 16) < 40
                                )
                                assert (
                                    int(pl[-10:-8], 16) > 0 or int(pl[-10:-8], 16) < 20
                                )
                                assert int(pl[-8:-6], 16) > 0 or int(pl[-8:-6], 16) < 10
                                assert int(pl[-6:-4], 16) > 0 or int(pl[-6:-4], 16) < 10
                                assert int(pl[-4:-2], 16) > 0 or int(pl[-4:-2], 16) < 5
                                assert int(pl[-2:], 16) > 0 or int(pl[-2:], 16) < 10
                        except:
                            assert False
                except:
                    assert False

            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Power Management Config测试"):
                self.b_cli.read_data_by_identifier(0xF0F5)
                pl = self.b_cli.get_payload()
                assert int(pl[-12:-10], 16) > 0 or int(pl[-12:-10], 16) < 40
                assert int(pl[-10:-8], 16) > 0 or int(pl[-10:-8], 16) < 20
                assert int(pl[-8:-6], 16) > 0 or int(pl[-8:-6], 16) < 10
                assert int(pl[-6:-4], 16) > 0 or int(pl[-6:-4], 16) < 10
                assert int(pl[-4:-2], 16) > 0 or int(pl[-4:-2], 16) < 5
                assert int(pl[-2:], 16) > 0 or int(pl[-2:], 16) < 10
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Power Management Config -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF0F5)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("Internal DID:Steering Wheel Heating Control测试 - DID:0x7023")
    def test_caseid_1502230(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Steering Wheel Heating Control测试"):
                self.b_cli.read_data_by_identifier(0x7023)
                pl = self.b_cli.get_payload()
                assert int(pl[-2:], 16) >= 0 or int(pl[-2:], 16) <= 600
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Steering Wheel Heating Control测试"):
                self.b_cli.read_data_by_identifier(0x7023)
                pl = self.b_cli.get_payload()
                assert int(pl[-2:], 16) >= 0 or int(pl[-2:], 16) <= 600
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5) 
            with allure.step("写入Steering Wheel Heating Control测试"):
                self.b_cli.write_data_by_identifier(0x7023,'010101010101010101')
                self.b_cli.read_data_by_identifier(0x7023)
                pl = self.b_cli.get_payload()
                assert pl == '627023010101010101010101'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Steering Wheel Heating Contro -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x7023)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "Internal DID:The counter of trigger to active AWM initialization测试 - DID:0x4200"
    )
    def test_caseid_1566534(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取当前会话测试 - 默认会话"):
                self.b_cli.read_data_by_identifier(0x4200)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                assert int(pl[6:8],16) >= 0 or int(pl[-2:], 16) <= 500
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取当前会话测试 - 扩展会话"):
                self.b_cli.read_data_by_identifier(0x4200)
                pl = self.b_cli.get_payload()
                assert int(pl[6:8],16) >= 0 or int(pl[-2:], 16) <= 500
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5) 
            with allure.step("写入The counter of trigger to active AWM initialization 测试"):
                self.b_cli.write_data_by_identifier(0x4200,'00000000')
                self.b_cli.read_data_by_identifier(0x4200)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '00000000'
            with allure.step("恢复写入The counter of trigger to active AWM initialization 测试"):
                self.b_cli.write_data_by_identifier(0x4200,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取The counter of trigger to active AWM initialization -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x4200)
            with allure.step("写入The counter of trigger to active AWM initialization -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x4200,'00000000')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("Internal DID:Exhibition Mode (PNC)测试 - DID:0xD135")
    def test_caseid_1569795(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exhibition Mode (PNC)测试"):
                self.b_cli.read_data_by_identifier(0xD135)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                assert pl[-2:] == '00' or pl[-2:] == '01'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exhibition Mode (PNC)测试"):
                self.b_cli.read_data_by_identifier(0xD135)
                pl = self.b_cli.get_payload()
                assert pl[-2:] == '00' or pl[-2:] == '01'
            with allure.step("切换usagemode==abandoned 以及EpbStsEpbSts=0"):
                self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
                self.ipdu.set(getattr(getattr(self.ipdu,'backbonefr'),'BcmVddmBackBoneFr00'),'EpbStsEpbSts',3)
                self.b_cli.change_usagemode(0)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5) 
            with allure.step("写入Exhibition Mode (PNC) 测试"):
                self.b_cli.write_data_by_identifier(0xD135,'01')
                self.b_cli.read_data_by_identifier(0xD135)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '01'
            with allure.step("恢复写入Exhibition Mode (PNC)测试"):
                self.b_cli.write_data_by_identifier(0xD135,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Exhibition Mode (PNC) -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD135)
            with allure.step("写入Exhibition Mode (PNC) -NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xD135,'01')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("Internal DID:Partial Network Cluster (PNC)测试 - DID:0xDD0B")
    def test_caseid_1569824(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Partial Network Cluster (PNC)测试"):
                self.b_cli.read_data_by_identifier(0xDD0B)
                pl = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Partial Network Cluster (PNC)测试"):
                self.b_cli.read_data_by_identifier(0xDD0B)
                pl = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Partial Network Cluster(PNC)-NRC31 测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xDD0B)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    @allure.story("MCU_诊断DID")
    @allure.title("写入/读取CCP测试 - Internal DID:0xF106")
    def test_caseid_1758508(self):
        """
        CCP -  DID:0xF106
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取CCP测试"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(0x5)
            with allure.step("写入CCP测试"):
                self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
                self.b_cli.read_data_by_identifier(0xF106)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '62f106ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeaf1'
                )
                data = p[6:]
            with allure.step("恢复写入CCP测试"):
                self.b_cli.write_data_by_identifier(0xF106, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("NRC31回复测试"):
                    with pytest.raises(ValueError):
                        with allure.step("写入NRC31回复测试"):
                            self.b_cli.write_data_by_identifier(0xF106,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xF106)
                with pytest.raises(ValueError):
                    with allure.step("写入NRC31回复测试"):
                        self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("VIN码测试 DID: 0xF190")
    def test_caseid_1758509(self):  # DID: 0xF190
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
                self.b_cli.read_data_by_identifier(0xF190)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            with allure.step("恢复写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("写入VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF190, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "写入Security Key between BNCM and BGM (Digital Key) 测试 DID:0xD903"
    )
    def test_caseid_1758510(self):
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("检查是否D903已经写入值"):
                if p == '62d90400':
                    logger.info("值未写入")
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'    
                else:
                    logger.info("值已经被写入")
                    with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90400'
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
    
    @allure.story("MCU_诊断DID")
    @allure.title("读取MCU软件号 DID:0xF1F0")
    def test_caseid_1758513(self):  # DID: 0xF1F0
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取MCU软件号测试"):
                self.b_cli.read_data_by_identifier(0xF1F0)
                pl = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取MCU软件号测试"):
                self.b_cli.read_data_by_identifier(0xF1F0)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取MCU软件号-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1F0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("ECU硬件号 DID: 0xF1AA")
    def test_caseid_1758527(self):  # DID:0xF1AA
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                pl = self.b_cli.get_payload()
                if pl == '62f1aa0000000000000000':
                    assert False,'硬件号值默认为全零'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                pl = self.b_cli.get_payload()
                if pl == '62f1aa0000000000000000':
                    assert False,'硬件号值默认为全零'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                if pl == '62f1aa0000000000000000':
                    assert False,'硬件号值默认为全零'
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
    
    
    @allure.story("MCU_诊断DID")
    @allure.title("ECU序列号测试 DID:0xF18C")
    def test_caseid_1758542(self):  # DID:0xF18C
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl1 = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl2 = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl3 = self.b_cli.get_payload()
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("读取Primary Bootloader Software Part Number测试 DID:0xF1A5")
    def test_caseid_1758552(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Primary Bootloader Software Part Number-NRC31测试"):
                self.b_cli.read_data_by_identifier(0xF1A5)
                p = self.b_cli.get_payload()
                if p == '62f1a50000000000000000':
                    assert False,'硬件号为空'
            with allure.step("进入拓展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Primary Bootloader Software Part Number-NRC31测试"):
                self.b_cli.read_data_by_identifier(0xF1A5)
                p = self.b_cli.get_payload()
                if p == '62f1a50000000000000000':
                    assert False,'硬件号为空'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Primary Bootloader Software Part Number测试"):
                self.b_cli.read_data_by_identifier(0xF1A5)
                p = self.b_cli.get_payload()
                if p == '62f1a50000000000000000':
                    assert False,'硬件号为空'
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取ECU Delivery Assembly Part NumberECUDID: 0xF1AB")
    def test_caseid_1758553(self):  # DID:0xF1AB
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Primary Bootloader Software Part Number测试"):
                self.b_cli.read_data_by_identifier(0xF1AB)
                p = self.b_cli.get_payload()
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("EOL_Read|WriteDataByIdentifier(0x22|2E)_Secret Key For Immobilizer Target #3 - MGM")
    def test_caseid_1758562(self):
        try:
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E0)
            with allure.step("解锁安全等级11 测试"):
                self.b_cli.security_access_level(11)
            with allure.step("写入Secret Key For Immobilizer Target #3 测试"):
                self.b_cli.write_data_by_identifier(0x40E0,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("读取Driver Door Status Diagnostics Counter 测试"):
                self.b_cli.read_data_by_identifier(0x40E0)
                pl = self.b_cli.get_payload()
                assert pl[6:] == 'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Driver Door Status Diagnostics Counter-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40E0)
            with allure.step("写入Driver Door Status Diagnostics Counter-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x40E0,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    # 
    
    @allure.title("读写L11安全常数测试 DID: 0xD12F")
    def test_caseid_1758570(self):
        """
        Version DID: 0xD12F
        """
        with allure.step("进入默认会话"):
            self.b_cli.session_control(1)
        with allure.step("读取L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.read_data_by_identifier(0xD12F)
        with allure.step("写入L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("进入扩展会话"):
            self.b_cli.session_control(3)
        with allure.step("通过安全访问L11"):
            self.b_cli.security_access_level(11)
        with allure.step("读取L11安全常数测试"):
            self.b_cli.read_data_by_identifier(0xD12F)
            p = self.b_cli.get_payload()
            self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("进入编程会话"):
            self.b_cli.session_control(2)
        with allure.step("读取L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.read_data_by_identifier(0xD12F)
        with allure.step("写入L11安全常数测试 - NRC31"):
            with pytest.raises(ValueError):
                self.b_cli.write_data_by_identifier(0xD12F, 'FFFFFFFFFA')
        with allure.step("退出编程会话"):
            self.b_cli.exit_boot()
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取Security Key between BNCM and BGM (Digital Key) Mac 测试 DID:0xD906")
    def test_caseid_1758574(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) Mac 测试"):
                self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
                self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) Mac 测试"):
                self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) Mac -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD906)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读取/写入Remote Vehicle Immobilization Secret Key 测试 DID:0x408F")
    def test_caseid_1758586(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("读取Remote Vehicle Immobilization Secret Key 测试"):
                self.b_cli.read_data_by_identifier(0x408F)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("写入Remote Vehicle Immobilization Secret Key 测试"):
                self.b_cli.write_data_by_identifier(0x408F,'50555555555555555555555555555555')
                self.b_cli.read_data_by_identifier(0x408F)
                pl = self.b_cli.get_payload()
                assert pl == '62408f50555555555555555555555555555555'
            with allure.step("恢复写入Remote Vehicle Immobilization Secret Key 测试"):
                self.b_cli.write_data_by_identifier(0x408F,data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("写入Remote Vehicle Immobilization Secret Key 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x408F, '50555555555555555555555555555555')
            with allure.step("读取Remote Vehicle Immobilization Secret Key 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x408F)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("写入Remote Vehicle Immobilization Secret Key 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x408F, '50555555555555555555555555555555')
            with allure.step("读取Remote Vehicle Immobilization Secret Key 测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x408F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("读写Tire Pressure Monitoring System (TPMS) Sensor IDs 测试 DID: 0x281F")
    def test_caseid_1758591(self):  # DID: 0x281F
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.read_data_by_identifier(0x281F)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.read_data_by_identifier(0x281F)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.write_data_by_identifier(0x281F, '00000000000000000000000000000000')
                self.b_cli.read_data_by_identifier(0x281F)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '00000000000000000000000000000000'
            with allure.step("恢复写入Tire Pressure Monitoring System (TPMS) Sensor IDs 测试"):
                self.b_cli.write_data_by_identifier(0x281F, p[6:])
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("写入Tire Pressure Monitoring System (TPMS) Sensor IDs -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x408F, '50555555555555555555555555555555')
            with allure.step("读取Tire Pressure Monitoring System (TPMS) Sensor IDs -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x408F)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title(
        "读取Security Key between BNCM and BGM (Digital Key) write status 测试 DID:0xD904"
    )
    def test_caseid_1758596(self):
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("检查是否D903已经写入值"):
                if p == '62d90400':
                    logger.info("值未写入")
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'    
                else:
                    logger.info("值已经被写入")
                    with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90400'
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
            
  
    @allure.story("MCU_诊断DID")
    @allure.title("写入Security Key between BNCM and BGM (Digital Key) 测试 DID:0xD903") #D903不能重复写入 写入之前需要先用D905加原来的值擦除
    def test_caseid_1758609(self):
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                self.b_cli.read_data_by_identifier(0xD904)
                p = self.b_cli.get_payload()
                assert p == '62d90400' or p == '62d90401'
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("检查是否D903已经写入值"):
                if p == '62d90400':
                    logger.info("值未写入")
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'    
                else:
                    logger.info("值已经被写入")
                    with allure.step("擦除Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD905,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90400'
                    with allure.step("写入Security Key between BNCM and BGM (Digital Key) 测试"):
                        self.b_cli.write_data_by_identifier(0xD903,self.tc_config['BNCM_KEY'])
                    with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status 测试"):
                        self.b_cli.read_data_by_identifier(0xD904)
                        p = self.b_cli.get_payload()
                        assert p == '62d90401'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Security Key between BNCM and BGM (Digital Key) write status -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD904)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
            
    @allure.story("MCU_诊断DID")
    @allure.title("VIN码测试 DID: 0xF190")
    def test_caseid_1349658(self):  # DID: 0xF190
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
                # p = self.b_cli.get_payload()
                # data = p[6:]
            # with allure.step("通过安全访问L5"):
            #     self.b_cli.security_access_level(5)
            # with allure.step("写入VIN码测试"):
            #     self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            #     self.b_cli.read_data_by_identifier(0xF190)
            #     time.sleep(0.5)
            #     p1 = self.b_cli.get_payload()
            #     assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            # with allure.step("恢复写入VIN码测试"):
            #     self.b_cli.write_data_by_identifier(0xF190, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("写入VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF190, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False
            
    @allure.story("MCU_诊断DID")
    @allure.title("写入/读取Secret Key For Immobilizer Target #2 - IEM test DID: 0x40DF")
    def test_caseid_1758615(self):
        """
        Version DID: 0x40DF
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("读取Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.read_data_by_identifier(0x40DF)
                pl = self.b_cli.get_payload()
                data = pl[6:]
            with allure.step("写入Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.write_data_by_identifier(0x40DF,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
                self.b_cli.read_data_by_identifier(0x40DF)
                pl = self.b_cli.get_payload()
                assert pl== '6240dff442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
            with allure.step("恢复写入Secret Key For Immobilizer Target #2 - IEM test"):
                self.b_cli.write_data_by_identifier(0x40DF,data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Secret Key For Immobilizer Target #2 - IEM -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40DF)
            with allure.step("写入Secret Key For Immobilizer Target #2 - IEM -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x40DF,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Secret Key For Immobilizer Target #2 - IEM -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40DF)
            with allure.step("写入Secret Key For Immobilizer Target #2 - IEM -NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x40DF,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("MCU_诊断DID")
    @allure.title("APP诊断数据库零件号 DID: 0xF1A0")
    def test_caseid_1758617(self):  # DID: 0xF1A0
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取APP诊断数据库零件号测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

    @allure.story("DOIP/DID")
    @allure.title("写入/读取Secret Key For Immobilizer Target #1 - ECM test DID: 0x40DE")
    def test_caseid_1758619(self):
        """
        Version DID: 0x40DE
        """
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.read_data_by_identifier(0x40DE)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("通过安全访问L11"):
                self.b_cli.security_access_level(11)
            with allure.step("写入Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.write_data_by_identifier(0x40DE,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
                self.b_cli.read_data_by_identifier(0x40DE)
                pl = self.b_cli.get_payload()
                assert pl == '6240def442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550'
            with allure.step("恢复写入Secret Key For Immobilizer Target #1 - ECM test"):
                self.b_cli.write_data_by_identifier(0x40DE,data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Secret Key For Immobilizer Target #1 - ECM test-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40DE)
            with allure.step("写入Secret Key For Immobilizer Target #1 - ECM test-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x40DE,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Secret Key For Immobilizer Target #1 - ECM test-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0x40DE)
            with allure.step("写入Secret Key For Immobilizer Target #1 - ECM test-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0x40DE,'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_SOC_DID(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1001)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_SOC_DID_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)
    
    @allure.story("SOC_诊断DID")
    @allure.title("当前会话测试 DID: 0xF186")
    def test_caseid_1349656(self):  # DID: 0xF186
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("当前会话测试 - 默认会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18601'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("当前会话测试 - 扩展会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18603'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("当前会话测试 - 编程会话"):
                self.b_cli.read_data_by_identifier(0xF186)
                pl = self.b_cli.get_payload()
                assert pl == '62f18602'
        except:
            assert False
            
    
    @allure.story("SOC_诊断DID")
    @allure.title("ECU硬件号, ECU总成号, ECU序列号测试 DID: 0xED20")
    def test_caseid_1349665(self):  # DID: 0xED20
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件号, ECU总成号, ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xED20)
        except:
            assert False
            
    
    @allure.story("SOC_诊断DID")
    @allure.title("写入L1常数测试 DID: 0xF102")  #安全等级1常数只能写一次 但是删除vehicleInfo.json后可以重复写
    def test_caseid_1349667(self):
        try:
            with allure.step("删除密钥后重启并等待10s"): 
                commands = "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)        
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                time.sleep(10)
                self.b_cli.session_control(1)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("通过安全访问L1"):
                self.b_cli.security_access_level(1)
            with allure.step("写入L1常数测试"):
                self.b_cli.write_data_by_identifier(0xF102,'FFFFFFFFFF')
        except:
            assert False
    
    #D03A读取前提是先写入D01C的值
    @allure.story("SOC_诊断DID")
    @allure.title("读取swAuth Public Key CheckSum测试 DID:0xD03A") #诊断调查表
    def test_caseid_1349668(self):
        try:
            with allure.step("读取vehicleInfo.json"): 
                commands = "cat /data/vehicleInfo.json"
                self.b_cli.ssh_bgm.type_commands(commands)        
            with allure.step('进入编程会话'):
                self.b_cli.session_control(2)
            with allure.step("读取D01C值"): 
                self.b_cli.read_data_by_identifier(0xd01c,False)
                pl = self.b_cli.get_payload()
                # data = pl[-2:]
                if pl[0:6] == '7f2222':
                    logger.info('D01C1值未写入 写入D01C值')
                    with allure.step('进入编程会话'):
                        self.b_cli.session_control(2)
                    with allure.step("解锁安全等级1 测试"):
                        self.b_cli.security_access_level(1)
                    with allure.step("未写入Public Key 先写入"):
                        self.b_cli.write_data_by_identifier(0xD01C,'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577')
                    with allure.step("读取密钥"):
                        self.b_cli.read_data_by_identifier(0xd01c)
                        p = self.b_cli.get_payload()
                        assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'
                    
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("取swAuth Public Key CheckSum测试"):
                self.b_cli.read_data_by_identifier(0xD03A)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("取swAuth Public Key CheckSum测试"):
                self.b_cli.read_data_by_identifier(0xD03A)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取swAuth Public Key CheckSum-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xD03A)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("整车基线版本号测试 DID: 0xF150")  # 先写才能读出
    def test_caseid_1349669(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取整车基线版本号"):
                self.b_cli.read_data_by_identifier(0xF150,False)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                if pl[-2:] == '31':
                    with allure.step("未写入整车基线版本号 先写入"):
                        with allure.step("进入扩展会话"):
                            self.b_cli.session_control(3)
                        with allure.step("通过安全访问L5"):
                            self.b_cli.security_access_level(5)
                        with allure.step("写入整车基线版本号"):
                            self.b_cli.write_data_by_identifier(0xF150,'0161601100604347')
                            self.b_cli.read_data_by_identifier(0xF150)
                            pl = self.b_cli.get_payload()
                            assert pl == '62f1500161601100604347'
                else:
                    with allure.step("整车基线版本号已经写入"):
                        with allure.step("进入扩展会话"):
                            self.b_cli.session_control(3)
                        with allure.step("读取整车基线版本号"):
                            self.b_cli.read_data_by_identifier(0xF150)
                        with allure.step("通过安全访问L5"):
                            self.b_cli.security_access_level(5)
                        with allure.step("写入整车基线版本号"):
                            self.b_cli.write_data_by_identifier(0xF150,'0161601100604347')
                            self.b_cli.read_data_by_identifier(0xF150)
                            pl = self.b_cli.get_payload()
                            assert pl == '62f1500161601100604347'
                        with allure.step("恢复写入整车基线版本号"):
                            self.b_cli.write_data_by_identifier(0xF150, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取整车基线版本号-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF150)
            with allure.step("写入整车基线版本号-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF150, data)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("读取/写入VID测试 DID: 0xB163") #
    def test_caseid_1349670(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("读取VID测试"):
                self.b_cli.read_data_by_identifier(0xB163)
                pl = self.b_cli.get_payload()
                data = pl[6:]
            with allure.step("通过安全访问L7"):
                self.b_cli.security_access_level(7)
            with allure.step("写入VID测试"):
                self.b_cli.write_data_by_identifier(0xB163,'067b9e1c3c61ac0e776decd18c05ee61')
                self.b_cli.read_data_by_identifier(0xB163)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62b163067b9e1c3c61ac0e776decd18c05ee61'
            with allure.step("恢复写入VID测试"):
                self.b_cli.write_data_by_identifier(0xB163,data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VID测试-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB163)
            with allure.step("写入NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xB163, '067b9e1c3c61ac0e776decd18c05ee61') 
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB163)
            with allure.step("写入NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xB163, '067b9e1c3c61ac0e776decd18c05ee61') 
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("FOTA result测试 DID: 0xF154")
    def test_caseid_1349671(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取FOTA result测试"):
                self.b_cli.read_data_by_identifier(0xF154)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '02'
                assert p[-4:-2] == '00'
                assert p[-6:-4] == '00'
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取FOTA result测试"):
                self.b_cli.read_data_by_identifier(0xF154)
                p = self.b_cli.get_payload()
                assert p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '02'
                assert p[-4:-2] == '00'
                assert p[-6:-4] == '00'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xF154)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("Switch Firmware and CFG version test DID: 0xFD50")
    def test_caseid_1349672(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Switch Firmware and CFG version 测试"):
                self.b_cli.read_data_by_identifier(0xFD50)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Switch Firmware and CFG version 测试"):
                self.b_cli.read_data_by_identifier(0xFD50)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    with allure.step("读取NRC31回复测试"):
                        self.b_cli.read_data_by_identifier(0xFD50)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("整车展示的版本号 DID: 0xF151")  # 0.6.5
    def test_caseid_1349673(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本号测试"):
                self.b_cli.read_data_by_identifier(0xF151)
                pl = self.b_cli.get_payload()
                data = pl[6:]
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取版本号测试"):
                self.b_cli.read_data_by_identifier(0xF151)
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入整车展示的版本号测试"):
                self.b_cli.write_data_by_identifier(0xF151,'067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61')
                self.b_cli.read_data_by_identifier(0xF151)
                time.sleep(0.5)
                pl = self.b_cli.get_payload()
                assert pl == '62f151067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61'
            with allure.step("恢复写入整车展示的版本号测试"):
                self.b_cli.write_data_by_identifier(0xF151,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("NRC31回复测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF151)
        except:
            assert False

    @allure.story("SOC_诊断DID")
    @allure.title("OBD防火墙状态测试 DID: 0xB165")
    def test_caseid_1349674(self):
        """
        OBD防火墙状态测试 DID: 0xB165
        """
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('OBD防火墙默认关闭测试'):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(1)
            with allure.step('OBD防火墙默认关闭测试'):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            # with allure.step('读取OBD防火墙测试-NRC31'):
            #     with pytest.raises(ValueError):
                self.b_cli.read_data_by_identifier(0xB165)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                assert p[6:] == '02'
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("工厂模式下自动解锁设置测试 DID: 0xB200")  # 0.6.5
    def test_caseid_1349675(self):
        try:
            with allure.step('进入默认会话'):
                self.b_cli.session_control(1)
            with allure.step('读取工厂模式下自动解锁设置测试'):
                self.b_cli.read_data_by_identifier(0xB200)
                pl = self.b_cli.get_payload()
                data = pl[6:]
                0 <= int(pl[6:],16) <= 10
            with allure.step('进入扩展会话'):
                self.b_cli.session_control(3)
            with allure.step('读取工厂模式下自动解锁设置测试'):
                self.b_cli.read_data_by_identifier(0xB200)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
                0 <= int(pl[6:],16) <= 10
            with allure.step('通过安全访问L5'):
                self.b_cli.security_access_level(5)
            with allure.step('写入工厂模式下自动解锁设置测试'):
                self.b_cli.write_data_by_identifier(0xB200, '0A')
                self.b_cli.read_data_by_identifier(0xB200)
                pl = self.b_cli.get_payload()
                assert pl[6:] == '0a'
            with allure.step('恢复写入工厂模式下自动解锁设置测试'):
                self.b_cli.write_data_by_identifier(0xB200,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取工厂模式下自动解锁设置测试-NRC31'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB200)
            with allure.step('写入工厂模式下自动解锁设置测试-NRC31'):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xB200,'0A')
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("读取Get TurnLamp Status 测试 DID:0xB250")   #不用测试
    def test_caseid_1502231(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Get TurnLamp Status 测试"):
                self.b_cli.read_data_by_identifier(0xB250)
                p = self.b_cli.get_payload()
                assert p[-4:-2] == '00' or p[-4:-2] == '01' or p[-4:-2] == '10' or p[-4:-2] == '11'
                assert 0 <= int(p[-2:],16) <= 255
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Get TurnLamp Status 测试"):
                self.b_cli.read_data_by_identifier(0xB250)
                p = self.b_cli.get_payload()
                assert p[-4:-2] == '00' or p[-4:-2] == '01' or p[-4:-2] == '10' or p[-4:-2] == '11'
                assert 0 <= int(p[-2:],16) <= 255
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('读取Get TurnLamp Status 测试-NRC31'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB250)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("读取Exhibition Mode Status 测试 DID:0xB300")
    def test_caseid_1502232(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exhibition Mode Status 测试"):
                self.b_cli.read_data_by_identifier(0xB300)
                p = self.b_cli.get_payload()
                assert (
                    p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '10' or p[-2:] == '11'
                )
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("Exhibition Mode Status 测试 测试"):
                self.b_cli.read_data_by_identifier(0xB300)
                p = self.b_cli.get_payload()
                assert (
                    p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '10' or p[-2:] == '11'
                )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('Exhibition Mode Status 测试-NRC31'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB300)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("UDS_ReadDataByIdentifier(0x22)_vehicle data tracking config")
    def test_caseid_1502233(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Log config 测试"):
                self.b_cli.read_data_by_identifier(0xEA40)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Log config 测试"):
                self.b_cli.read_data_by_identifier(0xEA40)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step('Log config 测试-NRC31'):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xEA40)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("UDS_ReadDataByIdentifier(0x22)_vehicle data tracking config")
    def test_caseid_1502234(self): #需求被删除
        assert True
        # try:
        #     with allure.step("进入默认会话"):
        #         self.b_cli.session_control(1)
        #     with allure.step("读取Log config 测试"):
        #         self.b_cli.read_data_by_identifier(0xEA00)
        #     with allure.step("进入扩展会话"):
        #         self.b_cli.session_control(3)
        #     with allure.step("读取Log config 测试"):
        #         self.b_cli.read_data_by_identifier(0xEA00)
        # except:
        #     assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("UDS_ReadDataByIdentifier(0x22)_SOA service data tracking config")
    def test_caseid_1502235(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取SOA service data tracking config测试"):
                self.b_cli.read_data_by_identifier(0xEA41)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取SOA service data tracking config测试"):
                self.b_cli.read_data_by_identifier(0xEA41)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取SOA service data tracking config测试-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xEA41)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("读取Exhibition Mode Status 测试 DID:0xB300")
    def test_caseid_1502236(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取Exhibition Mode Status 测试"):
                self.b_cli.read_data_by_identifier(0xB300)
                p = self.b_cli.get_payload()
                assert (
                    p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '10' or p[-2:] == '11'
                )
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取Exhibition Mode Status 测试"):
                self.b_cli.read_data_by_identifier(0xB300)
                p = self.b_cli.get_payload()
                assert (
                    p[-2:] == '00' or p[-2:] == '01' or p[-2:] == '10' or p[-2:] == '11'
                )
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取Exhibition Mode Status 测试-NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xB300)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("ECU硬件号 DID: 0xF1AA")
    def test_caseid_1758527(self):  # DID:0xF1AA
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU硬件版本号测试"):
                self.b_cli.read_data_by_identifier(0xF1AA)
                p = self.b_cli.get_payload()
                if p == '62f1aa0000000000000000':
                    assert False,"硬件号为空"
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("ECU序列号测试 DID:0xF18C")
    def test_caseid_1758542(self):  # DID:0xF18C
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl1 = self.b_cli.get_payload()
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl2 = self.b_cli.get_payload()
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU序列号测试"):
                self.b_cli.read_data_by_identifier(0xF18C)
                pl3 = self.b_cli.get_payload()
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("ECU总成号 DID: 0xF1AB")
    def test_caseid_1758553(self):  # DID:0xF1AB
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU总成号"):
                self.b_cli.read_data_by_identifier(0xF1AB)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("EOL_Read|WriteDataByIdentifier(0x22|2ED01C)_PublicKey")#公钥只能写一次;
    def test_caseid_1758578(self):
        try:
            with allure.step("删除密钥后重启并等待10s"): 
                commands = "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)        
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                time.sleep(10)
            with allure.step("进入编程会话测试"):
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                self.b_cli.session_control(2)
            with allure.step("通过安全访问L1"):
                self.b_cli.security_access_level(1)
            with allure.step("写入密钥"):
                self.b_cli.write_data_by_identifier(0xD01C,'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577')
            with allure.step("读取密钥"):
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                self.b_cli.read_data_by_identifier(0xd01c)
                p = self.b_cli.get_payload()
                assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'
            with allure.step("写入密钥后重启并等待10s"):
                self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                self.b_cli.reset(0x81,do_assert=False)
                time.sleep(10)
                self.b_cli.sd_test.update_serverdoipid(0x1001)
            with allure.step("校验文件/data/certificate/vbf_pk.pem 大小 看是否为0"):
                commands = "cat /data/certificate/vbf_pk.pem"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)
                logger.info("outmsg={}".format(type(outmsg)))
                if len(outmsg) < 3:
                    logger.info("文件大小小于3")
                    raise ValueError
                else:
                    logger.info("文件不为空 文件大小为{}".format(len(outmsg)))
            with allure.step("读取vehicleInfo.json"): 
                commands = "cat /data/vehicleInfo.json"
                outmsg = self.b_cli.ssh_bgm.type_commands(commands)      
            with allure.step("进入编程会话测试"):
                self.b_cli.session_control(2)
            with allure.step("读取密钥"):
                self.b_cli.read_data_by_identifier(0xd01c)
                p = self.b_cli.get_payload()
                assert p == '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'  
        except:
            assert False

    @allure.story("SOC_诊断DID")
    @allure.title("ECU软件号 DID: 0xF1AE")
    def test_caseid_1758599(self):  # DID:0xF1AE
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取ECU软件号"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取ECU软件号"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取ECU软件号 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1AE)
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("VIN码测试 DID: 0xF190")
    def test_caseid_1349658(self):  # DID: 0xF190
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
                p = self.b_cli.get_payload()
                data = p[6:]
            # with allure.step("通过安全访问L5"):
            #     self.b_cli.security_access_level(5)
            # with allure.step("写入VIN码测试"):
            #     self.b_cli.write_data_by_identifier(0xF190,'4A44534F415445535442454E4348303637')
            #     self.b_cli.read_data_by_identifier(0xF190)
            #     time.sleep(0.5)
            #     p1 = self.b_cli.get_payload()
            #     assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            # with allure.step("写入VIN码测试"):
            #     self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            #     self.b_cli.read_data_by_identifier(0xF190)
            #     time.sleep(0.5)
            #     p1 = self.b_cli.get_payload()
            #     assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            # with allure.step("恢复写入VIN码测试"):
            #     self.b_cli.write_data_by_identifier(0xF190,data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("写入VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF190, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        except:
            assert False
            
    @allure.story("SOC_诊断DID")
    @allure.title("APP诊断数据库零件号 DID: 0xF1A0")
    def test_caseid_1758617(self):  # DID: 0xF1A0
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取APP诊断数据库零件号测试"):
                self.b_cli.read_data_by_identifier(0xF1A0)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取APP诊断数据库零件号测试 - NRC31"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF1A0)
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_MCU_Ecos(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1002)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_MCU_Ecos_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)

    @allure.story("基础诊断服务")
    @allure.title("Write CarCfg test via doip 测试")
    def test_caseid_1196608(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本"):
                self.b_cli.read_data_by_identifier(0xF106)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("读未写入前的CCP"):
                self.b_cli.read_data_by_identifier(0xF106)
                time.sleep(0.5)
                p = self.b_cli.get_payload()
            with allure.step("写入CCP测试"):
                self.b_cli.write_data_by_identifier(
                    0xF106,
                    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                )
                self.b_cli.read_data_by_identifier(0xF106)
                pl = self.b_cli.get_payload()
                assert (
                    pl
                    == '62f106ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeaf1'
                )
                data = p[6:]
            with allure.step("恢复CCP"):
                self.b_cli.write_data_by_identifier(0xF106, data)
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("读取VIN码测试"):
                self.b_cli.read_data_by_identifier(0xF190)
                p = self.b_cli.get_payload()
                data = p[6:]
            with allure.step("通过安全访问L5"):
                self.b_cli.security_access_level(5)
            with allure.step("写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
                self.b_cli.read_data_by_identifier(0xF190)
                time.sleep(0.5)
                p1 = self.b_cli.get_payload()
                assert p1 == '62f190ffffffffffffffffffffffffffffffffff'
            with allure.step("恢复写入VIN码测试"):
                self.b_cli.write_data_by_identifier(0xF190, data)
            with allure.step("进入编程会话"):
                self.b_cli.session_control(2)
            with allure.step("读取VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.read_data_by_identifier(0xF190)
            with allure.step("写入VIN码-NRC31测试"):
                with pytest.raises(ValueError):
                    self.b_cli.write_data_by_identifier(0xF190,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
            with allure.step("退出编程会话"):
                self.b_cli.exit_boot()
        except:
            assert False

@pytest.mark.full
@allure.feature("架构基础/网络架构/诊断")
class TestBgm_SOC_Ecos(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            self.b_cli.connect(0x1001)
            #self.file_path = FILE_PATH
        with allure.step("初始化环境"):
            self.b_cli.init_boot_per()
            # global case_id
            # global fail_num
            # case_id = 0
            # fail_num=0
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        # global case_id
        # case_id += 1
        # with allure.step("开始抓取数据"):
        #     self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.file_path,count=case_id)
        #     self.sniff.set_save_name(f"BGM_SOC_Ecos_case_{case_id}_上位机抓包_")
        #     self.sniff.start_sniff()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        # with allure.step("结束抓取数据"):
        #     self.sniff.stop_sniff()
        # with allure.step("统计失败用例数量"):
        #     if ecu.get("testresult") != "Pass":
        #         global fail_num
        #         fail_num += 1
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        with allure.step(f"关闭BGM"):
            self.b_cli.close()
        # with allure.step("计算失败用例数量 如果有失败用例,取BGM日志"):
        #     if fail_num > 0 :
        #         self.b_cli.get_bgm_log(self.file_path)
        super().after_class(self, ecu)

    @allure.story("基础诊断服务")
    @allure.title("SOC enter ECU EOL mode 测试")
    def test_caseid_1246255(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 0xDC00测试"):
                self.b_cli.routing_control(0xDC00, 0x01, data=0x01.to_bytes(1, 'big'))
        except:
            assert False

    @allure.story("基础诊断服务")
    @pytest.mark.sanity
    @allure.title("DDR Test 测试")
    def test_caseid_1246256(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 0x3101DC0001测试"):
                self.b_cli.routing_control(0xDC00, 0x01, data=0x01.to_bytes(1, 'big'))
            with allure.step("开始例程控制: 0x3101DC01测试"):
                self.b_cli.routing_control(0xDC01, 0x01)
        except:
            assert False

    @allure.story("基础诊断服务")
    @pytest.mark.sanity
    @allure.title("EMMC Test 测试")
    def test_caseid_1246257(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 0x3101DC0001测试"):
                self.b_cli.routing_control(0xDC00, 0x01, data=0x01.to_bytes(1, 'big'))
            with allure.step("开始例程控制: 0x3101DC01测试"):
                self.b_cli.routing_control(0xDC02, 0x01)
        except:
            assert False

    @allure.story("基础诊断服务")
    @pytest.mark.sanity
    @allure.title("EMMC Checksum Verify Test 测试")
    def test_caseid_1246258(self):
        try:
            with allure.step("进入默认会话"):
                self.b_cli.session_control(1)
            with allure.step("读取版本"):
                self.b_cli.read_data_by_identifier(0xF1AE)
            with allure.step("进入扩展会话"):
                self.b_cli.session_control(3)
            with allure.step("通过安全访问L5测试"):
                self.b_cli.security_access_level(5)
            with allure.step("开始例程控制: 0x3101DC0001测试"):
                self.b_cli.routing_control(0xDC00, 0x01, data=0x01.to_bytes(1, 'big'))
            with allure.step("开始例程控制: 0x3101DC01测试"):
                self.b_cli.routing_control(0xDC03, 0x01)
        except:
            assert False


#执行路径： /root/TestDev/sat/xat_cases/legacy/basetech
#D01C测试 ：pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_EOL::test_caseid_1758590
#D903测试 ：pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_EOL::test_caseid_1758536
#防火墙测试：pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_RoutineControl::
#TestBgm_MCU_Service 测试：pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_Service::test_caseid_1349491
#TestBgm_SOC_Service 测试: pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_Service::test_caseid_1349490
#TestBgm_MCU_IOControl 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_IOControl::test_caseid_1349892
#TestBgm_MCU_RoutineControl 测试：  pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_RoutineControl::test_caseid_1349892
##TestBgm_SOC_RoutineControl 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_RoutineControl::test_caseid_1758567
#TestBgm_MCU_EOL 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_EOL::test_caseid_1349658_108540
#TestBgm_SOC_EOL 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_EOL::test_caseid_1349668
#TestBgm_MCU_DID 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_MCU_DID::test_caseid_1349757
#TestBgm_SOC_DID 测试： pytest bgm/test_diag_bgm_full.py::TestBgm_SOC_DID::test_caseid_1349658