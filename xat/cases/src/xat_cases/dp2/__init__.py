#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :__init__.py
@Time         :2024/10/23 10:34
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""

import os
import sys
import json
from time import sleep
import time
import hashlib
import datetime
import copy
import requests

# 正式环境   ecu-simulator 在 sat 目录下生效
if os.path.exists(os.path.join(os.getcwd(), "../../ecu-simulator/ecu_simulator")):
    sys.path.insert(0, os.path.join(os.getcwd(), "../../ecu-simulator"))

# # 测试环境   ecu-simulator 在 sat 同目录下生效
# if os.path.exists(os.path.join(os.getcwd(), "../../../ecu-simulator/ecu_simulator")):
#     sys.path.insert(0, os.path.join(os.getcwd(), "../../../ecu-simulator"))


import pytest
import allure

from framework.automotive.core.dp2.common_abc_test_base import CommonABCTestBase
from framework.automotive.core.dp2.common_sil_test_base import CommonSILTestBase
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interfaces.dp2 import *
from xat_ecu.legacy.interface.nuc_app import partner_process_check, defunc_process_check, exec_shell
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import *
