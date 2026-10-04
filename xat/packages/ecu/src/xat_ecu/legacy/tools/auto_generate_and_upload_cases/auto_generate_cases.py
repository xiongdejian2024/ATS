#!/usr/bin/python3
"""
@File        : auto_generate_cases.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/02/17 19:00
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
import copy


class Auto_Generate_Cases():
    def __init__(self, story_file_path=None, case_file_path=None):
        self.case_file_path = case_file_path.strip() if case_file_path else None
        self.story_file_path = story_file_path.strip() if story_file_path else None
        self.key_column_dict = {}
        self.excel_template_data = []

    def get_data_form_6185_story_file(self):
        # DTC
        data_info = []
        with open(self.story_file_path, "r") as f:
            story_lines = f.readlines()
            story_re = r'<td class="confluenceTd">(.+?)<'
            i = 0
            for story_line in story_lines:
                if "</del></td>" not in story_line:
                    if '<td class="confluenceTd">' in story_line:
                        story_line = story_line.replace("&nbsp;", "")
                        result = re.search(story_re, story_line)
                        if result:
                            story = result.group(1)
                            dtc_data = self.get_dtc_data(story)
                            if dtc_data:
                                dtc_info = []
                                dtc_info.append(dtc_data)
                                i = 4
                            if i > 0 and i < 5:
                                if i != 4:
                                    dtc_info.append(story)
                                if i == 1:
                                    data_info.append(dtc_info)
                                i -= 1
        return data_info

    def get_dtc_data(self, story_str):
        """
        D39F-83
        LCM_P communication error
        LCMPResponseErr ==1 is received for 5 times continously(LCM_D_BGM_02)
        Once LCMPResponseErr ==0 is received.
        D3AC-87
        Communication lost with DHS_FL
        LIN frame "DHS_FL_BGM_01" missed 10 times continously
        Once LIN frame "DHS_FL_BGM_01" received.
        """
        dtc_re = r"(\w{2})(\w{2})-(\w{2})"
        result = re.match(dtc_re, story_str)
        if result:
            result_list = result.groups()
            dtc_list = "[0x{0}, 0x{1}, 0x{2}]".format(result_list[0], result_list[1], result_list[2])
            return dtc_list
        else:
            return result

    def get_signal_from_str(self, data_str):
        # print(data_str)
        signal_re = r"(\w+).*?=1"
        result = re.findall(signal_re, data_str)
        # print(result)
        if result:
            return result[0]
        else:
            return None

    def get_key_column_dict(self, sh):
        row_1 = sh[1]
        i = 0
        for cell in row_1:
            if cell.value == "Summary":
                self.key_column_dict["Summary"] = i
            elif cell.value == "Action":
                self.key_column_dict["Action"] = i
            elif cell.value == "Expected Result":
                self.key_column_dict["Expected Result"] = i
            i += 1
        return self.key_column_dict

    def get_excel_template_data(self, sh):
        max_row = sh.max_row
        rows = sh[2: max_row]
        for row in rows:
            row_value = []
            for cell in row:
                row_value.append(cell.value)
            self.excel_template_data.append(row_value)
        sh.delete_rows(2, max_row)
        return self.excel_template_data

    def modify_cases_data(self, dtc_datas):
        # excel_template_data   and   dtc_datas
        new_excel_data_list = []
        summary_num = self.key_column_dict["Summary"]
        action_num = self.key_column_dict["Action"]
        expected_result_num = self.key_column_dict["Expected Result"]
        if "lost" in self.case_file_path:
            for dtc_data in dtc_datas:
                if "lost" in dtc_data[1]:
                    for excel_template_data_list in self.excel_template_data:
                        new_datas = copy.deepcopy(excel_template_data_list)

                        new_data = new_datas[summary_num].replace("DTC Communication lost with DSM", dtc_data[1])
                        del new_datas[summary_num]
                        new_datas.insert(summary_num, new_data)

                        new_data = new_datas[expected_result_num].replace("[0xD3, 0x5E, 0x87]", dtc_data[0])
                        del new_datas[expected_result_num]
                        new_datas.insert(expected_result_num, new_data)

                        new_excel_data_list.append(new_datas)
        elif "error" in self.case_file_path:
            for dtc_data in dtc_datas:
                if "error" in dtc_data[1]:
                    signal = self.get_signal_from_str(dtc_data[2])
                    if signal is None:
                        print("Warning : Do not Match signal")
                    for excel_template_data_list in self.excel_template_data:
                        new_datas = copy.deepcopy(excel_template_data_list)

                        new_data = new_datas[summary_num].replace("DTC RLS communication error", dtc_data[1])
                        del new_datas[summary_num]
                        new_datas.insert(summary_num, new_data)

                        new_data = new_datas[action_num].replace("RlsLINResponseError", signal)
                        del new_datas[action_num]
                        new_datas.insert(action_num, new_data)

                        new_data = new_datas[expected_result_num].replace("[0xD3, 0x61, 0x83]", dtc_data[0])
                        del new_datas[expected_result_num]
                        new_datas.insert(expected_result_num, new_data)
                        new_excel_data_list.append(new_datas)
        return new_excel_data_list

    def write_data_into_excel(self):
        testfile = openpyxl.load_workbook(self.case_file_path, keep_vba=True)
        sheet_all_names = testfile.sheetnames
        for sh_name in sheet_all_names:
            sh = testfile[sh_name]
            self.get_key_column_dict(sh)
            self.get_excel_template_data(sh)
            dtc_datas = self.get_data_form_6185_story_file()
            excel_data = self.modify_cases_data(dtc_datas)
            for data in excel_data:
                sh.append(data)
        self.case_file_path = self.case_file_path.replace("-Template", "")
        testfile.save(self.case_file_path)

if __name__ == "__main__":
    # work dir:  compass     only for BGM
    # Command:
    #       python3 ecu_simulator/tools/auto_generate_and_upload_cases/auto_generate_cases.py
    #       --story_file_path="/root/BGM-6158源码.txt"
    #       --case_file_path="/root/BGM-VB-DIAG-DTC-BGM-6158-lin-lost-Template.xlsm"

    parser = argparse.ArgumentParser()
    parser.add_argument('--story_file_path', type=str, help='stroy file path')
    parser.add_argument('--case_file_path', type=str, help='test case source')


    args = parser.parse_args()
    generater = Auto_Generate_Cases(story_file_path=args.story_file_path, case_file_path=args.case_file_path)

    generater.write_data_into_excel()

