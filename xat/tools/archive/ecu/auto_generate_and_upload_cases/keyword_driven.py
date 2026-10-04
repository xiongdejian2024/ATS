#!/usr/bin/python3
"""
@File        : keyword_driven.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/02/12 19:00
@Description :
@Examples    :
"""

import sys
import os
import json
import argparse
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.ecu_sim.ecu_sim import EcuSim
from xat_ecu.legacy.sdk.dut.bgm.bgm_nuc_app import BgwNucApp
from xat_ecu.legacy.sdk.dut.bgm.bgm_tsp import BgwTsp
from xat_ecu.legacy.sdk.dut.bgm.bgm_app_sim import BgwAppSim
import re


object_keyword_dict = {"nuc" : "self.bgm_nuc_app",
                       "bd" : "self.bd_test",
                       "tsp" : "self.bgm_tsp",
                       "app" : "self.bgm_app",
                       "ecu" : "self.bgm_sim"}

veh_dict = {"P":"PARKED",
            "P_EN":"PARKED_COMFENA_COMFORT_ENABLED",
            "P_NOT":"PARKED_COMFENA_COMFORT_NOT_ENABLED",
            "DP":"DRIVER_PRESENT",
            "D":"DRIVING",
            "SW":"SW_UPDATE"}

class KeywordDriven():
    def __init__(self, object_keyword_path):
        # object_keyword_path = "sdk/dut/bgm/bgm_keyword.json"
        self.object_keyword_path = object_keyword_path
        self.obj_kw = []
        self.method_kw = []
        self.param_kw = []
        self.object_keyword_dict = {}
        pass

    def get_object_keyword_json(self):
        self.object_keyword = {}
        self.nuc_method = self.get_vaild_methods_from_class_obj(BgwNucApp)
        self.bd_method = self.get_vaild_methods_from_class_obj(Sd_Tester)
        self.tsp_method = self.get_vaild_methods_from_class_obj(BgwTsp)
        self.app_method = self.get_vaild_methods_from_class_obj(BgwAppSim)
        self.ecu_method = self.get_vaild_methods_from_class_obj(EcuSim)
        self.object_keyword["nuc"] = self.nuc_method
        self.object_keyword["bd"] = self.bd_method
        self.object_keyword["tsp"] = self.tsp_method
        self.object_keyword["app"] = self.app_method
        self.object_keyword["ecu"] = self.ecu_method
        with open(self.object_keyword_path, "w", encoding='utf-8') as f:
            json.dump(self.object_keyword, f, indent=4)
        print("{} File created successfully".format(self.object_keyword_path))

    def get_vaild_methods_from_class_obj(self, class_obj):
        # except "__dir__" and so on
        # class_obj     such as   BgwNucApp,Sd_Tester,EcuSim,BgwTsp,BgwAppSim
        vaild_methods = []
        methods = dir(class_obj)
        for method in methods:
            result = re.match(r"_", method)
            if not result:
                vaild_methods.append(method)
        return vaild_methods

    def get_keyword_from_strline(self, strline):
        self.keyword_flag = True
        self.obj_kw = re.findall(r"<(.+?)>", strline)
        self.method_kw = re.findall(r"\{(.+?)\}", strline)
        self.param_kw = re.findall(r"\((.+?)\)", strline)
        self.result_param = re.findall(r"\|(.+?)\|", strline)
        self.expect_result = re.findall(r"\[.+?\]", strline)
        if self.obj_kw==[] and self.method_kw==[] and self.param_kw==[] and self.result_param==[] and self.expect_result==[]:
            self.keyword_flag = False
        return self.keyword_flag

    def get_object_keyword_dict(self, json_path):
        with open(json_path, "r", encoding='utf-8') as f:
            self.object_keyword_dict = json.load(f)

    def generate_cases_action_script_line(self):
        # Cases Action
        script_cmd = ""
        if self.obj_kw:
            if len(self.obj_kw) == 1:
                script_cmd = object_keyword_dict.get(self.obj_kw[0]) + "."
                method_lists = self.object_keyword_dict.get(self.obj_kw[0])
            elif len(self.obj_kw) > 1:
                print(self.obj_kw)
                print("Warning: cases_action object keyword too much(>1)")
        else:
            if len(self.method_kw) != 1:
                print("Warning : cases_action method keyword != 1")
            if self.method_kw[0] == "set_veh_state":
                param_key = self.param_kw[0]
                param_value = veh_dict.get(param_key)
                script_cmd = "self.set_veh_state(VehState.{})".format(param_value)
                return script_cmd
            elif self.method_kw[0] in ["sleep"]:
                if len(self.param_kw) != 1:
                    print(self.param_kw)
                    print("Warning : cases_action param keyword != 1")
                script_cmd = self.method_kw[0] + "({})".format(self.param_kw[0])
                return script_cmd
            script_cmd = self.method_kw[0]
            return script_cmd
        if self.method_kw:
            length = len(self.method_kw)
            for method in method_lists:
                i = 0
                for method_keyword in self.method_kw:
                    if method_keyword.lower() in method:
                        i += 1
                    else:
                        break
                if i == length:
                    # Method Match success
                    script_cmd += method
                    break
        else:
            print("Warning: cases_action there is not method keyword")
        if self.param_kw:
            if len(self.param_kw) > 1:
                print("Warning: param keyword too much(>1)")
            elif len(self.param_kw) == 1:
                script_cmd += "({})".format(self.param_kw[0])
        else:
            script_cmd += "()"
        if self.result_param:
            if len(self.result_param) == 1:
                script_cmd = self.result_param[0] + " = " + script_cmd
            # elif self.result_param == 2:
            #     script_cmd = self.result_param[0] + ", " + self.result_param[1] + " = " + script_cmd
            else:
                print(self.result_param)
                print("Warning : cases_action Result Param too much(>1)")
        return script_cmd

    def generate_cases_assert_script_line(self):
        # Cases Expect Result
        script_cmd = ""
        method = None
        if self.method_kw:
            if len(self.method_kw) == 1:
                method = self.method_kw[0]
            else:
                print("Warning : cases_assert method keyword too much (>1)")
        if self.result_param:
            if len(self.result_param) == 1:
                if method:
                    if "in" in method or "==" in method:
                        if len(self.expect_result) != 1:
                            print("Warning : cases_assert Expect Result != 1")
                        script_cmd = "assert " + self.expect_result[0] + " {} ".format(method) + self.result_param[0]
                        return script_cmd
                else:
                    script_cmd = "assert " + self.result_param[0] + " == "
            # elif self.result_param == 2:
            #     script_cmd = "assert " + "[" + self.result_param[0] + ", " + self.result_param[1] + "]" + " == "
            else:
                print("Warning : cases_assert Result Param too much (>1)")
        if self.expect_result:
            if len(self.expect_result) == 1:

                expect_result = self.expect_result[0].capitalize()
                if expect_result in ["[True]", "[False]", "[None]"]:
                    expect_result = expect_result.replace("[", "")
                    expect_result = expect_result.replace("]", "")
                    script_cmd += expect_result
                else:
                    script_cmd += self.expect_result[0]
            else:
                print("Warning : cases_assert Expect Result too much(>1)")
        return script_cmd


if __name__ == "__main__":
    # work dir:  compass     Only For BGM
    # Command:
    #       python3 ecu_simulator/tools/auto_generate_and_upload_cases/keyword_driven.py --object_keyword_path="sdk/dut/bgm/bgm_keyword.json"

    parser = argparse.ArgumentParser()
    parser.add_argument('--object_keyword_path', type=str, help='object_keyword_path source')

    args = parser.parse_args()
    keyword_driven = KeywordDriven(object_keyword_path=args.object_keyword_path)
    keyword_driven.get_object_keyword_json()


    # strline = "<ecu> send can{roof} signal{rlslinresponseerror} value{error} (3) |result|"
    # keyword_driven.get_keyword_from_strline(strline)
    # keyword_driven.get_object_keyword_dict(args.object_keyword_path)
    # a = keyword_driven.generate_cases_action_script_line()
    # print(a)



    # object_keyword_path = "sdk/dut/bgm/bgm_keyword.json"
    # keyword_driven = KeywordDriven(object_keyword_path)
    # keyword_driven.get_object_keyword_json()


