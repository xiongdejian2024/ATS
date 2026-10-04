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
import yaml

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase
from xat_ecu.api.abc_interface import *


class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)