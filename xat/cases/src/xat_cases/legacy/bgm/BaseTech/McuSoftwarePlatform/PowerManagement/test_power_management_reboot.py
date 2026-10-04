#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车方向盘功能
"""

import os
import sys
import threading
import time

import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from datetime import datetime


@allure.feature("电源管理")
@allure.story("电源管理测试")
@pytest.mark.first
class TestBgmPowerManagementReboot(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.io.tcam_power_off()

    def before_each_func(self, ecu):
        self.sd_tester.sd_tester.tester_present()
        pass

    def after_each_func(self, ecu):
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.io.tcam_power_on()

    def check_keyinfo(self, log_data, key_word, **kwargs):

        if log_data.find(key_word) != -1:
            string = f"查询到关键信息：{key_word}"
            with allure.step(string):
                logger.info(string)
        else:
            string = f"未能查询到关键信息：{key_word}"
            with allure.step(string):
                logger.error(string)
            assert False, string

    @allure.title(f"BGM_boot会话_MCU工作状态boot")
    @pytest.mark.sanity
    def test_pm_reboot_caseid_1919219(self):
        try:
            self.mix.init_boot_per()
            # 3. 四门两盖关闭
            logger.info("关闭四门两盖")
            self.io.set_five_door_sts(Door.close)
            self.io.set_hood_sts(HoodSts.Close)
            # 四门两盖是否关闭
            self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
            self.sd_tester.update_serverdoipid(0x1002)
            temp = time.time()
            self.sd_tester.enter_boot()
            sleep(10)  # 等日志落盘
            # SOC_SFGPIO_3 value: 1, MCU be in  boot mode.
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "MCU be in  boot mode" in sleep_log_last
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)

    @allure.title(f"BGM_台架_BOOT_MPU_进入发送1082")
    @pytest.mark.full
    def test_pm_reboot_caseid_111261(self):

        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x01])
        self.sd_tester.send_data([0x10, 0x82])
        sleep(2)
        t = time.time()
        self.sd_tester.sd_tester.reset_positive_ack()
        self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x02])
        # 重启的话 bgm需要15秒左右才能起来，诊断不会立马响应
        assert time.time() - t < 3

    @allure.title(f"BGM_台架_BOOT_MPU_进入发送1002")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919221(self):

        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x01])
        self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
        sleep(2)
        t = time.time()
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        # 重启的话 bgm需要15秒左右才能起来，诊断不会立马响应
        assert time.time() - t < 3

    @allure.title(f"BGM_台架_BOOT_MCU_退出发送1001")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919248(self):
        try:
            self.mix.init_boot_per()
            # 3. 四门两盖关闭
            logger.info("关闭四门两盖")
            self.io.set_five_door_sts(Door.close)
            self.io.set_hood_sts(HoodSts.Close)
            # 四门两盖是否关闭
            self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.enter_boot()
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
            sleep(20)  # 等退boot
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x01])
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)

    @allure.title(f"BGM_boot会话_MCU-MPU 仅支持DoIP 通讯")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919251(self):
        try:
            self.mix.init_boot_per()
            # 3. 四门两盖关闭
            logger.info("关闭四门两盖")
            self.io.set_five_door_sts(Door.close)
            self.io.set_hood_sts(HoodSts.Close)
            # 四门两盖是否关闭
            self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.enter_boot()
            self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X86], recv=[0x62, 0xF1, 0X86, 0x02])
            sleep(35)  # 等待日志落盘
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "sent heart beat to mcu" not in awakeup_log_last
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)

    @allure.title(f"BGM_重启原因_正常休眠唤醒")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919269(self):

        self.mix.network_sleep()
        with allure.step(f"诊断激活线唤醒"):
            logger.info(
                f"{Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE.name} 唤醒源{Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE.value}")
            self.io.bgm_diag_line_up()
            sleep(35)  # 等待日志落盘
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "Received power mode: 2, wakeup reason: 22, reboot reason: 0" not in awakeup_log_last

    @allure.title(f"BGM_重启原因_MCU请求重启")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919266(self):

        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(40)  # 等待日志落盘
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "power mode: 1 PowerOFF" in sleep_log_last and "reboot reason: 1" in sleep_log_last

        assert "reboot reason: 1" in awakeup_log_last and "Received power mode: 2" in awakeup_log_last

    @allure.title(f"BGM_重启原因_MPU请求重启")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919265(self):

        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(40)  # 等待日志落盘
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "power mode: 1 PowerOFF" in sleep_log_last

        assert "reboot reason: 2" in awakeup_log_last or "reboot reason: 1" in awakeup_log_last

    @allure.title(f"BGM_重启原因_MPU异常重启")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919267(self):

        self.ssh.type_commands(DeviceName.BGM, "shutdown -h",timeout=2)
        sleep(40)  # 等待日志落盘
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 4" in awakeup_log_last

    @allure.title("Check:MCU_重启发送1101 ")
    @pytest.mark.sanity
    def test_pm_reboot_caseid_111248(self):
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x11, 0x01], recv=[0x51, 0x01])
        sleep(40)# 等待日志落盘

        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last


    @allure.title("Check:MCU_重启发送1181 ")
    @pytest.mark.sanity
    def test_pm_reboot_caseid_111245(self):
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.sd_tester.send_data([0x11, 0x81])
        sleep(40)# 等待日志落盘
        self.sd_tester.sd_tester.reset_positive_ack()
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last

    @allure.title("Check:MPU_重启发送1101 ")
    @pytest.mark.sanity
    def test_pm_reboot_caseid_111255(self):

        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x11, 0x01], recv=[0x51, 0x01])
        sleep(40)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last or "reboot reason: 2" in awakeup_log_last

    @allure.title("Check:MPU_重启发送1181 ")
    @pytest.mark.sanity
    def test_pm_reboot_caseid_111226(self):
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.sd_tester.send_data([0x11, 0x81])
        sleep(50)
        self.sd_tester.sd_tester.reset_positive_ack()
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last or "reboot reason: 2" in awakeup_log_last

    @allure.title("BGM_台架_BOOT_MCU_进入shutdown ready等待3s")
    @pytest.mark.smoke
    def test_pm_reboot_caseid_1919249(self):

        try:
            self.mix.init_boot_per()
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
            sleep(10)
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x02])
            sleep(45)
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "Received shutdown prepare" in sleep_log_last
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)

    @allure.title("BGM_台架_BOOT_MCU_退出hw pin PGOOD等待2s")
    @pytest.mark.smoke
    def test_pm_reboot_caseid_1919250(self):

        try:
            self.mix.init_boot_per()
            # 3. 四门两盖关闭
            logger.info("关闭四门两盖")
            self.io.set_five_door_sts(Door.close)
            self.io.set_hood_sts(HoodSts.Close)
            # 四门两盖是否关闭
            self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
            sleep(10)
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x02])
            sleep(40)
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "Received shutdown prepare" in sleep_log_last
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)

    @allure.title("BGM_台架_BOOT_MCU_进入发送1082")
    @pytest.mark.smoke
    def test_pm_reboot_caseid_111258(self):
        try:
            self.mix.init_boot_per()
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_data([0x10, 0x82])
            sleep(10)
            self.sd_tester.sd_tester.reset_positive_ack()
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x02])
            sleep(40)
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "Received shutdown prepare" in sleep_log_last
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)


    @allure.title(f"BGM_台架_BOOT_MCU_退出发送1001")
    @pytest.mark.full
    def test_pm_reboot_caseid_1919220(self):
        try:
            self.mix.init_boot_per()
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
            sleep(10)
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x02])
            sleep(40)  # 等待日志落盘
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            assert "MCU be in  boot mode" in awakeup_log_last
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
            sleep(30)  # 等退boot
            self.ssh.read_bgm_jetlog()
            self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86, 0x01])
        except Exception as e:
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.quit_boot()
            assert 0, str(e)


#pytest BaseTech/McuSoftwarePlatform/PowerManagement/test_power_management_reboot2.py --disable_env=true -k 111214