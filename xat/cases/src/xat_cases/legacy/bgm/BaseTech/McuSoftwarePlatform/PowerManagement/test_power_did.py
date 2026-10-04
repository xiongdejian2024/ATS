# -*- coding: utf-8 -*-
"""
@File        : test_power_management.py
@Author      : 
@Time        : 2023/08/28 20:46 PM
@Description : 电源管理测试
@Examples    : example of how to use it
"""
import allure
import pytest
import time
from time import sleep
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH


@allure.feature("车身网关测试/整车控制")
@allure.story("Relay Control")
class TestRelayContolCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.nucapp.bgm_diag_line_up()
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester.diagnostic_client_sim_start()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        self.ssh=BGM_SSH()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        sleep(0.1)

    def after_each_func(self, ecu):
        self.sd_tester.change_car_mode(0)
        sleep(0.1)
        self.sd_tester.change_usage_mode(0)
        sleep(0.1)
        self.ipdu.reset_check_results()
        sleep(0.1)
        logger.info("诊断激活线连接")
        self.nucapp.bgm_diag_line_up()
        # sleep(1)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        self.nucapp.bgm_diag_line_down()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        logger.info("诊断激活线连接")
        self.nucapp.bgm_diag_line_up()
        sleep(0.5)
        super().after_class(self, ecu)



    @allure.title("电源管理_DTC_触发心跳异常")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919244(self):
        try:
            with allure.step("进入默认会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
            with allure.step("读取电源管理补电常数"):
                #self.sd_tester.send_request_and_recv_response([0x22,0xF0,0xF5],recv=[0x62,0xF0,0xF5,0X28,0X0A,0X03,0X05,0X03,0X02]) 
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0])
                self.sd_tester.change_usage_mode(13)
                self.sd_tester.send_request_and_recv_response([0x14,0xFF,0xFF,0XFF],recv=[0x54])
            with allure.step("制造心跳异常"): 
                self.sd_tester.stop_tester_present()  
                self.ssh.type_commands(commands="shutdown -h now")    
                time.sleep(20)
                self.sd_tester.update_serverdoipid(0x1002)
            with allure.step("BGM重连"):
                self.sd_tester.tester_present()
                self.sd_tester.change_usage_mode(13)
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0])
                time.sleep(1)
        except:
            assert False

    @allure.title("电源管理_DTC_心跳异常清除")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919245(self):
        try:
            with allure.step("进入默认会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
            with allure.step("读取电源管理补电常数"):
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0])
                self.sd_tester.change_usage_mode(13)
                self.sd_tester.send_request_and_recv_response([0x14,0xFF,0xFF,0XFF],recv=[0x54])
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0,0X00,0X00,0X00])
                time.sleep(1)
        except:
            assert False

    @allure.title("电源管理_DTC_心跳异常清除")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.smoke
    @pytest.mark.full 
    def test_HvActive_caseid_1919245(self):
        try:
            with allure.step("进入默认会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
            with allure.step("读取电源管理补电常数"):
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0])
                self.sd_tester.change_usage_mode(13)
                self.sd_tester.send_request_and_recv_response([0x14,0xFF,0xFF,0XFF],recv=[0x54])
                self.sd_tester.send_request_and_recv_response([0x19,0x04,0xF0,0X00,0X00,0X20],recv=[0x59,0x04,0xF0,0X00,0X00,0X50])
                time.sleep(1)
        except:
            assert False

    @allure.title("电源管理_参数配置_修改CCP")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.debug 
    def test_HvActive_caseid_1234567(self):
        try:
            with allure.step("进入默认会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
            with allure.step("读取电源管理补电常数"):
                #self.sd_tester.send_request_and_recv_response([0x22,0xF0,0xF5],recv=[0x62,0xF0,0xF5,0X28,0X0A,0X03,0X05,0X03,0X02]) 
                q,p = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x06],recv=[0x62,0xF1,0x06]) 
                #p = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                data = p[952]
                logger.info('data={}'.format(data))
                # assert p[963] == 0x00 or p[963] == 0x01 or p[963] ==0x02 or p[963] ==0x03, '返回值超出范围'    
            with allure.step("进入扩展会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
            with allure.step("通过安全访问L5"):
                self.sd_tester.security_access_level_l3()
            with allure.step("写入MPU心跳时间"):
                self.sd_tester.write_single_ccp(950,0x02)
                q,p = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x06],recv=[0x62,0xF1,0x06]) 
                #p = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                data = p[952]
                logger.info('data={}'.format(data))
                #assert p[963] == 0x01 or p[963] ==0x02, '返回值超出范围'   
        except:
    
            assert False
    
    @allure.title("电源管理_参数配置_修改整车版本")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.debug 
    def test_HvActive_caseid_1234568(self):
        try:
            with allure.step("进入默认会话"):
                self.sd_tester.update_serverdoipid(0x1001)
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
            
            with allure.step("进入扩展会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
            with allure.step("通过安全访问L5"):
                self.sd_tester.security_access_level_l3()
            with allure.step("写入整车版本"):
                
                self.sd_tester.send_request_and_recv_response([0x2E,0xF1,0x50,0X61,0X00,0X00,0X02,0X00,0X20,0X41,0X41],recv=[0x6E])
                  
        except:
    
            assert False