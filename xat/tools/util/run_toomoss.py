# -*- coding: utf-8 -*-
"""
@File        : run_toomoss.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/12/27 10:51 AM
@Description : run toomoss, scan devices
@Examples    : example of how to use it
"""

import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))

import time
from time import sleep
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_lin import ToomossLin


def get_toomoss_devices():
    lin_test = ToomossLin("1", "test")
    return lin_test.toomoss_scandevice()


if __name__=="__main__":
    # Work Path: sat/
    # Command: python3 tools/util/run_toomoss.py

    get_toomoss_devices()
    
    