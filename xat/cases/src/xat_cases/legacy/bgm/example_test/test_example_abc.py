# -*- coding: utf-8 -*-
"""
@File        : test_example_abc.py
@Author      : dejian.xiong@jiduatuo.com
@Time        : 2024/04/19 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from framework.automotive.core.common_abc_test_base import CommonABCTestBase


class TestExample(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # raise RuntimeError("前置处理错误")  # case 和 后置就不会run了

        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    @allure.title("Format test example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Fota Case Example 1502340',
    )
    @pytest.mark.example
    def test_format_example_caseid_1567118(self):
        self.serial.send(command='sys --update 10', pattern='CCCCCCCC', timeout=int(10))
        ret_data = self.serial.receive()
        logger.info(ret_data)


if __name__ == "__main__":
    pytest.main()
