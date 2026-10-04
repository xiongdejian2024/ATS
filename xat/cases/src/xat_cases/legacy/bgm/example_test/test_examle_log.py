#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_exampl_log.py
@Time: 2023/02/04 08:00
@Author: lei.tao
@Software: PyCharm
@Description: example of how to use it
@Examples:
"""
import json
import os
import sys
import time

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH


class Test_example(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("Format test log example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46',
        name='logmanagement Case Example 1196965',
    )
    @pytest.mark.examplelog
    def test01(self):
        print("do small something")
        # 在非bgm或者tcam目录执行用例需要设置参数dev
        data1 = Logmagment(logger=logger).nonblocking_pattern_check(
            bgm_ip="172.16.5.1",
            dev='tcam',
            pattern="Interface change happen id",
            cmd="ifconfig rmnet_data2 down",
            timeout=10,
        )
        if data1:
            print("do something")
        # 重启
        # BGM_SSH("172.16.5.1").type_commands("reboot")
        # print("BGM重启")
        # # check2
        # data2 = Logmagment(logger=logger).nonblocking_pattern_check("172.16.5.1", pattern="m_timerWorkingList is empty", timeout=3)
        # if data2:
        #     print("do other something")


if __name__ == '__main__':
    pytest.main()
