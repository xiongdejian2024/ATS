# -*- coding: utf-8 -*-
"""
@File        : det_def.py
@Author      : songjian.lin@jiduauto.com
@Time        : 2023/11/24 22:43
@Description :
@Examples    :
"""
import datetime
import json
import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))

from xat_ecu.legacy.common.logger import *

global enum_desc
enum_desc = {}


def get_file_in_dir(dir_path):
    """
    获取目录下的所有文件
    """
    file_list = []
    if not os.path.exists(dir_path):
        logger.info(f"文件不存在")
        return
        # 把文件夹下的内容放入列表,便于下一步分析
    listName = os.listdir(dir_path)
    for fileDirName in listName:
        # 拼接成绝对路径
        abspath = os.path.join(dir_path, fileDirName)
        if os.path.isfile(abspath) and abspath.endswith('.json'):
            file_list.append(abspath)
        if os.path.isdir(abspath):
            file_list.extend(get_file_in_dir(abspath))
    return file_list


def get_return_param_value(param_dict_info, param_type_info, param_arg_info, is_array):

    if param_type_info == 'bool':
        if isinstance(is_array, int):
            return [True]
        else:
            return True
    elif param_type_info in ['uint8', 'uint16', "uint32", 'uint64', 'int32', 'int8', 'int64', 'int16']:
        if isinstance(is_array, int):
            return [0]
        else:
            return 0
    elif param_type_info == 'float':
        if isinstance(is_array, int):
            return [0.0]
        else:
            return 0.0
    elif param_type_info == 'double':
        if isinstance(is_array, int):
            return [0.0]
        else:
            return 0.0
    elif param_type_info == 'string':
        if isinstance(is_array, int):
            return [True]
        else:
            return ''
    elif param_dict_info[param_type_info]["ref_type"] in ['struct', 'enum']:
        if param_dict_info[param_type_info]["ref_type"] == 'struct':
            return_value = {}
            for element in param_dict_info[param_type_info]["sub_element"]:
                return_value[element['arg']] = get_return_param_value(param_dict_info,
                                                                      element['ref_type'], element['arg'], element['array_size'])
            else:
                if isinstance(is_array, int):
                    return [return_value]
                else:
                    return return_value

        if param_dict_info[param_type_info]["ref_type"] == 'enum':
            enum_dict = param_dict_info[param_type_info]["compu_method"]
            enum_desc[param_arg_info] = enum_dict
            for enum_value in enum_dict.keys():
                if isinstance(is_array, int):
                    return [int(enum_value)]
                else:
                    return int(enum_value)
    else:
        logger.info(f"未覆盖类型：{param_type_info}")


class service_json_parse_result:
    def __init__(self):
        self.partner_key_list = []
        self.method_need_to_convert = ['send_method_request']


