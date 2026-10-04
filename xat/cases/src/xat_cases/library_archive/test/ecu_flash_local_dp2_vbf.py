# -*- coding: utf-8 -*-
"""
@File        : ecu_flash_local.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2024/11/14 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""


import os
import sys
import time
from time import sleep

# 测试环境   ecu-simulator 在 sat 同目录下生效
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.getcwd(), ".."))

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

        sbl_file_path = "/root/quansun_new/ecu-simulator/xat_ecu/legacy/test/PTZ_sbl.VBF"
        app_file_path = ["/root/quansun_new/ecu-simulator/xat_ecu/legacy/test/PTZ_Upd.VBF"]
        # self.flash_time_total = {}  # Multiple Flash Time Statistics
        # self.network_card_name = "enp0s3.5"

        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/local_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        tb_config = tb_config.yaml_content

        self.sd_test = Sd_Tester(**tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== sd_test started ==========================")

        self.ecu_flash_start("TCAM", 0x1011, sbl_file_path, app_file_path)
        sleep(timeout)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== BD Test Sim Stopped Error ==========================")
            logger.error(e)

        # logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def ecu_flash_start(self, ecu, doipip, sbl_file_path, app_file_path):
        ecu_thread = Thread(target=self.uds_flash_vmt, name=ecu , args= (ecu, doipip, sbl_file_path, app_file_path))
        ecu_thread.start()

    def uds_flash_vmt(self, ecu, doipip, sbl_file_path, app_file_path):
        # sleep(20)  # Wait for bgm to wake up and work normally
        #  flash pre-condition   BGM does not seem to be doing so at present
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        result = self.sd_test.flash_single_standard_ecu_vbf(sbl_file_path, app_file_path)

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== sd_test stopped ==========================")


        sleep(20)



if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/ecu_flash_local_dp2_vbf.py --time=1000
    # Note: 运行时 sd_test.py 80行左右  tru ... get_announcement_ip 都注解下


    from xat_ecu.legacy.common.logger import logger, Logger
    logger = Logger().get_logger()
    # logger.info("11111111111111111")


    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--time',  help='wait Flash time', default=500)
    args = argparser.parse_args()


    bgmflash = TestUdsFlashDoipSim()
    bgmflash.test_bgm(int(args.time))





