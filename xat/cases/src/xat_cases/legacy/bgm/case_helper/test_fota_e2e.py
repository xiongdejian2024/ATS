# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""

import os
import sys
import json

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase


class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        e2e_info = ecu.get("e2e_info")
        if e2e_info:
            self.e2e_info = eval(e2e_info)
        else:
            self.e2e_info =  self.tc_config.get("e2e_info")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.bgm_diag_line_up()