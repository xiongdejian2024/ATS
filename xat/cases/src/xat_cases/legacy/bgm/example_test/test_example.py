# -*- coding: utf-8 -*-
"""
@File        : test_example.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/05/28 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig


@allure.feature("Example Cases")
@allure.story("Test Example Set")
class TestExample(TestBase):
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

        # 如果需要根据每个测试结果来做不同的操作，例子如下
        # testresult    # "Pass", "Failure", "Blocking"
        if ecu.get("testresult") != "Pass":
            logger.info("case 失败, 需要等待10s让环境恢复")
            sleep(10)

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
        '''
        Test related example, Show the format
        '''
        with allure.step(f"Test Step 1"):
            logger.info("Test 1 ...... sleep 1s")
            sleep(1)

        with allure.step(f"Test Step 2"):
            logger.info("Test 2 ...... sleep 2s")
            sleep(2)

        with allure.step(f"Test Step 3"):
            allure.attach("Test 3 ...... sleep 3s")
            logger.info("Test 3 ...... sleep 3s")
            sleep(3)

        result = True

        assert result

    @allure.title("模拟测试失败后处理")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Fota Case Example 1502340',
    )
    @pytest.mark.testresultfail
    def test_format_example_caseid_1567119(self):
        '''
        Test related example, Show the format
        '''
        with allure.step(f"Test Step 1"):
            logger.info("Test 1 ...... sleep 1s")
            sleep(1)

        with allure.step(f"Test Step 2"):
            logger.info("Test 2 ...... sleep 2s")
            sleep(2)

        with allure.step(f"Test Step 3"):
            allure.attach("Test 3 ...... sleep 3s")
            logger.info("Test 3 ...... sleep 3s")
            sleep(3)

        result = False

        assert result

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Fota Case Example 1502340',
    )
    @pytest.mark.examplepd
    @pytest.mark.parametrize(
        "test_parameter1,test_parameter2,test_parameter3",
        [(11, 22, 33), (44, 55, 66)],
        ids=[1502340, 1502341],
    )
    def test_parameter_driven_example(
        self, test_parameter1, test_parameter2, test_parameter3
    ):
        '''
        Parameter driven related example
        '''
        allure.dynamic.title("Parameter driven test example {}".format(test_parameter1))

        with allure.step(f"Test Step 1"):
            logger.info("Test 1 ...... sleep 1s")
            logger.info(test_parameter1)
            sleep(1)

        with allure.step(f"Test Step 2"):
            logger.info("Test 2 ...... sleep 2s")
            logger.info(test_parameter2)
            sleep(2)

        with allure.step(f"Test Step 3"):
            allure.attach("Test 3 ...... sleep 3s")
            logger.info("Test 3 ...... sleep 3s")
            logger.info(test_parameter3)
            sleep(3)

        result = True

        assert result


if __name__ == "__main__":
    pytest.main()
