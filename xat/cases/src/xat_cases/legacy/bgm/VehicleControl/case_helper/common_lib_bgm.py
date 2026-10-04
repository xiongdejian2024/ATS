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

conf_file_path = r"sat/xat_cases/legacy/test_data/bgm/body_ctrl"


# Function：通过配置文件中服务相关的内容，获取服务相关的参数。
# Input Example：
#       service_parameter:functionName:SetAC;params:{'on':True};operation:method ('ClimateControlService', 'client')
#       service_name_type:
# Output Example：
#        parameterDic：{'serviceName': 'ClimateControlService', 'mode': 'client', 'functionName': 'SetAC', 'params': "{'on':True}", 'operation': 'method'}
def dealwith_service_parameter(service_parameter, service_name_type):
    parameterDic = {}
    if len(service_parameter) > 0:
        if service_parameter.find(";") != -1:
            data = service_parameter.split(';')
            for i in range(len(data)):
                data[i] = str.strip(data[i])
        elif service_parameter.find("/") != -1:
            data = service_parameter.split('/')
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


# Function：通过配置文件中服务相关的内容，获取信号相关的参数。
# Input Example：
#       signal_parameter:UsageMode:Driving;CarMode:Normal;EcoClimaSts(bodycan):0;DrvrSeatVentnLvlSts(bodycan):0;Sleep:3
# Output Example：
#        parameterDic:[{'name': 'UsageMode', 'value': 'Driving', 'bus_name': 'NA'},
#                      {'name': 'CarMode', 'value': 'Normal', 'bus_name': 'NA'},
#                      {'name': 'EcoClimaSts', 'value': 0, 'bus_name': 'bodycan'},
#                      {'name': 'DrvrSeatVentnLvlSts', 'value': 0, 'bus_name': 'bodycan'},
#                      {'name': 'Sleep', 'value': 3.0, 'bus_name': 'NA'}
#                     ]
def dealwith_singal_parameter(signal_parameter):
    parameterList = []
    if len(signal_parameter) > 0:
        data2 = signal_parameter.split(';')
        for i in range(len(data2)):
            data2[i] = str.strip(data2[i])
        for i in range(len(data2)):
            tempDic = {}
            if str.upper(data2[i]).find("SERVICE_") != -1:
                conf_list_temp = data2[i].split(":", 1)
                tempDic["name"] = conf_list_temp[0]
                tempDic["value"] = conf_list_temp[1][1:-1]
                tempDic["bus_name"] = "NA"
                parameterList.append(tempDic)
            else:
                data3 = data2[i].split(':')
                if (
                    str.upper(data3[0]) == "USAGEMODE"
                    or str.upper(data3[0]) == "CARMODE"
                ):
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


# Function：通过配置文件中check_singal相关的内容，获取需要验证的信号相关的参数。
# Input Example：
#       check_signal_parameter:HmiCmptmtTSpForRowFirstLe(bodycan-CEMBodyFr15):16;HmiCmptmtTSpForRowFirstRi(bodycan-CEMBodyFr15):18;HmiCmptmtTSpForRowSecLe(bodycan-CEMBodyFr15):20
# Output Example：
#        parameterList：[{'sig_name': 'HmiCmptmtTSpForRowFirstLe', 'sig_value': 16, 'msg_name': 'CEMBodyFr15', 'bus_name': 'bodycan'}, {'sig_name': 'HmiCmptmtTSpForRowFirstRi', 'sig_value': 18, 'msg_name': 'CEMBodyFr15', 'bus_name': 'bodycan'}, {'sig_name': 'HmiCmptmtTSpForRowSecLe', 'sig_value': 20, 'msg_name': 'CEMBodyFr15', 'bus_name': 'bodycan'}]
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


# Function：通过配置文件的配置来获取设置IO板块或者继电器的接口函数以及状态参数
# Input Example：
#       port_num:J3-21
#       status_str："Close""
# Output Example：
#        (operation_obj, status)：（"driver_door_ajar"，True）
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


# Function：通过usage mode配置文件的字符串参数转换为对应Usage mode的值。
# Input Example：
#       paras:"Driving"
# Output Example：
#        usagemode_value:13
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


# Function：通过car mode配置文件的字符串参数转换为对应car mode的值。
# Input Example：
#       paras:"Normal"
# Output Example：
#        carmode_value:0
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


# Function：数据格式转换
def check_and_transfer_data(str_data):
    try:
        int(str_data)
        return int(str_data)
    except Exception:
        try:
            return float(str_data)
        except Exception:
            return str_data


