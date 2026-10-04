#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_time_manage.py
@Time: 2023/06/01 12:00
@Author: lei.tao
@Software: PyCharm
@Description: 时间管理测试用例
@Examples:
"""

import os
import sys
import threading
import time
import json
from datetime import datetime

import allure
import pytest
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import send_can_wake_data

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase




@allure.story("BGM台架的时间管理模块验证")
class Test_Time_manage(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("case开始运行*******************************************************")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("case结束运行*******************************************************")
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

        
    @pytest.mark.full
    @allure.title("查看ConnectivityCANFD上VehTiAndData时间_无效时间")
    def test_caseid_1987710(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        #监控connectivitycanfd
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)    


    @pytest.mark.sanity
    @allure.title("诊断复位BGM场景验证时间同步")
    def test_caseid_1987711(self):
        with allure.step("发送BGM诊断复位命令"):
            self.sd_tester.send_data_and_check(0x1002, '1002', '5002')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.TCAM, 2)
        with allure.step("恢复测试环境"):
            self.sd_tester.send_data_and_check(0x1002, '1001', '5001')
        time.sleep(15)

    @pytest.mark.sanity
    @allure.title("诊断复位TCAM场景验证时间同步")
    def test_caseid_1987707(self):
        with allure.step("发送TCAM诊断复位命令"):
            self.sd_tester.send_data_and_check(0x1011, '1003', '5003')
            self.sd_tester.send_data_and_check(0x1011, '1103', '5103')
        time.sleep(200)
        self.ssh.verify_time_synchronization(DeviceName.TCAM, 2)

    @pytest.mark.smoke
    @allure.title("验证TCAM时间是否同步")
    def test_caseid_100260(self):
        self.ssh.verify_time_synchronization(DeviceName.TCAM, 2)


    @pytest.mark.full
    @allure.title("查看ConnectivityCANFD上VehTiAndData时间_有效时间")
    def test_caseid_1987709(self):
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "BgmConnectivityFr04": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["BgmConnectivityFr04"]["VehTiAndDataYr1"]
            month = result_dict["BgmConnectivityFr04"]["VehTiAndDataMth1"]
            day = result_dict["BgmConnectivityFr04"]["VehTiAndDataDay"]
            hour = result_dict["BgmConnectivityFr04"]["VehTiAndDataHr1"]
            minite = result_dict["BgmConnectivityFr04"]["VehTiAndDataMins1"]
            second = result_dict["BgmConnectivityFr04"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl


    @pytest.mark.full
    @allure.title("查看ConnectivityCANFD上CarTiGib时间_无效时间")
    def test_caseid_19887713(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "VgmConnFr12": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["VgmConnFr12"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.full
    @allure.title("查看ConnectivityCANFD上CarTiGib时间_有效时间")
    def test_caseid_1987708(self):
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "VgmConnFr12": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["VgmConnFr12"]["CarTiGlb"]
        rsl = True if period <= 2 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过2秒")
            assert rsl
