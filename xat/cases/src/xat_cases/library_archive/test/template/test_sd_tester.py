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
sys.path.append(os.path.join(os.getcwd(), ".."))
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


class TestSdTester:
    def __init__(self):
        tb_path = os.path.join(
            os.path.realpath(__file__).split("ecu_simulator")[0],
            "ecu_simulator/config/test_sd_tester_config.yaml",
        )
        tb_config = ParseTBConfig(tb_path)
        self.tb_config = tb_config.yaml_content

    def test_before(self):
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

    def test_after(self):
        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)

    def test_vin(self, vin: str, timeout=10):
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        #  ===================================
        self.sd_test.enter_extended_session()
        self.sd_test.check_and_print_response_result("enter_extended_session")

        self.sd_test.security_access_level_l3()
        self.sd_test.assert_security_access("L3")

        self.sd_test.write_vin(vin)
        self.sd_test.check_and_print_response_result("write_vin")

        self.sd_test.enter_default_session()
        self.sd_test.check_and_print_response_result("enter_default_session")
        #  ===================================

        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)

    def test_read_did(self, timeout=10):
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        #  ===================================
        self.sd_test.query_fota_status()
        #  ===================================

        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)

    def test_write_vid(self, vid: str, timeout=10):
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        #  ===================================
        self.sd_test.enter_extended_session()
        self.sd_test.check_and_print_response_result("enter_extended_session")

        self.sd_test.security_access_level_l4()
        self.sd_test.assert_security_access("L4")

        self.sd_test.write_vid(vid)
        self.sd_test.check_and_print_response_result("write_vid")

        self.sd_test.enter_default_session()
        self.sd_test.check_and_print_response_result("enter_default_session")
        #  ===================================

        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)

    def test_cancel_fota(self, timeout=10):
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        #  ===================================
        self.sd_test.enter_extended_session()
        self.sd_test.check_and_print_response_result("enter_extended_session")

        self.sd_test.security_access_level_l4()
        self.sd_test.assert_security_access("L4")

        self.sd_test.cancel_fota()
        self.sd_test.check_and_print_response_result("cancel_fota")

        self.sd_test.enter_default_session()
        self.sd_test.check_and_print_response_result("enter_default_session")
        #  ===================================

        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(
                "==================== SdTester Stopped Error =========================="
            )
            logger.error(e)

    def test_enter_fota_mode(self, timeout=10):
        self.test_before()

        #  ===================================
        self.sd_test.security_access_level_l1()
        self.sd_test.assert_security_access("L1")

        self.sd_test.request_enter_fota_mode()
        self.sd_test.check_and_print_response_result("request_enter_fota_mode")
        #  ===================================

        sleep(timeout)
        self.test_after()

    def test_exit_fota_mode(self, timeout=10):
        self.test_before()

        #  ===================================
        self.sd_test.security_access_level_l1()
        self.sd_test.assert_security_access("L1")

        self.sd_test.request_exit_fota_mode()
        self.sd_test.check_and_print_response_result("request_exit_fota_mode")
        #  ===================================

        sleep(timeout)
        self.test_after()

    def test_all_ecu_is_active(self, timeout=10):
        self.test_before()

        #  ===================================
        all_ecu_is_active_dict = self.sd_test.all_ecu_is_active()
        logger.info(all_ecu_is_active_dict)
        #  ===================================

        # sleep(timeout)
        self.test_after()


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/template/test_sd_tester.py --time=10

    from xat_ecu.legacy.common.logger import logger

    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--time', help='wait Flash time', default=500)
    args = argparser.parse_args()

    sdtest = TestSdTester()

    # vin = "LSTEST6R9F2086650"
    # sdtest.test_vin(vin, timeout=int(args.time))

    # sdtest.test_read_did(timeout=int(args.time))

    # sdtest.test_write_vid(vid="5946b3754b09b4a31175208bddce80e0", timeout=int(args.time))
    # sdtest.test_write_vid(vid="26e1a11ce6f9dff6db70fd54388d0d9b", timeout=int(args.time))

    # sdtest.test_cancel_fota(timeout=int(args.time))

    # sdtest.test_enter_fota_mode(timeout=int(args.time))

    # sdtest.test_exit_fota_mode(timeout=int(args.time))

    sdtest.test_all_ecu_is_active(timeout=int(args.time))
