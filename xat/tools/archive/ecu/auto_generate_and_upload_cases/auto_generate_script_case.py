#!/usr/bin/python3
"""
@File        : auto_generate_script_case.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/02/08 19:00
@Description :
@Examples    :
"""

import sys
import os
import openpyxl
# need to pip3 install openpyxl
import xml.etree.ElementTree as ET
# need to pip3 install ET
import re
import json
import argparse
from xat_ecu.legacy.tools.auto_generate_and_upload_cases.keyword_driven import KeywordDriven


class Auto_Generate_Script_Case():
    def __init__(self, case_file_path=None, script_file_path=None):
        self.case_file_path = case_file_path.strip() if case_file_path else None
        self.script_file_path = script_file_path.strip() if script_file_path else None

        object_keyword_path = "sdk/dut/bgm/bgm_keyword.json"
        self.keyword_driven =KeywordDriven(object_keyword_path)
        self.keyword_driven.get_object_keyword_dict(object_keyword_path)

    def get_xlsm_data(self):
        # :return type list
        # [{"Summary": "xxx", "Action": "xxx", "Expected Result": "xxx"}]
        testfile = openpyxl.load_workbook(self.case_file_path)
        sheet_all_names = testfile.sheetnames
        xlsm_data_dict = {}
        xlsm_datas = []
        for sh_name in sheet_all_names:
            sh = testfile[sh_name]
            for column in sh.columns:
                if column[0].value == "Summary":
                    xlsm_data_dict["Summary"] = column
                elif column[0].value == "Action":
                    xlsm_data_dict["Action"] = column
                elif column[0].value == "Expected Result":
                    xlsm_data_dict["Expected Result"] = column
            max_row = sh.max_row
            for i in range(1, max_row):
                xlsm_datas.append({"Summary": xlsm_data_dict["Summary"][i].value.replace("\n", ""),
                                   "Action": xlsm_data_dict["Action"][i].value,
                                   "Expected Result": xlsm_data_dict["Expected Result"][i].value
                                   })
        testfile.close()
        return xlsm_datas

    def write_script_head(self, f):
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# Automatic generation By ecu_simulator/tools/auto_generate_and_upload_cases/auto_generate_script_case.py\n")
        f.write("# Automatically generated code, please do not modify\n")

    def write_script_import(self, f):
        # import lib
        f.write("\n")
        f.write("import time\n")
        f.write("from time import sleep\n")
        f.write("import re\n")
        f.write("import pytest\n")
        f.write("import allure\n")
        f.write("from project.bgm.fixture.bgm import *\n")
        f.write("from project.bgm.case_helper.test_base_sim import TestBaseSim\n")
        f.write("from sdk.interface.pcan_const import PcanConst\n")
        f.write("from time import sleep\n")
        f.write("import inspect\n")
        f.write("from ecu_simulator.common.logger import logger\n")
        f.write("from sdk.dut.bgm.bgm_nuc_app import BgwNucApp\n")
        f.write("from ecu_simulator.ecu_sim.sd_tester import Sd_Tester\n")
        f.write("from sdk.dut.bgm.bgm_const import *\n")

    def write_script_cls(self, f, cls_name):
        f.write("class {}(TestBaseSim):\n".format(cls_name))

    def write_script_before_class(self, f, add_script_lines=[]):
        f.write("    def before_class(self, bgm):\n")
        f.write("        logger.info(inspect.stack()[0].function + ' start!')\n")
        f.write("        super().before_class(self, bgm)\n")
        if add_script_lines:
            for script_line in add_script_lines:
                f.write("        {}\n".format(script_line))

    def write_script_before_function(self, f, add_script_lines=[]):
        f.write("\n")
        f.write("    def before_each_func(self, bgm):\n")
        f.write("        logger.info(inspect.stack()[0].function + ' start!')\n")
        f.write("        super().before_each_func(bgm)\n")
        if add_script_lines:
            for script_line in add_script_lines:
                f.write("        {}\n".format(script_line))

    def write_scrip_after_function(self, f, add_script_lines=[]):
        f.write("\n")
        f.write("    def after_each_func(self, bgm):\n")
        f.write("        logger.info(inspect.stack()[0].function + ' start!')\n")
        if add_script_lines:
            for script_line in add_script_lines:
                f.write("        {}\n".format(script_line))
        f.write("        super().after_each_func(bgm)\n")

    def write_script_after_class(self, f, add_script_lines=[]):
        f.write("\n")
        f.write("    def after_class(self, bgm):\n")
        f.write("        logger.info(inspect.stack()[0].function + ' start!')\n")
        if add_script_lines:
            for script_line in add_script_lines:
                f.write("        {}\n".format(script_line))
        f.write("        super().after_class(self, bgm)\n")

    def write_script_add_bd_test_before_class(self, f):
        add_script_lines = [
            "self.bd_test = Sd_Tester(diag_mode='doip', server_id='172.20.1.1', is_via_gateway=False, ecu_name='BGM')",
            "self.bd_test.diagnostic_client_sim_start()",
            "logger.info('==================== BD Test Sim Started ==========================')",
            "",
            "sleep(0.5)",
            "self.bd_test.tester_present()"]
        self.write_script_before_class(f, add_script_lines)

    def write_script_add_obdfirewall_bd_test_before_class(self, f):
        add_script_lines = [
            "self.bgm_app.ssh_obd_firewall_env_is_prod()",
            "self.bd_test = Sd_Tester(diag_mode='doip', server_id='172.20.1.1', is_via_gateway=False, ecu_name='BGM')",
            "self.bd_test.diagnostic_client_sim_start()",
            "logger.info('==================== BD Test Sim Started ==========================')",
            "",
            "sleep(0.5)",
            "self.bd_test.tester_present()"]
        self.write_script_before_class(f, add_script_lines)

    def write_script_add_bd_test_after_class(self, f):
        add_script_lines = [
            "self.bd_test.stop_tester_present()",
            "sleep(0.5)",
            "self.bd_test.diagnostic_client_sim_close()",
            "logger.info('==================== BD Test Sim Stopped ==========================')"]
        self.write_script_after_class(f, add_script_lines)

    def write_script_add_obdfirewall_bd_test_after_class(self, f):
        add_script_lines = [
            "self.bd_test.stop_tester_present()",
            "sleep(0.5)",
            "self.bd_test.diagnostic_client_sim_close()",
            "logger.info('==================== BD Test Sim Stopped ==========================')",
            "self.bgm_app.ssh_obd_firewall_env_is_dummy()"]
        self.write_script_after_class(f, add_script_lines)

    def get_case_lines(self, case_str):
        case_lines = case_str.split("\n")
        return case_lines

    def generate_script_cases(self):
        # DTC Cases
        xlsm_datas = self.get_xlsm_data()
        with open(self.script_file_path, "w+") as f:
            self.write_script_head(f)
            self.write_script_import(f)

            f.write("\n")
            f.write("\n")
            f.write("@pytest.mark.dtc\n")
            f.write("@pytest.mark.diag\n")

            self.write_script_cls(f, "TestDtcAuto")
            self.write_script_add_bd_test_before_class(f)
            self.write_script_before_function(f)
            f.write("        self.set_veh_state(VehState.PARKED_COMFENA_COMFORT_NOT_ENABLED)\n")
            f.write("        self.bd_test.cleardiagnosticinformation_all_groups()\n")
            f.write("        self.bd_test.check_and_print_response_result('Cleardiagnosticinformation_All_Groups')\n")
            self.write_scrip_after_function(f)
            self.write_script_add_bd_test_after_class(f)

            for xlsm_data in xlsm_datas:
                if isinstance(xlsm_data, dict):
                    summary = xlsm_data.get("Summary")
                    summary = summary.replace(" ", "_")
                    summary = summary.replace("(", "_")
                    summary = summary.replace(")", "_")
                    summary = summary.replace("-", "_")
                    summary = summary.lower()
                    case_name = "test_" + summary
                    f.write("\n")
                    f.write("    def " + case_name + "(self):\n")
                    f.write("        logger.info(inspect.stack()[0].function + ' start!')")

                    
                    case_action = xlsm_data.get("Action")
                    case_action_lists = self.get_case_lines(case_action)
                    # print(case_action_lists)
                    for action_line in case_action_lists:
                        if action_line != "":
                            keyword_flag = self.keyword_driven.get_keyword_from_strline(action_line)
                            if keyword_flag:
                                # print(action_line)
                                action_script_line = self.keyword_driven.generate_cases_action_script_line()
                                if action_script_line:
                                    f.write("        " + action_script_line + "\n")
                        else:
                            print(r"Warning：action_line  \n is too much ")

                    case_assert = xlsm_data.get("Expected Result")
                    case_assert_lists = self.get_case_lines(case_assert)
                    for assert_line in case_assert_lists:
                        if assert_line != "":
                            keyword_flag = self.keyword_driven.get_keyword_from_strline(assert_line)
                            if keyword_flag:
                                assert_script_line = self.keyword_driven.generate_cases_assert_script_line()
                                if assert_script_line:
                                    f.write("        " + assert_script_line + "\n")
                        else:
                            print(r"Warning：case_assert  \n is too much ")

    def generate_obd_firewall_script_cases(self):
        # obd firewall cases
        xlsm_datas = self.get_xlsm_data()
        with open(self.script_file_path, "w+") as f:
            self.write_script_head(f)
            self.write_script_import(f)

            f.write("\n")
            f.write("\n")
            f.write("@pytest.mark.obd_firewall\n")
            f.write("@pytest.mark.diag\n")

            self.write_script_cls(f, "TestObdFirewallAuto")
            self.write_script_add_obdfirewall_bd_test_before_class(f)
            self.write_script_before_function(f)
            self.write_scrip_after_function(f)
            self.write_script_add_obdfirewall_bd_test_after_class(f)

            for xlsm_data in xlsm_datas:
                if isinstance(xlsm_data, dict):
                    summary = xlsm_data.get("Summary")
                    summary = summary.replace(" ", "_")
                    summary = summary.replace("(", "_")
                    summary = summary.replace(")", "_")
                    summary = summary.replace("-", "_")
                    summary = summary.lower()
                    case_name = "test_" + summary
                    f.write("\n")
                    f.write("    def " + case_name + "(self):\n")

                    case_action = xlsm_data.get("Action")
                    case_action_lists = self.get_case_lines(case_action)
                    # print(case_action_lists)
                    for action_line in case_action_lists:
                        if action_line != "":
                            keyword_flag = self.keyword_driven.get_keyword_from_strline(action_line)
                            if keyword_flag:
                                # print(action_line)
                                action_script_line = self.keyword_driven.generate_cases_action_script_line()
                                if action_script_line:
                                    f.write("        " + action_script_line + "\n")
                        else:
                            print(r"Warning：action_line  \n is too much ")

                    case_assert = xlsm_data.get("Expected Result")
                    case_assert_lists = self.get_case_lines(case_assert)
                    for assert_line in case_assert_lists:
                        if assert_line != "":
                            keyword_flag = self.keyword_driven.get_keyword_from_strline(assert_line)
                            if keyword_flag:
                                assert_script_line = self.keyword_driven.generate_cases_assert_script_line()
                                if assert_script_line:
                                    f.write("        " + assert_script_line + "\n")
                        else:
                            print(r"Warning：case_assert  \n is too much ")


if __name__ == "__main__":
    # work dir:  compass     only for BGM
    # Command:
    #       python3 ecu_simulator/tools/auto_generate_and_upload_cases/auto_generate_script_case.py
    #       --case_file_path="/root/BGM-VB-DIAG-DTC-BGM-6158.xlsm"
    #       --script_file_path="project/bgm/test/diag_nm/diag_dtc/test_dtc_auto.py"

    parser = argparse.ArgumentParser()
    parser.add_argument('--case_file_path', type=str, help='test case source')
    parser.add_argument('--script_file_path', type=str, help='target script path')

    args = parser.parse_args()
    generater = Auto_Generate_Script_Case(case_file_path=args.case_file_path, script_file_path=args.script_file_path)


    # DTC Cases
    # generater.generate_script_cases()

    # obd firewall cases
    generater.generate_obd_firewall_script_cases()

