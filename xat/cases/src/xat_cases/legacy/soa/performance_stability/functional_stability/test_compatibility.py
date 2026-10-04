#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#兼容性测试的case
#
#

import os
import sys
import time

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
import subprocess
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import DiagTestBase
from xat_ecu.legacy.driver.adb_client import Adb
from xat_cases.legacy.soa.case_helper.soa.pre_build import *


global a, b, c
# a为诊断上下电的次数，b为多域上下电的次数，c为进程重启后其他域的客户端服务端连接成功的次数
a = 3
b = 1
i = 1

@allure.feature("SOA中间件测试")
@allure.story("兼容性测试")
@pytest.mark.full
class Test_Power_up_down(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # 环境准备 只需要执行一次
        logger.info("环境准备")
        init_pre(self.nucapp)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        logger.info("检查磁盘剩余空间")
        init_disk()
      
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        reset_env()




# ============================== 四域上下电 case ===========================
    @pytest.mark.smoke
    @allure.title(f"四域同时上下电{b}次")
    def test_00_caseid_1892892_1892905(self):
        data=[
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "cdc",
                    "bgm",
                    "acu",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"四域同时上下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg

# ============================== 单域上下电 case ===========================

    @pytest.mark.sanity
    @allure.title(f"BGM上电后下电{b}次")
    def test_01_caseid_1892896_1892904(self):
        data=[
            {
                "poweroff": [
                    "bgm",
    
                ],
                "poweron": [
    
                     "bgm",
                     "sleep(60)"
    
                ],
                "times": b,
                "space": 6,
                "title": f"BGM上电后下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"TCAM上电后立马下电{b}次")
    def test_02_caseid_1892895_1892903(self):
        data = [
            {
                "poweroff": [
                    "tcam",

                ],
                "poweron": [
                    "tcam",
                    "sleep(300)"

                ],
                "times": b,
                "space": 6,
                "title": f"TCAM上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.sanity
    @allure.title(f"ACU上电后立马下电{b}次")
    def test_03_caseid_1892894_1892902(self):
        data = [
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    "sleep(0)",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"ACU上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.sanity
    @allure.title(f"CDC上电后立马下电{b}次")
    def test_04_caseid_1892893_1892901(self):
        data = [
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    "sleep(0)",
                    "cdc",
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.smoke
    @allure.title(f"四域依次休眠唤醒{i}次")
    def test05_caseid_1892900_1892909(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "bgm",
                    "tcam",
                    "sleep(0)"
                ],
                "times": i,
                "space": 6,
                "title": f"四域依次休眠唤醒{i}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU、BGM休眠唤醒{b}次")
    def test06_caseid_1892908_1892899(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "bgm",
                    "sleep(0)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU、BGM依次休眠唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU休眠唤醒{b}次")
    def test07_caseid_1892907_1892898(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "sleep(0)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU依次休眠唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC休眠唤醒{b}次")
    def test08_caseid_1892906_1892897(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "sleep(0)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC休眠唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg