# -*- coding: utf-8 -*-
"""
@File        : common_lib.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2023/04/25 10:00 PM
@Description : Do some general data processing operations
"""

from time import sleep
import pytest
import os
import xlrd2
import json

conf_file_path = "sat/xat_cases/legacy/test_data/soa"


def dealwith_service_parameter(service_parameter, service_name_type):
    parameterDic = {}
    if len(service_parameter) > 0:
        data = service_parameter.split(';')
        for i in range(len(data)):
            data[i] = str.strip(data[i])

        for i in range(len(data)):
            tem_list = data[i].split(':')
            if len(tem_list) == 2:
                name = tem_list[0]
                value = tem_list[1]
            elif len(tem_list) > 2:
                name = tem_list[0]
                value = data[i][len(name) + 1 :]
            else:
                print("Input paramater Error")

            parameterDic["serviceName"] = service_name_type[0]
            parameterDic["mode"] = service_name_type[1]
            if str.upper(name) == "FUNCTIONNAME":
                parameterDic["functionName"] = value
            if str.upper(name) == "PARAMS":
                parameterDic["params"] = value
            if str.upper(name) == "OPERATION":
                parameterDic["operation"] = value
            if str.upper(name) == "CHECK_INFO":
                parameterDic["check_info"] = value
    return parameterDic


# def dealwith_service_parameter(service_parameter):
#     parameterDic = {}
#     if len(service_parameter) > 0:
#         data = service_parameter.split(';')
#         for i in range(len(data)):
#             data[i] = str.strip(data[i])

#         for i in range(len(data)):
#             tem_list = data[i].split(':')
#             if len(tem_list) == 2:
#                 name = tem_list[0]
#                 value = tem_list[1]
#             elif len(tem_list) > 2:
#                 name = tem_list[0]
#                 value = data[i][len(name) + 1 :]
#             else:
#                 print("Input paramater Error")

#             if str.upper(name) == "SERVICENAME":
#                 parameterDic["serviceName"] = value
#             if str.upper(name) == "MODE":
#                 parameterDic["mode"] = value
#             if str.upper(name) == "FUNCTIONNAME":
#                 parameterDic["functionName"] = value
#             if str.upper(name) == "PARAMS":
#                 parameterDic["params"] = value
#             if str.upper(name) == "OPERATION":
#                 parameterDic["operation"] = value
#             if str.upper(name) == "CHECK_INFO":
#                 parameterDic["check_info"] = value
#     return parameterDic


def dealwith_singal_parameter(signal_parameter):
    parameterList = []
    if len(signal_parameter) > 0:
        data2 = signal_parameter.split(';')
        for i in range(len(data2)):
            data2[i] = str.strip(data2[i])

        for i in range(len(data2)):
            tempDic = {}
            data3 = data2[i].split(':')
            if str.upper(data3[0]) == "USAGEMODE" or str.upper(data3[0]) == "CARMODE":
                tempDic["name"] = data3[0]
                tempDic["value"] = data3[1]
                tempDic["bus_name"] = "NA"
            elif str.upper(data3[0]).find("IO-") != -1:
                tempDic["name"] = data3[0]
                tempDic["value"] = data3[1]
                tempDic["bus_name"] = "NA"
            elif str.upper(data3[0]) == "SLEEP":
                tempDic["name"] = data3[0]
                tempDic["value"] = float(data3[1])
                tempDic["bus_name"] = "NA"
            elif str.upper(data3[0]).find("CCP") != -1:
                tempDic["name"] = data3[0]
                tempDic["value"] = data3[1]
                tempDic["bus_name"] = "NA"
            elif data3[0].find("(") != -1:
                pos1 = data3[0].find("(")
                pos2 = data3[0].find(")")
                tempDic["name"] = data3[0][:pos1]
                tempDic["value"] = data3[1]
                tempDic["bus_name"] = data3[0][pos1 + 1 : pos2]

                if "." in tempDic["value"]:
                    tempDic["value"] = float(tempDic["value"])
                else:
                    tempDic["value"] = int(tempDic["value"])
            else:
                print("Input paramater Error")
                break
            parameterList.append(tempDic)
    return parameterList


def dealwith_check_signal(check_signal_parameter):
    parameterList = []
    if len(check_signal_parameter) > 0:
        data2 = check_signal_parameter.split(';')
        for i in range(len(data2)):
            data2[i] = str.strip(data2[i])
        for i in range(len(data2)):
            tempDic = {}
            data3 = data2[i].split(':')
            if data3[0].find("(") != -1:
                pos1 = data3[0].find("(")
                pos2 = data3[0].find(")")
                bus_msg_name = data3[0][pos1 + 1 : pos2]
                tmp_list = bus_msg_name.split("-")
                tempDic["sig_name"] = str.strip(data3[0][:pos1])
                tempDic["sig_value"] = str.strip(data3[1])
                tempDic["msg_name"] = str.strip(tmp_list[1])
                tempDic["bus_name"] = str.strip(tmp_list[0])
            else:
                print("Input paramater Error")
                break
            if "." in tempDic["sig_value"]:
                tempDic["sig_value"] = float(tempDic["sig_value"])
            else:
                tempDic["sig_value"] = int(tempDic["sig_value"])
            parameterList.append(tempDic)
    return parameterList


