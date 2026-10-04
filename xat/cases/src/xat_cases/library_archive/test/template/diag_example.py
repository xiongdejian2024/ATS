# -*- coding: utf-8 -*-
"""
@File        : diag_example.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/10/24 18:00 PM
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
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App


class DiagExample():
    def __init__(self):
        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/diag_example_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.tb_config = tb_config.yaml_content

    def test_before(self):
        self.ecusims = Ecu_Sim_App(**self.tb_config)
        self.ecusims.doip_sim_start()
        self.ecusims.all_ecu_start()

        # SdTester
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

            self.ecusims.doip_sim_close()
            self.ecusims.all_ecu_close()
        except Exception as e:
            logger.info("====================  Stopped Error ==========================")
            logger.error(e)

def diag_route_example(timeout):
    diagtest = DiagExample()
    diagtest.test_before()

    diagtest.sd_test.update_serverdoipid(0x1A12)
    sleep(1)

    #  ===================================
    diagtest.sd_test.diagnostic_session_check()
    diagtest.sd_test.check_and_print_response_result("diagnostic_session_check")
    #  ===================================

    sleep(int(timeout))

    diagtest.test_after()




if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/template/diag_example.py --time=10

    from xat_ecu.legacy.common.logger import logger

    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--time', help='wait Flash time', default=10)
    args = argparser.parse_args()

    timeout = int(args.time)

    diag_route_example(timeout)

  










