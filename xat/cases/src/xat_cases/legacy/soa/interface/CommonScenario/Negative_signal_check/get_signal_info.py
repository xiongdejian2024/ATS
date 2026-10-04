# -*- coding: utf-8 -*-

"""
@Time    : 2024/06/03 11:55
@Author  : lei.tao
@Email   : lei.tao@jiduauto.com
"""
import sys
import json
import os
import time
import xlrd2
import openpyxl
import pandas as pd


current_path = os.path.dirname(os.path.realpath(__file__))


def get_caseinfo_from_sdbsignals(file, sheet_name):
    """
    获取sdbsignals表格中的服务接口信号信息
    """
    excel_path = current_path.split("sat")[0] + file
    wb1 = xlrd2.open_workbook(excel_path)
    sheet = wb1.sheet_by_name(sheet_name)
    testcases_list = {}
    num_rows = sheet.nrows
    for i in range(1, num_rows):
        if "{" in sheet.cell_value(i, 16):
            testcases_begin = (
                sheet.cell_value(i, 0),
                sheet.cell_value(i, 1),
                sheet.cell_value(i, 2),
                sheet.cell_value(i, 3),
                sheet.cell_value(i, 4)
            )
            testcases_list[testcases_begin] = (
                    sheet.cell_value(i, 15),
                    sheet.cell_value(i, 16)
            )

    return testcases_list


def put_caseinfo_into_ms(sdbsignals_file, ms_file):
    """
    把sdbsignals表格中的服务接口信号信息转换成ms格式的用例
    """
    wb = openpyxl.load_workbook(current_path.split("sat")[0] + ms_file)
    sheet = wb.active
    header = []
    if not header:
        for c in range(1, sheet.max_column + 1):
            val = sheet.cell(1, c).value
            if val:
                header.append(val)
    ms_excel_path = current_path.split("sat")[0] + f"sign_{ms_file}"
    if os.path.exists(ms_excel_path):
        os.system(f"rm -rf {ms_excel_path}")
    wb.save(filename=ms_excel_path)
    # 只需要关注Mars1 sheet页
    for sdbsignals_sheet in ["Venus"]:
        data_list = get_caseinfo_from_sdbsignals(sdbsignals_file, sdbsignals_sheet)
        print(f"需要更新的{sdbsignals_sheet}信号数据：{data_list}")

        data = pd.read_excel(ms_excel_path, keep_default_na=True)
        data_dict = data.to_dict()
        print(data_dict)
        for key in enumerate(data_list.items()):
            print(f"开始插入数据：{key}")
            service_name = key[-1][0][0]
            interface_name = key[-1][0][1]
            signal_name = key[-1][0][2]
            network_name = key[-1][0][3]
            message_name = key[-1][0][4]

            result = key[-1][-1][1]
            col = len(data)

            # 插入用例名称，步骤和预期结果
            data.loc[key[0] + col, "用例名称"] = (
                f"{service_name}::{interface_name}_{signal_name}::{network_name}::{message_name}信号为负值时无异常"
            )
            if "info" in result:
                data.loc[key[0] + col, "步骤描述"] = (
                    f"【1】设置信号{signal_name}为0.0\
                    \n【2】设置信号{signal_name}为-1.0，观察partner事件\
                    \n【3】设置信号{signal_name}为0.0"
                )
                data.loc[key[0] + col, "预期结果"] = (
                    f"【1】NA\
                    \n【2】partner校验到{interface_name}事件{result}\
                    \n【3】NA"
                    )
            else:
                if ";" in result:
                    data.loc[key[0] + col, "步骤描述"] = (
                        f"【1】设置信号{signal_name}为0.0\
                        \n【2】设置信号{signal_name}为-1.0，调用接口{interface_name}，入参{result.split(';')[0]}，观察partner事件\
                        \n【3】设置信号{signal_name}为0.0"
                    )
                    data.loc[key[0] + col, "预期结果"] = (
                        f"【1】NA\
                        \n【2】partner返回结果{result.split(';')[1]}\
                        \n【3】NA"
                        )
                else:
                    data.loc[key[0] + col, "步骤描述"] = (
                        f"【1】设置信号{signal_name}为0.0\
                        \n【2】设置信号{signal_name}为-1.0，调用接口{interface_name}，观察partner事件\
                        \n【3】设置信号{signal_name}为0.0"
                    )
                    data.loc[key[0] + col, "预期结果"] = (
                        f"【1】NA\
                        \n【2】partner返回结果{result}\
                        \n【3】NA"
                        )
            
            # 插入前置条件
            data.loc[key[0] + col, "前置条件"] = key[-1][-1][0]
            # 其他列填入默认值
            data.loc[key[0] + col, "所属模块"] = (
                "/SOA服务接口/通用场景/信号组包含负数的场景/AllService"
            )
            data.loc[key[0] + col, "整车版本"] = '["V2.0.0 Beta2"]'
            data.loc[key[0] + col, "编辑模式"] = "STEP"
            data.loc[key[0] + col, "标签"] = "two_domain"
            data.loc[key[0] + col, "用例类型"] = "接口用例"
            data.loc[key[0] + col, "责任人"] = "陶磊 Lei(SOA)"
            data.loc[key[0] + col, "用例等级"] = "P3"
            data.loc[key[0] + col, "适用范围"] = "Full"
            data.loc[key[0] + col, "业务级别"] = "[PlatformTest-SOA]"
            data.loc[key[0] + col, "Automation"] = "Automated"
            data.loc[key[0] + col, "测试平台"] = "Bench"
            data.loc[key[0] + col, "函数名称"] = interface_name
            data.loc[key[0] + col, "适用车型"] = '["Mars One"]'

        data.to_excel(ms_excel_path, index=False)