def service_json_analysis(json_file_path):
    file_list = get_file_in_dir(json_file_path)
    logger.info(f"服务总数：{len(file_list)}")
    # logger.info(file_list)
    total_event = 0
    total_method = 0
    analysis_result = {}

    for file_name in file_list:
        param_dict = {}
        service_name = None
        with open(file_name, 'r') as f:
            data = f.read()
            json_dict = json.loads(data)
            for key in json_dict.keys():
                service_name = key
                for key2 in json_dict[key]:
                    if key2 == 'args':
                        param_dict = json_dict[key]['args']
                        break
        analysis_result[service_name] = {}

        with open(file_name, 'r') as f:
            data = f.read()
            json_dict = json.loads(data)
            for key in json_dict.keys():
                for key2 in json_dict[key].keys():
                    if key2 == 'apis':
                        for key3 in json_dict[key][key2].keys():
                            if key3.endswith("Proxy"):
                                for function_dict in json_dict[key][key2][key3]:
                                    if function_dict["api"].startswith('Event'):
                                        event_name = function_dict["api"].replace("Event", "", 1).replace('Callback',
                                                                                                          '')
                                        analysis_result[service_name][event_name] = {}
                                        analysis_result[service_name][event_name]['type'] = "event"
                                        total_event += 1
                                        for param in function_dict["args_in"]:  # 遍历event的参数列表
                                            enum_desc.clear()
                                            param_value = get_return_param_value(param_dict, param['ref_type'],
                                                                                 param['arg'], param['array_size'])
                                            # logger.info("1、事件 " + f"{event_name} " + "默认响应模板：{" +
                                            #             f"'{param['arg']}': {param_value}" + "}")
                                            analysis_result[service_name][event_name]['args_out'] = {param['arg']: param_value}

                                            if enum_desc:
                                                i = 0
                                                analysis_result[service_name][event_name][
                                                    'enum_info'] = {}
                                                for key_info in enum_desc.keys():
                                                    i = i + 1
                                                    # logger.info(
                                                    #     f"    1-{i}、枚举参数 {key_info} 说明: {str(enum_desc[key_info])}")
                                                    analysis_result[service_name][event_name][
                                                        'enum_info'][key_info] = str(enum_desc[key_info])
                                    else:
                                        analysis_result[service_name][function_dict["api"]] = {}
                                        analysis_result[service_name][function_dict["api"]]['type'] = "method"
                                        total_method += 1
                                        if function_dict['args_in']:
                                            j = 0
                                            analysis_result[service_name][function_dict['api']]['args_in'] = {}
                                            enum_desc.clear()
                                            for param in function_dict['args_in']:
                                                j = j + 1
                                                param_value = get_return_param_value(param_dict, param['ref_type'],
                                                                                     param['arg'], param['array_size'])
                                                # logger.info(f"1、方法 {function_dict['api']}" + " 默认输入参数模板：{" +
                                                #             f"'{param['arg']}': {param_value}" + "}")
                                                analysis_result[service_name][function_dict['api']]['args_in'][param['arg']] = param_value
                                            else:
                                                if enum_desc:
                                                    analysis_result[service_name][function_dict['api']][
                                                        'enum_info'] = {}
                                                    i = 0
                                                    for key_info in enum_desc.keys():
                                                        i = i + 1
                                                        analysis_result[service_name][function_dict['api']][
                                                            'enum_info'][key_info] = str(enum_desc[key_info])
                                        # else:
                                        #     logger.info(f"1、方法 {function_dict['api']} 的输入参数为空！")
                                        else:
                                            analysis_result[service_name][function_dict['api']]['args_in'] = function_dict['args_in']
                                        if function_dict['args_out']:  # 遍历方法的输出参数
                                            enum_desc.clear()
                                            param_value = get_return_param_value(param_dict,
                                                                                 function_dict['args_out']['ref_type'],
                                                                                 function_dict['args_out']['arg'], param['array_size'])
                                            # logger.info(
                                            #     f"2、方法 {function_dict['api']} " + "默认返回参数模板：{" +
                                            #     f"'{function_dict['args_out']['arg']}': "f"{param_value}" + "}")
                                            analysis_result[service_name][function_dict['api']]['args_out'] = {function_dict['args_out']['arg']: param_value}
                                            if enum_desc:
                                                i = 0
                                                analysis_result[service_name][function_dict['api']]['enum_info'] = {}
                                                for key_info in enum_desc.keys():
                                                    i = i + 1
                                                    # logger.info(
                                                    #     f"    2-{i}、{service_name}==>{function_dict['api']}枚举参数 {key_info} 说明: {str(enum_desc[key_info])}")
                                                    analysis_result[service_name][function_dict['api']]['enum_info'][key_info] = str(enum_desc[key_info])
                                        else:
                                            analysis_result[service_name][function_dict['api']]['args_out'] = function_dict['args_out']
    else:
        logger.info(f"总方法数：{total_method * 7}, 总event数{total_event * 6}，总服务数：{len(file_list)}")
        # logger.info(json.dumps(analysis_result, ensure_ascii=False, indent=4).
        #             encode('utf-8').decode('utf-8').replace('true', 'True'))
        return analysis_result


