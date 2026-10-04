# -*- coding: utf-8 -*-
"""
@File        : ecu_flash_local.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/03/11 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""


import os
import sys
import time
from time import sleep
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
import os
import pytest
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from time import sleep
import inspect
from xat_ecu.legacy.common.logger import logger
from threading import Thread
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig


flash_count = 0

# @pytest.mark.flash
# @pytest.mark.diag
class TestUdsFlashDoipSim():
    def test_bgm(self, timeout):
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)

        self.bgm_uds_flash_file_path1 = "/home/sun/2.pcap"
        self.bgm_uds_flash_file_path2 = "/home/sun/3.pcap"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_0CD428F5C45EDF896C3B']
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/local_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        tb_config = tb_config.yaml_content

        self.sd_test = Sd_Tester(**tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== sd_test started ==========================")

        self.ecu_flash_start("TCAM", 0x1011, self.bgm_uds_flash_file_path1, self.keyinfo)
        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== BD Test Sim Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def ecu_flash_start(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        ecu_thread = Thread(target=self.uds_flash_vmt, name=ecu , args= (ecu, doipip, bgm_uds_flash_file_path, keyinfo))
        ecu_thread.start()

    def uds_flash_vmt(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        # sleep(20)  # Wait for bgm to wake up and work normally
        #  flash pre-condition   BGM does not seem to be doing so at present
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"



        self.sd_test.update_serverdoipid(doipip)
        # self.sd_test.update_serverdoipid(0x44)   # PLG
        # self.sd_test.update_serverdoipid(0x48)   # SCU_D

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        # self.bgm_sim.pause_all_cyclic_msgs()

        # self.bgm_sim.ecudiagsim.single_ecu_sim_update_routine_control_p_data(ecu,
        #                                                                      {"FF00": { 1 : [0x00]}, "FF01": { 1 : [0x00]}} )
        # self.bgm_sim.ecudiagsim.single_ecu_sim_update_routine_control_p_data("SCU_D",
        #                                                                      {"FF00": {1: [0x00]}, "FF01": {1: [0x00]}})

        result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo)

        if not result:
            self.sd_test.reset_ecu_functional_addressing()
            logger.info("==================== ECUMOCK Flash Failed , Restart ECU ==========================")

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== sd_test stopped ==========================")

        # sleep(10)
        # self.bgm_sim.resume_all_cyclic_msgs()
        sleep(20)
        # BgwNucApp.stop_tcpdump(p)

        if result:
            global flash_count
            flash_count += 1

        # global flash_count
        # flash_count += 1
        # flash_count_name = "flash_count_{}".format(flash_count)
        # self.flash_time_total[flash_count_name] = self.sd_test.flash_time_statistics
        # logger.info("{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
        #             "flash_total_int_time] is {}".format(flash_count_name, self.sd_test.flash_time_statistics))
        #
        # assert result, "BGM Flash >>>>>>>>>>>>>>>>  Failed"

if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/ecu_flash_local.py --time=1000

    from xat_ecu.legacy.common.logger import logger


    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--time',  help='wait Flash time', default=500)
    args = argparser.parse_args()



    bgmflash = TestUdsFlashDoipSim()
    bgmflash.test_bgm(int(args.time))





