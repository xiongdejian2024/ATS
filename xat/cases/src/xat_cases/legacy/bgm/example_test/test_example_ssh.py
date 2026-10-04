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
import os
import sys

import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH


class Test_example(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bgm_ssh = BGM_SSH()
        self.tcam_ssh = TCAM_SSH()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("测试BGM重启")
    @pytest.mark.CI
    def test_bgm_reconnect(self):
        self.bgm_ssh.type_commands('uname')
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        time.sleep(10)
        assert self.bgm_ssh.type_commands('ls -la')

    @allure.title("测试TCAM重启")
    @pytest.mark.CI
    def test_tcam_reconnect(self):
        self.tcam_ssh.type_commands('uname')
        self.nucapp.tcam_power_off()
        self.nucapp.tcam_power_on()
        assert self.tcam_ssh.type_commands('ls -la')

    @allure.title("检查单个关键字")
    @pytest.mark.CI
    def test_log_single_keywords(self):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type='SSIG:',
            keywords=':',
            timeout=5
        )
        status, ret = self.log_manage.check_log_by_keywords_stop_thread()
        assert status

    @allure.title("检查多个关键字")
    @pytest.mark.CI
    def test_log_multi_keywords(self):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type='SSIG:',
            keywords=['can', 'fr'],
            timeout=5
        )
        status, ret = self.log_manage.check_log_by_keywords_stop_thread()
        assert status

    @allure.title("检查单个不期望的关键字")
    @pytest.mark.CI
    def test_log_single_unexpect_keywords(self):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type='SSIG:',
            unexpect_keywords='xdj',
            timeout=5
        )
        status, ret = self.log_manage.check_log_by_keywords_stop_thread()
        assert status

    @allure.title("检查多个不期望的关键字")
    @pytest.mark.CI
    def test_log_multi_unexpect_keywords(self):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type='SSIG:',
            unexpect_keywords=['xdj1', 'xdj'],
            timeout=5
        )
        status, ret = self.log_manage.check_log_by_keywords_stop_thread()
        assert status

    @allure.title("压测异步获取log的线程-BGM涉及重启")
    @pytest.mark.CI_stress
    @pytest.mark.repeat(100)
    def test_record_log(self):
        self.bgm_ssh.type_commands('ls')
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        self.bgm_ssh.type_commands('ls')

    @pytest.mark.repeat(2)
    def test_tcam_bug(self):
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        sleep(10)
        self.tcam_ssh.get_log(connect_type='obd')

    @pytest.mark.repeat(2)
    def test_tcam_ssh_bug(self):
        self.tcam_ssh.type_commands(commands='ls', connect_type='obd')
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        sleep(10)
        self.nucapp.tcam_kl15_down()
        sleep(60)
        self.nucapp.tcam_kl15_up()
        self.tcam_ssh.type_commands(commands='pwd', connect_type='obd', alias='1')


if __name__ == '__main__':
    pytest.main()