def service_server_sendMethodResponse(file_handle, service_name, method_name, args, enum_info):
    """
    当前服务作为server端需要封装的方法
    """

    file_handle.write(" " * 4 + f'def send_method_response_{service_name}_{method_name}(self, args={args}, **kwargs):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行send_method_response方法，args参数仅输入out内的部分即可' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值 {enum_key} 的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    update_agrs(file_handle, "args")
    file_handle.write(" " * 8 + f'self.send_method_response("{service_name}_server", "{method_name}", args)'
                      + "\n\n")


def service_server_method_ckS2sReq(file_handle, service_name, method_name, args, enum_info):
    """
    当前服务作为server端需要封装的方法: ck_s2s_req
    """

    file_handle.write(" " * 4 + f'def ck_s2s_req_{service_name}_{method_name}(self, args):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行ck_s2s_req方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.ck_s2s_req("{service_name}_server", "{method_name}", args)' + "\n")
    file_handle.write("\n")


def service_server_method_ckNoReq(file_handle, service_name, method_name, enum_info):
    """
    当前服务作为server端需要封装的方法: ck_no_req
    """

    file_handle.write(" " * 4 + f'def ck_no_req_{service_name}_{method_name}(self):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行ck_no_req方法' + "\n\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.ck_no_req("{service_name}_server", "{method_name}")' + "\n")
    file_handle.write("\n")


def service_client_method_sendMethodRequest(file_handle, service_name, method_name, args, enum_info):
    """
    当前服务作为client端需要封装的方法: send_method_request
    """

    file_handle.write(" " * 4 + f'def send_method_request_{service_name}_{method_name}(self, args={args}, **kwargs):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行send_method_request方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值 {enum_key} 的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    update_agrs(file_handle, "args")
    file_handle.write(" " * 8 + f'self.send_method_request("{service_name}_client", "{method_name}", args)'
                      + "\n\n")


def service_client_method_chkResp(file_handle, service_name, method_name, args, enum_info):
    """
    当前服务作为client端需要封装的方法: chk_resp
    """

    file_handle.write(" " * 4 + f'def chk_resp_{service_name}_{method_name}(self, args):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行chk_resp方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.chk_resp("{service_name}_client", "{method_name}", args)' + "\n")
    file_handle.write("\n")


def service_client_method_sendRequestAndCkFailType(file_handle, service_name, method_name, args, enum_info):
    """
    当前服务作为client端需要封装的方法: send_request_and_ck_failtype
    """

    file_handle.write(" " * 4 + f'def send_request_and_ck_fail_type_{service_name}_{method_name}(self, args={args}, '
                                f'fail_type=FailType.FAILTYPE_TIMEOUT):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行send_request_and_ck_fail_type方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    file_handle.write(" " * 8 + f':param fail_type: 默认格式: FailType.FAILTYPE_TIMEOUT' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值 {enum_key} 的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")

    file_handle.write(" " * 8 + f'self.send_request_and_ck_failtype("{service_name}_client", "{method_name}", args, fail_type)' + "\n")
    file_handle.write("\n")


def service_client_method_sendRequestAndCkResp(file_handle, service_name, method_name, args, ck_info, enum_info):
    """
    当前服务作为client端需要封装的方法: send_request_and_ck_failtype
    """

    file_handle.write(" " * 4 + f'def send_request_and_ck_resp_{service_name}_{method_name}(self, args={args}, ck_info={ck_info}, **kwargs):'
                      + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行send_request_and_ck_resp方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    file_handle.write(" " * 8 + f':param ck_info: 默认格式: {ck_info}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'备注：枚举值 {enum_key} 的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    update_agrs(file_handle, "args")

    file_handle.write(" " * 8 + f'self.send_request_and_ck_resp("{service_name}_client", "{method_name}", args, ck_info)' + "\n")
    file_handle.write("\n")


def service_server_event_sendEventNotify(file_handle, service_name, event_name, args, enum_info):
    """
    当前服务作为server端需要封装的方法: send_event_notify
    """

    file_handle.write(" " * 4 + f'def send_event_notify_{service_name}_{event_name}(self, args={args}, **kwargs):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'server端执行send_event_notify方法' + "\n\n")
    file_handle.write(" " * 8 + f':param args: 默认格式: {args}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    update_agrs(file_handle, "args")
    file_handle.write(" " * 8 + f'self.send_event_notify("{service_name}_server", "{event_name}", args)'
                      + "\n\n")


def service_client_event_chkNotify(file_handle, service_name, event_name, ck_info, enum_info):
    """
    当前服务作为client端需要封装的方法: chk_notify
    """

    file_handle.write(" " * 4 + f'def chk_notify_{service_name}_{event_name}(self, ck_info):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'client端执行chk_notify方法' + "\n\n")
    file_handle.write(" " * 8 + f':param ck_info: 默认格式: {ck_info}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.chk_notify("{service_name}_client", "{event_name}", ck_info)' + "\n")
    file_handle.write("\n")


def service_client_event_ckS2sEvent(file_handle, service_name, event_name, ck_info, enum_info):
    """
    当前服务作为client端需要封装的方法: ck_s2s_event_
    """

    file_handle.write(" " * 4 + f'def ck_s2s_event_{service_name}_{event_name}(self, ck_info={ck_info}, **kwargs):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'client端执行ck_s2s_event方法' + "\n\n")
    file_handle.write(" " * 8 + f':param ck_info: 默认格式: {ck_info}' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值 {enum_key} 的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    update_agrs(file_handle, "ck_info")

    file_handle.write(" " * 8 + f'self.ck_s2s_event("{service_name}_client", "{event_name}", ck_info)'
                      + "\n")
    file_handle.write("\n")


def service_client_event_returnLatestEvent(file_handle, service_name, event_name, enum_info):
    """
    当前服务作为client端需要封装的方法: return_latest_event
    """

    file_handle.write(" " * 4 + f'def return_latest_event_{service_name}_{event_name}(self):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'client端执行 return_latest_event 方法' + "\n\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'return self.return_latest_event("{service_name}_client", "{event_name}")'
                      + "\n\n")


def service_client_event_ckNoEvent(file_handle, service_name, event_name):
    """
    当前服务作为client端需要封装的方法: return_latest_event
    """

    file_handle.write(" " * 4 + f'def ck_no_event_{service_name}_{event_name}(self):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'client端执行 ck_no_event 方法' + "\n\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.ck_no_event("{service_name}_client", "{event_name}")' + "\n")
    file_handle.write("\n")


def service_client_event_ckNoSpecificEvent(file_handle, service_name, event_name, enum_info):
    """
    当前服务作为client端需要封装的方法: ck_no_specific_event
    """

    file_handle.write(" " * 4 + f'def ck_no_specific_event_{service_name}_{event_name}(self, hint):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'client端执行 ck_no_specific_event 方法' + "\n\n")
    file_handle.write(" " * 8 + f':param hint: 用户自定义' + "\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.ck_no_specific_event("{service_name}_client", "{event_name}", hint)'
                      + "\n\n")


def service_registerEvent(file_handle, service_name, enum_info):
    """
    当前服务作为client端需要封装的方法: ck_no_specific_event
    """

    file_handle.write(" " * 4 + f'def register_event_{service_name}'+'(self, event_list: list = [{"all": 1}]):' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'执行 register_event 方法' + "\n\n")
    if enum_info:
        for enum_key in enum_info:
            file_handle.write(" " * 8 + f'枚举值{enum_key}的参数列表: {enum_info[enum_key]}' + "\n")
    file_handle.write(" " * 8 + '"""' + "\n")
    file_handle.write(" " * 8 + f'self.register_event("{service_name}_client", event_list)' + "\n")
    file_handle.write("\n")


def update_agrs(file_handle, key):
    file_handle.write("\n")
    file_handle.write(" " * 8 + f'for key in kwargs:' + "\n")
    file_handle.write(" " * 12 + f'if key in {key}:' + "\n")
    file_handle.write(" " * 16 + f'{key}[key] = kwargs.get(key)' + "\n\n")


def convert_service_json_to_soa_partner(json_path, result_file_path, result_file_name="soa_partner.py"):
    analysis_result = service_json_analysis(json_path)
    now = datetime.datetime.now()
    with open(os.path.join(result_file_path, result_file_name), "w", encoding='utf-8') as file_handler:
        file_handler.write("#!/usr/bin/env python" + "\n")
        file_handler.write("# -*- encoding: utf-8 -*-" + "\n")
        file_handler.write('"""' + "\n")
        file_handler.write("@File         :soa.py" + "\n")
        file_handler.write(f"@Time         {now}" + "\n")
        file_handler.write("@Author       :songjian.lin@jiduauto.com" + "\n")
        file_handler.write("@Description  :soa通信能力模拟 实现接口" + "\n")
        file_handler.write('"""' + "\n")
        file_handler.write("\n\n")
        file_handler.write("from enum import Enum, auto" + "\n\n")
        file_handler.write("class FailType(Enum):" + "\n")
        file_handler.write(" " * 4 + "FAILTYPE_SUCCESS = 0" + "\n")
        file_handler.write(" " * 4 + "FAILTYPE_TIMEOUT = -1" + "\n")
        file_handler.write(" " * 4 + "FAILTYPE_SERVICE_BUSY = -2" + "\n")
        file_handler.write(" " * 4 + "FAILTYPE_SERVICE_UNAVAILIABLE = -3" + "\n")
        file_handler.write(" " * 4 + "FAILTYPE_TIME_OUT = 600  # operation timed out" + "\n\n")

        file_handler.write("class SoaBasePartner:" + "\n\n")
        # file_handler.write(" " * 4 + "def __init__(self, soa_partner):" + "\n")
        # file_handler.write(" " * 8 + '"""' + "\n")
        # file_handler.write(" " * 8 + "实例化S2sBaseClass" + "\n")
        # file_handler.write(" " * 8 + '"""' + "\n")
        # file_handler.write(" " * 8 + "self = soa_partner" + "\n\n")
        for key1 in analysis_result:
            for key2 in analysis_result[key1]:
                if 'Async' not in key2:
                    enum_info = analysis_result[key1][key2].get('enum_info', None)
                    if analysis_result[key1][key2]['type'] == "method":
                        if 'args_out' in analysis_result[key1][key2]:
                            agrs = analysis_result[key1][key2]['args_out']
                            if agrs:
                                if "out" in agrs:
                                    agrs = agrs["out"]
                                    if agrs == '':
                                        agrs = '\"\"'
                            service_server_sendMethodResponse(file_handler, key1, key2, f"{agrs}", enum_info)
                        if 'args_in' in analysis_result[key1][key2]:
                            agrs = analysis_result[key1][key2]['args_in']
                            service_client_method_sendMethodRequest(file_handler, key1, key2, f"{agrs}", enum_info)
                            service_client_method_sendRequestAndCkFailType(file_handler, key1, key2, f"{agrs}", enum_info)
                            if 'args_out' in analysis_result[key1][key2]:
                                agrs_out = analysis_result[key1][key2]['args_out']
                                service_client_method_sendRequestAndCkResp(file_handler, key1, key2, f"{agrs}", agrs_out, enum_info)
                    if analysis_result[key1][key2]['type'] == "event":
                        if 'args_out' in analysis_result[key1][key2]:
                            args = analysis_result[key1][key2]['args_out']
                            service_client_event_ckS2sEvent(file_handler, key1, key2, args, enum_info)
                            service_client_event_ckNoEvent(file_handler, key1, key2)
                            service_server_event_sendEventNotify(file_handler, key1, key2, f"{args}", enum_info)


if __name__ == "__main__":
    logger = Logger().get_logger("test")
    file_path = os.path.join(os.getcwd(), 'bin')
    convert_service_json_to_soa_partner(file_path, os.getcwd())
