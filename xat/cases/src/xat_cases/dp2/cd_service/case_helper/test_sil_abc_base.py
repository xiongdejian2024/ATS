#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_sil_abc_base.py
@Time         :2024/10/23 10:36
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""

from xat_cases.dp2 import *


class TestSILAbcBase(CommonSILTestBase):

    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)

    def after_each_func(self, ecu: EcuInfo):
        super().after_each_func(ecu)

    def after_class(self, ecu: EcuInfo):
        super().after_class(self, ecu)
