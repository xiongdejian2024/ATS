#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_abc_base.py
@Time         :2024/10/23 10:36
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from xat_cases.dp2 import *


class TestABCBase(CommonABCTestBase):

    def before_class(self, ecu: EcuInfo):
        pass

    def before_each_func(self, ecu: EcuInfo):
        pass

    def after_each_func(self, ecu: EcuInfo):
        pass

    def after_class(self, ecu: EcuInfo):
        pass