# Function：将json文件转换为字典
def json_read_to_dic(file_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    json_file_path = os.path.join(parent_dir, file_path)
    with open(json_file_path, 'r', encoding='utf8') as fp1:
        # loads() :将json字符串转换成字典格式
        json_data_dic = json.load(fp1)
        return json_data_dic


# Function：将字典数据保存为json文件
def dic_save_as_json(dic_obj, file_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + conf_file_path
    json_file_path = os.path.join(parent_dir, file_path)
    with open(json_file_path, "w") as js:
        jsondata = json.dumps(dic_obj)
        js.write(jsondata)


# Function：通过配置文件获取操作类型和操作配置
# Input Example：
#       conf_cont:
# Output Example：
#        cont:
def get_type_cont(conf_cont):
    conf_list_temp = conf_cont.split(":", 1)
    typeval = conf_list_temp[0]
    cont = conf_list_temp[1][1:-1]
    return (typeval, cont)


# Function：通过配置文件获取操作类型和操作配置
# Input Example：
#       conf_dic_obj:
# Output Example：
#        [serviceName, mode, functionName, params, operation]:0
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


# def get_signal_times_interval_old(ori_data, check_signal_value):
#     signal_account = 0
#     signal_account_last = 0
#     time_interval = []
#     time_interval_last = []
#     for i in range(len(ori_data)):
#         if ori_data[i][0] == check_signal_value:
#             signal_account = signal_account + 1
#             if signal_account > 1:
#                 time_interval.append(ori_data[i][1] - ori_data[i - 1][1])
#         elif (
#             ori_data[i][0] != check_signal_value
#             and signal_account >= signal_account_last
#         ):
#             signal_account_last = signal_account
#             time_interval_last = time_interval
#             signal_account = 0
#             time_interval = []

#     try:
#         time_interval_max = max(time_interval_last)
#         time_interval_min = min(time_interval_last)
#     except Exception as e:
#         time_interval_max = 0
#         time_interval_min = 0
#     return (signal_account_last, time_interval_max, time_interval_min)


def get_signal_times_interval(ori_data, check_signal_value):
    signal_account = 0
    signal_account_last = 0
    time_interval = []
    time_interval_last = []
    for i in range(len(ori_data)):
        if ori_data[i][0] == check_signal_value:
            signal_account = signal_account + 1
            if signal_account > 1:
                time_interval.append(ori_data[i][1] - ori_data[i - 1][1])
        else:
            if signal_account >= signal_account_last:
                signal_account_last = signal_account
                time_interval_last = time_interval
                signal_account = 0
                time_interval = []
            else:
                signal_account = 0
                time_interval = []

    try:
        time_interval_max = max(time_interval_last)
        time_interval_min = min(time_interval_last)
    except Exception as e:
        time_interval_max = 0
        time_interval_min = 0
    return (signal_account_last, time_interval_max, time_interval_min)


def check_all_value_is(ori_data, check_value):
    if isinstance(check_value,list):
        for i in range(len(ori_data)):
            if ori_data[i][0] not in check_value:
                return False
    else:
        for i in range(len(ori_data)):
            if ori_data[i][0] != check_value:
                return False
    return True

def calculate_signal_times_and_duration(ori_data):
    signal_account = len(ori_data)
    timestamp_first = ori_data[0][1]
    timestamp_last = ori_data[signal_account-1][1]
    duration = timestamp_last - timestamp_first
    return(signal_account,duration)
        

if __name__ == "__main__":
    result_ori = [(1, 1692948819.0174744), (1, 1692948819.1095252), (1, 1692948819.200107), (1, 1692948819.2698846), (1, 1692948819.3610604), (1, 1692948819.4384575), (1, 1692948819.5148406), (1, 1692948819.6201003), (1, 1692948819.6829062), (1, 1692948819.7630239), (1, 1692948819.8497264), (1, 1692948819.943313), (1, 1692948820.007558), (1, 1692948820.0985615), (1, 1692948820.1819959), (1, 1692948820.2624547), (1, 1692948820.3431842), (1, 1692948820.433704), (1, 1692948820.5019886), (1, 1692948820.5950594), (1, 1692948820.6761842), (1, 1692948820.758767), (1, 1692948820.847418), (1, 1692948820.9178214), (1, 1692948820.9981823), (1, 1692948821.0823627), (1, 1692948821.1654232), (1, 1692948821.2499647), (1, 1692948821.3340828), (1, 1692948821.4181395), (1, 1692948821.4981296), (1, 1692948821.586202), (1, 1692948821.6620648), (1, 1692948821.7459996), (1, 1692948821.8451967), (1, 1692948821.9145114), (1, 1692948821.9918258), (1, 1692948822.0818837), (1, 1692948822.1743705), (1, 1692948822.238227), (1, 1692948822.3177543), (1, 1692948822.4157941)]
    result_1 = get_signal_times_interval(result_ori, 0)
    result_2 = calculate_signal_times_and_duration(result_ori)
    print(result_2)
