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
        self.bgm_uds_flash_file_path1 = "/home/sun/6160110055OTR.bin"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_BB2FDDF6E1D3A32F326F']
        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.tb_config = tb_config.yaml_content
        self.flash_time_total = {}  # Multiple Flash Time Statistics

    def test_bgm(self):
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.network_card_name = "enp0s3.5"

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        self.uds_flash("BGM", 0x1001, self.bgm_uds_flash_file_path1, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=2, init_step=0)

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

        # if result:
        #     result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=4,
        #                                                     init_step=2)
        # if result:
        #     result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=13,
        #                                                     init_step=5)

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
            self.sd_test.reset_ecu_functional_addressing()
            logger.info("==================== BGM Flash Failed , Restart BGM ==========================")

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

        assert result, "BGM Flash >>>>>>>>>>>>>>>>  Failed"


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/template/test_flash_bgm.py

    from xat_ecu.legacy.common.logger import logger

    bgmflash = TestUdsFlashDoipSim()
    bgmflash.bgm_uds_flash_file_path1 = "/home/sun/6110110055AC.bin"
    # bgmflash.keyinfo = "${XAT_CREDENTIAL_SCAN_125B358DAF299B6FC017}"
    bgmflash.keyinfo = "d1AiyTAxRC2AmyayfbO2JE+B7d/OyI/127sOMuAdcujtAwETzMuOPvBpY6hgKfXpy/wSJBKQPdi5pMh7XXca6GrqHjU4D37dPQWqah+VggiU6u7MIrE/CXqzlLzsQZin2NnikK2Nf+4OGCN376RiRolnJY/gHticuKhG6y84aC8g5uLNPViy6vVMziHSKQNSpXARBDc90YfIsDvmsEpDdXTWdbAbKJoEGQ97AUEQ9K3CzkM8m7bXgrudsCnegan0u9ycys3EPYHrqILgE8dp6uxci2BsXVRxvY0GulpSwKF65vavXkxpV+1NpB1rzu/CPX8v8xFVma06DzPs7YYbrg=="

    bgmflash.test_bgm()
    # i = 0
    # while i < 2:
    #     i += 1
    #     logger.info("=========================  i is {}  ==========================".format(i))
    #     bgmflash.test_bgm()
    # logger.info("============= update OK  20 times ===================")











