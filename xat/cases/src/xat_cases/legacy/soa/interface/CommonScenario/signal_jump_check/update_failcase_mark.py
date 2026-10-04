# -*- coding: utf-8 -*-

"""
@Time    : 2024/06/03 11:55
@Author  : lei.tao
@Email   : lei.tao@jiduauto.com
"""

import os
import time
import pandas as pd

current_path = os.path.dirname(os.path.realpath(__file__))



def update_case_mark(file, sheet):
    """
    更新fail case的mark标签为failed
    """
    case_info = pd.read_excel(os.path.join(current_path.split("sat")[0], file), sheet_name=sheet, keep_default_na=True)
    case_data_dict = case_info.to_dict()
    print(case_data_dict['Caseid'])
    files_list = []
    for home, dirs, files in os.walk(os.path.join(current_path.split("sat")[0], "sat/xat_cases/legacy/soa/interface")):
        for filename in files:
            files_list.append(os.path.join(home, filename))
    
    for k,caseid in case_data_dict['Caseid'].items():
        for file in files_list:
            with open (file, "r") as f:
                lines = f.readlines()
            with open(file, "w", encoding="utf-8") as fd:
                for line, data in enumerate(lines):
                    if f"def test_caseid_{caseid}" in data:
                        fd.write("    @pytest.mark.failed\n")
                    fd.write(data)
        print(f"第{k}条用例标签{caseid}已添加完成")


def delete_case_mark(file, sheet_fail, sheet_double_fail):
    """
    case已稳定
    删除fail case的mark为failed标签
    """
    #第一周失败case
    case_info_fail = pd.read_excel(os.path.join(current_path.split("sat")[0], file), sheet_name=sheet_fail, keep_default_na=True)
    case_data_dict_fail = case_info_fail.to_dict()
    #再次失败case
    case_info_double_fail = pd.read_excel(os.path.join(current_path.split("sat")[0], file), sheet_name=sheet_double_fail, keep_default_na=True)
    case_data_dict_double_fail = case_info_double_fail.to_dict()
    print(case_data_dict_double_fail['Caseid'].values())
    #获取近一周没用失败的case
    case_data_dict = {}
    for k,w in case_data_dict_fail['Caseid'].items():
        if w not in case_data_dict_double_fail['Caseid'].values():
            case_data_dict[k] = w


    print(case_data_dict)
    files_list = []
    for home, dirs, files in os.walk(os.path.join(current_path.split("sat")[0], "sat/xat_cases/legacy/soa/interface")):
        for filename in files:
            files_list.append(os.path.join(home, filename))
    
    for k,caseid in case_data_dict.items():
        for file in files_list:
            with open (file, "r", errors='ignore') as f:
                lines = f.readlines()
            with open(file, "w", encoding="utf-8") as fd:
                for i in range(len(lines)-1):
                    if f"def test_caseid_{caseid}" not in lines[i+1]:
                        fd.write(lines[i])
                    if i == len(lines)-2:
                        fd.write(lines[i+1])
        print(f"第{k}条用例{caseid}已删除完成")


def add_py_default_timeout():
    """
    更新热启动的脚本中增加一条
    self.partner.method_default_timeout = 0.1
    """
    
    files_list = []
    for home, dirs, files in os.walk(os.path.join(current_path.split("sat")[0], "sat/xat_cases/legacy/soa/interface")):
        for filename in files:
            files_list.append(os.path.join(home, filename))
    write_flag = False
    for file in files_list:
        #if "VehicleModeService" in file:
        with open (file, "r") as f:
            lines = f.readlines()
        with open(file, "w", encoding="utf-8") as fd:
            for line, data in enumerate(lines):
                fd.write(data)
                if "super().before_class(self, ecu)" in data:
                    begin = line
                    write_flag = True
                elif "])" in data:
                    end = line
                    for i in range(begin, end+1):
                        if "self.partner" in lines[i] and "S2sBaseClass" in lines[i]:
                        
                            if write_flag:
                                print(lines[i])
                                fd.write("        self.partner.method_default_timeout = 0.1\n")
                                write_flag = False
                            break
                
        print(f"{file}文件已添加完成")


if __name__ == "__main__":
    #update_case_mark("SOA_fail_case.xlsx", "Failcase")
    #delete_case_mark("SOA_fail_case.xlsx", "Failcase", "double_Fail")
    add_py_default_timeout()