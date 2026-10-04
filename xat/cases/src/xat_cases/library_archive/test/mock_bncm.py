# -*- coding: utf-8 -*-
"""
@File        : ecu_doip_mock_local.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/05/28 18:00 PM
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


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/mock_bncm.py --time=1000

    from sdk.ecu_simulator_app import Ecu_Sim_App
    from xat_ecu.legacy.common.logger import logger
    from ecu_sim.parse_tb_config import ParseTBConfig
    from xat_ecu.legacy.common.logger import logger, Logger
    logger = Logger().get_logger()
    # logger.info("11111111111111111")

    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--time',  help='Doip Mock time', default=100)
    args = argparser.parse_args()

    tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0], "ecu_simulator/config/bncm_mock_config.yaml")
    tb_config = ParseTBConfig(tb_path)
    tb_config = tb_config.yaml_content

    bgmsim = Ecu_Sim_App(**tb_config)
    bgmsim.doip_sim_start()
    bgmsim.update_0x22_data(ecu_name="TCAM", did="F1AA", data_info_update=[0x88, 0x95, 0x03, 0x62, 0x17, 0x20, 0x20, 0x42])
    sleep(int(args.time))
    bgmsim.doip_sim_close()




