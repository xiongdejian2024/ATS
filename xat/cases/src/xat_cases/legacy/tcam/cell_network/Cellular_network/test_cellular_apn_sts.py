#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_cellular_network.py
@Time: 2023/11/17 10:21
@Author: yunpeng.zhou
@Software: Vscode
@Description: 蜂窝网络测试用例
@Examples:
"""
import inspect
import os
import sys
import time
import allure
import pytest

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("联网服务")
class Test_Cellular_network(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehspd_gear()
        sleep(1)

    def after_each_func(self, ecu):
        self.tsp.mno_setAPNsts()
        self.mix.set_tcam_bgm_to_wakeup()
        # self.sd_tester.start_sd_tester()
        sleep(10)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    
    @pytest.mark.join_sanity
    @allure.title("normal_云端下发")
    def test_caseid_1985706(self):
        self.tsp.mno_setAPNsts(APN4sts=0)
        self.tsp.mno_log_search()
        ping_result=self.ssh.tcam_ping_net(rmnet_data="rmnet_data1", ping_time=5)
        assert "Network is unreachable" in ping_result,f"云端关闭apn4后，仍能ping通网络"
        sleep(10)
        self.tsp.mno_setAPNsts()
        self.tsp.mno_log_search()
        self.mix.chk_tcam_ping()

    @pytest.mark.join_full
    @allure.title("standby后_云端下发")
    def test_caseid_1985705(self):
        with allure.step("TCAM进入休眠后关闭再打开apn4:"):
            self.mix.network_sleep()
            sleep(60)
            self.tsp.mno_setAPNsts(APN4sts=0)
            self.tsp.mno_log_search()
            sleep(5)
            self.tsp.mno_setAPNsts()
        self.mix.set_tcam_bgm_to_wakeup()
        self.mix.chk_tcam_ping()

    @pytest.mark.join_full
    @allure.title("standby前_云端下发")
    def test_caseid_1985704(self):
        with allure.step("云端关闭apn4:"):
            self.tsp.mno_setAPNsts(APN4sts=0)
            self.tsp.mno_log_search()
            ping_result=self.ssh.tcam_ping_net(rmnet_data="rmnet_data1",ping_time=5)
            assert "Network is unreachable" in ping_result,f"云端关闭apn4后，仍能ping通网络"
        with allure.step("TCAM进入休眠后打开apn4:"):
            self.mix.network_sleep()
            sleep(60)
            self.tsp.mno_setAPNsts()
        self.mix.set_tcam_bgm_to_wakeup()
        self.mix.chk_tcam_ping()

    @pytest.mark.join_smoke
    @allure.title("APN4状态车端主动请求")
    def test_caseid_1985701(self):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=10)
        sleep(80)
        self.tsp.mno_log_search(search_time=60, fuzz_match="车端主动获取开关状态", detail="apnStatus", keywords="OPEN")
    
    @pytest.mark.join_sanity
    @allure.title("APN4状态车端同步无异常")
    def test_caseid_1985700(self):
        with allure.step("云端关闭apn4:"):
            self.tsp.mno_setAPNsts(APN4sts=0)
            self.tsp.mno_log_search() 
        with allure.step("设置车辆driving,检查tcam是否重启"): 
            self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, veh_spd=70)
            self.mix.chk_tcam_reboot_or_not()

    @pytest.mark.join_sanity
    @allure.title("standby中_云端下发")
    def test_caseid_1985703(self):
        with allure.step("TCAM进入休眠后关闭apn4:"):
            self.mix.set_common_precontion()
            self.mix.network_sleep()
            sleep(10)
            self.tsp.mno_setAPNsts(APN4sts=0)
        with allure.step("唤醒TCAM,检查apn4网络:"):
            self.mix.network_recover_bgm()
            ping_result=self.ssh.tcam_ping_net(rmnet_data="rmnet_data1", ping_time=5)
            assert "Network is unreachable" in ping_result,f"云端关闭apn4后，仍能ping通网络"

    
    # 调试
    # @pytest.mark.join_full
    # def test_caseid_11111111(self):
    #     self.tsp.mno_setAPNsts()
    #     self.tsp.mno_log_search()



if __name__ == '__main__':
    pytest.main()

# pytest -vs -p no:warnings Cellular_network/test_cellular_network.py -k test_caseid_1568423