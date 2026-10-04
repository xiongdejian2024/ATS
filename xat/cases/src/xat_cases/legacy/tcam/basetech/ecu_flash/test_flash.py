# -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :
"""

import os
import sys
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.tcam.case_helper.test_base import TestBase
from xat_cases.legacy.tcam.case_helper.TcamFlashBase import *


class Test(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.diagtest = FlashTestBase(self.tc_config)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
 
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.diagtest.close()
        super().after_class(self, ecu)

    @pytest.mark.tcam
    def test_Flash_Tcam(self):
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_C46CF0D264542D6A7916']
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v1.3.0/6110110130AB/6110110130AB.bin"
        self.diagtest.Flash_Tcam(keyinfo, file_url)