def write_template(
    data,
    before_info=None,
    id=None,
    service_name=None,
    interface_name=None,
    network_name=None,
    message_id=None,
    signal=None,
    case_name=None,
    out=None
):
    file = os.path.join(current_path, "test_signal_is_negative.py")

    if not os.path.exists(file):
        with open(file, "w") as f:
            pass

    with open(file, "a") as fd:
        for i in data:
            if "{ID}" in i:
                fd.write(i.replace("{ID}", id))
            elif "{service}" in i:
                fd.write(i.replace("{service}", service_name))
            elif "{service_name}" in i:
                fd.write(i.replace("{service_name}", '"' + service_name + '"'))
            elif "{network_name}" and "{signal}" in i:
                fd.write(
                    i.replace("{network_name}", network_name.lower()).replace(
                        "{signal}", '"' + signal + '"'
                    )
                )
            elif "{network_name}" and "{message_id}" in i:
                fd.write(
                    i.replace(
                        "{network_name}", '"' + network_name.lower() + '"'
                    ).replace("{message_id}", '"' + message_id + '"')
                )
            elif "{network_name}" and 'f"{msg_id}"' in i:
                fd.write(i.replace("{network_name}", '"' + network_name.lower() + '"'))

            elif "{before_info}" in i:
                if isinstance(before_info, str):
                    if len(before_info.split('\n')) == 1:
                        fd.write(i.replace("{before_info}", before_info))
                    else:
                        fd.write(i.replace("{before_info}", before_info.split('\n')[0] + "\n" + 8 * " " + ("\n" + 8 * " ").join(before_info.split('\n')[1:])))
                # else:
                #     fd.write(i.replace("{before_info}", ""))

            elif "{out}" in i:
                if interface_name.lower().startswith("get"):
                    if out[0]:
                        fd.write(
                            i.replace("{ck_s2s}", "send_request_and_ck_resp")
                            .replace("{interface_name}", '"' + interface_name + '"')
                            .replace("{out}", out[-1].strip())
                            .replace("{}", ", " + out[0])
                        )
                    else:
                        fd.write(
                            i.replace("{ck_s2s}", "send_request_and_ck_resp")
                            .replace("{interface_name}", '"' + interface_name + '"')
                            .replace("{out}", out[-1].strip())
                            .replace("{}", ", {}")
                        )
                else:
                    fd.write(
                        i.replace("{ck_s2s}", "ck_s2s_event")
                        .replace("{interface_name}", '"' + interface_name + '"')
                        .replace("{out}", out[-1].strip())
                        .replace("{}", "")
                    )
            elif '{case_name}' in i:
                fd.write(i.replace('{case_name}', '"' + case_name + '"'))
            else:
                fd.write(i)


