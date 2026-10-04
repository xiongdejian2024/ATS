# -*- coding: utf-8 -*-
"""
@File        : test_can_lin_fr_signal_route.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/11/22 11:36
@Description :

"""

import os
import sys
import time

import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.sdk.sdk_tools import *


@allure.feature("MCU 基础平台/MCU性能")
@allure.story("业务性能/车辆公告发出时长")
class TestVehicleAnnouncementTime(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.first_veh_ann_time = None
        self.iface = self.tc_config['bus']['eth_obd']  # 'enp114s0'

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @pytest.mark.full
    @pytest.mark.sanity
    def test_app_mode_send_func_1181_caseid_1984468(self):
        """
        APPMode下_功能寻址_1181重启后车辆公告发出时长
        """
        self.mix.get_veh_ann_time_under_app_mode_send_func_1181(self.iface)


    @pytest.mark.smoke
    @pytest.mark.full
    @pytest.mark.sanity
    def test_app_mode_send_func_1082_caseid_1984469(self):
        """
        APPMode下_功能寻址_1082重启后车辆公告发出时长
        """
        self.mix.get_veh_ann_time_under_app_mode_send_func_1082(self.iface)


    @pytest.mark.smoke
    @pytest.mark.full
    @pytest.mark.sanity
    def test_boot_mode_send_func_1181_caseid_1984470(self):
        """
        BootMode下_功能寻址_1181重启后车后车辆公告发出时长
        """
        self.mix.get_veh_ann_time_under_boot_mode_send_func_1181(self.iface)
# pytest mcu_performance/business_performance/vehicle_ann_duration/test_vehicleAnnouncement.py
