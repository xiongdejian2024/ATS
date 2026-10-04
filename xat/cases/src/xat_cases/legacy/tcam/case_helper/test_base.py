# -*- coding: utf-8 -*-
"""
@File        : test_base.py
@Author      : quan.sun@jiduauto.com
@Time        : 2023/05/09 11:33
@Description :
@Examples    :
"""

import os, sys

from xat_cases.legacy.common_test_base import CommonTestBase

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)


class TestBase(CommonTestBase):
    pass