def put_case_into_python(ms_file):
    """
    把ms用例输出成python脚本到test_signal_jump_check_event.py
    需要下载ms上带caseid的excel表格
    """
    # 生成所有适用mars1车型的脚本
    case_info = pd.read_excel(
        os.path.join(current_path.split("sat")[0], ms_file),
        sheet_name="Sheet1",
        keep_default_na=True,
    )
    case_data_dict = case_info.to_dict()
    service_name_begin = ""

    with open(os.path.join(current_path, "update_template.txt"), "r") as fd:
        lines = fd.readlines()
        template_from = lines[:14]
        template_class = lines[14:35]
        template_method = lines[35:] + ["\n"]
        write_template(template_from)
        for i in range(len(case_data_dict["ID"])):
            id = str(case_data_dict["ID"][i])
            before_info = case_data_dict["前置条件"][i]
            service_name = case_data_dict["用例名称"][i].split("::")[0]
            interface_name = case_data_dict["用例名称"][i].split("::")[1].split("_")[0]
            signal_name = case_data_dict["用例名称"][i].split("::")[1].split("_")[-1]
            network_name = case_data_dict["用例名称"][i].split("::")[2]
            message_ID = case_data_dict["用例名称"][i].split("::")[3].split("信号")[0]
            if "入参" in case_data_dict["步骤描述"][i]:
                args_2 = (
                    case_data_dict["步骤描述"][i]
                    .split("，观察partner事件")[0]
                    .split("入参")[-1]
                )
            else:
                args_2 = None
            if "事件" in case_data_dict["预期结果"][i]:
                result_2 = (
                    case_data_dict["预期结果"][i]
                    .split("事件")[1]
                    .split("【3】")[0]
                    .replace("，", ",")
                )
            else:
                result_2 = (
                    case_data_dict["预期结果"][i]
                    .split("【2】partner返回结果")[-1]
                    .split("【3】")[0]
                    .replace("，", ",")
                )
            out = [args_2, result_2]

            if service_name != service_name_begin:
                write_template(
                    template_class,
                    before_info,
                    id,
                    service_name,
                    interface_name,
                    network_name,
                    message_ID,
                    signal_name,
                    case_data_dict['用例名称'][i],
                    out,
                )
            service_name_begin = service_name
            write_template(
                template_method,
                before_info,
                id,
                service_name,
                interface_name,
                network_name,
                message_ID,
                signal_name,
                case_data_dict['用例名称'][i],
                out,
            )


def change_intercasename_reqid(from_file, ms_file):
    """
    修改case的req和接口名称信息
    """
    # 获取需要修改REQ和接口名称的case信息
    case_info = pd.read_excel(
        os.path.join(current_path.split("sat")[0], ms_file), keep_default_na=True
    )
    case_data_dict = case_info.to_dict()
    # 获取所有ms上接口中的case信息
    from_case_info = pd.read_excel(
        os.path.join(current_path.split("sat")[0], from_file), keep_default_na=True
    )
    from_dict = from_case_info.to_dict()
    # 开始修改REQ和接口名称的case信息
    for i in range(len(case_data_dict["用例名称"])):
        for j in range(len(from_dict["ID"])):

            if case_data_dict["函数名称"][i] == from_dict["函数名称"][j]:
                case_info.loc[i, "JamaReqID"] = from_dict["JamaReqID"][j]
                case_info.loc[i, "接口名称"] = from_dict["接口名称"][j]
            elif case_data_dict["函数名称"][i] == from_dict["接口名称"][j]:
                case_info.loc[i, "JamaReqID"] = from_dict["JamaReqID"][j]
                case_info.loc[i, "接口名称"] = from_dict["函数名称"][j]
            elif case_data_dict["函数名称"][i] in str(from_dict["函数名称"][j]).replace(
                "，", ","
            ).split(","):
                case_info.loc[i, "JamaReqID"] = from_dict["JamaReqID"][j]
                case_info.loc[i, "接口名称"] = from_dict["接口名称"][j]
            elif case_data_dict["函数名称"][i] in str(from_dict["接口名称"][j]).replace(
                "，", ","
            ).split(","):
                case_info.loc[i, "JamaReqID"] = from_dict["JamaReqID"][j]
                case_info.loc[i, "接口名称"] = from_dict["接口名称"][j]

    case_info.to_excel(os.path.join(current_path.split("sat")[0], ms_file), index=False)


if __name__ == "__main__":
    # put_caseinfo_into_ms("信号组包含负数的服务接口.xlsx", "Metersphere_case_SOA平台测试.xlsx")
    # change_intercasename_reqid("caseid_Metersphere_case_SOA平台测试.xlsx", "E2E_Metersphere_case_SOA平台测试.xlsx")
    # 需要分开跑，下面需上传ms后获取caseid再下载下来生成脚本
    put_case_into_python("sign_Metersphere_case_SOA平台测试.xlsx")
