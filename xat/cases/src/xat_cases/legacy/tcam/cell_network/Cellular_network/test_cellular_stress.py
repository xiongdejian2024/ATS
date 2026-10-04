#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_cellular_stress.py
@Time: 2023/09/21 19:10
@Author: yunpeng.zhou
@Software: VScode
@Description: 蜂窝网络测试用例
@Examples:
"""

import time
import allure
import pytest

from threading import *
# from ecu_simulator.interface.cdc.cdca_adb import CDCA_ADB
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM交付")
@allure.story("蜂窝网络压力测试")
class Test_Cellular_stress(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)


    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.ssh.set_cell_band(Cell_band.SA)
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1568579?projectId=46")
    @allure.title("5G网络拨号压力测试")
    def test_caseid_1980297(self):
        """
        触发5G网络重新拨号，拨号成功，APN ping成功
        """
        Thread(target=self.ssh.type_commands, args=(DeviceName.TCAM, "cd /oemapp/bin/;sleep 2;./trigger.sh cell deactive apn4;./trigger.sh cell deactive apn1", "timeout=5")).start()
        result = self.mix.chk_tcam_ping(8)
        assert len(result) == 0,f"5G网络重新拨号后，APN ping失败"

    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1568579?projectId=46")
    @allure.title("5G网络TCAM reboot注网压力测试")
    def test_caseid_1978456(self):
        """
        SA注网时间不超过4min，注网成功率100%
        """
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        sleep(80)
        with allure.step("TCAM重启后再次查看网络"):
            result = self.mix.chk_tcam_ping()
        assert len(result) == 0 , f"重启后驻网失败"
    
    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1567808?projectId=46")
    @allure.title("5G 飞行模式注网压力测试")
    def test_caseid_1978455(self):
        self.ssh.set_airplane_mode(isOn.On) #打开飞行模式
        sleep(5)
        result = self.mix.chk_tcam_ping()
        self.ssh.set_airplane_mode(isOn.Off) #关闭飞行模式
        sleep(5)
        result1 = self.mix.chk_tcam_ping()
        assert len(result) == 1,f"打开飞行后,不能上网"
        assert len(result1) ==0,f"关闭飞行后，可以上网"

    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1567808?projectId=46")
    @allure.title("4-5G 切换压力测试")
    def test_caseid_1978454(self):
        time.sleep(30)
        self.ssh.set_cell_band(Cell_band.LTE) #切4G
        result = self.mix.chk_tcam_ping()
        sleep(3)
        self.ssh.set_cell_band(Cell_band.SA) #切5G
        result1 = self.mix.chk_tcam_ping()
        assert len(result) == 0, f"切换4g后，不能上网"
        assert len(result1) ==0, f"切换5g后，不能上网"      

    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1567808?projectId=46")
    @allure.title("休眠唤醒压力测试")
    def test_caseid_100980(self):
        self.mix.network_sleep()
        sleep(10)
        self.mix.network_recover_bgm()
        result = self.mix.chk_tcam_ping()
        assert len(result) == 0,f"唤醒后，不能上网"
    
    @pytest.mark.longtime
    @pytest.mark.repeat(1)
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1567808?projectId=46")
    @allure.title("蜂窝网络与wifi压力测试")
    def test_caseid_1979205(self):
        cdc_devices = self.tb_config["adbdevice"]["cdc"]
        with allure.step("CDC连接可用wifi:"):
            os.popen(f"adb -s {cdc_devices} shell svc wifi enable")
            sleep(5)
            # os.popen(f"adb -s {cdc_devices} shell cmd wifi start-scan")
            # sleep(2)
            os.popen(f"adb -s {cdc_devices} shell cmd wifi connect-network JiDU-Guest wpa2 JiDU6666 -r none")
            sleep(10)

            # self.cdca_adb.adb_commands(f"adb -s {cdc_devices} shell svc wifi enable", timeout=5)
            # self.cdca_adb.adb_commands(f"adb -s {cdc_devices} shell cmd wifi start-scan", timeout=5)
            # self.cdca_adb.adb_commands(f"adb -s {cdc_devices} shell cmd wifi connect-network JiDU-Car open -h -r none", timeout=5)
            # os.open(f"adb -s {cdc_devices} shell svc wifi enable",f"adb -s {cdc_devices} shell cmd wifi start-scan",
            #                            f"adb -s {cdc_devices} shell cmd wifi connect-network JiDU-Car open -h -r none")
            wifi_route = self.ssh.type_commands(DeviceName.TCAM, "ip route")
            wifi_line = wifi_route.strip().splitlines()[0]
            assert "eth0.11" in wifi_line, f"连接wifi后，默认路由未切换至eth11"
            # self.mix.chk_tcam_ping(60)
        with allure.step("CDC关闭wifi:"):
            os.popen(f"adb -s {cdc_devices} shell svc wifi disable")
            sleep(10)
            route = self.ssh.type_commands(DeviceName.TCAM, "ip route")
            line = route.strip().splitlines()[0]
            assert "rmnet_data" in line, f"关闭wifi后，默认路由未切换至蜂窝路由"

    # 调试 pingdog reboot
    # @pytest.mark.full  
    # def test_caseid_000001(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL, veh_spd=70, vehmtnst=VehMtnSts.FwdVal2)
    #     sleep(900)


if __name__ == '__main__':
    pytest.main()
