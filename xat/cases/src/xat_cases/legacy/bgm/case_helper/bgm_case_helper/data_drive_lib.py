
"""
@File        :data_drive_lib.py
@Author      :hui.zhao@jiduatuo.com
@Time        :2023/11/6 11:00 AM
@Description :Provide the common interface about data drive case
"""

import os
import sys
from time import sleep
from typing import Union
import pytest
import allure
from threading import Thread


from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *

json_file = r"signal_message_matrix.json"
signal_msg_info_dic = {}
current_file_path = os.path.realpath(__file__)
pos = current_file_path.rfind(r'/')
file_signal_json_file = current_file_path[: pos + 1] + json_file
signal_msg_info_dic = json_read_to_dic(json_file)


class DataDriveInterface:
    """数据驱动相关的case"""
    def __init__(self, tc_config, ipdu,io,sd_tester,partner,conf_file,servie_name):
        self.ipdu = ipdu
        self.tc_config = tc_config
        self.sd_tester = sd_tester
        self.io = io
        self.partner = partner
        self.config_file = conf_file
        self.service_obj = servie_name

    # Function：获取配置的操作类型和配置内容
    # Input Example：
    #       conf_cont:service_resquest:{functionName:SetAC;params:{'on':True};operation:method}
    # Output Example：
    #       (typeval, cont):(service_resquest，functionName:SetAC;params:{'on':True};operation:method）
    def get_type_cont(self, conf_cont):
        conf_list_temp = conf_cont.split(":", 1)
        typeval = conf_list_temp[0]
        cont = conf_list_temp[1][1:-1]
        return (typeval, cont)

    # 功能：定义event_check函数用于后面开启多线程
    def event_check(self, conn_obj, functionName, check_info, timeout=3):
        result = self.partner.ck_s2s_event(
            conn_obj,
            functionName,
            ck_info=check_info,
            timeout=timeout,
        )
        assert result
        logger.info("Check result is:{}".format(result))
        

    # Function：根据service_params_dic中参数来调用self.partner中的接口发送不同的服务请求：
    #           send_method_request、send_request_and_ck_resp、ck_s2s_event。
    # Input Example：service_params_dic：{'serviceName': 'ClimateControlService', 'mode': 'client', 'functionName': 'Off', 'params': "{'zoneId':0}", 'operation': 'method'}
    # Output Example：Null
    def send_service_cmd_basedon_type(self, service_params_dic, types="resquest"):
        conn_obj = "{}_{}".format(
            service_params_dic["serviceName"], service_params_dic["mode"]
        )
        if isinstance(service_params_dic["params"], str):
            input_params = eval(service_params_dic["params"])
        if str.upper(service_params_dic["operation"]) == 'METHOD':
            if types == "resp":
                sleep(3)
            self.partner.send_method_request(
                conn_obj,
                service_params_dic["functionName"],
                input_params,
            )

        elif str.upper(service_params_dic["operation"]) == 'EVENT_CHECK':
            if isinstance(service_params_dic["check_info"], str):
                check_info = eval(service_params_dic["check_info"])
                logger.info(
                    "------------>Statr threading to check event,event check_info: {}".format(
                        check_info
                    )
                )
                thread = Thread(
                    target=self.event_check,
                    args=(conn_obj, service_params_dic["functionName"], check_info),
                )
                thread.setDaemon(True)
                thread.start()

        elif str.upper(service_params_dic["operation"]) == 'REQUEST_AND_CHECK':
            if types == "resp":
                sleep(3)

            if "check_info" not in service_params_dic.keys():
                logger.error("trigger parameters need add check info")
                assert False
            else:
                if isinstance(service_params_dic["check_info"], str):
                    check_info = eval(service_params_dic["check_info"])
                    logger.info("------------>check_info: {}".format(check_info))
                    result = self.partner.send_request_and_ck_resp(
                        conn_obj,
                        service_params_dic["functionName"],
                        args=input_params,
                        ck_info=check_info,
                        timeout=3,
                        cycle_time=1,
                    )
                    assert result
                    logger.info("Check result is:{}".format(result))
        else:
            logger.info("--------->Other service type need to be updated<--------")

    # Function：更加信号字典对象或者bus_name, msg_name, msg_id, signal_name, signal_value
    # Input Example：
    #       conf_dic_obj:{'name': 'EcoClimaSts', 'value': 0, 'bus_name': 'bodycan'}
    # Output Example：
    #       [bus_name, msg_name, msg_id, signal_name, signal_value]:['bodycan', 'CcmBodyFr31', '0x127', 'EcoClimaSts', 0]
    def get_signal_params(self, conf_dic_obj):
        # logging.info("----------------->{}".format(conf_dic_obj))
        global signal_msg_info_dic, json_file
        bus_name = conf_dic_obj["bus_name"]
        signal_name = conf_dic_obj["name"]
        signal_value_ori = conf_dic_obj["value"]
        signal_value = check_and_transfer_data(signal_value_ori)
        key_info = signal_name + "_" + bus_name
        if key_info not in signal_msg_info_dic:
            check_result = get_msgname_by_read_excel_baseon_busname(
                signal_name, bus_name, self.config_file
            )
            if check_result == "NotFound":
                return ("NotFound", signal_name)
            else:
                signal_msg_info_dic[key_info] = check_result
                dic_save_as_json(signal_msg_info_dic, json_file)
                sleep(0.5)
        else:
            check_result = signal_msg_info_dic[key_info]

        msg_name = check_result[0]
        msg_id = check_result[1]
        if "times" in conf_dic_obj.keys():
            signal_received_times = conf_dic_obj["times"]
            return [
                bus_name,
                msg_name,
                msg_id,
                signal_name,
                signal_value,
                signal_received_times,
            ]
        else:
            return [bus_name, msg_name, msg_id, signal_name, signal_value]
        
    def test_data_drive_case(self, test_case):
        allure.dynamic.title(
            "CaseID:{}--{}".format(int(test_case.case_id), test_case.case_name)
        )
        allure.dynamic.testcase(
            "https://jama.jiduauto.com/perspective.req#/testCases/{}?projectId=46".format(
                int(test_case.case_id)
            ),
            name="Link:{},CaseID:{}".format(
                test_case.case_name,
                int(test_case.case_id),
            ),
        )
        if test_case.action != "NA" and test_case.check_result != "NA":
            logger.info("test_case Action parameter:{}".format(test_case.action))
            logger.info(
                "test_case CheckExpectResult parameter:{}".format(
                    test_case.check_result
                )
            )
            if len(test_case.action) != len(test_case.check_result):
                print("Parameter Error")
            else:
                for i in range(len(test_case.action)):
                    operation_type = "Normal"
                    logger.info(
                        "-------------------> Processing(total/current):{}/{} <------------------------".format(
                            len(test_case.action), i + 1
                        )
                    )
                    if test_case.pre_condition[i] != "NA" or "":
                        with allure.step(
                            "Step:设置初始条件:{}".format(test_case.pre_condition)
                        ):
                            pre_condition_list = dealwith_singal_parameter(
                                test_case.pre_condition[i]
                            )
                            logger.info(
                                "pre_condition_list:{}".format(pre_condition_list)
                            )
                            logger.info(len(pre_condition_list))
                            for index in range(len(pre_condition_list)):
                                tempDic = pre_condition_list[index]
                                # logging.info(
                                #     "----------1------------>{}".format(tempDic)
                                # )
                                if tempDic["name"] == "UsageMode":
                                    usagemode_value = analysis_usage_mode(
                                        tempDic["value"]
                                    )
                                    if usagemode_value != "NOK":
                                        self.sd_tester.change_usage_mode(
                                            usagemode_value, do_assert=1
                                        )
                                    else:
                                        logger.info("输入的Usage Mode参数不合理")
                                        assert False
                                elif tempDic["name"] == "CarMode":
                                    carmode_value = analysis_car_mode(tempDic["value"])
                                    if carmode_value != "NOK":
                                        self.sd_tester.change_car_mode(
                                            carmode_value, do_assert=1
                                        )
                                    else:
                                        logger.info("输入的Usage Mode参数不合理")
                                        assert False
                                elif tempDic["name"].find("CCP") != -1:
                                    logger.info("Enter Car Config")
                                    logger.info(
                                        "Enter Car Config {}".format(tempDic["name"])
                                    )
                                    pos = str(tempDic["name"].split("_")[1])
                                    value = str(tempDic["value"])
                                    ccp_val = (
                                        self.sd_tester.make_ccp_according_id_and_data(
                                            pos, value
                                        )
                                    )
                                    self.sd_tester.write_ccp(ccp_val)
                                    logger.info(
                                        "将{}写入:{}".format(tempDic["name"], value)
                                    )
                                elif tempDic["name"].find("IO-") != -1:
                                    logger.info(
                                        "Enter IO interface control {}".format(
                                            tempDic["name"]
                                        )
                                    )
                                    io_contrl_str = tempDic["name"].replace("IO-", "")
                                    [
                                        operation_obj,
                                        status,
                                    ] = dealwith_usb_relay_setting(
                                        io_contrl_str, tempDic["value"]
                                    )
                                    if operation_obj == "NotFound":
                                        logger.info(
                                            "Not found IO interface:{}".format(
                                                io_contrl_str
                                            )
                                        )
                                    else:
                                        logger.info(
                                            "Set IO interface:{} to {}".format(
                                                operation_obj, status
                                            )
                                        )
                                        self.io_obj.set_do_level(operation_obj, status)
                                elif str.upper(tempDic["name"]) == "SLEEP":
                                    logger.info(
                                        "Waiting For {} seconds".format(
                                            tempDic["value"]
                                        )
                                    )
                                    sleep(tempDic["value"])
                                else:
                                    signal_params_list = self.get_signal_params(tempDic)
                                    logger.info(
                                        "signal_params_list {}".format(
                                            signal_params_list
                                        )
                                    )
                                    if signal_params_list[0] == "NotFound":
                                        logger.error(
                                            "{} not found".format(signal_params_list[1])
                                        )
                                        assert False
                                    msg_obj = getattr(
                                        getattr(self.ipdu, signal_params_list[0]),
                                        signal_params_list[1],
                                    )
                                    self.ipdu.set(
                                        msg_obj,
                                        signal_params_list[3],
                                        signal_params_list[4],
                                    )
                                    logger.info(
                                        "{}发送消息{}(ID:{}):{} = {}".format(
                                            signal_params_list[0],
                                            signal_params_list[1],
                                            signal_params_list[2],
                                            signal_params_list[3],
                                            signal_params_list[4],
                                        )
                                    )
                                    sleep(0.5)

                    if test_case.check_result[i] != "NA":
                        [result_type, result_cont] = self.get_type_cont(
                            test_case.check_result[i]
                        )
                        if result_type == "service_resquest":
                            result_dic = dealwith_service_parameter(
                                result_cont, self.service_obj
                            )
                            operation_type = result_dic["operation"]
                    if operation_type != "event_check":
                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, self.service_obj
                                )
                                print(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                )
                                self.send_service_cmd_basedon_type(action_dic)

                            elif action_type == "signal_resquest":
                                action_list = dealwith_singal_parameter(action_cont)
                                for index in range(len(action_list)):
                                    tempDic = action_list[index]
                                    [
                                        bus_name,
                                        msg_name,
                                        msg_id,
                                        signal_name,
                                        signal_value,
                                    ] = self.get_signal_params(tempDic)

                                    with allure.step(
                                        "发送的消息:(总线类型:{},消息名{}-ID:{},信号:{}={})".format(
                                            bus_name,
                                            msg_name,
                                            msg_id,
                                            signal_name,
                                            signal_value,
                                        )
                                    ):
                                        msg_obj = getattr(
                                            getattr(self.ipdu, bus_name),
                                            msg_name,
                                        )
                                        self.ipdu.set(
                                            msg_obj,
                                            signal_name,
                                            signal_value,
                                        )
                                        logger.info(
                                            "发送的请求命令是:self.ipdu.set({},{},{})".format(
                                                msg_obj, signal_name, signal_value
                                            )
                                        )

                        if test_case.check_result[i] != "NA":
                            [result_type, result_cont] = self.get_type_cont(
                                test_case.check_result[i]
                            )
                            if result_type == "service_resquest":
                                result_dic = dealwith_service_parameter(
                                    result_cont, self.service_obj
                                )
                                print(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        result_dic["serviceName"],
                                        result_dic["functionName"],
                                        result_dic["params"],
                                        result_dic["operation"],
                                    )
                                )
                                self.send_service_cmd_basedon_type(result_dic, "resp")

                            elif result_type == "signal_resquest":
                                result_list = dealwith_singal_parameter(result_cont)
                                for index in range(len(result_list)):
                                    tempDic = result_list[index]
                                    [
                                        bus_name,
                                        msg_name,
                                        msg_id,
                                        signal_name,
                                        signal_value,
                                    ] = self.get_signal_params(tempDic)

                                    with allure.step(
                                        "发送的消息:(总线类型:{},消息名{}-ID:{},信号:{}={})".format(
                                            bus_name,
                                            msg_name,
                                            msg_id,
                                            signal_name,
                                            signal_value,
                                        )
                                    ):
                                        msg_obj = getattr(
                                            getattr(self.ipdu, bus_name),
                                            msg_name,
                                        )
                                        self.ipdu.set(
                                            msg_obj,
                                            signal_name,
                                            signal_value,
                                        )
                                        logger.info(
                                            "发送的请求命令是:self.ipdu.set({},{},{})".format(
                                                msg_obj, signal_name, signal_value
                                            )
                                        )
                            elif result_type == "signal_check":
                                check_list = []
                                result_list = dealwith_check_signal(result_cont)
                                for index in range(len(result_list)):
                                    tempDic = result_list[index]
                                    # logger.info("----------->tempDic {}".format(tempDic))
                                    sig_name = tempDic["sig_name"]
                                    sig_value = tempDic["sig_value"]
                                    msg_name = tempDic["msg_name"]
                                    bus_name = tempDic["bus_name"]

                                    with allure.step(
                                        "检查是否发出消息:(总线{}->消息名->信号{}={})".format(
                                            bus_name,
                                            msg_name,
                                            sig_name,
                                            sig_value,
                                        )
                                    ):
                                        msg_obj = getattr(
                                            getattr(self.ipdu, bus_name),
                                            msg_name,
                                        )
                                    check_list.append((msg_obj, sig_name, sig_value))
                                self.ipdu.check_multiple_signals(check_list)
                    else:
                        print(
                            "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                result_dic["serviceName"],
                                result_dic["functionName"],
                                result_dic["params"],
                                result_dic["operation"],
                            )
                        )
                        self.send_service_cmd_basedon_type(result_dic, "resp")

                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, self.service_obj
                                )
                                print(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                )
                                self.send_service_cmd_basedon_type(action_dic)

                            elif action_type == "signal_resquest":
                                action_list = dealwith_singal_parameter(action_cont)
                                for index in range(len(action_list)):
                                    tempDic = action_list[index]
                                    [
                                        bus_name,
                                        msg_name,
                                        msg_id,
                                        signal_name,
                                        signal_value,
                                    ] = self.get_signal_params(tempDic)

                                    with allure.step(
                                        "发送的消息:(总线类型:{},消息名{}-ID:{},信号:{}={})".format(
                                            bus_name,
                                            msg_name,
                                            msg_id,
                                            signal_name,
                                            signal_value,
                                        )
                                    ):
                                        msg_obj = getattr(
                                            getattr(self.ipdu, bus_name),
                                            msg_name,
                                        )
                                        self.ipdu.set(
                                            msg_obj,
                                            signal_name,
                                            signal_value,
                                        )
                                        logger.info(
                                            "发送的请求命令是:self.ipdu.set({},{},{})".format(
                                                msg_obj, signal_name, signal_value
                                            )
                                        )

                    sleep(0.5)
        sleep(2)
