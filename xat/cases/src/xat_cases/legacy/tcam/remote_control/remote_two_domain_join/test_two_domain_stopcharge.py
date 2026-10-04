#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@time         :2024/3/8 14:51
@author       :xxx@jiduauto.com
@description  :新增远程停止充电的业务稳定性用例
"""

import os
import sys
import time
import threading
import pytest
import allure


from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM性能稳定性/业务稳定性/远程充电控制")
@allure.story("远控结束充电")
class TestStopChargeRepeat(TestABCBase):
    def before_class(self, ecu):
        # self.soa.update(['VehicleSetStatusService_server'])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.mix.set_car_mode(CarMode.NORMAL)
        # 2域环境也通过soa发送维修模式
        # self.soa.s2s_set_mntnmode(False)
        self.bus_comm.set_gear_pos(Gear.Park)
        # self.mix.back_fota_to(FOTAMasteSts.IDLE)
        self.bus_comm.set_charging_sts(ChargingSts.ACCharging)
        

    def after_each_func(self, ecu):
        time.sleep(1.5)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远程结束充电_inactive两域联调")
    @pytest.mark.join_smoke
    def test_max_soc_caseid_1982885(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_thread_start("backbonefr","IHUBackBoneFr08","ChrgSoftSwCtrlSt_2_IHUBackBoneSignalIPdu08",2, timeout=10)
        with allure.step('模拟远程发送停止充电请求'):
            execid = self.tsp.rvc_charge_operation(-1)
        with allure.step('TCAN已发送结束充电请求,BGM发送CAN报文:'):
            result = self.bus_comm.check_thread_stop('ChrgSoftSwCtrlSt_2_IHUBackBoneSignalIPdu08')
            logger.info(f'CAN——ChrgSoftSwCtrlSt_2_IHUBackBoneSignalIPdu08抓取结果: {result}')
            assert result[0]
        with allure.step('停止ACC充电'):
            self.bus_comm.set_charging_sts(ChargingSts.ACChargingEnd)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid = execid)