def dealwith_usb_relay_setting(port_num, status_str):
    if port_num.upper() == "J3-21":
        operation_obj = "driver_door_ajar"
    elif port_num.upper() == "J3-08":
        operation_obj = "passenger_door_ajar"
    elif port_num.upper() == "J3-12":
        operation_obj = "left_rear_door_ajar"
    elif port_num.upper() == "J3-09":
        operation_obj = "right_rear_door_ajar"
    elif port_num.upper() == "J3-37":
        operation_obj = "hood_ajar_1"
    elif port_num.upper() == "J3-36":
        operation_obj = "hood_ajar_2"
    elif port_num.upper() == "J3-34":
        operation_obj = "trunk_ajar"
    elif port_num.upper() == "J3-26":
        operation_obj = "charge_lid_switch"
    elif port_num.upper() == "J3-31":
        operation_obj = "trunk_unlock_ext_button"
    elif port_num.upper() == "J3-39":
        operation_obj = "driver_door_handle"
    elif port_num.upper() == "J3-38":
        operation_obj = "passenger_door_handle"
    elif port_num.upper() == "J3-41":
        operation_obj = "left_rear_door_handle"
    elif port_num.upper() == "J3-40":
        operation_obj = "right_rear_door_handle"
    elif port_num.upper() == "J3-35":
        operation_obj = "driver_occupy_sensor"
    elif port_num.upper() == "J3-07":
        operation_obj = "hazard_switch"
    elif port_num.upper() == "J3-20":
        operation_obj = "horn_switch"
    elif port_num.upper() == "DDM C16":
        operation_obj = "driver_door_open"
    elif port_num.upper() == "PDM C16":
        operation_obj = "passenger_door_open"
    elif port_num.upper() == "RLDM B6":
        operation_obj = "left_rear_door_open"
    elif port_num.upper() == "RRDM B6":
        operation_obj = "right_rear_door_open"
    else:
        operation_obj = "NotFound"

    if status_str.strip().upper() == "OPEN":
        status = False
    elif status_str.strip().upper() == "CLOSE":
        status = True
    else:
        status = "NotFound"

    return (operation_obj, status)


def analysis_usage_mode(paras):
    if "ABAND" in str.upper(paras):
        usagemode_value = 0
    elif "INACT" in str.upper(paras):
        usagemode_value = 1
    elif "CONV" in str.upper(paras):
        usagemode_value = 2
    elif "ACT" in str.upper(paras):
        usagemode_value = 11
    elif "DRIV" in str.upper(paras):
        usagemode_value = 13
    else:
        usagemode_value = "NOK"
    return usagemode_value


def analysis_car_mode(paras):
    if "NORM" in str.upper(paras):
        carmode_value = 0
    elif "TRANS" in str.upper(paras):
        carmode_value = 1
    elif "FAC" in str.upper(paras):
        carmode_value = 2
    elif "CRA" in str.upper(paras):
        carmode_value = 3
    elif "DYNO" in str.upper(paras):
        carmode_value = 5
    else:
        carmode_value = "NOK"
    return carmode_value


def check_and_transfer_data(str_data):
    try:
        int(str_data)
        return int(str_data)
    except Exception:
        try:
            return float(str_data)
        except Exception:
            return str_data


def json_read_to_dic(file_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    json_file_path = os.path.join(parent_dir, file_path)
    with open(json_file_path, 'r', encoding='utf8') as fp1:
        # loads() :将json字符串转换成字典格式
        json_data_dic = json.load(fp1)
        return json_data_dic


def dic_save_as_json(dic_obj, file_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    json_file_path = os.path.join(parent_dir, file_path)
    with open(json_file_path, "w") as js:
        jsondata = json.dumps(dic_obj)
        js.write(jsondata)


def get_type_cont(conf_cont):
    conf_list_temp = conf_cont.split(":", 1)
    typeval = conf_list_temp[0]
    cont = conf_list_temp[1][1:-1]
    return (typeval, cont)


def get_service_params(conf_dic_obj):
    serviceName = conf_dic_obj['serviceName']
    mode = conf_dic_obj['mode']
    functionName = conf_dic_obj['functionName']
    params = eval(conf_dic_obj['params'])
    operation = conf_dic_obj['operation']
    if "check_info" in conf_dic_obj.keys():
        check_info = conf_dic_obj['check_info']
        return [serviceName, mode, functionName, params, operation, check_info]
    else:
        return [serviceName, mode, functionName, params, operation]


# if __name__ == "__main__":
#     a = 'UsageMode:Convenience;CarMode:Normal;CCP_98:02;IceBreakDoorDrvrActv(bodycan):1;VehMtnStVehMtnSt(backbonefr):3;GearLvrIndcn(backbonefr):0;TrsmParkLockdTrsmParkLockd(backbonefr):0;TrOpenerSts(bodycan):0'

#     b = dealwith_singal_parameter(a)
#     print(b)
