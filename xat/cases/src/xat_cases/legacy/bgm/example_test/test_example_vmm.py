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
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig


class Test_Change_Usage_Car_Mode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path).yaml_content

        self.sd_test = Sd_Tester(**tb_config)
        self.sd_test.diagnostic_client_sim_start()
        time.sleep(0.5)
        self.sd_test.tester_present()
        time.sleep(0.5)
        self.sd_test.update_serverdoipid(0x1002)

        # todo 一定要发送这个报文，fr报文

        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_ukwn()
        sleep(1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，总线开始收发报文
        time.sleep(0.5)
        self.sd_test.stop_tester_present()
        time.sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()

    def test_change_car_mode_func(self):
        self.change_car_mode1()

    def change_car_mode1(
        self,
    ):
        '''
        Test related example, Show the format
        '''
        # todo 能切成功
        self.ipdu.set_vehspd()
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        sleep(5)
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()

        curr_mode = self.sd_test.change_usage_mode(0, do_assert=1)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )

        curr_mode = self.sd_test.change_usage_mode(1, do_assert=1)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )

        curr_mode = self.sd_test.change_usage_mode(2, do_assert=1)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )

        time.sleep(2)
        curr_mode = self.sd_test.change_usage_mode(11, do_assert=1)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )

        time.sleep(2)
        curr_mode = self.sd_test.change_usage_mode(13, do_assert=1)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )

        # todo 不能切成功
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        sleep(2)
        curr_mode = self.sd_test.change_usage_mode(0, do_assert=0)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )
        assert not curr_mode == 0, "不应该切成功 切成功了"

        curr_mode = self.sd_test.change_usage_mode(1, do_assert=0)
        logger.info(
            f"====curr_mode================ {curr_mode} =========================="
        )
        assert not curr_mode == 1, "不应该切成功 切成功了"


# cd /root/sat/xat_cases/legacy/bgm

#  pytest flash/test_change_mode_demo.py
