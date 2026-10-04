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
    def __init__(self):
        self.bgm_uds_flash_file_path1 = "/home/sun/6110110055SOC.bin"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_AF3E8EEC0ECEB10CF3CC']
        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/tcam_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.tb_config = tb_config.yaml_content

    def test_tcam(self):
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        self.uds_flash("TCAM", 0x1011, self.bgm_uds_flash_file_path1, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash(self, ecu, doipip, tcam_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, skip_step=[2])


        result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, target_step=2, init_step=0)

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        sleep(10)

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)
        logger.info("==================== SdTester started ==========================")

        if result:
            # "At BGM's request, wait 20 s from 10 82 to 10 02"
            sleep(10)
            try:
                result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, target_step=13,
                                                                init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            self.sd_test.reset_ecu_functional_addressing()
            logger.info("==================== TCAM Flash Failed , Restart TCAM ==========================")

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

        assert result, "TCAM Flash >>>>>>>>>>>>>>>>  Failed"


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/template/test_flash_tcam.py

    from xat_ecu.legacy.common.logger import logger

    tcamflash = TestUdsFlashDoipSim()
    tcamflash.bgm_uds_flash_file_path1 = "/home/sun/6110110055AS.bin"
    tcamflash.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_6E1E743EA830D955DAA2']
    # tcamflash.keyinfo = "${XAT_CREDENTIAL_SCAN_57169E615DC2AB8B6A0B}"
    # tcamflash.keyinfo = "${XAT_CREDENTIAL_SCAN_69BF5BFEE1D47EA34917}"
    # tcamflash.keyinfo = "${XAT_CREDENTIAL_SCAN_BFB0CEE5977FADF76DBA}"
    tcamflash.test_tcam()











