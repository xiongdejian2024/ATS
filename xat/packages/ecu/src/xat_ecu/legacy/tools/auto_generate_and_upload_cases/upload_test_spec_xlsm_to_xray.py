# -*- coding: utf-8 -*-
"""
@File        : upload_test_spec_xlsm_to_xray.py
@Description : This script includes two functions: Import data from xlsm to jira,
               and upload mapping relationship to xray json document.
@Examples    :

=>  To operate two function at the same time, you should stay at compass/tools/xray folder and use
    following command:

    python3 upload_test_spec_xlsm_to_xray.py \
        --username=zhishang.guo \
        --password='************' \
        --case_file_path=../../../BGM-Vehicle-State-Test-Plan-v1.6.xlsm \
        --script_file_path=../../project/bgm/test/aurix/bodycancontrol/vehiclestate/test_vehiclestate.py \
        --project_type=bgm \

    --project_type has 'bgm' as default

    Note:
    1. You need your jira login info as --username and --password to login jira and execute
       issue operation; You can execute script without providing --password and input your
       password later if you found any difficulty typing it in the command line.
    2. Script will take data out of your test case file and upload to jira,and output
       xlsm_jira_xray_import_output.xlsm with column "JIRA Key" filled in your
       personal directory;
    3. Currently, script ONLY support import test case to project"DSTMS" and type"test spec"
    4. It also support updating issues, so script will update tickets rather than creating new ones
       when column "JIRA Key" filled in test case.
    5. To only import jira ticket, add --import_jira_only=True in command line
    6. To only generate xray mapping, add --generate_xray_json_only=True in command line

       Xray mapping rule:
        Summary: manual front wiper on
        Test ID: xxxx_xxx_xx_002
        JIRA Key: DSTMS-99999
        => "test_manual_front_wiper_002": "DSTMS-99999"

        Summary: manual front wiper [on driver present]
        Test ID: xxxx_xxx_xx_008
        JIRA Key: DSTMS-66666
        => "test_manual_front_wiper_":{
                "on_driver_present_008": "DSTMS-66666"
            }
    8. The script is test-case based so it will ONLY upload function mapping in the test case. You need
       to mannually input other test function mapping if they are not in test case table.
"""
import os
import re
import json
import logging
from getpass import getpass
import pandas as pd
import openpyxl
from jira import JIRA
import sys
import argparse
import importlib

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class UploadTestSpecXlsmtoXray(object):
    """
    XlsmJiraXrayImport Class that can user import jira and xray json automatically with xlsm provided.
    To import to jira, test case xlsm, jira username, jira password, and target test repository path
    are required
    To upload to xray json, test case xlsm, test script path, and test class name are required
    Initialition will check test case path and test script path, raise exception if failed to open
    """

    def __init__(self, username=None, password=None,
                 case_file_path=None, script_file_path=None,
                 project_type="bgm"):
        self.username = username
        self.password = password
        self.case_file_path = case_file_path.strip() if case_file_path else None
        self.script_file_path = script_file_path.strip() if script_file_path else None
        self.project_type = project_type.strip().lower()

        if self.case_file_path:
            try:
                logger.info("--------------FILE-PREPARATION--------------")
                logger.info("--------------LOAD-SOURCE-FILE--------------")
                logger.info("=> Loading file from path: %s" % self.case_file_path)
                self.read_xlsm_file()
                logger.info("=> LOAD SOURCE FILE SUCCESS")
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/auto_generate_and_upload_cases/upload_test_spec_xlsm_to_xray.py")
                logger.info("=> LOAD SOURCE FILE FAILED")
                raise

        if self.script_file_path:
            try:
                logger.info("--------------OPEN-SCRIPT-FILE--------------")
                self.fhandle = open(self.script_file_path, "r")
                logger.info("=> OPEN SCRIPT FILE SUCCESS")
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/auto_generate_and_upload_cases/upload_test_spec_xlsm_to_xray.py")
                logger.info("=> OPEN SCRIPT FILE FAILED")
                raise

        self.CSV_JIRA_COLUMN_MAPPING_DICT = {
            "Test Set": "customfield_14114",
            # sample: ['DSTMS-7349']
            "Assignee": "assignee",
            # sample: {'name': 'yong.wei'}
            "Feature Name": "customfield_14163",
            # sample: 'BGM Aurix Manual Front Wiping'
            "Test ID": "customfield_10669",
            # sample: 'interior_light_226'
            "Summary": "summary",
            # sample: 'test trunk light on headlamps on backlights on 80 parked comfena 226'
            "Precondition ID": "customfield_14115",
            # ['DSTMS-19']
            "Action": "customfield_14111",
            # sample:
            "Expected Result": "customfield_14111",
            # sample:
            "Priority": "priority",
            # sample: {'name': 'P2 - High'}
            "Labels": "labels",
            # sample: ['CGW', 'full', 'interiorlighting', 'sanity']
            "Automatable": "customfield_14159",
            # sample: {'value': 'Yes'}
            "Automation Status": "customfield_14158",
            # sample: {'value': 'Yes'}
            "Linked \"tests\"": "Linked \"tests\"",
            # sample: []
            "Vehicle Phase": "customfield_23400",
            # sample: [{'value': 'VB'}, {'value': 'TT'}]
            "Vehicle Types": "customfield_21827",
            # sample: ['ES6G1.2', 'ES8G1.1', 'ES8G1.F', 'FURY']
            "Component": "components",
            # sample: [{'name':'BGM-Diag-NM'}]
            "Test Stage": "customfield_22000",
            # sample: [{'value': 'Integration Test'}]
            "Test Repository Path": "customfield_14118"
            # sample: /BGM/Platform/Upgrade
        }

    def read_xlsm_file(self):
        """
        read xlsm file using pandas package
        :return: a data frame
        """
        return pd.read_excel(self.case_file_path)

    def import_xlsm_to_jira(self):
        """
        import data collected from xlsm to jira, filing JIRA Key column
        :return: JIRA Key column filled in ../../../xlsm_jira_xray_import_output.xlsm
                and a updated dataframe returned
        """
        if not self.username:
            raise Exception("No username provided, Login failed")
        elif not self.password:
            self.password = getpass("Username provided without password, please input your password\n")

        count = 0
        nio_jira = JIRA(server="https://jira.nioint.com/", auth=(self.username, self.password))
        data_upload = self.generate_data_upload_to_jira()
        df_write = self.read_xlsm_file()
        df_write["JIRA Key"] = df_write["JIRA Key"].astype(str)
        workbook = openpyxl.load_workbook(self.case_file_path, read_only=False, keep_vba=True)
        ws = workbook.worksheets[0]
        jira_key_num_col = df_write.columns.get_loc("JIRA Key") + 1
        try:
            for data in data_upload:
                if "Linked \"tests\"" in data:
                    linked_issue_list = data.pop("Linked \"tests\"")
                else:
                    linked_issue_list = []
                jira_key = data.pop("TEMP_JIRA_KEY")
                if not jira_key:
                    new_issue = nio_jira.create_issue(fields=data)
                    df_write["JIRA Key"][count] = new_issue.key
                    for linked_issue in linked_issue_list:
                        jira_outward_issue = nio_jira.issue(linked_issue)
                        nio_jira.create_issue_link('tests', new_issue, jira_outward_issue)
                    ws.cell(count + 2, jira_key_num_col).value = new_issue.key
                    count += 1
                    logger.info("=> Imported Case %s" % new_issue.key)
                else:
                    data.pop("project")
                    data.pop("issuetype")
                    issue = nio_jira.issue(jira_key)
                    issue.update(fields=data)
                    for linked_issue in linked_issue_list:
                        jira_outward_issue = nio_jira.issue(linked_issue)
                        nio_jira.create_issue_link('tests', issue, jira_outward_issue)
                    count += 1
                    logger.info("=> Updated Case %s" % jira_key)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/auto_generate_and_upload_cases/upload_test_spec_xlsm_to_xray.py")
            logger.info("Exception Occured, upload stopped\n %s" % e)
        finally:
            workbook.save('../../../xlsm_jira_xray_import_output.xlsm')

        return df_write

    def generate_data_upload_to_jira(self):
        """
        Helper function to generate upload data dictionary from xlsm
        :return: a dictionary of upload data
        """
        upload_data_list = []
        df = self.read_xlsm_file()
        for index, row in df.iterrows():
            single_upload_data = {}
            for field in self.CSV_JIRA_COLUMN_MAPPING_DICT:
                single_upload_data["project"] = "DSTMS"
                single_upload_data["issuetype"] = "Test Spec"
                single_upload_data["TEMP_JIRA_KEY"] = row["JIRA Key"] if not pd.isnull(row["JIRA Key"]) else ""
                single_upload_data = self.__process_single_upload_data(single_upload_data, row, field)
            upload_data_list.append(single_upload_data)
        return upload_data_list

    def __process_single_upload_data(self, single_upload_data, row, field):
        if field == "Test Set":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [row[field]]
        elif field == "Assignee":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = {'name': row[field]}
        elif field == "Feature Name":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = row[field]
        elif field == "Test ID":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = row[field]
        elif field == "Summary":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = row[field].replace(
                row[field][row[field].find("{"):row[field].find("}") + 1], "").replace("\n", " ")
        elif field == "Precondition ID":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [row[index]
                                                                            for index, data in row.iteritems()
                                                                            if (re.match("Precondition ID.?[0-9]?", index)
                                                                                and not pd.isnull(row[index]))]
        elif field == "Action":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = {'steps': [{'fields': {}}]}
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]]['steps'][0]['fields']['Action'] = row[field]
        elif field == "Expected Result":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]]['steps'][0]['fields']['Expected Result'] = row[
                field]
        elif field == "Priority":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = {'name': row[field]}
        elif field == "Labels":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [row[index]
                                                                            for index, data in row.iteritems()
                                                                            if (re.match("Labels.?[0-9]?", index)
                                                                                and not pd.isnull(row[index]))]
        elif field == "Automatable":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = {'value': row[field]}
        elif field == "Automation Status":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = {'value': row[field]}
        elif field == "Linked \"tests\"":
            linked_issue_list = [row[index] for index, data in row.iteritems()
                                 if (re.match("Linked \"tests\".?[0-9]?", index)
                                     and not pd.isnull(row[index]))]
            if linked_issue_list:
                single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = linked_issue_list
        elif field == "Vehicle Phase":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [{'value': row[index]}
                                                                            for index, data in row.iteritems()
                                                                            if (re.match("Vehicle Phase.?[0-9]?", index)
                                                                                and not pd.isnull(row[index]))]
        elif field == "Vehicle Types":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [row[index]
                                                                            for index, data in row.iteritems()
                                                                            if (re.match("Vehicle Types.?[0-9]?", index)
                                                                                and not pd.isnull(row[index]))]
        elif field == "Component":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [{"name": row[field]}]
        elif field == "Test Stage":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = [{"value": row[field]}]
        elif field == "Test Repository Path":
            single_upload_data[self.CSV_JIRA_COLUMN_MAPPING_DICT[field]] = row[field]
        return single_upload_data

    def generate_mapping_table(self, df=pd.DataFrame()):
        """
        Generate JIRA Key and function name mapping to json according to project type
        :param df: dataframe updated from import or from read_xlsm_file()
        """
        if not self.script_file_path:
            raise Exception("Script file or test class name is not provided, generate mapping json failed")
        else:
            for line in self.fhandle:
                if line.strip().startswith("class"):
                    test_class_name = line[line.find(" ")+1:line.find("(")]
                    break
            sys.path.append(os.path.join(os.getcwd(), "../../"))
            print(self.script_file_path[:-3].replace("../", "").replace("/", "."))
            handle_moudle = importlib.import_module(self.script_file_path[:-3].replace("../", "").replace("/", "."))
            test_file = eval("handle_moudle.%s" % test_class_name)
            test_func_list = [func for func in dir(test_file) if not func.startswith('_')]

            if not df.empty:
                pass
            else:
                df = self.read_xlsm_file()

            row_count = df.shape[0]
            num_dstms = sum(1 for i in range(0, df.shape[0]) if not pd.isnull(df["JIRA Key"][i]))

            if num_dstms != row_count:
                logger.info("=>Number of DSTMS don't match! Number of DSTMS found: %d, "
                      "while number of test case found: %d" % (num_dstms, row_count))
            else:
                logger.info("=>Every test case has its DSTMS ID, %d cases generating" % num_dstms)

            mapping_dict = {}
            for index, row in df.iterrows():
                summary = row["Summary"].lower()
                # pick summary in {} bracket
                if ("{" in summary) and ("}" in summary):
                    summary = summary[summary.find("{") + 1:summary.find("}")]
                # pick function name and parameter out of summary
                if ("[" in summary) and ("]" in summary):
                    summary_func_name = summary[:summary.find("[")].replace(" ", "_")
                    test_function_name = "test_" + summary_func_name
                    summary_parameter = summary[summary.find("[") + 1:summary.find("]")].replace(" ", "_") + \
                                        "_" + row["Test ID"].split("_")[-1]
                    if test_function_name in test_func_list:
                        for param_list in eval("test_file.%s.parametrize._marks[0].args" % test_function_name):
                            if isinstance(param_list, list):
                                para_list = [single_param.id for single_param in param_list]
                                if summary_parameter in para_list:
                                    try:
                                        mapping_dict[test_function_name][summary_parameter] = row["JIRA Key"]
                                    except:
                                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/auto_generate_and_upload_cases/upload_test_spec_xlsm_to_xray.py")
                                        mapping_dict[test_function_name] = {}
                                        mapping_dict[test_function_name][summary_parameter] = row["JIRA Key"]
                                else:
                                    print("%s not found in %s, skip input" % (summary, self.script_file_path))
                    else:
                        print("%s not found in %s, skip input" % (summary, self.script_file_path))

                # else use single "Function-Jira Key" mapping method
                else:
                    summary = summary.replace(" ", "_") + "_" + row["Test ID"].split("_")[-1]
                    test_function_name = "test_" + summary
                    # write mapping if a row has JIRA Key and single function is found is script
                    if not pd.isnull(row["JIRA Key"]) and test_function_name in test_func_list:
                        mapping_dict[test_function_name] = row["JIRA Key"]
                    elif test_function_name in test_func_list:
                        mapping_dict[test_function_name] = ""
                    else:
                        print("%s not found in %s, skip input" % (summary, self.script_file_path))
            if self.project_type == "bgm":
                mapping_json_path = "../../project/bgm/config/bgm_test_id_list.json"
            elif self.project_type == "cgw":
                mapping_json_path = "../../project/cgw_oncar/config/oncar_test_id_list.json"
            else:
                mapping_json_path = "../../project/bgm/config/bgm_test_id_list.json"

            test_file_name = self.script_file_path[self.script_file_path.find("test"):]
            with open(mapping_json_path, "r") as f:
                data = json.load(f)
                if test_file_name in data:
                    logger.info("%s already in json file, adding new mapping pairs" % test_file_name)
                    for test_function_name in mapping_dict:
                        if isinstance(mapping_dict[test_function_name], str):
                            data[test_file_name][test_function_name] = mapping_dict[test_function_name]
                        elif isinstance(mapping_dict[test_function_name], dict):
                            if test_function_name in data[test_file_name]:
                                for parameter in mapping_dict[test_function_name]:
                                    data[test_file_name][test_function_name][parameter] = mapping_dict[test_function_name][parameter]
                            else:
                                data[test_file_name][test_function_name] = mapping_dict[test_function_name]
                else:
                    logger.info("%s not found in json file, adding new mapping pairs" % test_file_name)
                    data[test_file_name] = mapping_dict
                f = open(mapping_json_path, "w")
                json.dump(data, f, indent=1)

    def jira_read_single_issue(self, jira_ticket):
        if not self.username:
            raise Exception("No username provided, Login failed")
        elif not self.password:
            self.password = getpass("Username provided without password, please input your password\n")

        nio_jira = JIRA(server="https://jira.nioint.com/", auth=(self.username, self.password))
        issue = nio_jira.issue(jira_ticket)
        for field_name in issue.raw['fields']:
            if issue.raw['fields'][field_name]:
                print("Field:", field_name, "Value:", issue.raw['fields'][field_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, help='who is using this script?')
    parser.add_argument('--password', type=str, help='password of username')
    parser.add_argument('--case_file_path', type=str, help='test case source csv')
    parser.add_argument('--script_file_path', type=str, help='target script path')
    parser.add_argument('--project_type', type=str, help='pcan_type will be used', default='bgm')
    parser.add_argument('--import_jira_only', type=bool, help='Whether program will import jira ticket', default=False)
    parser.add_argument('--generate_xray_json_only', type=bool, help='Whether program will upload json file',
                        default=False)

    args = parser.parse_args()
    uploader = UploadTestSpecXlsmtoXray(username=args.username, password=args.password,
                                        case_file_path=args.case_file_path, script_file_path=args.script_file_path,
                                        project_type=args.project_type)

    if args.import_jira_only:
        uploader.import_xlsm_to_jira()
    elif args.generate_xray_json_only:
        uploader.generate_mapping_table()
    else:
        df = uploader.import_xlsm_to_jira()
        uploader.generate_mapping_table(df)

    #testing command
    # uploader.jira_read_single_issue("DSTMS-6262")