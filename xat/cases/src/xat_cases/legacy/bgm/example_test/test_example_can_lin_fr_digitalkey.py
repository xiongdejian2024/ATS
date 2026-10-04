# -*- coding: utf-8 -*-
"""
@File        : test_example_can_lin_fr.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023/01/10 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey


@allure.feature("Example Cases")
@allure.story("Test Example can lin fr Set")
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        sleep(10)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    @allure.title("Format test can lin example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46',
        name='Can_Lin Case Example 1196965',
    )
    @pytest.mark.examplekey
    def test_format_example_can_lin_caseid_1196965(self):
        '''
        Test related example, Show the format
        '''
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr07")
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr08")
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr16")
        sleep(2)
        self.test_a = DigitalKey(self.ipdu, self.busapp, self.nucapp, self.tc_config)

        # i = 0
        # while i < 200:
        #     self.test_a.send_rke_lock()
        #     i += 1

        # self.test_a.set_cenlock_sts(0x1)
        # self.set_usage_mode(0x1)
        time.sleep(1)
        self.test_a.send_rke_lock()
        try:
            self.test_a.ck_four_door_lock_cmd(2)
        except Exception:
            pass
        time.sleep(2)

        self.ipdu.remove_preheating("connectivitycanfd", "BncmConnectivityFr07")
        self.ipdu.remove_preheating("connectivitycanfd", "BncmConnectivityFr08")
        self.ipdu.remove_preheating("connectivitycanfd", "BncmConnectivityFr16")
