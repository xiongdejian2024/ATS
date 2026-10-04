# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :

"""
import time
import pytest
import allure
import sys, os
import json

import requests

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
from xat_ecu.legacy.interface.ms.ms_lib import meterSphere_client
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.common.logger import logger


class Test_MS_Reset(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):

        super().after_class(self, ecu)

    @allure.title("重置BGM的测试结果")
    def test_caseid_10001(self):
        """
        重置BGM的测试结果
        @return:
        """
        ms_client = meterSphere_client()
        (
            ms_cases_info,
            jama_id_mapping,
            fail_case_result_description,
        ) = ms_client.get_customnum_mappings_from_planid("411b35ed-0430-41e2-889a-1661ec89af6f")
        if ms_cases_info:
            for case_id_str in ms_cases_info:
                id_info = ms_cases_info.get(case_id_str)
                if id_info:
                    MSId = id_info[0]
                    MSnodeId = id_info[1]
                    caseId = id_info[3]
                    if id_info[2] != "Prepare":
                        ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, "Prepare", caseId)

    @allure.title("重置TCAM的测试结果")
    def test_caseid_10002(self):
        """
        重置TCAM的测试结果
        @return:
        """
        ms_client = meterSphere_client()
        (
            ms_cases_info,
            jama_id_mapping,
            fail_case_result_description,
        ) = ms_client.get_customnum_mappings_from_planid("e0d876ba-913f-4e5f-a71f-4cc89ab435bd")
        if ms_cases_info:
            for case_id_str in ms_cases_info:
                id_info = ms_cases_info.get(case_id_str)
                if id_info:
                    MSId = id_info[0]
                    MSnodeId = id_info[1]
                    caseId = id_info[3]
                    if id_info[2] != "Prepare":
                        ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, "Prepare", caseId)

    @allure.title("重置SOA的测试结果")
    def test_caseid_10003(self):
        """
        重置SOA的测试结果
        @return:
        """
        # 增加140和200的smoke测试计划清空
        for planid in ["2cc45bae-c4bf-45e7-85a5-cf43fc5a3725", "a61d464d-69d3-499c-9e55-8a66c27628da", "e02fc663-45a1-472d-974f-8f056bedeba4", "8c3422d4-343b-4b67-9e07-f5e97359127a"]:
            ms_client = meterSphere_client()
            (
                ms_cases_info,
                jama_id_mapping,
                fail_case_result_description,
            ) = ms_client.get_customnum_mappings_from_planid(planid)
            if ms_cases_info:
                for case_id_str in ms_cases_info:
                    id_info = ms_cases_info.get(case_id_str)
                    if id_info:
                        MSId = id_info[0]
                        MSnodeId = id_info[1]
                        caseId = id_info[3]
                        if id_info[2] != "Prepare":
                            ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, "Prepare", caseId)

    @allure.title("重置VO的测试结果")
    def test_caseid_10004(self):
        """
        重置VO的测试结果
        @return:
        """
        ms_client = meterSphere_client()
        (
            ms_cases_info,
            jama_id_mapping,
            fail_case_result_description,
        ) = ms_client.get_customnum_mappings_from_planid("ff784c90-4b1f-4f79-9a3c-5438c5ad6efd")
        if ms_cases_info:
            for case_id_str in ms_cases_info:
                id_info = ms_cases_info.get(case_id_str)
                if id_info:
                    MSId = id_info[0]
                    MSnodeId = id_info[1]
                    caseId = id_info[3]
                    if id_info[2] != "Prepare":
                        ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, "Prepare", caseId)


if __name__ == "__main__":
    pytest.main()
    # pytest bgm_tools/test_check_prenv.py

