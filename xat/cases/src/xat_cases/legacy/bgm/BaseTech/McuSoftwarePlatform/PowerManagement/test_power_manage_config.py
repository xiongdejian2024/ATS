# -*- coding: utf-8 -*-
"""
@File        : test_power_management.py
@Author      : 
@Time        : 2023/08/28 20:46 PM
@Description : 电源管理测试
@Examples    : example of how to use it

MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
reset MPU times 的消息 3次 (可标定) 0-5
退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10

"""
import copy
import os
import random
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


@allure.feature("BGM BaseTech/MCU软件平台")
@allure.story("电源管理/did")
@pytest.mark.first
class TestBgmPowerManageDid(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.update_serverdoipid(0x1002)



    def before_each_func(self, ecu):
        self.write_f0f5_default_value()
        pass

    def after_each_func(self, ecu):
        self.write_f0f5_default_value()

    def after_class(self, ecu):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.io.tcam_power_on()

    def write_f0f5_default_value(self):
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("恢复默认配置 0x2E, 0xF0, 0xF5, 0X28, 0X0A, 0X03, 0X05, 0X03, 0X02")
        w_data = [0X28, 0X0A, 0X03, 0X05, 0X03, 0X02]
        ret, msg = self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5])
        if msg == [0x62, 0xF0, 0xF5] + w_data:
            return
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5] + w_data,
                                                      recv=[0x6E, 0xF0, 0xF5])
        self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5],
                                                      recv=[0x62, 0xF0, 0xF5] + w_data)

    def check_f0f5_default_value(self):
        self.sd_tester.update_serverdoipid(0x1002)
        with allure.step("读取电源管理补电常数"):
            self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5],
                                                          recv=[0x62, 0xF0, 0xF5, 0X28, 0X0A, 0X03, 0X05, 0X03, 0X02])

    @allure.title("BGM_台架_配置_默认配置读取")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109478?projectId=46'
    )
    @pytest.mark.smoke
    def test_power_config_caseid_1919252(self):
        with allure.step("进入默认会话"):
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.check_f0f5_default_value()

    def write_f0f5_data(self, index: int, data_min: int, data_max: int):
        '''

        @param index:  取值范围 为 1,2 3,4,5,6
        @param data_min:
        @param data_max:
        @return:
        '''
        if not 1 <= index <= 6:
            assert 0, "index 的范围为 1-6"
        # 默认值
        data_value = copy.deepcopy([0x2E, 0xF0, 0xF5, 0X28, 0X0A, 0X03, 0X05, 0X03, 0X02])
        check_value = copy.deepcopy([0x62, 0xF0, 0xF5, 0X28, 0X0A, 0X03, 0X05, 0X03, 0X02])
        # 加上 did
        index = 2 + index
        self.sd_tester.update_serverdoipid(0x1002)
        # 读取下did
        self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5])
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("写入非法 app启动时间测试"):
            if data_min - 1 >= 0:
                data_value[index] = data_min - 1
                logger.info(f"写入随机的非法的最小时间{data_value[index]}")
                self.sd_tester.send_request_and_recv_response(data_value, recv=[0x7F])
            if data_max + 1 <= 0xff:
                data_value[index] = data_max + 1
                logger.info(f"写入随机的非法的时间2{data_value[index]}")
                self.sd_tester.send_request_and_recv_response(data_value, recv=[0x7F])

            data0 = random.randint(data_max + 2, 0xff)
            data_value[index] = data0
            logger.info(f"写入随机的非法的时间参数3{data0}")
            self.sd_tester.send_request_and_recv_response(data_value, recv=[0x7F])

        with allure.step(f"写入测试最小值{data_min} "):
            data_value[index] = data_min
            check_value[index] = data_min
            logger.info(f"写入正常的正常最小值{data_min}")
            self.sd_tester.send_request_and_recv_response(data_value, recv=[0x6E, 0xF0, 0xF5])
            self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5], recv=check_value)

        with allure.step(f"写入测试最大值{data_max} "):
            data_value[index] = data_max
            check_value[index] = data_max
            logger.info(f"写入正常的正常最大值{data_max}")
            self.sd_tester.send_request_and_recv_response(data_value, recv=[0x6E, 0xF0, 0xF5])
            self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5], recv=check_value)

        data0 = random.randint(data_min, data_max)
        with allure.step(f"写入正常随机值{data0} "):
            data_value[index] = data0
            check_value[index] = data0
            logger.info(f"写入正常的正常随机值{data0}")
            self.sd_tester.send_request_and_recv_response(data_value, recv=[0x6E, 0xF0, 0xF5])
            self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5], recv=check_value)
        # 恢复默认值
        self.write_f0f5_default_value()

    def get_info_time(self, log_msg: str, info_lis: list):
        '''
        获取 内容 对应的时间
        @param log_msg:
        @param info_lis:
        @return: {string :(time,string)}
        '''
        string_list = log_msg.split("\n")
        value_dict = {}
        for item in string_list[1:]:
            if not item.strip():
                continue
            # 2024-09-10 16:50:10.368
            time_string = item[:23]
            value_string = item.split("]:")[-1]
            time_list = time_string.split(".")
            t1 = time_list[0]
            t2 = time_list[1]
            # 将字符串转换为datetime对象
            dt_obj = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
            # 将datetime对象转换为时间戳
            timestamp = int(time.mktime(dt_obj.timetuple())) * 1000 + int(t2)

            for info in info_lis:
                if info in value_string:
                    value_dict[info] = (timestamp, item)
        print("value_dict", value_dict)
        logger.info(f"value_dict={value_dict}")
        return value_dict

    @allure.title("BGM_台架_配置_timer for wait boot complete 修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919253(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-0X40  默认40秒
        @return:
        '''
        self.write_f0f5_data(index=1, data_min=0, data_max=0x40)
        # 重启
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(50)
        self.sd_tester.sd_tester.reset_positive_ack()
        self.check_f0f5_default_value()
        info_lis = ["PowerManager", "successful to send BootCompleted"]
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        ret_dict = self.get_info_time(sleep_log_last, info_lis)
        temp = ret_dict[info_lis[1]][0] - ret_dict[info_lis[0]][0]
        logger.info(f"temp={temp}毫秒")
        assert temp <= 40 * 1000, "MPU进程全部启动后 通知MCU boot complete 的等待时间大于40s"

    @allure.title("BGM_台架_配置_timer for wait sleep ready 时间修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919254(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
        APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
        进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

        APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
        reset MPU times 的消息 3次 (可标定) 0-5
        退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10
        @return:
        '''
        self.write_f0f5_data(index=2, data_min=0, data_max=0x20)
        # 重启
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(50)
        self.check_f0f5_default_value()
        info_lis = ["Received shutdown prepare!!"]
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        ret_dict = self.get_info_time(sleep_log_last, info_lis)
        # 防止只打印一个
        info_lis2 = ["mpu send shutdown ready succeed", "Received shutdown2 response with nullptr"]
        ret_dict2 = self.get_info_time(sleep_log_last, info_lis2)
        t2 = ret_dict2.get(info_lis2[0])[0] if ret_dict2.get(info_lis2[0], None) else ret_dict2.get(info_lis2[1])[0]

        temp = t2 - ret_dict[info_lis[0]][0]
        logger.info(f"temp={temp}毫秒")
        assert temp <= 10 * 1000, "APP模式下 MCU 最多等待shutdown ready 的消息 10s"

    @allure.title("BGM_台架_配置_Timer for wait sleep ready going to boot 时间修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919255(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
        APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
        进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

        APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
        reset MPU times 的消息 3次 (可标定) 0-5
        退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10
        @return:
        '''
        self.mix.init_boot_per()
        self.write_f0f5_data(index=3, data_min=0, data_max=0x10)
        # 重启
        try:
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.sd_tester.send_data([0x10, 0x82])
            sleep(10)
            self.sd_tester.sd_tester.reset_positive_ack()
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86])
            sleep(45)
            info_lis = ["Received shutdown prepare!!"]
            sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
            ret_dict = self.get_info_time(sleep_log_last, info_lis)

            # 防止只打印一个
            info_lis2 = ["mpu send shutdown ready succeed", "Received shutdown2 response with nullptr"]
            ret_dict2 = self.get_info_time(sleep_log_last, info_lis2)
            t2 = ret_dict2.get(info_lis2[0])[0] if ret_dict2.get(info_lis2[0], None) else ret_dict2.get(info_lis2[1])[0]

            temp = t2 - ret_dict[info_lis[0]][0]
            logger.info(f"temp={temp}毫秒")
            assert temp <= 3 * 1000, "boot MCU 等待 shutdown ready 的时间为 3s（可标定）"
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.sd_tester.send_data([0x10, 0x01])
            sleep(20)
        except Exception as e:
            logger.error(f"{str(e)}")
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.sd_tester.send_data([0x10, 0x01])
            sleep(20)
            assert 0, str(e)

    @allure.title("BGM_台架_配置_timer for wait PGOOD 时间修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919256(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
        APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
        进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

        APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
        reset MPU times 的消息 3次 (可标定) 0-5
        退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10
        @return:
        '''
        self.write_f0f5_data(index=4, data_min=0, data_max=0x10)
        # 重启
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(20)
        self.sd_tester.sd_tester.reset_positive_ack()
        self.check_f0f5_default_value()

    @allure.title("BGM_台架_配置_reset MPU times 修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919257(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
        APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
        进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

        APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
        reset MPU times 的消息 3次 (可标定) 0-5
        退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10
        @return:
        '''
        self.write_f0f5_data(index=5, data_min=0, data_max=0x5)
        # 重启
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(20)
        self.sd_tester.sd_tester.reset_positive_ack()
        self.check_f0f5_default_value()

    @allure.title("BGM_台架_配置_timer for wait PGOOD in boot 修改验证")
    @pytest.mark.smoke
    def test_power_config_caseid_1919258(self):
        '''
        MPU进程全部启动后 通知MCU boot complete 的等待时间为40s(可标定) 1-40
        APP模式下 MCU 最多等待shutdown ready 的消息 10s (可标定) 0-20
        进BOOT下 MCU 最多等待shutdown ready 的消息 3s (可标定) 0-10

        APP模式下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时5s（可标定）0-10
        reset MPU times 的消息 3次 (可标定) 0-5
        退BOOT下 MCU检查 hw pin PGOOD，检测到pin 变低, 超时2s（可标定）0-10
        @return:
        '''
        self.write_f0f5_data(index=6, data_min=0, data_max=0x10)
        # 重启
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(20)
        self.sd_tester.sd_tester.reset_positive_ack()
        self.check_f0f5_default_value()

# pytest BaseTech/McuSoftwarePlatform/PowerManagement/test_power_manage_config2.py --disable_env=true -k 111214
