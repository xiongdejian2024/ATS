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
        # Code Location

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    @allure.title("Format test can route example")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46', name='Can_Lin Case Example 1196965')
    @pytest.mark.example3
    def test_format_example_can_route_caseid_1196965(self):
        '''
        Test related example, Show the format
        '''
        ecu_sims = Ecu_Sim_App(**self.tc_config)
        ecu_sims.all_ecu_start()

        self.flash_time_total = {}  # Multiple Flash Time Statistics

        self.sd_test = Sd_Tester(**self.tc_config)

        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")
        self.sd_test.tester_present()
        
        self.sd_test.information_check_f1ae()

        file_path = "/root/1.bin"
        self.keyinfo = "1111111111111111111111111"
        self.uds_flash("BNCM", 0x1023, file_path, self.keyinfo)
        
        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

        self.ipdu.time_control_stop()        # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()   # 停止 can lin fr 驱动，总线开始收发报文

        ecu_sims.all_ecu_close()

    def uds_flash(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, skip_step=[2])

        try:
            result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=2, init_step=0)
        except Exception as e:
            logger.info("==================== flash_single_standard_ecu Error ==========================")
            logger.error(e)

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        sleep(10)

        obd_ip = get_obd_ip()
        if obd_ip:
            self.tc_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.update_serverdoipid(doipip)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)
        logger.info("==================== SdTester started ==========================")

        if result:
            # "At BGM's request, wait 20 s from 10 82 to 10 02"
            sleep(10)
            try:
                result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=13,
                                                                init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            try:
                self.sd_test.reset_ecu_functional_addressing()
                logger.info("==================== bgm Flash Failed , Restart bgm ==========================")
            except Exception as e:
                logger.error(e)
                logger.warning("==================== BGM Flash Failed , Restart BGM Failed ==========================")

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== SdTester stopped ==========================")

        sleep(20)
        BgwNucApp.stop_tcpdump(p)

        # if result:
        #     global flash_count
        #     flash_count += 1

        global flash_count
        flash_count += 1
        flash_count_name = "flash_count_{}".format(flash_count)
        self.flash_time_total[flash_count_name] = self.sd_test.flash_time_statistics
        logger.info("{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                    "flash_total_int_time] is {}".format(flash_count_name, self.sd_test.flash_time_statistics))

 
        assert result, "bgm Flash >>>>>>>>>>>>>>>>  Failed"









        



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



