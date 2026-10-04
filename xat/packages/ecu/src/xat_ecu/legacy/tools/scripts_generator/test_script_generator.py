# -*- coding: utf-8 -*-
"""
@File        : test_script_generator.py
=>  To generate sdk functions and write test scripts at the same time, you should stay at
    compass/tools/scipt_generator folder and use following command:
    python3 test_script_generator.py \
        --case_file_path=../../../BGM-Wiper-Test-Plan-v1.1.xlsm \
        --script_file_path=../../project/bgm/test/aurix/bodycancontrol/wiper/test_wiper.py \
        --project_type="bgm" \
        --generate_sdk_only=False

     --project_type has 'bgm' as default, --generate_sdk_only has False as default.

    Note:
    1. With --script_file_path provided, generator will OVERWRITE all content in file with
       generated script. You are recommended to generate scripts first in a draft file, and
       then move content to your target testing file.
    2. Generator will first search column Actions and Expected Result with info split by line,
       then change line to sdk_write_item contain info to write sdk if meeting patterns.
    3. To only generate methods in sdk, set --generate_sdk_only=True. You could use the generator
       without providing --script_file_path.
    4. Using generator in cgw is possible but not recommended. It might generate redundant sdk
       methods that operate same signal

    Current Matching Patterns:
    1. Action - Set
        "Set bodycan.SCM_02.{FrntWiprSwtSts}/FrntWiprSwtSts = v_Front_wiper_low_speed"
            => "pcan", "set_fix", ["dbc", "bodycan", "SCM_02", "FrntWiprSwtSts", "v_Front_wiper_low_speed"]
            => pcan.bodycan_scm_02_frntwiprswtsts_front_wiper_low_speed()

        "set bodycan.BCU_04.{VehSpd} = 0"
            => "pcan", "set_flex", ["dbc", "bodycan", "BCU_04", "VehSpd", 0"]
            => pcan.bodycan_bcu_04_vehspd(0)

    2. Expected Result - Check
        "bodycan.BGM_WIPR.{FrntWiprReq}/FrntWiprReq = v_Low_speed"
            =>"pcan", "check_fix", ["dbc", "bodycan", "BGM_WIPR", "FrntWiprReq", "v_Low_speed")]
            => pcan.assert_bodycan_bgm_wipr_frntwiprreq_is_low_speed()

        "bodycan.BCU_04.{VehSpd} = 56.25"
            =>"pcan", "set_flex", ["dbc", "bodycan", "BCU_04", "VehSpd", 56.25"]
            =>pcan.assert_bodycan_bcu_04_vehspd(56.25)
    3. Action - Wait
        "2. Wait for half of t_FrntWiprBlkProtn timer (1 seconds)/ Wait 1 minute"
            =>("special", "wait", [1.0])/           =>("special", "wait", [60.0])
            =>  logger.debug("Wait 1.0 seconds")    =>  logger.debug("Wait 60.0 seconds")
                time.sleep(1.0)                         time.sleep(60.0)

    4. Action - Set Vehstate/vehiclestate
        "5. Set vehState/vehiclestate to Driver Present"
            =>("special", "set", [vehstate, "driver present"])
            =>assert self.app.set_veh_state(PcanConst.VehState.DRIVER_PRESENT)

    Others:
        =>("special", None, [action_line])
        => "TODO: PLEASE FILLIN SPECIAL ACTION:
           #your special action in test case"
"""
import os
import sys
import pandas as pd
import argparse
import importlib
import logging
from test_script_generator_helper import TestScriptGeneratorHelper

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestScriptGenerator(object):
    def __init__(self, case_file_path, script_file_path, project_type):
        self.case_file_path = case_file_path
        self.script_file_path = script_file_path
        self.project_type = project_type.lower()
        self.helper = TestScriptGeneratorHelper()

        try:
            logger.info("--------------FILE-PREPARATION--------------")
            logger.info("--------------LOAD-SOURCE-FILE--------------")
            logger.info("=> Loading file from path: %s" % self.case_file_path)
            self.read_xlsm_file()
            logger.info("=> LOAD SOURCE FILE SUCCESS")
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/test_script_generator.py")
            logger.info("=> LOAD SOURCE FILE FAILED")
            raise

    def read_xlsm_file(self):
        return pd.read_excel(self.case_file_path)

    def open_script_writting_file(self):
        try:
            logger.info("--------------OPEN-SCRIPT-FILE--------------")
            if os.path.exists(self.script_file_path):
                logger.info("=> Target script file path exists, replacing %s" % self.script_file_path)
                fhandle = open(self.script_file_path, "w")
            else:
                try:
                    os.makedirs(os.path.dirname(self.script_file_path))
                    logger.info("=> New script path found, creating %s" % self.script_file_path)
                except:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/test_script_generator.py")
                    pass
                fhandle = open(self.script_file_path, "w")
            return fhandle
            logger.info("=> OPEN SCRIPT FILE SUCCESS")
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/test_script_generator.py")
            logger.info("=> OPEN SCRIPT FILE FAILED")
            raise

    def get_sdk_write_list(self):
        sdk_write_list = []
        df = self.read_xlsm_file()
        for case_action in df["Action"]:
            if (str(case_action)=="nan"):
                continue
            for single_action_line in case_action.split("\n"):
                sdk_write_item = self.helper.load_single_action_line(single_action_line)
                sdk_write_list.append(sdk_write_item)
        for case_check in df["Expected Result"]:
            if (str(case_check)=="nan"):
                continue
            for single_check_line in case_check.split("\n"):
                sdk_write_item = self.helper.load_single_check_line(single_check_line)
                sdk_write_list.append(sdk_write_item)
        return sdk_write_list

    def generate_pcan_sdk_methods(self):
        write_content_list = []
        # First get all functions in ***_pcan.py
        if self.project_type == 'bgm':
            sys.path.append(os.path.join(os.getcwd(), "../../"))
            handle_moudle = importlib.import_module("sdk.dut.bgm.bgm_pcan")
            pcan = handle_moudle.BgwPcan
            pcan_func_list = [func for func in dir(pcan) if not func.startswith('_')]
        elif self.project_type == 'cgw':
            sys.path.append(os.path.join(os.getcwd(), "../../"))
            handle_moudle = importlib.import_module("sdk.dut.cgw.cgw_pcan")
            pcan = handle_moudle.CgwPcan
            pcan_func_list = [func for func in dir(pcan) if not func.startswith('_')]

        # Analyze every line in "Action" and "Expected Result" column to sdk_write_list
        # element sample ('pcan', 'check', ['dbc', 'bodycan', 'BGM_WIPR', 'FrntWiprReq', 'v_Off'])
        sdk_write_list = self.get_sdk_write_list()
        # pick up all pcan.set/pcan.check element and change to sdk functions to write_content_list
        for element in sdk_write_list:
            if element[0] == "pcan":
                if element[1] == "set_fix":
                    write_content = self.helper.sdk_pcan_set_fix_content(element)
                elif element[1] == "set_flex":
                    write_content = self.helper.sdk_pcan_set_flex_content(element)
                elif element[1] == "check_fix":
                    write_content = self.helper.sdk_pcan_check_fix_content(element)
                elif element[1] == "check_flex":
                    write_content = self.helper.sdk_pcan_check_flex_content(element)
                if write_content["sdk_name"] not in pcan_func_list:
                    write_content_list.append(write_content["sdk_func_content"])
                    pcan_func_list.append(write_content["sdk_name"])
        # report sdk function number to be written and sample functions
        logger.info("=> %d distinct valid action need to be added to %s pcan" % (len(write_content_list), self.project_type))
        if write_content_list:
            logger.info("=> Sample SDK function: ")
            for i in write_content_list[:2]:
                logger.info(i)

        # write sdk functions into ***_pcan.py
        with open(('../../sdk/dut/%s/%s_pcan.py' % (self.project_type, self.project_type)), "a") as pcan_file:
            for functions in write_content_list:
                pcan_file.write(functions)
            pcan_file.close()
        return

    def generate_test_scripts(self):
        # open script file
        fhandle = self.open_script_writting_file()
        # open case file as pandas DataFrame
        df = self.read_xlsm_file()
        test_script = ""
        # use "Labels" and "Component" to generate test class name and header
        test_label = df["Labels.4"][0]
        component = df["Component"][0]
        test_script += self.helper.write_test_header(test_label, component)
        for index, row in df.iterrows():
            empty_case_validation = [str(row["Summary"]), str(row["Test ID"]),
                                     str(row["Action"]), str(row["Expected Result"])]
            if "nan" in empty_case_validation:
                logger.info("=> Empty case detected, skip case %s" % empty_case_validation)
                continue
            single_case_script = ""
            # use "Priority" to generate test priority marker
            priority = row["Priority"]
            single_case_script += self.helper.write_proprity(priority)

            # use "Summary" and "Test ID" to generate test function name
            summary = row["Summary"].lower()
            test_id = row["Test ID"]
            single_case_script += self.helper.write_func_name(summary, test_id)

            # use "Preconditon ID"s to add precondition actions
            preconditon_id_list = [row["Precondition ID"], row["Precondition ID.1"], row["Precondition ID.2"]]
            single_case_script += self.helper.write_precondition(preconditon_id_list)

            # use "Action" to write test script content
            action_string_list = row["Action"].split("\n")
            for action_line in action_string_list:
                if action_line:
                    # analyze action line
                    sdk_write_item = self.helper.load_single_action_line(action_line)
                    # when finding errors, uncomment below lines
                    # print("=> processing action line:", action_line)
                    # print("=> generated item:", str(sdk_write_item))
                    if sdk_write_item[0] == "pcan":
                        if sdk_write_item[1] == "set_fix":
                            single_case_script += self.helper.write_pcan_set_fix(sdk_write_item)
                        elif sdk_write_item[1] == "set_flex":
                            single_case_script += self.helper.write_pcan_set_flex(sdk_write_item)
                    # "special" "check" refers "Check ***" in "Action",
                    # process line in "Expected Results" with same step number
                    elif sdk_write_item[0] == "special":
                        if sdk_write_item[1] == "check":
                            step_number = action_line.split(".", 1)[0]
                            check_string_list = row["Expected Result"].split("\n")
                            for check_line in check_string_list:
                                if check_line:
                                    if check_line.split(".", 1)[0] == step_number:
                                        sdk_write_item = self.helper.load_single_check_line(check_line)
                                        # when finding errors, uncomment below lines
                                        # print("=> processing check line:", action_line)
                                        # print("=> generated item:", str(sdk_write_item))
                                        if sdk_write_item[1] == "check_fix":
                                            single_case_script += self.helper.write_pcan_check_fix(sdk_write_item)
                                        elif sdk_write_item[1] == "check_flex":
                                            single_case_script += self.helper.write_pcan_check_flex(sdk_write_item)
                                        else:
                                            single_case_script += self.helper.write_special_line(sdk_write_item)
                        # "special" "wait" refer "wait" in "Action", write time.sleep() in script
                        elif sdk_write_item[1] == "wait":
                            single_case_script += self.helper.write_wait(sdk_write_item)
                        # "special" "set" refer set target to targetstate in "Action"
                        elif sdk_write_item[1] == "set":
                            set_target = sdk_write_item[2][0].lower()
                            # when target == vehstate, write set vehiclestate in script
                            if (set_target == "vehstate") or (set_target == "vehiclestate"):
                                single_case_script += self.helper.write_set_vehstate(sdk_write_item)
                        # "special" "comment" refer "# ***" in action, write logger.info()
                        elif sdk_write_item[1] == "comment":
                            single_case_script += self.helper.write_comment(sdk_write_item)
                        # write special action comment in script
                        else:
                            single_case_script += self.helper.write_special_line(sdk_write_item)
                    else:
                        single_case_script += self.helper.write_special_line(sdk_write_item)
                else:
                    single_case_script += "\n"
            test_script += single_case_script
        test_script = test_script.replace('""""', '"""')
        fhandle.write(test_script)
        fhandle.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--case_file_path', type=str, help='test case source csv')
    parser.add_argument('--script_file_path', type=str, help='target script path')
    parser.add_argument('--project_type', type=str, help='pcan_type will be used', default='bgm')
    parser.add_argument('--generate_sdk_only', type=bool, help='choice to generator sdk methods', default='False')
    args = parser.parse_args()
    generator = TestScriptGenerator(args.case_file_path, args.script_file_path, args.project_type)
    if not args.generate_sdk_only:
        generator.generate_pcan_sdk_methods()
    else:
        generator.generate_pcan_sdk_methods()
        generator.generate_test_scripts()
