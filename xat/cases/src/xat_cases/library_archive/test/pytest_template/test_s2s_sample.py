# -*- coding: utf-8 -*-
"""
@File        : test_s2s_sample.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/8/26 11:00
@Description : 
@Examples    :
"""

import os
import sys
import argparse
import json

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
import pytest
import time
from xat_ecu.legacy.tools.s2s_mcu_sim.signal2service_local import S2sTest
import os


class TestS2S():
    @pytest.mark.smoke
    def test_s2s_local(self):
        os.system("mkdir ../report")
        os.system("touch ../report/report_summary.json")
        s2s_test = S2sTest("sdk/data/mars1/can_lin_fr_cls/v_0_5_5")

        s2s_test.test_s2s_cfg("./tools/s2s_mcu_sim/config/sample.json")
        assert True
            
        
