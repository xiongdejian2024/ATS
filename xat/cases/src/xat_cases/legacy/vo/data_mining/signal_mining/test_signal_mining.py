#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure

from xat_ecu.api.interfaces.dp1.buscomm import BusComm

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interface import *
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.api.common.common import get_signals_info_and_send_with_time
from xat_ecu.api.call_tracker import BaseABCMeta
from framework.automotive.utils.bench_helper import BenchHelper
from xat_ecu.api.call_tracker import ObjExecutor
import datetime


def send_signal_and_get_time(excel_path, sheet_name):
    bh = BenchHelper()
    tc_config = bh.get_tccfg('config/latest_config.yaml')
    tb_config = bh.get_tbcfg('')
    tc_config.update(tb_config)
    veh_type = tc_config.get("veh_type")
    bl_ver = tc_config.get("bl_ver")
    cls_path = f"sdk/data/{veh_type}/can_lin_fr_cls/{bl_ver}"
    bus_comm = BusComm(cls_path, **tc_config)
    try:
        signals_info = get_signals_info_and_send_with_time(excel_path=excel_path, sheet_name=sheet_name)
        return bus_comm.send_signal_and_get_time(signals_info)
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'BusComm':
                    logger.info("停止sd_tester, 避免对下干扰")
                    bus_comm.stop_all_cyclic_msgs()

backbone_cases = send_signal_and_get_time("signal_mining.xlsx", "BackboneFR")
@allure.feature("互联服务/远程控制/远控除霜控制")
@allure.story("远控除霜控制")
class TestRCDefrost(TestABCBase):
    def before_class(self, ecu):
        time.sleep(10)
        self.vid = self.tb_config["vid"]
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H")
        logger.info("当前时间：{0}".format(datetime_now))
        [t_day, t_hour] = datetime_now.split(" ")
        logger.info("当前时间：{0}, {1}".format(t_day, t_hour))
        time.sleep(3700)
        self.file_name = self.tsp.get_signal_mining_data(vid=self.vid, hour=t_hour, dt = t_day)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        time.sleep(10)
        logger.info("等待10s再操作")

    def after_class(self, ecu):
        pass


    @pytest.mark.BackboneFR
    @pytest.mark.parametrize("test_case", backbone_cases)
    def test_data_signal_backbone(self, test_case):
        logger.info("测试内容：{0}".format(test_case))
        """FR信号"""
        assert self.tsp.validate_signal_mining_data(vid=self.vid, 
                                                signame=test_case[4], 
                                                sigvalue=test_case[5], 
                                                message_id=test_case[2], 
                                                timestamp=test_case[6], 
                                                csv_file=self.file_name)