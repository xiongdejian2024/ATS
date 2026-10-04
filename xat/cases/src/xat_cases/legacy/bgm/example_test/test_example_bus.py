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
from xat_ecu.legacy.sdk.bus_app import BusApp

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

    @allure.title("压测CAN的启动和停止")
    @pytest.mark.CI_stress
    @pytest.mark.repeat(3000)
    def test_can_lin(self):
        self.busapp = BusApp(self.ipdu, **self.tc_config)
        logger.info("===========    启动 can 总线    ==============")
        self.busapp.start_all_cyclic_msg()

        logger.info("===========    停止 can 总线     ==============")
        self.busapp.stop_all_cyclic_msgs()
        del self.busapp


if __name__ == '__main__':
    pytest.main()
