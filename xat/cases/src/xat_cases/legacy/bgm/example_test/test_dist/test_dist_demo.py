#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_dist_demo.py
@Time         :2024/10/30 14:09
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import pytest

from xat_ecu.legacy.common.logger import logger
from framework.automotive.core.common_abc_test_base import CommonABCTestBase


class TestDemo1(CommonABCTestBase):
    @pytest.mark.Venus_800V
    def test_caseid_1984943(self):
        logger.info("测试用例test_caseid_1984943")

    @pytest.mark.Venus_800V
    def test_caseid_1984942(self):
        logger.info("测试用例test_caseid_1984942")

    @pytest.mark.Venus_800V
    def test_caseid_1984941(self):
        logger.info("测试用例test_caseid_1984941")

    @pytest.mark.Venus_800V
    def test_caseid_1984940(self):
        logger.info("测试用例test_caseid_1984940")

    @pytest.mark.Venus_800V
    def test_caseid_1984938(self):
        logger.info("测试用例test_caseid_1984938")


class TestDemo2(CommonABCTestBase):
    @pytest.mark.MarsOne
    def test_caseid_1984937(self):
        logger.info("测试用例test_caseid_1984937")

    @pytest.mark.MarsOne
    def test_caseid_1984934(self):
        logger.info("测试用例test_caseid_1984934")

    @pytest.mark.MarsOne
    def test_caseid_1984583(self):
        logger.info("测试用例test_caseid_1984583")


class TestDemo3(CommonABCTestBase):
    @pytest.mark.Venus
    def test_caseid_1984582(self):
        logger.info("测试用例test_caseid_1984582")

    @pytest.mark.Venus
    def test_caseid_1984580(self):
        logger.info("测试用例test_caseid_1984580")

    @pytest.mark.Venus
    def test_caseid_1983451(self):
        logger.info("测试用例test_caseid_1983451")
