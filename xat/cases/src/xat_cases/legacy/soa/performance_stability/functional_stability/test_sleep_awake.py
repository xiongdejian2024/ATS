#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#四域休眠唤醒case

import os
import sys
import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.soa.pre_build import init_pre,reset_env, start_awake, init_disk
from xat_ecu.legacy.interface.ecuinterface import *

global i, b
# i为四域休眠唤醒的次数，b为多域休眠唤醒的次数
i = 5
b = 1

@allure.feature("性能稳定性")
@allure.story("业务稳定性/休眠唤醒服务连接稳定性")
@pytest.mark.full
class Test_sleep_awake(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # 开始数据模拟（数据库周期性报文和调度表）
        self.ipdu.start_all_time_control()  
        # 开启can lin fr 驱动，开始在总线收发报文
        self.busapp.start_all_cyclic_msg()  
        # 环境准备 只需要执行一次
        # logger.info("关闭五门")
        # self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # self.dk.set_door_sts([0, 0, 0, 0, 0])
        # self.ipdu.set_vehspd(0.0)
        logger.info("环境准备")
        init_pre(nucapp=self.nucapp)
     
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        logger.info("检查磁盘剩余空间")
        init_disk()
      
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.ipdu.time_control_stop()  
        self.busapp.stop_all_cyclic_msgs() 
        # 删除 tcam中 推包文件，否则升级会导致tcam 挂死
        reset_env()
        logger.info("删除tcam中的推包文件")
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title(f"四域依次休眠唤醒{i}次")
    def test01_caseid_1892922(self):
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

    @pytest.mark.smoke
    @allure.title(f"CDC、ACU、BGM休眠唤醒{b}次")
    def test02_caseid_1892921(self):
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
    @allure.title(f"CDC、ACU、BGM休眠间隔5s唤醒{b}次")
    def test02_caseid_1892920(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "bgm",
                    "sleep(5)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU、BGM依次休眠间隔5s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU、BGM休眠间隔20s唤醒{b}次")
    def test02_caseid_1892919(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "bgm",
                    "sleep(20)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU、BGM依次休眠间隔20s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU、BGM休眠间隔60s唤醒{b}次")
    def test02_caseid_1892918(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "bgm",
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU、BGM依次休眠间隔60s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"CDC、ACU休眠唤醒{b}次")
    def test03_caseid_1892917(self):
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
    @allure.title(f"CDC、ACU休眠间隔5s唤醒{b}次")
    def test03_caseid_1892916(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "sleep(5)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU依次休眠间隔5s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU休眠间隔20s唤醒{b}次")
    def test03_caseid_1892915(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "sleep(20)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU依次休眠间隔20s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC、ACU休眠间隔60s唤醒{b}次")
    def test03_caseid_1892914(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "acu", 
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC、ACU依次休眠间隔60s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"CDC休眠唤醒{b}次")
    def test04_caseid_1892913(self):
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

    @pytest.mark.sanity
    @allure.title(f"CDC休眠间隔5s唤醒{b}次")
    def test04_caseid_1892912(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "sleep(5)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC休眠间隔5s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC休眠间隔20s唤醒{b}次")
    def test04_caseid_1892911(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "sleep(20)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC休眠间隔20s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"CDC休眠间隔60s唤醒{b}次")
    def test04_caseid_1892910(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC休眠间隔60s唤醒{b}次"
                }
        ]
        ret,msg=start_awake(data, self.tc_config, self.ipdu, self.nucapp)
        logger.info(msg)
        assert ret,msg


# @allure.feature("性能稳定性")
# @allure.story("业务稳定性/休眠唤醒服务连接稳定性")
# @pytest.mark.full
# class Test_sleep_awake1(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         # 开始数据模拟（数据库周期性报文和调度表）
#         self.ipdu.start_all_time_control()  
#         # 开启can lin fr 驱动，开始在总线收发报文
#         self.busapp.start_all_cyclic_msg()  
#         # 环境准备 只需要执行一次
#         logger.info("环境准备")
#         init_pre(nucapp=self.nucapp)
     
#     def before_each_func(self, ecu):
#         super().before_each_func(ecu, start=False)
#         logger.info("检查磁盘剩余空间")
#         init_disk()
      
#     def after_each_func(self, ecu):
#         super().after_each_func(ecu, start=False)

#     def after_class(self, ecu):
#         self.ipdu.time_control_stop()  
#         self.busapp.stop_all_cyclic_msgs() 
#         # 删除 tcam中 推包文件，否则升级会导致tcam 挂死
#         reset_env()
#         logger.info("删除tcam中的推包文件")
#         super().after_class(self, ecu)