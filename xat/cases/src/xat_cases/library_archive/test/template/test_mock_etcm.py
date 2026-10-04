# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App


def mock_etcm():
    tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                           "ecu_simulator/config/diag_example_config.yaml")
    tb_config = ParseTBConfig(tb_path)
    tb_config = tb_config.yaml_content
    ecusims = Ecu_Sim_App(**tb_config)
    # ecusims.single_ecu_start('ETCM')
    ecusims.all_ecu_start()
    time.sleep(1000)


if __name__ == '__main__':
    mock_etcm()
