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


flash_count = 0


@allure.feature("Example Cases")
@allure.story("Test Example can lin fr Set")
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        # self.sd_test.tester_present()
        # Code Location

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        try:
            # self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)
        super().after_class(self, ecu)

    @pytest.mark.exampleuds
    @pytest.mark.repeat(5)
    def test_uds_daig(self):
        sleep(20)
        flash_result = None
        self.sd_test.update_serverdoipid(0x1001, "BGM")
        self.sd_test.diagnostic_session_check()
        flash_result = self.sd_test.check_and_print_response_result(
            "Step 3  Confirm Program Mode"
        )
        sleep(5)

        assert flash_result, " >>>>>>>>>>>>>>>>  Failed"

        # with allure.step(f"Test Step 1 can_lin_fr 启动"):
        #     self.ipdu.start_all_time_control()
        #     self.busapp.start_all_cyclic_msg()

        # with allure.step(f"Test Step 2 can_lin_fr 设置信号"):
        #     sleep(2)
        #     # can
        #     self.ipdu.bodycan_ppodbodyfr01_doorpassopenreqoutdswt2_psdnotpsd3_psd()

        #     # lin
        #     self.ipdu.cem_lin6_awmcem_lin6fr01_actvresplrintfltactrflt2_flt_fault()

        # with allure.step(f"Test Step 3 can_lin_fr 检查信号"):
        #     # can
        #     sleep(2)
        #     result, realvalue, expectedvalue = self.ipdu.check(self.ipdu.bodycan.CemBodyFr121, 'InteCleanUnpleSmell', 'OnOff1_Off')    # 0x114
        #     logger.info("result {}, realvalue {}, expectedvalue {}".format(result, realvalue, expectedvalue))

        #     # lin
        #     sleep(2)
        #     result, realvalue, expectedvalue = self.ipdu.check(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrIntFltActrFlt2', 1)  # 0x20
        #     logger.info("result {}, realvalue {}, expectedvalue {}".format(result, realvalue, expectedvalue))

        # with allure.step(f"Test Step 4 can_lin_fr can_lin_fr 停止"):
        #     sleep(5)
        #     self.ipdu.time_control_stop()
        #     self.busapp.stop_all_cyclic_msgs()

        # result = True

        # assert result
