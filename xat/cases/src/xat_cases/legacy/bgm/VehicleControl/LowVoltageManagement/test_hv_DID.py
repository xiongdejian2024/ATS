#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_OuterRearView_ctrl.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设智能补电
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *

class DidFlag(object):
    read_did_flag = False
    a_did = []
    b_did = []
    c_did = []
    d_did = []
    e_did = []
    f_did = []

@allure.feature("车控车设")
@allure.story("智能补电")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        # self.soa.update(["HighVoltageService_client","CentralLockService_client","WTIService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    @allure.title("智能补电_参数配置_定时器唤醒4532")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109473?projectId=46'
    )
    @pytest.mark.smoke 
    def test_HvActive_caseid_109473(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x32],recv=[0x62,0x45,0x32])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x00 or data[-1] == 0x01 , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x32,0x01],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x32],recv=[0x62,0x45,0x32,0x01])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x32],recv=[0x62,0x45,0x32,0x01])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x32,0x00],recv=[0x6E])
            time.sleep(1)
    
    @allure.title("智能补电_参数配置_电压唤醒充电4530")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109487?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109487(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x30],recv=[0x62,0x45,0x30])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x00 or data[-1] == 0x01 , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x30,0x01],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x30],recv=[0x62,0x45,0x30,0x01])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x30],recv=[0x62,0x45,0x30,0x01])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x30,0x00],recv=[0x6E])
            time.sleep(1)
    
    @allure.title("智能补电_参数配置_睡眠唤醒电压4531")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109483?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109483(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x31],recv=[0x62,0x45,0x31])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x76 or data[-1] == 0x6E , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x31,0x6E],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x31],recv=[0x62,0x45,0x31,0x6E])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x31],recv=[0x62,0x45,0x31,0x6E])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x31,0x76],recv=[0x6E])
            time.sleep(1)
    
    @allure.title("智能补电_参数配置_停止充电4533")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109476?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109476(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x33],recv=[0x62,0x45,0x33])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x5D or data[-1] == 0x6E , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x33,0x6E],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x33],recv=[0x62,0x45,0x33,0x6E])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x33],recv=[0x62,0x45,0x33,0x6E])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x33,0x5D],recv=[0x6E])
            time.sleep(1)

    @allure.title("智能补电_参数配置_inactive充电电压4534")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109475?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109489_109475(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x34],recv=[0x62,0x45,0x34])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x73 or data[-1] == 0x6E , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x34,0x73],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x34],recv=[0x62,0x45,0x34,0x73])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x34],recv=[0x62,0x45,0x34,0x73])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x34,0x6E],recv=[0x6E])
            time.sleep(1)
        
    @allure.title("智能补电_参数配置_inactive充电电压4535")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109478(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        with allure.step("读取Timer Wake Up Charging At Sleep Enable 测试"):
            p,data = self.sd_tester.send_request_and_recv_response([0x22,0x45,0x35],recv=[0x62,0x45,0x35])
            logger.info('data={}'.format(data))
            assert data[-1] == 0x4B or data[-1] == 0x50 , '返回值超出范围'
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入Timer Wake Up Charging At Sleep Enable 测试"):
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x35,0x50],recv=[0x6E])
            time.sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x35],recv=[0x62,0x45,0x35,0x50])
        with allure.step("BGM重启"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step("BGM重连"):
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x35],recv=[0x62,0x45,0x35,0x50])
        with allure.step("恢复写入前的值"):
            self.sd_tester.send_data([0x10,0x03])
            time.sleep(1)
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
            self.sd_tester.send_request_and_recv_response([0x2E,0x45,0x35,0x4B],recv=[0x6E])
            time.sleep(1)

    @allure.title("BMS_参数配置_默认值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.debug
    @pytest.mark.V_1_4noly
    def test_HvActive_caseid_2000000(self):
        self.sd_tester.write_bms_did_value(0xBB00,write_data="4b",check_resp="6ebb00",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB01,write_data="00",check_resp="6ebb01",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB02,write_data="4b",check_resp="6ebb02",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB03,write_data="00",check_resp="6ebb03",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB04,write_data="76",check_resp="6ebb04",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB05,write_data="00",check_resp="6ebb05",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB06,write_data="8080",check_resp="6ebb06",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB07,write_data="00",check_resp="6ebb07",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB08,write_data="8080",check_resp="6ebb08",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB09,write_data="10e0",check_resp="6ebb09",wait_time=1)

    @allure.title("BMS_参数配置_2.0版本默认值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.debug
    @pytest.mark.V_2_0noly
    def test_HvActive_caseid_2000001(self):
        self.sd_tester.write_bms_did_value(0xBB00,write_data="4b",check_resp="6ebb00",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB01,write_data="00",check_resp="6ebb01",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB02,write_data="4b",check_resp="6ebb02",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB03,write_data="00",check_resp="6ebb03",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB04,write_data="8C",check_resp="6ebb04",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB05,write_data="00",check_resp="6ebb05",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB06,write_data="0032",check_resp="6ebb06",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB07,write_data="00",check_resp="6ebb07",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB08,write_data="01F4",check_resp="6ebb08",wait_time=1)
        self.sd_tester.write_bms_did_value(0xBB09,write_data="10e0",check_resp="6ebb09",wait_time=1)
    
    @allure.title("BMS_参数配置_BB00_开始补电的小电池SOC阈值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919301_1983134(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB00, "4b", default_mode=True)
        self.sd_tester.write_bms_did_value(0xBB00, write_data="50", check_resp="6ebb00", wait_time=1)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB00, "50")
        self.sd_tester.recover_bms_did_to_default_value(0xBB00, "4b")


    @allure.title("BMS_参数配置_BB01_BMS低SOC唤醒网络设置")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919297(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB01, "00", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocEna, value=GeneralSts.Enable)
        self.sd_tester.write_bms_did_value(0xBB01,write_data="01",check_resp="6ebb01",out_range_value=["02"],wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocEna, value=GeneralSts.Disable)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB01, "01")
        self.sd_tester.recover_bms_did_to_default_value(0xBB01, "00")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocEna, value=GeneralSts.Enable)

    @allure.title("BMS_参数配置_BB02")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1919300(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value("0xbb02", "4b", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=750)
        self.sd_tester.write_bms_did_value(0xBB02, write_data="50", check_resp="6ebb02", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=800)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB02, "50")
        self.sd_tester.recover_bms_did_to_default_value("0xbb02", "4b")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=750)

    @allure.title("BMS_参数配置_BB02")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919300(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value("0xbb02", "4b", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=75)
        self.sd_tester.write_bms_did_value(0xBB02, write_data="50", check_resp="6ebb02", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=80)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB02, "50")
        self.sd_tester.recover_bms_did_to_default_value("0xbb02", "4b")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocThd,value=75)

    @allure.title("BMS_参数配置_BB03")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919298(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB03, "00", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolEna, value=GeneralSts.Enable)
        self.sd_tester.write_bms_did_value(0xBB03,write_data="01",check_resp="6ebb03",out_range_value=["02"],wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolEna, value=GeneralSts.Disable)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB03, "01")
        self.sd_tester.recover_bms_did_to_default_value(0xBB03, "00")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolEna, value=GeneralSts.Enable)

    @allure.title("BMS_参数配置_BB04")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1919299(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB04, "76", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=272)
        self.sd_tester.write_bms_did_value(0xBB04, write_data="50", check_resp="6ebb04", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=120)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB04, "50")
        self.sd_tester.recover_bms_did_to_default_value(0xBB04, "76")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=272)

    @allure.title("BMS_参数配置_BB04")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919299(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB04, "8C", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=11.8)
        self.sd_tester.write_bms_did_value(0xBB04, write_data="78", check_resp="6ebb04", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=11.4)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB04, "78")
        self.sd_tester.recover_bms_did_to_default_value(0xBB04, "8C")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolThd,value=11.8)

    @allure.title("BMS_参数配置_BB05")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1983544(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB05, "00", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrEna, value=GeneralSts.Enable)
        self.sd_tester.write_bms_did_value(0xBB05,write_data="01",check_resp="6ebb05",out_range_value=["02"],wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrEna, value=GeneralSts.Disable)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB05, "01")
        self.sd_tester.recover_bms_did_to_default_value(0xBB05, "00")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrEna, value=GeneralSts.Enable)

    @allure.title("BMS_参数配置_BB06")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1984938(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB06, "8080", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=32896)
        self.sd_tester.write_bms_did_value(0xBB06, write_data="4000", check_resp="6ebb06", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=16384)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB06, "4000")
        self.sd_tester.recover_bms_did_to_default_value(0xBB06, "8080")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=32896)

    @allure.title("BMS_参数配置_BB06")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1984938(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB06, "0032", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=50)
        self.sd_tester.write_bms_did_value(0xBB06, write_data="4000", check_resp="6ebb06", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=16384)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB06, "4000")
        self.sd_tester.recover_bms_did_to_default_value(0xBB06, "0032")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrThd,value=50)

    @allure.title("BMS_参数配置_BB07")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1984939(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB07, "00", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrEna, value=GeneralSts.Enable)
        self.sd_tester.write_bms_did_value(0xBB07,write_data="01",check_resp="6ebb07",out_range_value=["02"],wait_time=1,)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrEna, value=GeneralSts.Disable)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB07, "01")
        self.sd_tester.recover_bms_did_to_default_value(0xBB07, "00")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrEna, value=GeneralSts.Enable)

    @allure.title("BMS_参数配置_BB08")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1984940(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB08, "8080", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=32896)
        self.sd_tester.write_bms_did_value(0xBB08, write_data="4000", check_resp="6ebb08", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=16384)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB08, "4000")
        self.sd_tester.recover_bms_did_to_default_value(0xBB08, "8080")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=32896)

    @allure.title("BMS_参数配置_BB08")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1984940(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value(0xBB08, "01F4", default_mode=True)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=500)
        self.sd_tester.write_bms_did_value(0xBB08, write_data="4000", check_resp="6ebb08", wait_time=1)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=16384)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB08, "4000")
        self.sd_tester.recover_bms_did_to_default_value(0xBB08, "01F4")
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrThd,value=500)

    @allure.title("BMS_参数配置_BB09")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1984941(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.write_bms_did_value(0xBB09, write_data="10e0", check_resp="6ebb09", wait_time=1)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.sd_tester.read_bms_did_value(0xBB09, "10e0", default_mode=True)
        self.bus_comm.check_RTC_time(4320)
        self.sd_tester.write_bms_did_value(0xBB09, write_data="0002", check_resp="6ebb09", wait_time=1)
        self.bus_comm.check_RTC_time(2)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB09, "0002")
        self.sd_tester.recover_bms_did_to_default_value(0xBB09, "10e0")
        self.bus_comm.check_RTC_time(4320)
        
    

    @allure.title("DID_41CE_运输方式电池充电状态_BattSocMinInTrnsp")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985556?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985556(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("运输方式电池充电状态"):
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0xCE],recv=[0x62,0x41,0xCE])
            # self.sd_tester.send_request_and_recv_response([0x22,0x41,0xCE],recv=[0x62,0x41,0xCE,
            #                                                                      0x64])
            
            
    
    @allure.title("DID_40AF_自上次重置后的秒数_BattChrgBalStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985558?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985558(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("自上次重置后的秒数"):
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xAF],recv=[0x62,0x40,0xAF])
            # self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x04,0xC3,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00])
            
            
        
    @allure.title("DID_40FC_电池监控器传感器故障统计计数器_BattSnsrFltStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985559?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985561(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池监控器传感器故障统计计数器"):
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xFC],recv=[0x62,0x40,0xFC])
            # self.sd_tester.send_request_and_recv_response([0x22,0x40,0xFC],recv=[0x62,0x40,0xFC,
            #                                                                      0x00,0x00,0x00])
            
    @allure.title("DID_414B_电池A温度统计_BattTStc_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985559?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985562(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池A温度统计"):
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x4B],recv=[0x7F,0x22,0x31])
            # self.sd_tester.send_request_and_recv_response([0x22,0x41,0x4B],recv=[0x62,0x41,0x4B,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00,
            #                                                                      0x00,0x00])
            
    
            
            
    @allure.title("DID_42D3_电池内阻_BattRRec")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985564?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985565(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池内阻"):
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD3],recv=[0x62,0x42,0xD3,
                                                                                 0x00,0x00,
                                                                                 0x00,0x00,
                                                                                 0x00,0x00,
                                                                                 0x00,0x00,
                                                                                 0x00,0x00])

    @allure.title("DID_40E5_低压系统状态_LVPwrSplyErrSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985564?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985411(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压电源系统故障统计"):
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE5,0x00])
            logger.info('data={}'.format(data))
            self.mix.set_usage_mode(UsageMode.DRIVING)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            sleep(5)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x01])

    # @allure.title("DID_F022_外灯控制_Exterior_Lights_Control")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.V_1_4
    # def test_HvActive_caseid_1985416(self):
    #     with allure.step("进入扩展会话"):
    #         self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
    #     with allure.step("通过安全访问L5"):
    #         self.sd_tester.security_access_level(UnLock.L5)
    #     with allure.step("写入外灯控制"):
    #         self.sd_tester.send_request_and_recv_response([0x2F,0x70,0x22,0X03,0x00,0x00,0x00,0xFF,0xFF,0xFF],recv=[0x6F])    
    #     with allure.step("外灯控制"):
    #         self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #         self.sd_tester.send_request_and_recv_response([0x22,0x70,0x22],recv=[0x62,0x70,0x22,0x00,0x00,0x00])
    
    
    @allure.title("DID_F022_外灯控制_Exterior_Lights_Control")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985417(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入外灯控制"):
            self.sd_tester.send_request_and_recv_response([0x2F,0x70,0x22,0X03,0x01,0x00,0x00,0x01,0x00,0x00],recv=[0x6F])    
        with allure.step("外灯控制"):
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x70,0x22],recv=[0x62,0x70,0x22,0x01,0x00,0x00])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x2F,0x70,0x22,0X03,0x00,0x00,0x00,0xFF,0xFF,0xFF],recv=[0x6F])
    
    
    
    @allure.title("DID_4516_工厂模式下低压电池 Battery SoC")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985578(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("工厂模式下低压电池"):
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
            self.sd_tester.send_request_and_recv_response([0x22,0x45,0x16],recv=[0x62,0x45,0x16,0x00])
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)    
        
    @allure.title("DID_433E_运输模式下低压电池 Battery SoC")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985579(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("运输模式下低压电池"):
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
            self.sd_tester.send_request_and_recv_response([0x22,0x43,0x3E],recv=[0x62,0x43,0x3E,0x00])
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
    
    @allure.title("DID_4148_可用能源登记册_BattLoWarnStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985490(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用能源登记册"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x48],recv=[0x62,0x41,0x48])
            # self.sd_tester.send_request_and_recv_response([0x22,0x41,0x48],recv=[0x62,0x41,0x48,0x00,0x00,0x00,0x00])
            
    @allure.title("DID_4187_可用能源登记册_BattLoWarnStcIn TrnspMod")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985491(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用能源登记册"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x87],recv=[0x62,0x41,0x87,0x00,0x00])
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
    
    @allure.title("DID_40E2_可用Delta电源信号输出_Delta Power")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985487(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用Delta电源信号输出"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0xFF,0x9C])
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入框架设置"):
            self.sd_tester.send_request_and_recv_response([0x2F,0x40,0xE2,0X03,0x7F,0xFF],recv=[0x6F,0x40,0xE2]) 
            sleep(2)   
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0x7F,0xFF])
            self.sd_tester.send_request_and_recv_response([0x2F,0x40,0xE2,0X03,0xFF,0x9C],recv=[0x6F,0x40,0xE2]) 
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0xFF,0x9C])
     

    @allure.title("DID_D934_电池可用Delta能量_Delta Energy")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985488(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池可用Delta能量"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34])
            # self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34,0x00])

    @allure.title("DID_D935_电池能量可用警告_Delta Energy")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985489(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池能量可用警告"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35])
            # self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35,0x14])        
    
    @allure.title("DID_40CA_低压报警次数统计_ Battery Warning")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985581(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压报警次数统计"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCA],recv=[0x62,0x40,0xCA])
            # self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCA],recv=[0x62,0x40,0xCA,0x02,0X01])
    
    @allure.title("DID_40CA_低压报警次数统计_ Battery Warning")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985617(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压报警次数统计"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCA],recv=[0x62,0x40,0xCA])
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCA],recv=[0x62,0x40,0xCA,0x00,0X00])
    
    @allure.title("DID_DD02_车辆电池电压_VehBattUSysU")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988860(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("车辆电池电压"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x02],recv=[0x62,0xDD,0x02])
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x02],recv=[0x62,0xDD,0x02,0x34])
    
    @allure.title("DID_4025_电池静态电流-低范围_BattIQuiscFildLongRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988840(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池静态电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscFildLongRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x25],recv=[0x62,0x40,0x25,0x01,0xFF])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscFildLongRaw",-10.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x25],recv=[0x62,0x40,0x25,0x01,0xF5])
    
    # @allure.title("DID_4026_发动机关闭时电池的归一化累积放电_BattCycDchaCntrDurgConvceRaw")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.V_1_4
    # def test_HvActive_caseid_1985584(self):
    #     with allure.step("进入默认会话"):
    #         self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
    #     with allure.step("发动机关闭时电池的归一化累积放电"):
    #         self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
    #         self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",0.0)
    #         sleep(2)
    #         self.sd_tester.send_request_and_recv_response([0x22,0x40,0x26],recv=[0x62,0x40,0x26,0x00,0x00])
    #         self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",800.0)
    #         sleep(2)
    #         self.sd_tester.send_request_and_recv_response([0x22,0x40,0x26],recv=[0x62,0x40,0x26,0x3E,0x80])

    @allure.title("DID_4027_车辆电池-使用时间_BattTiInSrvRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988839(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("车辆电池-使用时间"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattTiInSrvRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x27],recv=[0x62,0x40,0x27,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattTiInSrvRaw",2.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x27],recv=[0x62,0x40,0x27,0x00,0x02])
    
    @allure.title("DID_4028_车辆电池充电状态_BattSocFild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988841(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("车辆电池充电状态"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x28],recv=[0x62,0x40,0x28,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x28],recv=[0x62,0x40,0x28,0x00,0xC8])
    
    @allure.title("DID_4029_汽车电池温度_BattTFild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988842_1985508(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("汽车电池温度"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattTRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x29],recv=[0x62,0x40,0x29,0x01,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattTRaw",40.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x29],recv=[0x62,0x40,0x29,0x01,0x50])

    @allure.title("DID_402A_车载电池电压_VehBattU")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1988843(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("车载电池电压"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            U2 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysU')
            logger.info(F"{U2}")
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x2A],recv=[0x62,0x40,0x2A,U2])
            
    
    @allure.title("DID_4090_电池电流_BattIFIld")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985574(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr01","BattIRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x90],recv=[0x62,0x40,0x90,0x80,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr01","BattIRaw",1.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x90],recv=[0x62,0x40,0x90,0x80,0x40])
    
    
    @allure.title("433438_BMS参数寄存器_BattChrgBalStc_40A2（休眠）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1118
    def test_HvActive_caseid_1985558(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电量平衡记录"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattChrgnBalDurgDrvgRaw",-5.0)
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data))
            sleep(2)
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            p,data1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data1={}'.format(data1))
            assert data1[-1] == data[-1]+1, '数值累加异常'
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,data2 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data2))
            assert data2[-1] == data1[-1],  '数值存储异常'

    @allure.title("433438_BMS参数寄存器_BattChrgBalStc_40A2（诊断）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1118
    def test_HvActive_caseid_1996218(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电量平衡记录"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattChrgnBalDurgDrvgRaw",0.0)
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data))
            sleep(2)
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            p,data1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data1={}'.format(data1))
            assert data1[-5] == data[-5]+1, '数值累加异常'
            self.sd_tester.reboot_bgm_by_diag_hardreset()
            p,data2 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data2))
            assert data2[-5] == data1[-5],  '数值存储异常'

    @allure.title("433438_BMS参数寄存器_BattChrgBalStc_40A2（上下电）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1118
    def test_HvActive_caseid_1996219(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电量平衡记录"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattChrgnBalDurgDrvgRaw",-1.0)
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data))
            sleep(2)
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            p,data1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data1={}'.format(data1))
            assert data1[-3] == data[-3]+1, '数值累加异常'
            self.io.bgm_power_off()
            self.io.bgm_power_on()
            p,data2 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xA2],recv=[0x62,0x40,0xA2])
            logger.info('data={}'.format(data2))
            assert data2[-3] == data1[-3],  '数值存储异常'  
    
    @allure.title("DID_40B0_电池容量_BattCpRel")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985568(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池容量"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",16.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xB0],recv=[0x62,0x40,0xB0,0x20])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",40.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xB0],recv=[0x62,0x40,0xB0,0x50])
    
    @allure.title("DID_40B0_电池容量_BattCpRel")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_2_0
    def test_HvActive_caseid_1985568(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池容量"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",16.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xB0],recv=[0x62,0x40,0xB0,0x1B])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",40.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xB0],recv=[0x62,0x40,0xB0,0x50])

    @allure.title("DID_40CB_电池传感器一致性检查_BattSnsrCalcnNotVldFild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981628(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池传感器一致性检查"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattSnsrCalcnNotVldRaw",0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCB],recv=[0x62,0x40,0xCB,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattSnsrCalcnNotVldRaw",1)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCB],recv=[0x62,0x40,0xCB,0x01])

    @allure.title("DID_40CB_电池传感器一致性检查_BattSnsrCalcnNotVldFild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_2_0
    def test_HvActive_caseid_1981628(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池传感器一致性检查"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattSnsrCalcnNotVldRaw",0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCB],recv=[0x62,0x40,0xCB,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattSnsrCalcnNotVldRaw",1)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCB],recv=[0x62,0x40,0xCB,0x00])
    
    @allure.title("DID_411D_请求充电电压_ChrgnUReq")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985500(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("请求充电电压"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
            self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
            self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x1D],recv=[0x62,0x41,0x1D,0x98])
            self.mix.set_low_volt_servse_mode(sys_falt=True, time_wait=20)
            self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=13.5)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x1D],recv=[0x62,0x41,0x1D,0x74])

    @allure.title("DID_40D1_充电模式_ChrgModReq")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985498(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("充电模式"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00","EngSt1WdStsEngSt1WdSts",0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD1],recv=[0x62,0x40,0xD1,0x00])
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00","EngSt1WdStsEngSt1WdSts",6)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD1],recv=[0x62,0x40,0xD1,0x02])
    
    @allure.title("DID_42E3_电池静态电流短时间滤波_低范围_BattIQuiscFildShoRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981580(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池静态电流短时间滤波_低范围"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattIQuiscFildShoRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0xE3],recv=[0x62,0x42,0xE3,0x01,0XFF])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattIQuiscFildShoRaw",-10.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0xE3],recv=[0x62,0x42,0xE3,0x01,0XF5])
    
    @allure.title("DID_42E4_电池平均静态电流_高范围_BattIQuiscAvgRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981579(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池平均静态电流_高范围"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscAvgRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0xE4],recv=[0x62,0x42,0xE4,0x01,0XFF])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscAvgRaw",-10.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0xE4],recv=[0x62,0x42,0xE4,0x01,0XFD])

    # @allure.title("DID_E503_VFC Vector框架设置_VFCInfoEna")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.V_1_4
    # def test_HvActive_caseid_1981535(self):
    #     with allure.step("进入默认会话"):
    #         self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
    #     with allure.step("VFC Vector框架设置"):
    #         self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
    #         self.sd_tester.send_request_and_recv_response([0x22,0xE5,0x03],recv=[0x62,0xE5,0x03,0x01])
    #     with allure.step("进入扩展会话"):
    #         self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
    #     with allure.step("通过安全访问L5"):
    #         self.sd_tester.security_access_level(UnLock.L5)
    #     with allure.step("写入框架设置"):
    #         self.sd_tester.send_request_and_recv_response([0x2E,0xE5,0x03,0x00],recv=[0x6E]) 
    #         sleep(2)   
    #         self.sd_tester.send_request_and_recv_response([0x22,0xE5,0x03],recv=[0x62,0xE5,0x03,0x00])
    #         self.sd_tester.send_request_and_recv_response([0x2E,0xE5,0x03,0x01],recv=[0x6E]) 
    #         sleep(2)
    #         self.sd_tester.send_request_and_recv_response([0x22,0xE5,0x03],recv=[0x62,0xE5,0x03,0x01])

    @allure.title("DID_F010_BGM唤醒原因_BWake Up Cause")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981531(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("BGM唤醒原因"):
            self.sd_tester.send_request_and_recv_response([0x22,0xF0,0x10],recv=[0x62,0xF0,0x10])
            
    @allure.title("DID_F011_BGM保持唤醒的原因_Keep Active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981530(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("BGM保持唤醒的原因"):
            self.sd_tester.send_request_and_recv_response([0x22,0xF0,0x11],recv=[0x62,0xF0,0x11])

    @allure.title("DID_4444_BGM计算的小电池SOC值_BattSoc2Fild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981477(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("BGM计算的小电池SOC值"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.sd_tester.reboot_bgm_by_diag_hardreset()
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x44,0x44],recv=[0x62,0x44,0x44,0x00,0X63])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",100.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x44,0x44],recv=[0x62,0x44,0x44,0x00,0X63])

    @allure.title("DID_4253_ECM唤醒控制_BattSoc2Fild")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981767(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("ECM唤醒控制"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入框架设置"):    
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x53,0x03,0x01],recv=[0x6F,0x42,0x53])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0x53],recv=[0x62,0x42,0x53,0x01])
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x53,0x03,0x00],recv=[0x6F,0x42,0x53])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x42,0x53],recv=[0x62,0x42,0x53,0x00])

    # @allure.title("DID_D136_SALM休眠唤醒控制_BattSoc2Fild")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.V_1_4
    # def test_HvActive_caseid_1981475(self):
    #     with allure.step("进入扩展会话"):
    #         self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
    #     with allure.step("SALM休眠唤醒控制"):
    #         self.sd_tester.security_access_level(UnLock.L5)
    #         self.sd_tester.send_request_and_recv_response([0x2F,0xD1,0x36,0x03,0x01],recv=[0x6F])
    #         sleep(2)
    #         self.sd_tester.send_request_and_recv_response([0x22,0xD1,0x36],recv=[0x62,0xD1,0x36,0x02])
    #         self.sd_tester.send_request_and_recv_response([0x2F,0xD1,0x36,0x03,0x00],recv=[0x6F])
    #         sleep(2)
    #         self.sd_tester.send_request_and_recv_response([0x22,0xD1,0x36],recv=[0x62,0xD1,0x36,0x00])

    @allure.title("DID_2022_电池传感器请求_Sensor Request")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1981839(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("电池传感器请求"):
            self.sd_tester.send_request_and_recv_response([0x31,0x01,0x20,0x22,0x01],recv=[0x71,0x01,0x20,0x22,0x22])
            self.sd_tester.send_request_and_recv_response([0x31,0x02,0x20,0x22],recv=[0x71,0x02,0x20,0x22,0x20])
            self.sd_tester.send_request_and_recv_response([0x31,0x03,0x20,0x22],recv=[0x71,0x03,0x20,0x22,0x20])

    @allure.title("DID_4311_BMS电池电流_BattIRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985575(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr01","BattIRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x43,0x11],recv=[0x62,0x43,0x11,0x80,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr01","BattIRaw",1.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x43,0x11],recv=[0x62,0x43,0x11,0x80,0x40])

    @allure.title("DID_417C_归一化蓄电池累计放电总量_BattCycDchaTo_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985573(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x7C],recv=[0x62,0x41,0x7C,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x7C],recv=[0x62,0x41,0x7C,0x00,0x28])

    @allure.title("DID_40D0_点火过程中电池累计放电归一化_BattCycDchaCntrDurgQuiscPhaRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985572(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgQuiscPhaRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD0],recv=[0x62,0x40,0xD0,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgQuiscPhaRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD0],recv=[0x62,0x40,0xD0,0x05,0x00])

    @allure.title("DID_40CF_点火过程中电池电归一化_BattCycDchaCntrDurgDrvgRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985571(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgDrvgRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCF],recv=[0x62,0x40,0xCF,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgDrvgRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCF],recv=[0x62,0x40,0xCF,0x01,0x90])

    @allure.title("DID_4026_发动机关闭后电池累计放电归一化_BattCycDchaCntrDurgConvceRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985570(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x26],recv=[0x62,0x40,0x26,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycDchaCntrDurgConvceRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0x26],recv=[0x62,0x40,0x26,0x01,0x90])

    @allure.title("DID_40CE_发动机关闭后电池累计放电归一化_BattCycChrgCntrRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985569(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycChrgCntrRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCE],recv=[0x62,0x40,0xCE,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr02","BattCycChrgCntrRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCE],recv=[0x62,0x40,0xCE,0x01,0x90])

    @allure.title("DID_40CC_发动机关闭后电池累计放电归一化_BattCpEstimdRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985567(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCC],recv=[0x62,0x40,0xCC,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattCpEstimdRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xCC],recv=[0x62,0x40,0xCC,0x14])

    @allure.title("DID_438B_发动机关闭后电池累计放电归一化_BattChrgnBalDurgDrvgRaw_删除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985566(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池电流"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattChrgnBalDurgDrvgRaw",0.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x43,0x8B],recv=[0x62,0x43,0x8B,0x4E,0x20])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04","BattChrgnBalDurgDrvgRaw",20.0)
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0x43,0x8B],recv=[0x62,0x43,0x8B,0x5D,0xC0])


    @allure.title("DID_40E2_电池能量_PwrAvlDelta_DcDcActvd")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.ceshi
    def test_HvActive_caseid_1989415(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用Delta电源信号输出"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcAvlMaxLoSide',3.0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcActLoSideIDcDcActLoSide',3.0)
            sleep(12)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0xF8,0x30])
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", -2000.0)
        with allure.step("高压状态"):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',1)
            self.bus_comm.set_batturaw(BattURaw=15.0)
            self.bus_comm.set_battiraw(BattIRaw=2.0)
            sleep(10)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.SysOk)
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", 1920.0)  #64*BattURaw*attIRaw
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0x07,0x80])
     
    @allure.title("DID_40E2_电池能量_PwrAvlDelta_DcDcActvd")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.ceshi
    def test_HvActive_caseid_1990779(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用Delta电源信号输出"):
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcAvlMaxLoSide',13.0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcActLoSideIDcDcActLoSide',3.0)
            sleep(12)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0xF8,0x30])
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", -2000.0)
        with allure.step("高压状态"):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',1)
            self.bus_comm.set_batturaw(BattURaw=15.0)
            self.bus_comm.set_battiraw(BattIRaw=2.0)
            sleep(10)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.SysOk)
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", 150.0)  #64*BattURaw*attIRaw
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0x00,0x96])

    @allure.title("DID_40E2_电池能量_PwrAvlDelta_DcDcActvd")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.ceshi
    def test_HvActive_caseid_1990780(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("可用Delta电源信号输出"):
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcAvlMaxLoSide',13.0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr11",'IDcDcActLoSideIDcDcActLoSide',3.0)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00","EngSt1WdStsEngSt1WdSts", 8)
            sleep(12)
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0xF8,0x30])
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", -2000.0)
        with allure.step("高压状态"):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',1)
            self.bus_comm.set_batturaw(BattURaw=12.0)
            self.bus_comm.set_battiraw(BattIRaw=2.0)
            sleep(10)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.SysOk)
            self.bus_comm.check_singal("bodycan","CemBodyFr69","PwrAvlDelta", 120.0)  #64*BattURaw*attIRaw
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE2],recv=[0x62,0x40,0xE2,0x00,0x78])

    @allure.title("DID_4148_可用能源登记册_BattLoWarnStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985494(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
            self.mix.sd_tester.reset_bgm()    
        with allure.step("可用能源登记册"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", -16.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", -16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34,0x00])
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35,0x00])
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x48],recv=[0x62,0x41,0x48,0x00,0x00,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",70.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", 12.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", 16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34,0x20])
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35,0x1c])
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x48],recv=[0x62,0x41,0x48,0x00,0x01,0x00,0x01])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", -16.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", -16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x48],recv=[0x62,0x41,0x48,0x00,0x01,0x00,0x01])

    @allure.title("DID_4148_电量不足告警统计EgyAvlToWarn_Transport")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1985492(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
            self.mix.sd_tester.reset_bgm()    
        with allure.step("可用能源登记册"):
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", -16.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", -16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34,0x00])
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35,0x00])
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x87],recv=[0x62,0x41,0x87,0x00,0x00])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",70.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", 12.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", 16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x34],recv=[0x62,0xD9,0x34,0x20])
            self.sd_tester.send_request_and_recv_response([0x22,0xD9,0x35],recv=[0x62,0xD9,0x35,0x1c])
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x87],recv=[0x62,0x41,0x87,0x01,0x01])
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlToWarn", -16.0)
            self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr23","EgyAvlDelta", -16.0)
            self.sd_tester.send_request_and_recv_response([0x22,0x41,0x87],recv=[0x62,0x41,0x87,0x01,0x01])

    @allure.title("DID_BB0A_左前门端电压触发闭合冗余回路的电压阈值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1987639(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value("0xBB0A", "5A", default_mode=True)
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="7E", check_resp="6eBB0A", wait_time=1)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0A, "7E")
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A")

    @allure.title("DID_BB0B_BGM检测IPM端电压触发闭合冗余回路的电压阈值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1987640(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value("0xBB0B", "5A", default_mode=True)
        self.sd_tester.write_bms_did_value(0xBB0B, write_data="7E", check_resp="6eBB0B", wait_time=1)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0B, "7E")
        self.sd_tester.recover_bms_did_to_default_value("0xBB0B", "5A")

    @allure.title("DID_BB0C_BGM检测IPM端电压断开冗余回路的电压阈值")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1987641(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_bms_did_value("0xBB0C", "73", default_mode=True)
        self.sd_tester.write_bms_did_value(0xBB0C, write_data="7E", check_resp="6eBB0C", wait_time=1)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0C, "7E")
        self.sd_tester.recover_bms_did_to_default_value("0xBB0C", "73")

    @allure.title("门模块电压检测_FLDoorSysU")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_HvActive_caseid_1987611(self):
        self.sd_tester.write_ccp({965 : 0x0})
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        U2 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysU')
        logger.info("BGM电压检测: VehBattUSysU {}".format(U2))
        if U1 ==U2:
            logger.info("BGM电压检测正常")
            pass
        else:
            logger.info("BGM电压检测异常")
            assert False,"门模块电压检测"

    @allure.title("DID_40E4_低压电源系统故障统计_LVPwrSplyFltStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1127
    def test_HvActive_caseid_1985414(self):
        with allure.step("进入默认会话"):
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压电源系统故障统计"):
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x00])
            logger.info('data={}'.format(data))
            self.mix.set_usage_mode(UsageMode.DRIVING)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            sleep(5)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            start=time.time()
            while time.time()-start < 30:
                self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x01])
                p,data1 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
                logger.info('data={}'.format(data1))
                sleep(1)
                if data1[3] == data[3]+1:
                    logger.info(f"耗时{time.time()-start}")
                    break
            else:
                assert 0, '数值累加异常'
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            self.sd_tester.reboot_bgm_by_diag_hardreset()
            p,data2 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            logger.info('data={}'.format(data2))
            assert data2[3] == data1[3],  '数值存储异常'

    @allure.title("DID_40E4_低压电源系统故障统计_LVPwrSplyFltStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985415?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1127
    def test_HvActive_caseid_1985415(self):
        with allure.step("进入默认会话"):
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压电源系统故障统计"):
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x00])
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            logger.info('data={}'.format(data))
            self.mix.set_usage_mode(UsageMode.DRIVING)
            self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            self.bus_comm.set_fltelecdcdc(BattSnsrHwFltRaw.DevErrSts2_Flt)
            sleep(10)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.FltElecDcDc)
            start=time.time()
            while time.time()-start < 30:
                self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x07])
                p,data1 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
                logger.info('data={}'.format(data1))
                sleep(1)
                if data1[9] == data[9]+1:
                    logger.info(f"耗时{time.time()-start}")
                    break
            else:
                assert 0, '数值累加异常'
            self.bus_comm.set_fltelecdcdc(BattSnsrHwFltRaw.DevErrSts2_NoFlt)
            self.io.bgm_power_off()
            self.io.bgm_power_on()
            p,data2 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            logger.info('data={}'.format(data2))
            assert data2[9] == data1[9],  '数值存储异常'

    @allure.title("DID_40E4_低压电源系统故障统计_LVPwrSplyFltStc")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985415?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    @pytest.mark.test1127
    def test_HvActive_caseid_1996208(self):
        with allure.step("进入默认会话"):
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("低压电源系统故障统计"):
            self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x00])
            p,data =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            logger.info('data={}'.format(data))
            self.mix.set_usage_mode(UsageMode.DRIVING)
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            self.bus_comm.pause_bus_send("cem_lin6")
            sleep(20)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.BattSnsrComFlt)
            start=time.time()
            while time.time()-start < 30:
                self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE5],recv=[0x62,0x40,0xE5,0x04])
                p,data1 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
                logger.info('data={}'.format(data1))
                sleep(1)
                if data1[6] == data[6]+1:
                    logger.info(f"耗时{time.time()-start}")
                    break
            else:
                assert 0, '数值累加异常'
            self.bus_comm.resume_bus_send("cem_lin6")
            sleep(10)
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,data2 = self.sd_tester.send_request_and_recv_response([0x22,0x40,0xE4],recv=[0x62,0x40,0xE4])
            logger.info('data={}'.format(data2))
            assert data2[6] == data1[6],  '数值存储异常' 
            
    @allure.title("BMS_参数配置_默认值（休眠唤醒）")
    @pytest.mark.parametrize("did,data,resp",[(0xBB00,"4b","6ebb00"),(0xBB01,"00","6ebb01"),(0xBB02,"4b","6ebb02"),(0xBB03,"00","6ebb03"),
                                              (0xBB04,"76","6ebb04"),(0xBB05,"00","6ebb05"),(0xBB06,"8080","6ebb06"),(0xBB07,"00","6ebb07"),
                                              (0xBB08,"8080","6ebb08"),(0xBB09,"10e0","6ebb09")],
                              ids=[1994519,1994518,1994520,1994521,1994522,1994523,1994524,1994525,1994526,1994527])
    @pytest.mark.nvm
    def test_HvActive_Lowpressure(self,did,data,resp):
        self.sd_tester.write_bms_did_value(did,write_data=data,check_resp=resp,wait_time=1)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.sd_tester.read_bms_did_value(did, data)

    @allure.title("BMS_参数配置_默认值（上下电）")
    @pytest.mark.parametrize("did,data,resp",[(0xBB00,"4b","6ebb00"),(0xBB01,"00","6ebb01"),(0xBB02,"4b","6ebb02"),(0xBB03,"00","6ebb03"),
                                              (0xBB04,"8c","6ebb04"),(0xBB05,"00","6ebb05"),(0xBB06,"0032","6ebb06"),(0xBB07,"00","6ebb07"),
                                              (0xBB08,"01F4","6ebb08"),(0xBB09,"10e0","6ebb09")],
                              ids=[1994529,1994528,1999134,1994530,1994531,1994532,1994533,1994534,1994535,1994536])
    @pytest.mark.nvm
    def test_HvActive_Lowrestart(self,did,data,resp):
        self.sd_tester.write_bms_did_value(did,write_data=data,check_resp=resp,wait_time=1)
        sleep(2.0)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(20)
        self.sd_tester.read_bms_did_value(did, data)

    @allure.title("BMS_电池储存（诊断）")
    @pytest.mark.parametrize("did,resp",[([0x22,0x42,0xD1],[0x62,0x42,0xD1]),([0x22,0x42,0xCD],[0x62,0x42,0xCD])
                                         ,([0x22,0x42,0xCF],[0x62,0x42,0xCF]),([0x22,0x40,0xD7],[0x62,0x40,0xD7])
                                         ,([0x22,0x40,0x94],[0x62,0x40,0x94]),([0x22,0x42,0xD2],[0x62,0x42,0xD2])],
                              ids=[1994539,1994538,1996210,1996214,1996216,1996212])
    @pytest.mark.nvm
    @pytest.mark.test1127
    def test_bms_nvm(self,did,resp):
        p,a1 =self.sd_tester.send_request_and_recv_response(did,recv=resp)
        logger.info('a1={}'.format(a1))
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        p,b1 =self.sd_tester.send_request_and_recv_response(did,recv=resp)
        logger.info('a1={}'.format(b1))
        assert a1 == b1,  '数值存储异常' 

    @allure.title("BMS_电池储存（上下电）")
    @pytest.mark.parametrize("did,resp",[([0x22,0x42,0xD1],[0x62,0x42,0xD1]),([0x22,0x42,0xCD],[0x62,0x42,0xCD])
                                         ,([0x22,0x42,0xCF],[0x62,0x42,0xCF]),([0x22,0x40,0xD7],[0x62,0x40,0xD7])
                                         ,([0x22,0x40,0x94],[0x62,0x40,0x94]),([0x22,0x42,0xD2],[0x62,0x42,0xD2])],
                              ids=[1996209,1994537,1996211,1996215,1996217,1996213])
    @pytest.mark.nvm
    @pytest.mark.test1127
    def test_bms_nvm1(self,did,resp):
        p,a1 =self.sd_tester.send_request_and_recv_response(did,recv=resp)
        logger.info('a1={}'.format(a1))
        sleep(2.0)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(20)
        p,b1 =self.sd_tester.send_request_and_recv_response(did,recv=resp)
        logger.info('a1={}'.format(b1))
        assert a1 == b1,  '数值存储异常'
    
    def read_did(self):
        with allure.step("进入默认会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
        with allure.step("电池DID-统计"):
            p,a =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD1],recv=[0x62,0x42,0xD1])
            logger.info('a={}'.format(a))
            DidFlag.a_did = a
            p,b =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCD],recv=[0x62,0x42,0xCD])
            logger.info('b={}'.format(b))  
            DidFlag.b_did = b
            p,c =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCF],recv=[0x62,0x42,0xCF])
            logger.info('c={}'.format(c)) 
            DidFlag.c_did = c
            p,d =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD7],recv=[0x62,0x40,0xD7])
            logger.info('d={}'.format(d)) 
            DidFlag.d_did = d
            p,e =self.sd_tester.send_request_and_recv_response([0x22,0x40,0x94],recv=[0x62,0x40,0x94])
            logger.info('e={}'.format(e))
            DidFlag.e_did = e
            p,f =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD2],recv=[0x62,0x42,0xD2])
            logger.info('f={}'.format(f))
            DidFlag.f_did = f
            self.mix.set_usage_mode(UsageMode.INACTIVE)
            self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
            
        with allure.step("仿真BMS信号"):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr08",'DcDcActvd',1)
            self.bus_comm.set_batturaw(BattURaw=15.0)
            self.bus_comm.set_battiraw(BattIRaw=2.0)
            self.bus_comm.set_battTraw(BattTRaw=40.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscFildLongRaw",-30.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04", 'BattRRaw', 1.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSOHLAMRaw",25.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03", 'BattCpEstimdRaw', 10)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03", 'BattIQuiscAvgRaw', -10.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr04", 'BattCircOpenU', 6.0)
            sleep(1)
            self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
            sleep(5)
            self.mix.set_usage_mode(UsageMode.ABANDONED)
            sleep(10)
            sleep(28800)
            self.mix.set_usage_mode(UsageMode.INACTIVE)
            sleep(60)
            DidFlag.read_did_flag = True
            

    @allure.title("DID_42D1_电池R阻值统计_BattRStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985563(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD1],recv=[0x62,0x42,0xD1])
            logger.info('a1={}'.format(a1))
            assert a1[-1] == DidFlag.a_did[-1]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD1],recv=[0x62,0x42,0xD1])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'

    @allure.title("DID_42CD_电池平均等效电流-统计_BattIAvgQuiscStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985560(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCD],recv=[0x62,0x42,0xCD])
            logger.info('a1={}'.format(a1))
            assert a1[-1] == DidFlag.b_did[-1]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCD],recv=[0x62,0x42,0xCD])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'
    
    @allure.title("DID_42CF_电池容量统计计数器_BattCpStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985557(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCF],recv=[0x62,0x42,0xCF])
            logger.info('a1={}'.format(a1))
            assert a1[-1] == DidFlag.c_did[-1]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xCF],recv=[0x62,0x42,0xCF])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'

    @allure.title("DID_40D7_电池静态电流-统计_BattIQuiscStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985559(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD7],recv=[0x62,0x40,0xD7])
            logger.info('a1={}'.format(a1))
            assert a1[8] == DidFlag.d_did[8]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0xD7],recv=[0x62,0x40,0xD7])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'

    @allure.title("DID_4094_电池充电状态统计计数器_BattSocStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985555(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0x94],recv=[0x62,0x40,0x94])
            logger.info('a1={}'.format(a1))
            assert a1[-1] == DidFlag.e_did[-1]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x40,0x94],recv=[0x62,0x40,0x94])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'

    @allure.title("DID_42D2_电池归一化内阻统计计数器_BattRNomStc")
    @pytest.mark.longtime
    @pytest.mark.nvm
    def test_HvActive_caseid_1985564(self):
        logger.info(f"========{DidFlag.read_did_flag}")
        if not DidFlag.read_did_flag:
            self.read_did()
            logger.info(f"--------------{DidFlag.read_did_flag}")
        with allure.step("电池DID-统计"):
            p,a1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD2],recv=[0x62,0x42,0xD2])
            logger.info('a1={}'.format(a1))
            assert a1[-1] == DidFlag.f_did[-1]+1, '数值累加异常'
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
            p,b1 =self.sd_tester.send_request_and_recv_response([0x22,0x42,0xD2],recv=[0x62,0x42,0xD2])
            logger.info('a1={}'.format(b1))
            assert a1 == b1, '休眠唤醒存储异常'

    

    