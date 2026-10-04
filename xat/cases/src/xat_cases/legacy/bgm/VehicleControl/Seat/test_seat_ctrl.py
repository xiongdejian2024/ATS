# -*- coding: utf-8 -*-
"""
@File        : test_body_control_auto.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2023/04/23 18:00 PM
@Description : Test body control test case automatically based on configuration file
version: V3,merge to gitlab
"""

import os
import sys
from time import sleep
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.bgm_case_helper.common_interface import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey


conf_file_name = r"testcase_config_bodyctrl_seat.xlsx"
json_file = r"signal_message_matrix.json"
service_name_type = ("SeatService", "client")
signal_msg_info_dic = {}
signal_msg_info_dic = json_read_to_dic(json_file)
global case_list_full
global case_id_list_full
global case_list_smoke
global case_id_list_smoke
case_list_full, case_id_list_full = get_testconfig_by_read_excel(conf_file_name, "seat")
case_list_smoke, case_id_list_smoke = get_testconfig_by_read_excel(
    conf_file_name, "smoke"
)
# logger.info(case_list)
# logger.info(case_id_list)


@allure.feature("车身网关测试/整车控制")
@allure.story("座椅控制")
# @pytest.mark.run(order=1)
class TestHeatCtrl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global case_list
        global case_id_list
        global signal_msg_info_dic

        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)

        with allure.step("Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )

        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
        partner_process_check()
        sleep(1)

        # 启动partner operator
        self.partner = S2sBaseClass([service_name_type])
        sleep(0.1)
        self.sd_tester.change_usage_mode(1, do_assert=0)
        sleep(0.1)
        self.sd_tester.change_car_mode(0, do_assert=0)
        sleep(1)
        self.com_lib = CommonInterface(
            self.tc_config,
            self.ipdu,
            self.busapp,
            self.nucapp,
            self.dk,
            self.io,
            self.sd_tester,
            self.partner,
        )
        # sleep(15)

    def before_each_func(self, ecu):
        sleep(0.1)
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        sleep(0.1)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，总线开始收发报文
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        self.partner.stop_operators()
        sleep(0.5)
        partner_process_check()
        sleep(0.5)
        super().after_class(self, ecu)

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
        if str.upper(service_params_dic["operation"]) == "METHOD":
            if types == "resp":
                sleep(3)
            self.partner.send_method_request(
                conn_obj,
                service_params_dic["functionName"],
                input_params,
            )

        elif str.upper(service_params_dic["operation"]) == "EVENT_CHECK":
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

        elif str.upper(service_params_dic["operation"]) == "REQUEST_AND_CHECK":
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
                signal_name, bus_name, conf_file_name
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

    @pytest.mark.full
    @pytest.mark.parametrize("test_case", case_list_full, ids=case_id_list_full)
    def test_seat_ctrl_full_case(self, test_case):
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
        global service_name_type
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
                                result_cont, service_name_type
                            )
                            operation_type = result_dic["operation"]
                    if operation_type != "event_check":
                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, service_name_type
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
                                    result_cont, service_name_type
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
                                    action_cont, service_name_type
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

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_case", case_list_smoke, ids=case_id_list_smoke)
    def test_seat_ctrl_smoke_case(self, test_case):
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
        global service_name_type
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
                                    ccp_val = {int(pos):int(value)}
                                    self.sd_tester.write_multi_ccp(ccp_val)
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
                                result_cont, service_name_type
                            )
                            operation_type = result_dic["operation"]
                    if operation_type != "event_check":
                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, service_name_type
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
                                    result_cont, service_name_type
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
                                    action_cont, service_name_type
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

    @allure.title("主驾座椅占位状态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
        name="主驾座椅占位状态",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_114272(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=2)
            self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr17, "DrvrSeatSts", 0)
            sleep(2)

        with allure.step(f"Step:J3-35接地"):
            self.io.driver_seat_present()

        with allure.step(f"获取总线检测结果"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr12, "DrvrSeatSts", 2)
            self.ipdu.reset_check_results()

        with allure.step(f"Step:J3-35悬空"):
            self.io.driver_seat_notpresent()

        with allure.step(f"获取总线检测结果"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr12, "DrvrSeatSts", 1)
            self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("副驾座椅占位状态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
        name="副驾座椅占位状态",
    )
    @pytest.mark.full
    @pytest.mark.verify
    def test_tailgate_ctrl_caseid_114271(self):
        with allure.step(f"Step:设置初始条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "PassSeatSts", 2),
            ("bodycan.CEMBodyFr19", "PassSeatSts", 2),
        )
        sleep(1)
        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "PassSeatSts", 0),
            ("bodycan.CEMBodyFr19", "PassSeatSts", 0),
        )
        sleep(3)

    @allure.title("后排左侧座椅占位状态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
        name="后排左侧座椅占位状态",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118761(self):
        with allure.step(f"Step:设置初始条件"):
            self.com_lib.set_common_precontion(usage_mode=2)
        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecLe", 2),
            ("bodycan.CEMBodyFr19", "SeatOccptAtRowSecLe", 2),
        )
        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecLe", 0),
            ("bodycan.CEMBodyFr19", "SeatOccptAtRowSecLe", 0),
        )

    @allure.title("后排中间座椅占位状态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
        name="后排中间座椅占位状态",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118762(self):
        with allure.step(f"Step:设置初始条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecMid", 2),
            ("bodycan.CEMBodyFr28", "SeatOccptAtRowSecMid", 2),
        )
        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecMid", 0),
            ("bodycan.CEMBodyFr28", "SeatOccptAtRowSecMid", 0),
        )

    @allure.title("后排右侧座椅占位状态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
        name="后排右侧座椅占位状态",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118763(self):
        with allure.step(f"Step:设置初始条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecRi", 2),
            ("bodycan.CEMBodyFr19", "SeatOccptAtRowSecRi", 2),
        )
        self.com_lib.set_signal_and_check(
            ("backbonefr.SrsBackBoneFr04", "SeatOccptAtRowSecRi", 0),
            ("bodycan.CEMBodyFr19", "SeatOccptAtRowSecRi", 0),
        )

    # @allure.title("主驾座椅高度向上调节")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
    #     name="后排右侧座椅占位状态",
    # )
    # @pytest.mark.smoke_debug
    # def test_tailgate_ctrl_caseid_118753(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         self.com_lib.set_common_precontion(usage_mode=2)

    #     with allure.step(f"Step:大屏设置主驾座椅高度向上调节:(服务:SeatService;函数名:StartMoveDirectio)"):
    #         self.partner.send_method_request(
    #             "SeatService_client",
    #             "StartMoveDirectio",
    #             {"id": 0, "part": 0, "direction": 2},
    #         )

    #     with allure.step(f"获取总线检测结果"):
    #         self.ipdu.check(
    #             self.ipdu.bodycan.CemBodyFr74, "SeatHeiAdjmtRowFirstDrvr", 1
    #         )
    #         self.ipdu.reset_check_results()
    #     sleep(3)

    # @allure.title("主驾座椅高度向下调节")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/118753?projectId=46",
    #     name="主驾座椅高度向下调节",
    # )
    # @pytest.mark.smoke_debug
    # def test_tailgate_ctrl_caseid_118754(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         self.com_lib.set_common_precontion(usage_mode=2)

    #     with allure.step(f"Step:大屏设置主驾座椅高度向上调节:(服务:SeatService;函数名:StartMoveDirectio)"):
    #         self.partner.send_method_request(
    #             "SeatService_client",
    #             "StartMoveDirectio",
    #             {"id": 0, "part": 0, "direction": 5},
    #         )

    #     with allure.step(f"获取总线检测结果"):
    #         self.ipdu.check(
    #             self.ipdu.bodycan.CemBodyFr74, "SeatHeiAdjmtRowFirstDrvr", 2
    #         )
    #         self.ipdu.reset_check_results()
    #     sleep(3)

    # @allure.title("副驾座椅高度向上调节")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/118756?projectId=46",
    #     name="副驾座椅高度向上调节",
    # )
    # @pytest.mark.smoke_debug
    # def test_tailgate_ctrl_caseid_118756(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         self.com_lib.set_common_precontion(usage_mode=2)

    #     with allure.step(f"Step:大屏设置主驾座椅高度向上调节:(服务:SeatService;函数名:StartMoveDirectio)"):
    #         self.partner.send_method_request(
    #             "SeatService_client",
    #             "StartMoveDirectio",
    #             {"id": 1, "part": 0, "direction": 2},
    #         )

    #     with allure.step(f"获取总线检测结果"):
    #         self.ipdu.check(
    #             self.ipdu.bodycan.CemBodyFr74, "SeatHeiAdjmtRowFirstPass", 1
    #         )
    #         self.ipdu.reset_check_results()
    #     sleep(3)

    # @allure.title("副驾座椅高度向下调节")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/118755?projectId=46",
    #     name="副驾座椅高度向下调节",
    # )
    # @pytest.mark.smoke_debug
    # def test_tailgate_ctrl_caseid_118755(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         self.com_lib.set_common_precontion(usage_mode=2)

    #     with allure.step(f"Step:大屏设置主驾座椅高度向上调节:(服务:SeatService;函数名:StartMoveDirectio)"):
    #         self.partner.send_method_request(
    #             "SeatService_client",
    #             "StartMoveDirectio",
    #             {"id": 1, "part": 0, "direction": 5},
    #         )

    #     with allure.step(f"获取总线检测结果"):
    #         self.ipdu.check(
    #             self.ipdu.bodycan.CemBodyFr74, "SeatHeiAdjmtRowFirstPass", 2
    #         )
    #         self.ipdu.reset_check_results()
    #     sleep(3)
