# -*- coding: utf-8 -*-
"""
@File        : ecu_doip_sim_bmgmcu.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/05/21 18:00 PM
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


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 test/ecu_doip_mock_local.py --time=50000

    from sdk.ecu_simulator_app import Ecu_Sim_App
    from xat_ecu.legacy.common.logger import logger

    from ecu_sim.parse_tb_config import ParseTBConfig
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--time', help='Doip Mock time', default=100)
    args = argparser.parse_args()

    tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                           "ecu_simulator/config/bgmmcu_config.yaml")
    tb_config = ParseTBConfig(tb_path)
    tb_config = tb_config.yaml_content

    bgmsim = Ecu_Sim_App(**tb_config)
    bgmsim.doip_sim_start()
    sleep(int(args.time))
    bgmsim.doip_sim_close()




