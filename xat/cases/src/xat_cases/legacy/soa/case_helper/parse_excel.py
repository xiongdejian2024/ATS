# -*- coding: utf-8 -*-
"""
@File        : common_lib.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2023/05/24 14:00 PM
@Description : Extract data from Excel
"""

import os
import xlrd2

caseid = 0

conf_file_name = r"soa_testcase_conf.xlsx"
conf_file_path = "sat/xat_cases/legacy/test_data/soa"


class excelCase:
    def __init__(
        self,
        case_id,
        case_name,
        pre_condition,
        action,
        check_result,
    ):
        self.case_id = case_id
        self.case_name = case_name
        self.pre_condition = pre_condition
        self.action = action
        self.check_result = check_result


def get_testconfig_by_read_excel_new(excel_path, sheet_name):
    """
    读取excel获取excel中的测试用例，返回测试用例集
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases_list = []
    testcaseid_list = []
    num_rows = sheet1.nrows
    pre_condition_list = []
    action_list = []
    check_result_list = []
    global caseid
    for j1 in range(1, num_rows):
        case_id = str(sheet1.cell_value(j1, 0))
        if j1 == 1:
            pass
        elif case_id.upper() == "END":
            test_case = excelCase(
                caseid,
                case_name,
                pre_condition_list,
                action_list,
                check_result_list,
            )
            testcases_list.append(test_case)
            testcaseid_list.append(test_case.case_id)
            pre_condition_list = []
            action_list = []
            check_result_list = []
            continue

        elif case_id != "" and case_id != str(sheet1.cell_value(j1 - 1, 0)):
            test_case = excelCase(
                caseid,
                case_name,
                pre_condition_list,
                action_list,
                check_result_list,
            )
            testcases_list.append(test_case)
            testcaseid_list.append(test_case.case_id)
            pre_condition_list = []
            action_list = []
            check_result_list = []

        if case_id != "":
            caseid = case_id.split(".")[0]
            case_name = sheet1.cell_value(j1, 1)
            pre_condition = sheet1.cell_value(j1, 2)
            action = sheet1.cell_value(j1, 3)
            check_result = sheet1.cell_value(j1, 4)
            pre_condition_list.append(pre_condition)
            action_list.append(action)
            check_result_list.append(check_result)
        else:
            pre_condition = sheet1.cell_value(j1, 2)
            action = sheet1.cell_value(j1, 3)
            check_result = sheet1.cell_value(j1, 4)
            pre_condition_list.append(pre_condition)
            action_list.append(action)
            check_result_list.append(check_result)
            continue
    return testcases_list, testcaseid_list


def get_testconfig_by_read_excel(excel_path, sheet_name):
    """
    读取excel获取excel中的测试用例，返回测试用例集
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases_list = []
    testcaseid_list = []
    num_rows = sheet1.nrows
    action_list = []
    check_result_list = []
    global caseid
    for j1 in range(1, num_rows):
        case_id = str(sheet1.cell_value(j1, 0))
        if j1 == 1:
            pass
        elif case_id.upper() == "END":
            test_case = excelCase(
                caseid,
                case_name,
                pre_condition,
                action_list,
                check_result_list,
            )
            testcases_list.append(test_case)
            testcaseid_list.append(test_case.case_id)
            action_list = []
            check_result_list = []
            continue

        elif case_id != "" and case_id != str(sheet1.cell_value(j1 - 1, 0)):
            test_case = excelCase(
                caseid,
                case_name,
                pre_condition,
                action_list,
                check_result_list,
            )
            testcases_list.append(test_case)
            testcaseid_list.append(test_case.case_id)
            action_list = []
            check_result_list = []

        if case_id != "":
            caseid = case_id.split(".")[0]
            case_name = sheet1.cell_value(j1, 1)
            pre_condition = sheet1.cell_value(j1, 2)
            action = sheet1.cell_value(j1, 3)
            check_result = sheet1.cell_value(j1, 4)
            action_list.append(action)
            check_result_list.append(check_result)
        else:
            action = sheet1.cell_value(j1, 3)
            check_result = sheet1.cell_value(j1, 4)
            action_list.append(action)
            check_result_list.append(check_result)
            continue
    return testcases_list, testcaseid_list


def get_msgname_by_read_excel_baseon_busname(
    signal_name, bus_name, excel_path=conf_file_name
):
    """
    读取excel获取excel中的测试用例，返回测试用例集
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(str.lower(bus_name))
    num_rows = sheet1.nrows
    num_cols = sheet1.ncols
    posdic = {}
    for i in range(num_cols):
        if sheet1.cell_value(0, i) == "Frame":
            posdic["Frame"] = i
        elif sheet1.cell_value(0, i) == "Sig":
            posdic["Sig"] = i
        elif sheet1.cell_value(0, i) == "Bus":
            posdic["Bus"] = i
        elif sheet1.cell_value(0, i) == "FrameID":
            posdic["FrameID"] = i

    for line_num in range(1, num_rows + 1):
        if line_num == num_rows:
            return "NotFound"
        elif sheet1.cell_value(line_num, posdic["Sig"]) == signal_name and str.upper(
            sheet1.cell_value(line_num, posdic["Bus"])
        ) == str.upper(bus_name):
            return [
                sheet1.cell_value(line_num, posdic["Frame"]),
                sheet1.cell_value(line_num, posdic["FrameID"]),
            ]


# if __name__ == '__main__':
#     # testcases = get_testconfig_by_read_excel(r"soa_testcase_conf.xlsx", "door")
#     # print("读取到的用例总数：{}".format(len(testcases)))
#     # for i in range(len(testcases)):
#     #     print(testcases[i].case_id)
#     #     print(testcases[i].case_name)
#     #     print(testcases[i].pre_condition)
#     #     print(testcases[i].action)
#     #     print(testcases[i].check_result)
#     pass
