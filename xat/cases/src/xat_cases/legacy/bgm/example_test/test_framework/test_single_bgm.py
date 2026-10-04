#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_single_bgm.py.py
@Time         :2024/10/14 16:40
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from framework.automotive.core.common_abc_test_base import CommonABCTestBase
from framework.automotive.utils.data_type import EcuInfo


class TestSingleBgm(CommonABCTestBase):
    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = None
        return ecu

    def test_single_bgm(self):
        assert self.domain.single_bgm is True
