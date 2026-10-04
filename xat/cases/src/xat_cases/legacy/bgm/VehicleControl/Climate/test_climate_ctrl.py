# -*- coding:utf-8 -*-
"""
@File        :test_climate_ctrl.py
@Author      :xiangyue.li@jiduatuo.com
@Time        :2023/06/16 11:00 AM
@Description :Test body control test case about climate
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
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.bgm_case_helper.common_interface import *


conf_file_name = r"testcase_config_bodyctrl_climate.xlsx"
json_file = r"signal_message_matrix.json"
service_name_type = ("ClimateControlService", "client")
service_name_type_reset = ("ResetSOAConfigService", "client")
service_name_type_rear = ("OuterRearViewService", "client")
signal_msg_info_dic = {}
signal_msg_info_dic = json_read_to_dic(json_file)
global case_list_full
global case_id_list_full
global case_list_smoke
global case_id_list_smoke

case_list_full, case_id_list_full = get_testconfig_by_read_excel(
    conf_file_name, "climate"
)
case_list_smoke, case_id_list_smoke = get_testconfig_by_read_excel(
    conf_file_name, "smoke"
)


@allure.feature("车身网关测试/整车控制")
@allure.story("空调控制")
class TestClimateCtrl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global case_list_full
        global case_id_list_full

        global case_list_smoke
        global case_id_list_smoke

        global signal_msg_info_dic

        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)

        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)


        # 检查上位机上是否有其它未关闭的soa_partner进程在运行,如果有,则杀死进程
        partner_process_check()
        sleep(1)

        with allure.step("Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动,总线开始收发报文

        # 启动partner operator
        self.partner = S2sBaseClass([service_name_type, service_name_type_reset, service_name_type_rear])
        sleep(1)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        sleep(1)
        self.com_lib = CommonInterface(self.tc_config, self.ipdu, self.busapp, self.nucapp, self.dk, self.io, self.sd_tester)

        sleep(1)
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        sleep(0.1)
        # self.sd_tester.change_usage_mode(2, do_assert=1)

    def after_each_func(self, ecu):
        try:
            self.sd_tester.change_car_mode(0, do_assert=False)
            sleep(0.1)
            self.sd_tester.change_usage_mode(0, do_assert=False)
            sleep(0.1)
        except Exception as e:
            pass
        self.ipdu.reset_check_results()
        self.ipdu.resume_all_bus_send()
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
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
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
                    "------------>Statr threading to check event,event check_info:{}".format(
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
                    logger.info("------------>check_info:{}".format(check_info))
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
    # @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.parametrize("test_case", case_list_full, ids=case_id_list_full)
    def test_body_ctrl_full_case(self, test_case):
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
                                elif str.upper(tempDic["name"]).find("SERVICE") != -1:
                                    action_dic = dealwith_service_parameter(
                                        tempDic["value"], service_name_type
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
                                sleep(1)

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
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                ):
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
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        result_dic["serviceName"],
                                        result_dic["functionName"],
                                        result_dic["params"],
                                        result_dic["operation"],
                                    )
                                ):
                                    self.send_service_cmd_basedon_type(
                                        result_dic, "resp"
                                    )
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
                                        "检查是否发出消息:(总线{}->消息名{}->信号{}={})".format(
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
                        with allure.step(
                            "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                result_dic["serviceName"],
                                result_dic["functionName"],
                                result_dic["params"],
                                result_dic["operation"],
                            )
                        ):
                            self.send_service_cmd_basedon_type(result_dic)

                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, service_name_type
                                )
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                ):
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

                    sleep(1)
        sleep(2)

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_case", case_list_smoke, ids=case_id_list_smoke)
    def test_body_ctrl_smoke_case(self, test_case):
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
                                elif str.upper(tempDic["name"]).find("SERVICE") != -1:
                                    action_dic = dealwith_service_parameter(
                                        tempDic["value"], service_name_type
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
                                sleep(1)

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
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                ):
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
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        result_dic["serviceName"],
                                        result_dic["functionName"],
                                        result_dic["params"],
                                        result_dic["operation"],
                                    )
                                ):
                                    self.send_service_cmd_basedon_type(
                                        result_dic, "resp"
                                    )
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
                                        "检查是否发出消息:(总线{}->消息名{}->信号{}={})".format(
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
                        with allure.step(
                            "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                result_dic["serviceName"],
                                result_dic["functionName"],
                                result_dic["params"],
                                result_dic["operation"],
                            )
                        ):
                            self.send_service_cmd_basedon_type(result_dic)

                        if test_case.action[i] != "NA":
                            [action_type, action_cont] = self.get_type_cont(
                                test_case.action[i]
                            )
                            if action_type == "service_resquest":
                                action_dic = dealwith_service_parameter(
                                    action_cont, service_name_type
                                )
                                with allure.step(
                                    "Step:请求服务(服务:{};函数名:{};参数:{};类型:{})".format(
                                        action_dic["serviceName"],
                                        action_dic["functionName"],
                                        action_dic["params"],
                                        action_dic["operation"],
                                    )
                                ):
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

                    sleep(1)
        sleep(2)

    # @allure.title("出厂化设置_AC状态") 已做抽象接口
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1684132?projectId=46',
    #     name='空调测试case:109688',
    # )
    # @pytest.mark.smoke
    # def test_climate_soa_caseid_109688(self):
    #     with allure.step("设置初始条件"):
    #         logger.info("Usage Mode 设置为Active")
    #         self.sd_tester.change_usage_mode(11, do_assert=1)
    #         sleep(1)

    #     with allure.step(f"调用接口SetAC,设置参数:'on':False"):
    #         logger.info("调用接口SetAC,设置参数:'on':False")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'SetAC',
    #             args={'on': False},
    #         )
    #         sleep(1)
    #     with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
    #         logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
    #         self.partner.send_method_request(
    #             'ResetSOAConfigService_client',
    #             'ResetAllVehicleSOAConfig',
    #             args={},
    #         )
    #     with allure.step(f"查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq"):
    #         logger.info("查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq")
    #         self.ipdu.check_thread_start(
    #             self.ipdu.bodycan.CEMBodyFr15,
    #             'HmiCmptmtCoolgReq',
    #             1,
    #             timeout=2,
    #         )
    #         result = self.ipdu.check_thread_stop('HmiCmptmtCoolgReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         assert result[0]
    #         self.ipdu.reset_check_results()

    #     sleep(1)
    #     with allure.step(f"调用接口GetAC"):
    #         logger.info("调用接口GetAC")
    #         self.partner.send_request_and_ck_resp(
    #             'ClimateControlService_client',
    #             'GetAC',
    #             args={},
    #             ck_info={'out': True},
    #             timeout=3,
    #         )
    #     sleep(3)

    @allure.title("出厂化设置_吹风模式")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684132?projectId=46',
        name='空调测试case:109688',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109688(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口SetAC,设置参数:'on':False"):
            logger.info("调用接口SetAC,设置参数:'on':False")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': False},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step(f"查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq"):
            logger.info("查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr15,
                'HmiCmptmtCoolgReq',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiCmptmtCoolgReq', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

        sleep(1)
        with allure.step(f"调用接口GetAC"):
            logger.info("调用接口GetAC")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAC',
                args={},
                ck_info={'out': True},
                timeout=3,
            )
        sleep(3)


    @allure.title("出厂化设置_内外循环模式")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684133?projectId=46',
        name='空调测试case:109687',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109687(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':3"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':3")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 3},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

        sleep(1)
        with allure.step(f"调用接口GetAC"):
            logger.info("调用接口GetAC")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetCycleMode',
                args={},
                ck_info={'out': 1},
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_前后排空调开关状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684117?projectId=46',
        name='空调测试case:109702',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109702(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step("调用接口Off,设置参数:{'zoneId':0}；调用接口Off,设置参数:{'zoneId':2}"):
            logger.info("调用接口Off,设置参数:{'zoneId':0}；调用接口Off,设置参数:{'zoneId':2}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
            sleep(0.5)
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 2},
            )
            sleep(1)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        sleep(1)
        with allure.step(f"调用接口GetClimateSystemStatus"):
            logger.info("调用接口GetClimateSystemStatus")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateSystemStatus',
                args={},
                ck_info={
                    'out': {'firstRowPowerStatus': True, 'secondRowPowerStatus': True}
                },
                timeout=3,
            )
        sleep(2)

    @allure.title("出厂化设置_前后排风量")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684125?projectId=46',
        name='空调测试case:1684125',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109695(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 3},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step(
            f"查看空调前排后排风量信号BodyCan:0x140:HmiHvacFanLvlFrnt ,BodyCan:0x140:HmiHvacFanLvlRe "
        ):
            logger.info(
                "查看空调前排后排风量信号BodyCan:0x140:HmiHvacFanLvlFrnt ,BodyCan:0x140:HmiHvacFanLvlRe "
            )
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacFanLvlRe',
                12,
                timeout=2,
            )
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacFanLvlFrnt',
                12,
                timeout=2,
            )
            result_1 = self.ipdu.check_thread_stop('HmiHvacFanLvlRe', timeout=5)
            result_2 = self.ipdu.check_thread_stop('HmiHvacFanLvlFrnt', timeout=5)
            logger.info("result_1 {}".format(result_1))
            logger.info("result_2 {}".format(result_2))
            assert result_1[0] and result_2[0]
            self.ipdu.reset_check_results()

        sleep(1)
        with allure.step(f"调用接口GetAC"):
            logger.info("调用接口GetAC")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetCycleMode',
                args={},
                ck_info={'out': 1},
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_温度")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684119?projectId=46',
        name='空调测试case:1684119',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109700(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step("调用接口SetTemperatureAndOn"):
            logger.info("调用接口SetTemperatureAndOn")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 2, 'value': 21},
            )
            sleep(0.5)
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 3, 'value': 23},
            )
            sleep(0.5)
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 4, 'value': 24},
            )
            sleep(0.5)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step(
            "查看空调温度信号:BodyCan:0x180:HmiCmptmtTSpForRowFirstLe,BodyCan:0x180:HmiCmptmtTSpForRowFirstRi,BodyCan:0x180:HmiCmptmtTSpForRowSecLe"
        ):
            logger.info(
                "查看空调温度信号:BodyCan:0x180:HmiCmptmtTSpForRowFirstLe,BodyCan:0x180:HmiCmptmtTSpForRowFirstRi,BodyCan:0x180:HmiCmptmtTSpForRowSecLe"
            )
            # self.ipdu.check_thread_start(
            #     self.ipdu.bodycan.CEMBodyFr15,
            #     'HmiCmptmtTSpForRowFirstLe',
            #     14,
            #     timeout=2,
            # )
            # self.ipdu.check_thread_start(
            #     self.ipdu.bodycan.CEMBodyFr15,
            #     'HmiCmptmtTSpForRowFirstRi',
            #     14,
            #     timeout=2,
            # )
            # self.ipdu.check_thread_start(
            #     self.ipdu.bodycan.CEMBodyFr15,
            #     'HmiCmptmtTSpForRowSecLe',
            #     14,
            #     timeout=2,
            # )
            # result_1 = self.ipdu.check_thread_stop(
            #     'HmiCmptmtTSpForRowFirstLe', timeout=5
            # )
            # result_2 = self.ipdu.check_thread_stop(
            #     'HmiCmptmtTSpForRowFirstRi', timeout=5
            # )
            # result_3 = self.ipdu.check_thread_stop('HmiCmptmtTSpForRowSecLe', timeout=5)
            # logger.info("result_1 {}".format(result_1))
            # logger.info("result_2 {}".format(result_2))
            # logger.info("result_3 {}".format(result_3))
            # # assert result_1[0] and result_2[0] and result_3[0]
            # self.ipdu.reset_check_results()
            # sleep(1)

        check_list = [
            (self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstLe', 14),
            (self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstRi', 14),
            (self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecLe', 14),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(1)

        with allure.step("调用接口GetClimateSystemStatus 查看温度信息"):
            logger.info("调用接口 GetClimateSystemStatus 查看温度信息")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateSystemStatus',
                args={},
                ck_info={
                    'out': {
                        'tempDriver': 22.0,
                        'tempPassenger': 22.0,
                        'tempSecRow': 22.0,
                    }
                },
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_温度同步设置状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684124?projectId=46',
        name='空调测试case:1684124',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109696(self):
        
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step("调用接口SetAutoSyncMode,设置参数:{'on':False}"):
            logger.info("调用接口SetAutoSyncMode,设置参数:{'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAutoSyncMode',
                args={'on': False},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        sleep(1)
        with allure.step("调用接口GetAutoSyncMode查看空调温度同步设置状态"):
            logger.info("调用接口GetAutoSyncMode查看空调温度同步设置状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAutoSyncMode',
                args={},
                ck_info={'out': True},
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_空调自动模式状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1684128?projectId=46',
        name='空调测试case:1684128',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109692(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        sleep(1)
        with allure.step("调用接口GetClimateAuto,设置参数 {'zoneId':0}"):
            logger.info("调用接口GetClimateAuto,设置参数 {'zoneId':0}")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateAuto',
                args={'zoneId': 0},
                ck_info={'out': {'zoneId': 0, 'isOn': True}},
                timeout=3,
            )
        sleep(2)

    @allure.title("出厂化设置_出风口开关状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109691?projectId=46',
        name='空调测试case:109691',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109691(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step('调用接口：[SetAirVent]设置参数：{"zoneId": 8, "on": False}；'):
            logger.info('调用接口：[SetAirVent]设置参数：{"zoneId": 8, "on": False}；')
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAirVent',
                args={"zoneId": 8, "on": False},
            )
            sleep(1)
        with allure.step('调用接口：[SetAirVent]设置参数：{"zoneId": 9, "on": False}；'):
            logger.info('调用接口：[SetAirVent]设置参数：{"zoneId": 9, "on": False}；')
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAirVent',
                args={"zoneId": 9, "on": False},
            )
            sleep(1)
        with allure.step('调用接口：[SetAirVent]设置参数：{"zoneId": 10, "on": False}；'):
            logger.info('调用接口：[SetAirVent]设置参数：{"zoneId": 10, "on": False}；')
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAirVent',
                args={"zoneId": 10, "on": False},
            )
            sleep(1)
        with allure.step('调用接口：[SetAirVent]设置参数：{"zoneId": 11, "on": False}；'):
            logger.info('调用接口：[SetAirVent]设置参数：{"zoneId": 11, "on": False}；')
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAirVent',
                args={"zoneId": 11, "on": False},
            )
            sleep(1)
        with allure.step('调用接口：[SetAirVent]设置参数：{"zoneId": 12, "on": False}；'):
            logger.info('调用接口：[SetAirVent]设置参数：{"zoneId": 12, "on": False}；')
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAirVent',
                args={"zoneId": 12, "on": False},
            )
            sleep(1)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
            sleep(1)
        with allure.step("调用接口GetAirVent查看第一排左左出风口开关状态"):
            logger.info("调用接口GetAirVent查看第一排左左出风口开关状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAirVent',
                args={"zoneId": 8},
                ck_info={'out': True},
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetAirVent查看第一排左右出风口开关状态"):
            logger.info("调用接口GetAirVent查看第一排左右出风口开关状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAirVent',
                args={"zoneId": 9},
                ck_info={'out': True},
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetAirVent查看第一排右左出风口开关状态"):
            logger.info("调用接口GetAirVent查看第一排右左出风口开关状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAirVent',
                args={"zoneId": 10},
                ck_info={'out': True},
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetAirVent查看第一排右右出风口开关状态"):
            logger.info("调用接口GetAirVent查看第一排右右出风口开关状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAirVent',
                args={"zoneId": 11},
                ck_info={'out': True},
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetAirVent查看第二排左左出风口开关状态"):
            logger.info("调用接口GetAirVent查看第二排左左出风口开关状态")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetAirVent',
                args={"zoneId": 12},
                ck_info={'out': True},
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_出风口角度")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109698?projectId=46',
        name='空调测试case:109698',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109698(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(
            '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 3, "side": 0, "horizontal": 20, "vertical": 25}]}；'
        ):
            logger.info(
                '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 3, "side": 0, "horizontal": 20, "vertical": 25}]}；'
            )
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetOutletAngle',
                args={
                    "outlets": [{"id": 3, "side": 0, "horizontal": 20, "vertical": 25}]
                },
            )
            sleep(1)

        with allure.step(
            '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 4, "side": 0, "horizontal": 20, "vertical": 25}]}；'
        ):
            logger.info(
                '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 4, "side": 0, "horizontal": 20, "vertical": 25}]}；'
            )
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetOutletAngle',
                args={
                    "outlets": [{"id": 4, "side": 0, "horizontal": 20, "vertical": 25}]
                },
            )
            sleep(1)

        with allure.step(
            '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 2, "side": 0, "horizontal": 20, "vertical": 25}]}；'
        ):
            logger.info(
                '调用接口：[SetOutletAngle]设置参数： {"outlets": [{"id": 2, "side": 0, "horizontal": 20, "vertical": 25}]}；'
            )
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetOutletAngle',
                args={
                    "outlets": [{"id": 2, "side": 0, "horizontal": 20, "vertical": 25}]
                },
            )
            sleep(1)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
            sleep(1)
        with allure.step("调用接口GetOutletAngle查看第一排左侧出风口角度"):
            logger.info("调用接口GetOutletAngle查看第一排左侧出风口角度")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetOutletAngle',
                args={"zoneId": [3]},
                ck_info={
                    'out': [
                        {'id': 3, 'side': 0, 'horizontal': 50, 'vertical': 50},
                        {'id': 3, 'side': 1, 'horizontal': 50, 'vertical': 50},
                    ]
                },
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetOutletAngle查看第一排右侧出风口角度"):
            logger.info("调用接口GetOutletAngle查看第一排右侧出风口角度")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetOutletAngle',
                args={"zoneId": [4]},
                ck_info={
                    'out': [
                        {'id': 4, 'side': 0, 'horizontal': 50, 'vertical': 50},
                        {'id': 4, 'side': 1, 'horizontal': 50, 'vertical': 50},
                    ]
                },
                timeout=3,
            )
            sleep(1)
        with allure.step("调用接口GetOutletAngle查看第二排侧出风口角度"):
            logger.info("调用接口GetOutletAngle查看第二排侧出风口角度")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetOutletAngle',
                args={"zoneId": [2]},
                ck_info={
                    'out': [
                        {'id': 2, 'side': 0, 'horizontal': 50, 'vertical': 50},
                        {'id': 2, 'side': 1, 'horizontal': 50, 'vertical': 50},
                    ]
                },
                timeout=3,
            )
        sleep(3)

    @allure.title("出厂化设置_除霜除雾状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109693?projectId=46',
        name='空调测试case:109693',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_109693(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step("查看空调除霜除雾状态信号:BodyCan:0x140:HmiDefrstMaxReq"):
            logger.info("查看空调除霜除雾状态信号:BodyCan:0x140:HmiDefrstMaxReq")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiDefrstMaxReq',
                0,
                timeout=2,
            )

            result_1 = self.ipdu.check_thread_stop('HmiDefrstMaxReq', timeout=5)
            logger.info("result_1 {}".format(result_1))
            assert result_1[0]
            self.ipdu.reset_check_results()
        sleep(2)

    @allure.title("出厂化设置_空调状态机模式_Auto模式")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118614?projectId=46',
        name='空调测试case:118614',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_118614(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口SetClimateAuto,设置参数:'zoneId': 0, 'on': true"):
            logger.info("调用接口SetClimateAuto,设置参数:'zoneId': 0, 'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )

        sleep(1)
        with allure.step("调用接口GetClimateMode"):
            logger.info("调用接口GetClimateMode")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateMode',
                args={},
                ck_info={'out': 2},
                timeout=3,
            )

        sleep(1)
        with allure.step("调用接口GetClimateAuto,设置参数 {'zoneId':0}"):
            logger.info("调用接口GetClimateAuto,设置参数 {'zoneId':0}")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateAuto',
                args={'zoneId': 0},
                ck_info={'out': {'zoneId': 0, 'isOn': True}},
                timeout=3,
            )
        sleep(2)

    @allure.title("出厂化设置_空调状态机模式_Manual")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118612?projectId=46',
        name='空调测试case:118612',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_118612(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口SetWindSpeed,设置参数:'zoneId': 0, 'speed': 3"):
            logger.info("调用接口SetWindSpeed,设置参数:'zoneId': 0, 'speed': 3")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 0, 'speed': 3},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )

        sleep(1)
        with allure.step("调用接口GetClimateMode"):
            logger.info("调用接口GetClimateMode")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateMode',
                args={},
                ck_info={'out': 2},
                timeout=3,
            )

        sleep(1)
        with allure.step("调用接口GetClimateAuto,设置参数 {'zoneId':0}"):
            logger.info("调用接口GetClimateAuto,设置参数 {'zoneId':0}")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateAuto',
                args={'zoneId': 0},
                ck_info={'out': {'zoneId': 0, 'isOn': True}},
                timeout=3,
            )
        sleep(2)

    @allure.title("出厂化设置_空调状态机模式_Off")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118611?projectId=46',
        name='空调测试case:118611',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_118611(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口Off设置参数:'zoneId': 0"):
            logger.info("调用接口Off,设置参数:'zoneId': 0")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )

        sleep(1)
        with allure.step("调用接口GetClimateMode"):
            logger.info("调用接口GetClimateMode")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateMode',
                args={},
                ck_info={'out': 2},
                timeout=3,
            )

        sleep(1)
        with allure.step("调用接口GetClimateAuto,设置参数 {'zoneId':0}"):
            logger.info("调用接口GetClimateAuto,设置参数 {'zoneId':0}")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateAuto',
                args={'zoneId': 0},
                ck_info={'out': {'zoneId': 0, 'isOn': True}},
                timeout=3,
            )
        sleep(2)

    @allure.title("出厂化设置_空调状态机模式_前除霜除雾")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118613?projectId=46',
        name='空调测试case:118613',
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_118613(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )
            sleep(1)
        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )

        sleep(1)
        with allure.step("调用接口GetClimateMode"):
            logger.info("调用接口GetClimateMode")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateMode',
                args={},
                ck_info={'out': 2},
                timeout=3,
            )

        sleep(1)
        with allure.step("调用接口GetClimateAuto,设置参数 {'zoneId':0}"):
            logger.info("调用接口GetClimateAuto,设置参数 {'zoneId':0}")
            self.partner.send_request_and_ck_resp(
                'ClimateControlService_client',
                'GetClimateAuto',
                args={'zoneId': 0},
                ck_info={'out': {'zoneId': 0, 'isOn': True}},
                timeout=3,
            )
        sleep(2)

    @allure.title("初始化默认_香氛信息")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682846?projectId=46',
        name='空调测试case:1682846',
    )
    @pytest.mark.full
    @pytest.mark.restart
    def test_climate_soa_caseid_109705(self):
        with allure.step(
            "调用接口SetFragranceType,设置参数:{'fragrance':[{'channel':1, 'ratio':100}]}"
        ):
            logger.info(
                "调用接口SetFragranceType,设置参数:{'fragrance':[{'channel':1, 'ratio':100}]}"
            )
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFragranceType',
                args={'fragrance': [{'channel': 1, 'ratio': 100}]},
            )

        with allure.step("调用接口SetFragranceLevel,设置参数:{'level':2}"):
            logger.info("调用接口SetFragranceLevel,设置参数:{'level':2}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFragranceLevel',
                args={'level': 2},
            )
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            self.ipdu.rx_flag_reset_all()
            sleep(20)

        try:
            with allure.step("检查香氛相关信号"):
                logger.info("检查香氛相关信号")
                check_cem_46 = [
                    (self.ipdu.bodycan.CemBodyFr46, 'HmiFragraLvlReq', 0)  
                ]
                check_cem_48 = [
                    (self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0)
                ]
                check_cem_51 = [
                    (
                        self.ipdu.bodycan.CemBodyFr51,
                        'HmiFragraChRatReqFragRatForCh1',
                        0,
                    ),
                    (
                        self.ipdu.bodycan.CemBodyFr51,
                        'HmiFragraChRatReqFragRatForCh2',
                        0,
                    ),
                    (
                        self.ipdu.bodycan.CemBodyFr51,
                        'HmiFragraChRatReqFragRatForCh3',
                        0,
                    ),
                    (
                        self.ipdu.bodycan.CemBodyFr51,
                        'HmiFragraChRatReqFragRatForCh4',
                        0,
                    ),
                    (
                        self.ipdu.bodycan.CemBodyFr51,
                        'HmiFragraChRatReqFragRatForCh5',
                        0,
                    ),
                ]
                for single_check in [check_cem_46, check_cem_48, check_cem_51]:
                    self.ipdu.check_multiple_signals(single_check)
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)


    @allure.title("初始化默认_除霜模式状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682848?projectId=46',
        name='空调测试case:1682848',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109703(self):
        with allure.step("调用接口SetFastDefrostMode,设置参数{'on':True}"):
            logger.info("调用接口SetFastDefrostMode,设置参数{'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("观察信号BodyCan:0x140:HmiDefrstMaxReq"):
                logger.info("观察信号BodyCan:0x140:HmiDefrstMaxReq")
                result = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiDefrstMaxReq',
                    0,
                    timeout=2,
                )
                logger.info("result {}".format(result))
                assert result[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_温度同步")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1776227?projectId=46',
        name='空调测试case:1776227',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_116009(self):
        with allure.step("调用接口SetTemperatureAndOn,设置参数{'zoneId':3, 'value':24.0}"):
            logger.info("调用接口SetTemperatureAndOn,设置参数{'zoneId':3, 'value':24.0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 3, 'value': 24.0},
            )
        sleep(1)
        with allure.step("调用接口SetAutoSyncMode,设置参数 {'on':True}"):
            logger.info("调用接口SetAutoSyncMode,设置参数 {'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAutoSyncMode',
                args={'on': True},
            )

        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step(
                "BodyCan:0x180:HmiCmptmtTSpForRowFirstLe；BodyCan:0x180:HmiCmptmtTSpForRowFirstRi；BodyCan:0x180:HmiCmptmtTSpForRowSecLe"
            ):
                logger.info(
                    "BodyCan:0x180:HmiCmptmtTSpForRowFirstLe；BodyCan:0x180:HmiCmptmtTSpForRowFirstRi；BodyCan:0x180:HmiCmptmtTSpForRowSecLe"
                )
                check_list = [
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowFirstLe',
                        18,
                    ),
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowFirstRi',
                        18,
                    ),
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowSecLe',
                        18,
                    ),
                ]
                self.ipdu.check_multiple_signals(check_list)
                self.ipdu.reset_check_results()
            sleep(1)
            with allure.step("调用接口GetAutoSyncMode"):
                logger.info("调用接口GetAutoSyncMode")
                self.partner.send_request_and_ck_resp(
                    'ClimateControlService_client',
                    'GetAutoSyncMode',
                    args={},
                    ck_info={'out': True},
                    timeout=3,
                )
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)


    @allure.title("初始化默认_节能模式")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682843?projectId=46',
        name='空调测试case:1682843',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109707(self):
        with allure.step("调用接口SetEcoMode,设置参数{'on':True}"):
            logger.info("调用接口SetEcoMode,设置参数{'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetEcoMode',
                args={'on': True},
            )
        sleep(2)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("观察信号BodyCan:0x357:HMIClimaEgySaveReq"):
                logger.info("观察信号BodyCan:0x357:HMIClimaEgySaveReq")
                result = self.ipdu.check(
                    self.ipdu.bodycan.CemBodyFr48,
                    'HMIClimaEgySaveReq',
                    1,
                    timeout=2,
                )
                logger.info("result {}".format(result))
                assert result[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_温度不同步")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1776421?projectId=46',
        name='空调测试case:1776421',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_115821(self):
        with allure.step("调用接口SetAutoSyncMode,设置参数 {'on':False}"):
            logger.info("调用接口SetAutoSyncMode,设置参数 {'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAutoSyncMode',
                args={'on': False},
            )
        with allure.step("调用接口SetTemperatureAndOn,设置参数{'zoneId':3, 'value':23.0}"):
            logger.info("调用接口SetTemperatureAndOn,设置参数{'zoneId':3, 'value':23.0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 3, 'value': 23.0},
            )
        sleep(1)
        with allure.step("调用接口SetTemperatureAndOn,设置参数{'zoneId':4, 'value':24.0}"):
            logger.info("调用接口SetTemperatureAndOn,设置参数{'zoneId':4, 'value':24.0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 4, 'value': 24.0},
            )
        sleep(1)
        with allure.step("调用接口SetTemperatureAndOn,设置参数{'zoneId':2, 'value':25.0}"):
            logger.info("调用接口SetTemperatureAndOn,设置参数{'zoneId':2, 'value':25.0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetTemperatureAndOn',
                args={'zoneId': 2, 'value': 25.0},
            )
        sleep(1)

        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step(
                "查看信号:BodyCan:0x180:HmiCmptmtTSpForRowFirstLe；BodyCan:0x180:HmiCmptmtTSpForRowFirstRi；BodyCan:0x180:HmiCmptmtTSpForRowSecLe；"
            ):
                logger.info(
                    "查看信号:BodyCan:0x180:HmiCmptmtTSpForRowFirstLe；BodyCan:0x180:HmiCmptmtTSpForRowFirstRi；BodyCan:0x180:HmiCmptmtTSpForRowSecLe；"
                )
                check_list = [
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowFirstLe',
                        16,
                    ),
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowFirstRi',
                        18,
                    ),
                    (
                        self.ipdu.bodycan.CEMBodyFr15,
                        'HmiCmptmtTSpForRowSecLe',
                        20,
                    ),
                ]
                self.ipdu.check_multiple_signals(check_list)
                self.ipdu.reset_check_results()
            sleep(1)
            with allure.step("调用接口GetAutoSyncMode"):
                logger.info("调用接口GetAutoSyncMode")
                self.partner.send_request_and_ck_resp(
                    'ClimateControlService_client',
                    'GetAutoSyncMode',
                    args={},
                    ck_info={'out': False},
                    timeout=3,
                )
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_AC开关状态_Manual状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682836?projectId=46',
        name='空调测试case:1682836',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109711(self):
        with allure.step("调用接口SetAC,设置参数:{'on':False}"):
            logger.info("调用接口SetAC,设置参数:{'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': False},
            )
        sleep(1)
        with allure.step("调用接口SetAC,设置参数:{'on':True}"):
            logger.info("调用接口SetAC,设置参数:{'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': True},
            )
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("查看信号BodyCan:0x180:HmiCmptmtCoolgReq"):
                logger.info("查看信号BodyCan:0x180:HmiCmptmtCoolgReq")
                result = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr15,
                    'HmiCmptmtCoolgReq',
                    1,
                    timeout=2,
                )
                logger.info("result {}".format(result))
                assert result[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_前后排风速_OFF状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682844?projectId=46',
        name='空调测试case:1682844',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109706(self):
        with allure.step("调用接口Off,设置参数{'zoneId':0}；"):
            logger.info("调用接口Off,设置参数{'zoneId':0}；")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        sleep(1)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step(
                "观察信号BodyCan:0x140:HmiHvacFanLvlFrnt,BodyCan:0x140:HmiHvacFanLvlRe"
            ):
                logger.info(
                    "观察信号BodyCan:0x140:HmiHvacFanLvlFrnt,BodyCan:0x140:HmiHvacFanLvlRe"
                )
                result_1 = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiHvacFanLvlFrnt',
                    0,
                    timeout=2,
                )

                result_2 = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiHvacFanLvlRe',
                    0,
                    timeout=2,
                )
                logger.info("result_1 {}".format(result_1))
                logger.info("result_2 {}".format(result_2))
                assert result_1[0] and result_2[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_前后排风速_Auto状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682847?projectId=46',
        name='空调测试case:1682847',
    )
    @pytest.mark.full
    @pytest.mark.restart
    def test_climate_soa_caseid_109704(self):
        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 3},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True};"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True};")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        with allure.step("调用接口On,设置参数{'zoneId':2}"):
            logger.info("调用接口On,设置参数{'zoneId':2}")
            self.partner.send_method_request(
                 'ClimateControlService_client',
                 'On',
                 args={'zoneId': 2},
            )
        sleep(1)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step(
                "观察信号BodyCan:0x140:HmiHvacFanLvlFrnt,BodyCan:0x140:HmiHvacFanLvlRe"
            ):
                logger.info(
                    "观察信号BodyCan:0x140:HmiHvacFanLvlFrnt,BodyCan:0x140:HmiHvacFanLvlRe"
                )
            with allure.step("查看信号BodyCan:0x140:HmiHvacFanLvlFrnt"):
                logger.info("查看信号BodyCan:0x140:HmiHvacFanLvlFrnt")
                result_1 = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiHvacFanLvlFrnt',
                    12,
                    timeout=2,
                )

                result_2 = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiHvacFanLvlRe',
                    12,
                    timeout=2,
                )
                logger.info("result_1 {}".format(result_1))
                logger.info("result_2 {}".format(result_2))
                assert result_1[0] and result_2[0]
                assert result_1[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_前后排风速_Manual状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682840?projectId=46',
        name='空调测试case:1682840',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109708(self):
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False};"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False};")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )
        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 3},
            )
        sleep(1)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("查看信号BodyCan:0x140:HmiHvacFanLvlFrnt"):
                logger.info("查看信号BodyCan:0x140:HmiHvacFanLvlFrnt")
                result_1 = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr14,
                    'HmiHvacFanLvlFrnt',
                    3,
                    timeout=2,
                )
                logger.info("result_1 {}".format(result_1))
                assert result_1[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_AC开关状态_Auto状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682839?projectId=46',
        name='空调测试case:1682839',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109709(self):
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True};"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True};")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        sleep(1)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("查看信号BodyCan:0x180:HmiCmptmtCoolgReq"):
                logger.info("查看信号BodyCan:0x180:HmiCmptmtCoolgReq")
                result = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr15,
                    'HmiCmptmtCoolgReq',
                    1,
                    timeout=2,
                )
                logger.info("result {}".format(result))
                assert result[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("初始化默认_AC开关状态_OFF状态")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1682838?projectId=46',
        name='空调测试case:1682838',
    )
    @pytest.mark.smoke
    @pytest.mark.restart
    def test_climate_soa_caseid_109710(self):
        with allure.step("调用接口Off,设置参数{'zoneId':0}；"):
            logger.info("调用接口Off,设置参数{'zoneId':0}；")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        sleep(1)
        with allure.step("Step:BGM Reboot"):
            logger.info("BGM Reboot")
            self.ipdu.pause_all_bus_send()
            self.restart_bgm_and_connect_service(
                "ClimateControlService_client"
            )
            sleep(5)
        try:
            with allure.step("查看信号BodyCan:0x180:HmiCmptmtCoolgReq"):
                logger.info("查看信号BodyCan:0x180:HmiCmptmtCoolgReq")
                result = self.ipdu.check(
                    self.ipdu.bodycan.CEMBodyFr15,
                    'HmiCmptmtCoolgReq',
                    0,
                    timeout=2,
                )

                logger.info("result_1 {}".format(result))
                assert result[0]
                self.ipdu.reset_check_results()
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()
        sleep(2)



    # @pytest.mark.smoke_001
    # @pytest.mark.checklist
    # @pytest.mark.full
    # @pytest.mark.restart
    # def test_climate_soa_caseid_116029(self):
    #     with allure.step("调用接口Off,设置参数{'zoneId':0}；"):
    #         logger.info("调用接口Off,设置参数{'zoneId':0}；")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'Off',
    #             args={'zoneId': 0},
    #         )
    #     sleep(1)
    #     with allure.step("调用接口On,设置参数{'zoneId':0}；"):
    #         logger.info("调用接口On,设置参数{'zoneId':0}；")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'On',
    #             args={'zoneId': 0},
    #         )
    #     sleep(1)
    #     with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False};"):
    #         logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False};")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'SetClimateAuto',
    #             args={'zoneId': 0, 'on': False},
    #         )
    #     sleep(1)
    #     with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
    #         logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'SetFastDefrostMode',
    #             args={'on': True},
    #         )
    #         sleep(1)
    #     with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': False"):
    #         logger.info("调用接口SetFastDefrostMode,设置参数:'on': False")
    #         self.partner.send_method_request(
    #             'ClimateControlService_client',
    #             'SetFastDefrostMode',
    #             args={'on': False},
    #         )
        
    #     logger.info("----------------------->1")
    #     self.com_lib.check_signal_value_and_times(("bodycan.CemBodyFr46", 'HmiClimaFrntAutReq_UB', 1, 1))
    #     logger.info("----------------------->2")

    #     # thread_1 = Thread(target=self.com_lib.check_signal_value_and_times,args=(("bodycan.CEMBodyFr46", 'HmiClimaFrntAutReq_UB', 1, 1),))
    #     # thread_1.start()
    #     # thread_2 = Thread(target=self.com_lib.check_signal_value_and_times,args=(("bodycan.CEMBodyFr46", 'HmiClimaReAutReq_UB', 1, 1),))
    #     # thread_2.start()

    #     sleep(5)

    @allure.title("联动_OFF_打开前除霜除雾_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_109306(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed", {"zoneId": 0, "speed": 5})
        
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})
        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"Step:查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt"):
            logger.info("查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt" )
            self.ipdu.check_thread_start(self.ipdu.bodycan.CEMBodyFr14,'HmiHvacFanLvlFrnt',9,timeout=2,)
            self.ipdu.check_thread_stop('HmiHvacFanLvlFrnt', timeout=5)
        
        self.ipdu.reset_check_results()

    @allure.title("联动_手动模式_打开前除霜除雾_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108193(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed", {"zoneId": 0, "speed": 3})
             
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"Step:查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt"):
            logger.info("查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt" )
            self.ipdu.check_thread_start(self.ipdu.bodycan.CEMBodyFr14,'HmiHvacFanLvlFrnt',9,timeout=2,)
            self.ipdu.check_thread_stop('HmiHvacFanLvlFrnt', timeout=5)
        
        self.ipdu.reset_check_results()


    @allure.title("联动_手动模式_打开前除霜除雾_AC状态")
    @pytest.mark.smoke
    def test_climate_soa_caseid_116107(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetAC,设置参数:'on':False"):
            logger.info("调用接口SetAC,设置参数:'on':False")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': False},
            )
        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq"):
            logger.info("查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr15,
                'HmiCmptmtCoolgReq',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiCmptmtCoolgReq', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_OFF_打开前除霜除雾_AC状态")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108735(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetAC,设置参数:'on':False"):
            logger.info("调用接口SetAC,设置参数:'on':False")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': False},
            )
        
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})
        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq"):
            logger.info("查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr15,
                'HmiCmptmtCoolgReq',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiCmptmtCoolgReq', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_OFF_打开前除霜除雾_内外循环模式_外循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115458(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':3"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':3")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 3},
            )
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})

        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_手动模式_打开前除霜除雾_内外循环模式_外循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115462(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':3"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':3")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 3},
            )

        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 3},
            )


        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_手动模式_打开前除霜除雾_内外循环模式_内循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_116118(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':2"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':2")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 2},
            )

        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':3}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 3},
            )


        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_OFF_开前除霜除雾_内外循环模式_内循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_109290(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
 
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':2"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':2")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 2},
            )
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})

        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                1,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_Auto模式_关闭")
    @pytest.mark.smoke
    def test_climate_soa_caseid_116029(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off", {"zoneId": 0})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"On", {"zoneId": 0})

        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':2"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':2")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 2},
            )

        with allure.step("调用接口SetAutoSyncMode,设置参数:{'on':False}"):
            logger.info("调用接口SetAutoSyncMode,设置参数:{'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAutoSyncMode',
                args={'on': False},
            )
        
        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': true"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': true")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': True},
            )

        with allure.step(f"调用接口SetFastDefrostMode,设置参数:'on': false"):
            logger.info("调用接口SetFastDefrostMode,设置参数:'on': false")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetFastDefrostMode',
                args={'on': False},
            )

        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                2,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_1995062(self):
        with allure.step(f"调用接口SetCycleMode,设置参数:'mode':2"):
            logger.info("调用接口SetCycleMode,设置参数:'mode':2")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetCycleMode',
                args={'mode': 2},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )
        sleep(5)
        with allure.step("调用接口Off,设置参数:{'zoneId':0}"):
            logger.info("调用接口Off,设置参数:{'zoneId':0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        with allure.step("调用接口On,设置参数{'zoneId':0}"):
            logger.info("调用接口On,设置参数{'zoneId':0}")
            self.partner.send_method_request(
                 'ClimateControlService_client',
                 'On',
                 args={'zoneId': 0},
            )
        sleep(5)
        with allure.step(f"查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd "):
            logger.info("查看循环模式信号BodyCan:0x140:HmiHvacRecircCmd ")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr14,
                'HmiHvacRecircCmd',
                2,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiHvacRecircCmd', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()
            sleep(0.5)

    @allure.title("泛化记忆_Auto模式_风量记忆Auto_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_1995063(self):
        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':5}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':5}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 5},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )

        with allure.step("调用接口Off,设置参数:{'zoneId':0}"):
            logger.info("调用接口Off,设置参数:{'zoneId':0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        with allure.step("调用接口On,设置参数{'zoneId':0}"):
            logger.info("调用接口On,设置参数{'zoneId':0}")
            self.partner.send_method_request(
                 'ClimateControlService_client',
                 'On',
                 args={'zoneId': 0},
            )

        with allure.step(f"Step:查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt"):
            logger.info("查看风量信号BodyCan:0x140:HmiHvacFanLvlFrnt" )
            self.ipdu.check_thread_start(self.ipdu.bodycan.CEMBodyFr14,'HmiHvacFanLvlFrnt',5,timeout=2,)
            self.ipdu.check_thread_stop('HmiHvacFanLvlFrnt', timeout=5)
        
        self.ipdu.reset_check_results()

    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_118010(self):
        with allure.step("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':5}"):
            logger.info("调用接口SetWindSpeed,设置参数:{'zoneId':1, 'speed':5}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetWindSpeed',
                args={'zoneId': 1, 'speed': 5},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )

        with allure.step("调用接口Off,设置参数:{'zoneId':0}"):
            logger.info("调用接口Off,设置参数:{'zoneId':0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        with allure.step("调用接口On,设置参数{'zoneId':0}"):
            logger.info("调用接口On,设置参数{'zoneId':0}")
            self.partner.send_method_request(
                 'ClimateControlService_client',
                 'On',
                 args={'zoneId': 0},
            )

        with allure.step(f"Step:查看风量信号BodyCan:0x140:HmiHvacFanLvlRe"):
            logger.info("查看风量信号BodyCan:0x140:HmiHvacFanLvlRe" )
            self.ipdu.check_thread_start(self.ipdu.bodycan.CEMBodyFr14,'HmiHvacFanLvlRe',5,timeout=2,)
            self.ipdu.check_thread_stop('HmiHvacFanLvlRe', timeout=5)
        
        self.ipdu.reset_check_results()

    @allure.title("泛化记忆_Auto模式_AC记忆ON_关闭Auto模式 ")
    @pytest.mark.full
    def test_climate_soa_caseid_1995064(self):
        with allure.step("调用接口SetAC,设置参数:{'on':False}"):
            logger.info("调用接口SetAC,设置参数:{'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetAC',
                args={'on': False},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':True}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': True},
            )
        with allure.step("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}"):
            logger.info("调用接口SetClimateAuto,设置参数:{'zoneId':0, 'on':False}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'SetClimateAuto',
                args={'zoneId': 0, 'on': False},
            )

        with allure.step("调用接口Off,设置参数:{'zoneId':0}"):
            logger.info("调用接口Off,设置参数:{'zoneId':0}")
            self.partner.send_method_request(
                'ClimateControlService_client',
                'Off',
                args={'zoneId': 0},
            )
        with allure.step("调用接口On,设置参数{'zoneId':0}"):
            logger.info("调用接口On,设置参数{'zoneId':0}")
            self.partner.send_method_request(
                 'ClimateControlService_client',
                 'On',
                 args={'zoneId': 0},
            )
        with allure.step(f"查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq"):
            logger.info("查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq")
            self.ipdu.check_thread_start(
                self.ipdu.bodycan.CEMBodyFr15,
                'HmiCmptmtCoolgReq',
                0,
                timeout=2,
            )
            result = self.ipdu.check_thread_stop('HmiCmptmtCoolgReq', timeout=5)
            logger.info("result {}".format(result))
            assert result[0]
            self.ipdu.reset_check_results()


    @allure.title("电动出风口副驾风向")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109698?projectId=46',
        name='空调测试case:109698',
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1982788(self):
        self.sd_tester.change_usage_mode(11, do_assert=1)

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 4, "side": 0, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 4, "side": 1, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_request_and_ck_resp(
            'ClimateControlService_client',
            'GetOutletAngle',
            args={"zoneId": [4]},
            ck_info={
                'out': [
                    {'id': 4, 'side': 0, 'horizontal': 50, 'vertical': 50},
                    {'id': 4, 'side': 1, 'horizontal': 50, 'vertical': 50},
                ]
            },
            timeout=3,
        )

    @allure.title("电动出风口主驾风向")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109698?projectId=46',
        name='空调测试case:109698',
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1982785(self):
        self.sd_tester.change_usage_mode(11, do_assert=1)

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 3, "side": 0, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 3, "side": 1, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_request_and_ck_resp(
            'ClimateControlService_client',
            'GetOutletAngle',
            args={"zoneId": [3]},
            ck_info={
                'out': [
                    {'id': 3, 'side': 0, 'horizontal': 50, 'vertical': 50},
                    {'id': 3, 'side': 1, 'horizontal': 50, 'vertical': 50},
                ]
            },
            timeout=3,
        )
        
    @allure.title("电动出风口后排风向")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109698?projectId=46',
        name='空调测试case:109698',
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1982791(self):
        self.sd_tester.change_usage_mode(11, do_assert=1)

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 2, "side": 0, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetOutletAngle',
            args={
                "outlets": [{"id": 2, "side": 1, "horizontal": 50, "vertical": 50}]
            },
        )

        self.partner.send_request_and_ck_resp(
            'ClimateControlService_client',
            'GetOutletAngle',
            args={"zoneId": [2]},
            ck_info={
                'out': [
                    {'id': 2, 'side': 0, 'horizontal': 50, 'vertical': 50},
                    {'id': 2, 'side': 1, 'horizontal': 50, 'vertical': 50},
                ]
            },
            timeout=3,
        )
        
        
    @allure.title("后除霜除雾_Normal_Convenience_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119094(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Convenience_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119096(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  

    @allure.title("后除霜除雾_Normal_Convenience_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119098(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Inactive_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119099(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Inactive_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119100(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Inactive_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119101(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Active_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119104(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Active_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119105(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Active_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119106(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Driving_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119109(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Driving_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119110(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Driving_温度10度_PCL5_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119114(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Abandoned_温度10度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119115(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=00 Abandoned
            self.sd_tester.change_usage_mode(0)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        


    @allure.title("后除霜除雾_Dyno_Convenience_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119137(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Convenience_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119118(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  

    @allure.title("后除霜除雾_Transport_Convenience_温度10度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119140(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 01 Transport
            self.sd_tester.change_car_mode(1)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results() 
        
    @allure.title("后除霜除雾_Factory_Convenience_温度10度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119139(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 02 Factory
            self.sd_tester.change_car_mode(2)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Crash_Convenience_温度10度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119141(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 03 Crash
            self.sd_tester.change_car_mode(3)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Convenience_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119117(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Inactive_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119119(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Inactive_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119131(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Inactive_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119135(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Active_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119133(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Active_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119128(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Active_温度10度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119122(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Driving_温度10度_PCL3_可以加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119121(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)

            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Driving_温度10度_PCL4_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119125(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Driving_温度10度_PCL5_可以加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119116(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Abandoned_温度10度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119126(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=00 Abandoned
            self.sd_tester.change_usage_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 10.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Convenience_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119095(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Convenience_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119097(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Inactive_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119102(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=01 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  

    @allure.title("后除霜除雾_Normal_Inactive_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119103(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=01 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
                
    @allure.title("后除霜除雾_Normal_Active_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119107(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=11 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Active_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119108(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=11 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Driving_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119111(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Normal_Driving_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119112(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Normal_Driving_温度40度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119113(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Convenience_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119134(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Convenience_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119123(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Inactive_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119132(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=01 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Inactive_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119129(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=01 Inactive
            self.sd_tester.change_usage_mode(1)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Active_温度40度_PCL3_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119120(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=11 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Active_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119136(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=11 Active
            self.sd_tester.change_usage_mode(11)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Driving_温度40度_PCL3_无法加热 ")
    @pytest.mark.full
    def test_climate_soa_caseid_119130(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)

            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
                        
    @allure.title("后除霜除雾_Dyno_Driving_温度40度_PCL4_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119124(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            self.sd_tester.write_multi_ccp({182: 0x4, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
 
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("后除霜除雾_Dyno_Driving_温度40度_PCL5_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_119127(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            # 车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            # 使用模式 Usage Mode=13 Driving
            self.sd_tester.change_usage_mode(13)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 40.0)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',3,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  
        
    @allure.title("出厂化设置_出风口模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109690(self):
        with allure.step("设置初始条件"):
            logger.info("Usage Mode 设置为Active")
            self.sd_tester.change_usage_mode(11, do_assert=1)
            sleep(1)

        with allure.step(f"调用接口ResetAllVehicleSOAConfig做出厂化设置"):
            logger.info("调用接口ResetAllVehicleSOAConfig做出厂化设置")
            self.partner.send_method_request(
                'ResetSOAConfigService_client',
                'ResetAllVehicleSOAConfig',
                args={},
            )
        with allure.step(
            "查看空调出风口模式信号:BodyCan:0x3A0:HmiElecAirDirModReqDrvrMod,BodyCan:0x3A0:HmiElecAirDirModReqPassMod,BodyCan:0x180:HmiReElecAirDirModReqReLeElecAirDirModReq,BodyCan:0x264:HmiReElecAirDirModReqReRiElecAirDirModReq"
        ):
            logger.info(
                "查看空调出风口模式信号:BodyCan:0x3A0:HmiElecAirDirModReqDrvrMod,BodyCan:0x3A0:HmiElecAirDirModReqPassMod,BodyCan:0x180:HmiReElecAirDirModReqReLeElecAirDirModReq,BodyCan:0x264:HmiReElecAirDirModReqReRiElecAirDirModReq"
            )
            check_list = [
                (self.ipdu.bodycan.CemBodyFr46, 'HmiElecAirDirModReqDrvrMod', 0),
                (self.ipdu.bodycan.CemBodyFr46, 'HmiElecAirDirModReqPassMod', 0),
                (self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirModReqReLeElecAirDirModReq', 0),
                (self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirModReqReRiElecAirDirModReq', 0)
            ]
            self.ipdu.check_multiple_signals(check_list)
            self.ipdu.reset_check_results()
            sleep(1)
        
    @allure.title("后除霜除雾_Normal_Convenience_温度35.3度_无法加热")
    @pytest.mark.full
    def test_climate_soa_caseid_1994505(self):
        with allure.step(f"Step:设置初始条件"):
            # 使用模式 Usage Mode=02 Convenience
            self.sd_tester.change_usage_mode(2)
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 0x5, 13: 0x4})        
        with allure.step(f"Step:Amb相关信号"):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideQly', 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'AmbTRawAtPassSideAmbTVal', 35.3)
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',2,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()    
        self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        self.ipdu.reset_check_results()  