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

class Test_Multi_Frame(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        #time.sleep(30)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    def test_multi_frame_bodycan_1A11(self):
        self.multi_frame(0x1A11)
    
    def test_multi_frame_bodycan_1A22(self):
        self.multi_frame(0x1A22)
    
    def test_multi_frame_bodycan_1A13(self):
        self.multi_frame(0x1A13)

    def test_multi_frame_bodycan_1A15(self):
        self.multi_frame(0x1A15)

    def test_multi_frame_bodycan_1A16(self):
        self.multi_frame(0x1A16)
    
    def test_multi_frame_bodycan_1A21(self):
        self.multi_frame(0x1A21)
    
    def test_multi_frame_bodycan_1A22(self):
        self.multi_frame(0x1A22)

    def test_multi_frame_bodycan_1A27(self):
        self.multi_frame(0x1A27)
    
    def test_multi_frame_bodycan_1A28(self):
        self.multi_frame(0x1A28)
    
    def test_multi_frame_bodycan_1A40(self):
        self.multi_frame(0x1A40)
    
    def test_multi_frame_bodycan_1A41(self):
        self.multi_frame(0x1A41)
    
    def test_multi_frame_bodycan_1A42(self):
        self.multi_frame(0x1A42)
    
    def test_multi_frame_bodycan_1A43(self):
        self.multi_frame(0x1A43)
    
    def test_multi_frame_bodycan_1A82(self):
        self.multi_frame(0x1A82)
    
    def test_multi_frame_bodycan_1A83(self):
        self.multi_frame(0x1A83)
    
    def test_multi_frame_connectivitycanfd_1023(self):
        self.multi_frame(0x1023)

    def multi_frame(self,logical_Address):
        '''
        Test related example, Show the format
        '''
        obd_ip = get_obd_ip()
        if obd_ip:
            self.tc_config["gateway_ip"] = obd_ip

        ecu_sims = Ecu_Sim_App(**self.tc_config)
        ecu_sims.all_ecu_start()

        self.flash_time_total = {}  # Multiple Flash Time Statistics

        self.sd_test = Sd_Tester(**self.tc_config)

        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")
        self.sd_test.information_check_f1ae()

        file_path = "/root/1.bin"
        self.keyinfo = "1111111111111111111111111"

        self.uds_flash("CCM", logical_Address, file_path, self.keyinfo)
        #self.uds_flash("BNCM", 0x1023, file_path, self.keyinfo)
        
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
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        self.sd_test.update_serverdoipid(doipip)
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
        # BgwNucApp.stop_tcpdump(p)

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

class Test_Single_Frame(TestBase):
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
    
    def test_signal_frame_bodycan_1A11(self):
        self.single_frame(0x1A11)
    
    def test_signal_frame_bodycan_1A22(self):
        self.single_frame(0x1A22)
    
    def test_signal_frame_bodycan_1A13(self):
        self.single_frame(0x1A13)

    def test_signal_frame_bodycan_1A15(self):
        self.single_frame(0x1A15)

    def test_signal_frame_bodycan_1A16(self):
        self.single_frame(0x1A16)
    
    def test_signal_frame_bodycan_1A21(self):
        self.single_frame(0x1A21)
    
    def test_signal_frame_bodycan_1A22(self):
        self.single_frame(0x1A22)

    def test_signal_frame_bodycan_1A27(self):
        self.single_frame(0x1A27)
    
    def test_signal_frame_bodycan_1A28(self):
        self.single_frame(0x1A28)
    
    def test_signal_frame_bodycan_1A40(self):
        self.single_frame(0x1A40)
    
    def test_signal_frame_bodycan_1A41(self):
        self.single_frame(0x1A41)
    
    def test_signal_frame_bodycan_1A42(self):
        self.single_frame(0x1A42)
    
    def test_signal_frame_bodycan_1A43(self):
        self.single_frame(0x1A43)
    
    def test_signal_frame_bodycan_1A82(self):
        self.single_frame(0x1A82)
    
    def test_signal_frame_bodycan_1A83(self):
        self.single_frame(0x1A83)
    
    def test_signal_frame_passivesafetycan_1510(self):
        self.single_frame(0x1510)
    
    def test_signal_frame_bodyexposedcanfd_1BB3(self):
        self.single_frame(0x1BB3)
    
    
    def single_frame(self,logical_Address):
        '''
        Test related example, Show the format
        '''
        ecu_sims = Ecu_Sim_App(**self.tc_config)
        ecu_sims.all_ecu_start()

        self.flash_time_total = {}  # Multiple Flash Time Statistics

        self.sd_test = Sd_Tester(**self.tc_config)

        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        self.sd_test.update_serverdoipid(logical_Address)
        
        time.sleep(3)

        self.sd_test.cleardiagnosticinformation_all_groups()
        
        time.sleep(3)

        self.ipdu.time_control_stop()        # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()   # 停止 can lin fr 驱动，总线开始收发报文

        ecu_sims.all_ecu_close()
        time.sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()




#cd /root/sat/xat_cases/legacy/bgm
#pytest uds/test_diag_routing.py::Test_Multi_Frame::test_multi_frame_bodycan_1A11  --tbcfg="bench_config/soa_bench_005.yaml"
#pytest uds/test_diag_routing.py::Test_Single_Frame::test_signal_frame_bodycan_1A11  --tbcfg="bench_config/soa_bench_005.yaml"