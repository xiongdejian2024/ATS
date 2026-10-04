#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mix.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :需要多个基础能力一起模拟的场景，提供对应实现接口；
"""
import copy
import json
import yaml
import func_timeout

from .tsp import Tsp as CommonTsp
from .logmanagment import LogManagement as CommonLogManagement
from .io import Io as CommonIo
from .serial import Serial as CommonSerial
from .sdtest import SdTest as CommonSdTest
from .buscomm import BusComm as CommonBusComm
from .soa import Soa as CommonSoa
from .ssh import Ssh as CommonSsh
from .diagmock import DiagMock as CommonDiagMock
from .log_trigger_handler import LogTriggerHandler
from xat_ecu.api.call_tracker import BaseABCMeta
from typing import Any

from xat_ecu.api.common.common import *
from threading import Thread
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.sdk.sdk_tools import *
import datetime
from xat_ecu.legacy.sdk.Internal_ETH.tools.utils import write_s2s_json, s2s_path
test_count = 0


class Mix(metaclass=BaseABCMeta):
    def __init__(
            self,
            tsp: CommonTsp,
            log_manage: CommonLogManagement,
            io: CommonIo,
            serial: CommonSerial,
            sd_tester: CommonSdTest,
            bus_comm: CommonBusComm,
            soa: CommonSoa,
            ssh: CommonSsh,
            diag_mock: CommonDiagMock
    ):
        self.tsp = tsp
        self.log_manage = log_manage
        self.io = io
        self.serial = serial
        self.sd_tester = sd_tester
        self.bus_comm = bus_comm
        self.soa = soa
        self.ssh = ssh
        self.diag_mock = diag_mock
        self.func_param = {}  # 用于存储自动回复SOA报文的参数
        self.ignore_func = []
        self.log_special_obj = LogTriggerHandler(self)
        self.all_bus_data_info = {}
        self.all_bus_msgid_info = {}

    def set_usage_mode(self, usage_mode: UsageMode, do_assert: bool = True):
        with allure.step(f"设置usage mode {usage_mode.name}"):
            self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", "VehSpdLgtA", 0)
            time.sleep(0.1)
            self.bus_comm.set(
                "backbonefr",
                "BcmVddmBackBoneFr06",
                "VehSpdLgtQf",
                3,
            )
            time.sleep(0.1)
            self.bus_comm.set(
                "backbonefr",
                "BcmVddmBackBoneFr00",
                "VehMtnStVehMtnSt",
                "VehMtnSt2_StandStillVal3",
            )
            time.sleep(0.1)
            self.sd_tester.change_usage_mode(usage_mode, do_assert=do_assert)
        logger.info(f"设置usage mode {usage_mode.name} 成功")

    def set_car_mode(self, car_mode: CarMode):
        with allure.step(f"设置car mode {car_mode.name}"):
            self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", "VehSpdLgtA", 0)
            time.sleep(0.1)
            self.bus_comm.set(
                "backbonefr",
                "BcmVddmBackBoneFr06",
                "VehSpdLgtQf",
                3,
            )
            time.sleep(0.1)
            self.bus_comm.set(
                "backbonefr",
                "BcmVddmBackBoneFr00",
                "VehMtnStVehMtnSt",
                "VehMtnSt2_StandStillVal3",
            )
            time.sleep(0.1)
            self.sd_tester.change_car_mode(car_mode)
        logger.info(f"设置car mode {car_mode.name} 成功")

    def send_s2s_service_request(self, send_s2s_request_parameter: Union[tuple, list]):
        if isinstance(send_s2s_request_parameter, list):
            for send_s2s_request_parameter_tuple in send_s2s_request_parameter:
                if len(send_s2s_request_parameter_tuple) != 0:
                    logger.info(
                        "模拟发送s2s请求(服务:{},接口:{},参数:{})".format(
                            send_s2s_request_parameter_tuple[0],
                            send_s2s_request_parameter_tuple[1],
                            send_s2s_request_parameter_tuple[2],
                        )
                    )

                    if (
                        len(send_s2s_request_parameter_tuple) > 3
                        and "timeout" in send_s2s_request_parameter_tuple[3]
                    ):
                        timeout = float(
                            send_s2s_request_parameter_tuple[3].split("=")[-1]
                        )
                    else:
                        timeout = 2

                    if "_client" not in send_s2s_request_parameter_tuple[0]:
                        service_name = send_s2s_request_parameter_tuple[0] + "_client"
                    else:
                        service_name = send_s2s_request_parameter_tuple[0]
                    self.soa.send_method_request(
                        service_name,
                        send_s2s_request_parameter_tuple[1],
                        send_s2s_request_parameter_tuple[2],
                        timeout,
                    )
                sleep(0.5)
        elif isinstance(send_s2s_request_parameter, tuple):
            if len(send_s2s_request_parameter) != 0:
                send_s2s_request_parameter_tuple = send_s2s_request_parameter
                logger.info(
                    "模拟发送s2s请求(服务:{},接口:{},参数:{})".format(
                        send_s2s_request_parameter_tuple[0],
                        send_s2s_request_parameter_tuple[1],
                        send_s2s_request_parameter_tuple[2],
                    )
                )

                if (
                    len(send_s2s_request_parameter_tuple) > 3
                    and "timeout" in send_s2s_request_parameter_tuple[3]
                ):
                    timeout = float(send_s2s_request_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in send_s2s_request_parameter_tuple[0]:
                    service_name = send_s2s_request_parameter_tuple[0] + "_client"
                else:
                    service_name = send_s2s_request_parameter_tuple[0]
                self.soa.send_method_request(
                    service_name,
                    send_s2s_request_parameter_tuple[1],
                    send_s2s_request_parameter_tuple[2],
                    timeout,
                )
        else:
            raise Exception("send_s2s_request_parameter 参数类型只能为数组和元组")

    def check_s2s_event(self, check_s2s_event_parameter: Union[tuple, list]):
        if isinstance(check_s2s_event_parameter, list):
            for check_s2s_event_parameter_tuple in check_s2s_event_parameter:
                if len(check_s2s_event_parameter_tuple) != 0:
                    logger.info(
                        "模拟发送s2s请求(服务:{},接口:{},参数:{})".format(
                            check_s2s_event_parameter_tuple[0],
                            check_s2s_event_parameter_tuple[1],
                            check_s2s_event_parameter_tuple[2],
                        )
                    )

                    if (
                        len(check_s2s_event_parameter_tuple) > 3
                        and "timeout" in check_s2s_event_parameter_tuple[3]
                    ):
                        timeout = float(
                            check_s2s_event_parameter_tuple[3].split("=")[-1]
                        )
                    else:
                        timeout = 2

                    if "_client" not in check_s2s_event_parameter_tuple[0]:
                        service_name = check_s2s_event_parameter_tuple[0] + "_client"
                    else:
                        service_name = check_s2s_event_parameter_tuple[0]
                    self.soa.ck_s2s_event(
                        service_name,
                        check_s2s_event_parameter_tuple[1],
                        check_s2s_event_parameter_tuple[2],
                        timeout,
                    )
        elif isinstance(check_s2s_event_parameter, tuple):
            if len(check_s2s_event_parameter) != 0:
                check_s2s_event_parameter_tuple = check_s2s_event_parameter
                logger.info(
                    "模拟发送s2s请求(服务:{},接口:{},参数:{})".format(
                        check_s2s_event_parameter_tuple[0],
                        check_s2s_event_parameter_tuple[1],
                        check_s2s_event_parameter_tuple[2],
                    )
                )

                if (
                    len(check_s2s_event_parameter_tuple) > 3
                    and "timeout" in check_s2s_event_parameter_tuple[3]
                ):
                    timeout = float(check_s2s_event_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in check_s2s_event_parameter_tuple[0]:
                    service_name = check_s2s_event_parameter_tuple[0] + "_client"
                else:
                    service_name = check_s2s_event_parameter_tuple[0]
                self.soa.ck_s2s_event(
                    service_name,
                    check_s2s_event_parameter_tuple[1],
                    check_s2s_event_parameter_tuple[2],
                    timeout,
                )
        else:
            raise Exception("check_s2s_event_parameter 参数类型只能为数组和元组")

    def send_s2s_request_and_check_response(
        self, send_s2s_req_and_check_resp: Union[tuple, list]
    ):
        if isinstance(send_s2s_req_and_check_resp, list):
            for send_s2s_req_and_check_resp_tuple in send_s2s_req_and_check_resp:
                if len(send_s2s_req_and_check_resp_tuple) != 0:
                    logger.info(
                        "模拟发送s2s请求(服务:{},接口:{},参数:{},期望返回值是{})".format(
                            send_s2s_req_and_check_resp_tuple[0],
                            send_s2s_req_and_check_resp_tuple[1],
                            send_s2s_req_and_check_resp_tuple[2],
                            send_s2s_req_and_check_resp_tuple[3],
                        )
                    )

                    if (
                        len(send_s2s_req_and_check_resp_tuple) > 4
                        and "timeout" in send_s2s_req_and_check_resp_tuple[3]
                    ):
                        timeout = float(
                            send_s2s_req_and_check_resp_tuple[4].split("=")[-1]
                        )
                    else:
                        timeout = 2

                    if "_client" not in send_s2s_req_and_check_resp_tuple[0]:
                        service_name = send_s2s_req_and_check_resp_tuple[0] + "_client"
                    else:
                        service_name = send_s2s_req_and_check_resp_tuple[0]
                    self.soa.send_request_and_ck_resp(
                        service_name,
                        send_s2s_req_and_check_resp_tuple[1],
                        send_s2s_req_and_check_resp_tuple[2],
                        send_s2s_req_and_check_resp_tuple[3],
                        timeout,
                    )
                sleep(1)
        elif isinstance(send_s2s_req_and_check_resp, tuple):
            if len(send_s2s_req_and_check_resp) != 0:
                send_s2s_req_and_check_resp_tuple = send_s2s_req_and_check_resp
                logger.info(
                    "模拟发送s2s请求(服务:{},接口:{},参数:{},期望返回值是{})".format(
                        send_s2s_req_and_check_resp_tuple[0],
                        send_s2s_req_and_check_resp_tuple[1],
                        send_s2s_req_and_check_resp_tuple[2],
                        send_s2s_req_and_check_resp_tuple[3],
                    )
                )

                if (
                    len(send_s2s_req_and_check_resp_tuple) > 4
                    and "timeout" in send_s2s_req_and_check_resp_tuple[3]
                ):
                    timeout = float(send_s2s_req_and_check_resp_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in send_s2s_req_and_check_resp_tuple[0]:
                    service_name = send_s2s_req_and_check_resp_tuple[0] + "_client"
                else:
                    service_name = send_s2s_req_and_check_resp_tuple[0]
                self.soa.send_request_and_ck_resp(
                    service_name,
                    send_s2s_req_and_check_resp_tuple[1],
                    send_s2s_req_and_check_resp_tuple[2],
                    send_s2s_req_and_check_resp_tuple[3],
                    timeout,
                )
        else:
            raise Exception("send_s2s_req_and_check_resp 参数类型只能为数组和元组")

    def set_common_precontion(
        self,
        usage_mode: Union[UsageMode, None] = UsageMode.INACTIVE,
        car_mode: Union[CarMode, None] = CarMode.NORMAL,
        veh_spd: Union[float, int] = 0.0,
        vehmtnst: Union[VehMtnSts, None] = None,
        doors_sts: Union[Door, None] = None,
        cenlock_sts: Union[CenLockSts, None] = None,
        ccp: dict = {},
    ):
        with allure.step("置初始化条件"):
            self.bus_comm.set(
                    "backbonefr",
                    "BcmVddmBackBoneFr00",
                    "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
                    VehMtnSts.StandStillVal3.value,
                )
            logger.info("设置UsageMode={},CarMode={}".format(usage_mode, car_mode))
            if usage_mode==UsageMode.DRIVING:                
                self.set_car_mode(car_mode)
                sleep(0.5)
                self.set_usage_mode(usage_mode)
                sleep(0.5)
            else:
                self.set_usage_mode(usage_mode)
                sleep(0.5)
                self.set_car_mode(car_mode)
                sleep(0.5)
            
            logger.info("设置车速为{}".format(veh_spd))
            self.bus_comm.set_vehspd_gear(vehspd=veh_spd)
            sleep(0.5)

            logger.info("车辆状态为{}".format(vehmtnst))
            if vehmtnst != None:
                # 设置车辆状态VehMtnSt
                self.bus_comm.set(
                    "backbonefr",
                    "BcmVddmBackBoneFr00",
                    "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
                    vehmtnst.value,
                )
                sleep(0.1)
                self.bus_comm.set(
                    "backbonefr", "VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 0
                )

            elif veh_spd == 0.0:
                # 设置车辆状态VehMtnSt
                self.bus_comm.set(
                    "backbonefr",
                    "BcmVddmBackBoneFr00",
                    "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
                    VehMtnSts.StandStillVal3.value,
                )
                sleep(0.1)
                self.bus_comm.set(
                    "backbonefr", "VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 0
                )

            if doors_sts != None:
                logger.info("设置4门状态为{}".format(doors_sts.value))
                if doors_sts.value == "close":
                    self.io.set_five_door_sts(Door.close)
                elif doors_sts.value == "open":
                    self.io.set_five_door_sts(Door.open)

            if cenlock_sts != None:
                logger.info("设置中控锁状态为{}".format(cenlock_sts.value))
                # self.dk.set_cenlock_sts(cenlock_sts.value)
                sleep(0.5)

            logger.info("设置CCP为{}".format(ccp))
            if ccp != {}:
                self.sd_tester.write_ccp(ccp)
            sleep(1)

    def send_s2s_request_and_check(
        self,
        send_s2s_request_parameter: Union[tuple, list],
        check_signal_parameter: Union[tuple, list] = (),
        check_service_response: Union[tuple, list] = (),
        check_s2s_event_parameter: Union[tuple, list] = (),
    ):
        if isinstance(check_signal_parameter, list):
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = bus_msg_list[0]
                    obj_msg = bus_msg_list[1]

                    if (
                        len(check_signal_parameter_tuple) > 3
                        and "timeout" in check_signal_parameter_tuple[3]
                    ):
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    logger.info(
                        "启动检测信号{}({})的进程,期望的信号值是{}".format(
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[0],
                            check_signal_parameter_tuple[2],
                        )
                    )
                    self.bus_comm.check_thread_start(
                        obj_bus,
                        obj_msg,
                        check_signal_parameter_tuple[1],
                        check_signal_parameter_tuple[2],
                        timeout,
                    )
                else:
                    logger.info("不需要检测总线信号")

            self.send_s2s_service_request(send_s2s_request_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(2)
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    logger.info(
                        "结束检测信号{}({})的进程,获取实际检测结果".format(
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[0],
                        )
                    )
                    result = self.bus_comm.check_thread_stop(
                        check_signal_parameter_tuple[1], timeout=5
                    )
                    logger.info("实际检测结果{}".format(result))
                    if result == None:
                        assert False
                    else:
                        assert result[0]
                else:
                    logger.info("不需要检测总线信号")

            self.bus_comm.ipdu.reset_check_results()
            self.send_s2s_request_and_check_response(check_service_response)

        elif isinstance(check_signal_parameter, tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) != 0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = bus_msg_list[0]
                obj_msg = bus_msg_list[1]
                if (
                    len(check_signal_parameter_tuple) > 3
                    and "timeout" in check_signal_parameter_tuple[3]
                ):
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                logger.info(
                    "启动检测信号{}({})的进程,期望的信号值是{}".format(
                        check_signal_parameter_tuple[1],
                        check_signal_parameter_tuple[0],
                        check_signal_parameter_tuple[2],
                    )
                )
                self.bus_comm.check_thread_start(
                    obj_bus,
                    obj_msg,
                    check_signal_parameter_tuple[1],
                    check_signal_parameter_tuple[2],
                    timeout,
                )
            else:
                logger.info("不需要检测总线信号")

            self.send_s2s_service_request(send_s2s_request_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(2)
            if len(check_signal_parameter_tuple) != 0:
                logger.info(
                    "结束检测信号{}({})的进程,获取实际检测结果".format(
                        check_signal_parameter_tuple[1], check_signal_parameter_tuple[0]
                    )
                )
                result = self.bus_comm.check_thread_stop(
                    check_signal_parameter_tuple[1], timeout=5
                )
                logger.info("实际检测结果{}".format(result))
                if result == None:
                    assert False
                else:
                    assert result[0]
                self.bus_comm.ipdu.reset_check_results()
            else:
                logger.info("不需要检测总线信号")
            sleep(2)
            self.send_s2s_request_and_check_response(check_service_response)
        else:
            raise Exception("send_s2s_req_and_check_resp 参数类型只能为数组和元组")
        sleep(3)

    def check_signal_value_all_is(self, check_signal_parameter_tuple: tuple):
        bus_msg_list = check_signal_parameter_tuple[0].split(".")
        obj_bus = bus_msg_list[0]
        obj_msg = bus_msg_list[1]

        logger.info(
            "检测信号{}({})信号值是否全部是{}".format(
                check_signal_parameter_tuple[1],
                check_signal_parameter_tuple[0],
                check_signal_parameter_tuple[2],
            )
        )
        if (
            len(check_signal_parameter_tuple) > 3
            and "timeout" in check_signal_parameter_tuple[3]
        ):
            timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
        else:
            timeout = 2

        result_ori = self.bus_comm.check_signal(
            obj_bus, obj_msg, check_signal_parameter_tuple[1], timeout
        )
        logger.info(
            "{}秒内获取信号{}所有的值是:{}".format(
                timeout, check_signal_parameter_tuple[0], result_ori
            )
        )
        result = check_all_value_is(result_ori, int(check_signal_parameter_tuple[2]))
        logger.info("期望值的统计结果:{}".format(result))
        assert result
        self.bus_comm.ipdu.reset_check_results()

    # def check_signal_value_and_times(self, check_signal_parameter_tuple: tuple):
    #     bus_msg_list = check_signal_parameter_tuple[0].split(".")
    #     obj_bus = bus_msg_list[0]
    #     obj_msg = bus_msg_list[1]

    #     logger.info(
    #         "检测信号{}({})信号值{}是否发了{}次".format(
    #             check_signal_parameter_tuple[1],
    #             check_signal_parameter_tuple[0],
    #             check_signal_parameter_tuple[2],
    #             check_signal_parameter_tuple[3],
    #         )
    #     )
    #     if (len(check_signal_parameter_tuple) > 4 and "timeout" in check_signal_parameter_tuple[4]):
    #         timeout = float(check_signal_parameter_tuple[4].split("=")[-1])
    #     else:
    #         timeout = 2

    #     result_ori = self.bus_comm.check_signal(obj_bus, obj_msg, check_signal_parameter_tuple[1], timeout)
    #     logger.info("{}秒内获取信号{}所有的值是:{}".format(timeout, check_signal_parameter_tuple[0], result_ori)
    #     )
    #     result = get_signal_times_interval(
    #         result_ori, int(check_signal_parameter_tuple[2])
    #     )
    #     logger.info("期望值的统计结果:{}".format(result))
    #     assert result[0] == check_signal_parameter_tuple[3]
    #     self.bus_comm.ipdu.reset_check_results()

    def set_signal_value(self, set_signal_parameter: Union[tuple, list]):
        if isinstance(set_signal_parameter, list):
            for set_signal_parameter_tuple in set_signal_parameter:
                if len(set_signal_parameter_tuple) != 0:
                    bus_msg_list = set_signal_parameter_tuple[0].split(".")
                    obj_bus = bus_msg_list[0]
                    obj_msg = bus_msg_list[1]

                    logger.info(
                        "设置信号{}({})信号值为{}".format(
                            set_signal_parameter_tuple[1],
                            set_signal_parameter_tuple[0],
                            set_signal_parameter_tuple[2],
                        )
                    )
                    if (
                        len(set_signal_parameter_tuple) > 3
                        and "timeout" in set_signal_parameter_tuple[3]
                    ):
                        timeout = float(set_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    self.bus_comm.set(
                        obj_bus,
                        obj_msg,
                        set_signal_parameter_tuple[1],
                        set_signal_parameter_tuple[2],
                        timeout,
                    )
                    sleep(0.1)
        elif isinstance(set_signal_parameter, tuple):
            set_signal_parameter_tuple = set_signal_parameter
            if len(set_signal_parameter_tuple) != 0:
                bus_msg_list = set_signal_parameter_tuple[0].split(".")
                obj_bus = bus_msg_list[0]
                obj_msg = bus_msg_list[1]

                logger.info(
                    "设置信号{}({})信号值为{}".format(
                        set_signal_parameter_tuple[1],
                        set_signal_parameter_tuple[0],
                        set_signal_parameter_tuple[2],
                    )
                )
                if (
                    len(set_signal_parameter_tuple) > 3
                    and "timeout" in set_signal_parameter_tuple[3]
                ):
                    timeout = float(set_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                self.bus_comm.set(
                    obj_bus,
                    obj_msg,
                    set_signal_parameter_tuple[1],
                    set_signal_parameter_tuple[2],
                    timeout,
                )
                sleep(0.1)
        else:
            raise Exception("set_signal_parameter 参数类型只能为数组和元组")

    def check_signal_value(self, check_signal_parameter: Union[tuple, list]):
        if isinstance(check_signal_parameter, list):
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = bus_msg_list[0]
                    obj_msg = bus_msg_list[1]

                    logger.info(
                        "Check信号{}({})信号值是否为{}".format(
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[0],
                            check_signal_parameter_tuple[2],
                        )
                    )
                    if (
                        len(check_signal_parameter_tuple) > 3
                        and "timeout" in check_signal_parameter_tuple[3]
                    ):
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2

                    thread = Thread(
                        target=self.bus_comm.check,
                        args=(
                            obj_bus,
                            obj_msg,
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[2],
                            timeout,
                        ),
                    )
                    thread.setDaemon(True)
                    thread.start()

        elif isinstance(check_signal_parameter, tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) != 0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = bus_msg_list[0]
                obj_msg = bus_msg_list[1]

                logger.info(
                    "Check信号{}({})信号值是否为{}".format(
                        check_signal_parameter_tuple[1],
                        check_signal_parameter_tuple[0],
                        check_signal_parameter_tuple[2],
                    )
                )
                if (
                    len(check_signal_parameter_tuple) > 3
                    and "timeout" in check_signal_parameter_tuple[3]
                ):
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                self.bus_comm.check(
                    obj_bus.obj_msg,
                    check_signal_parameter_tuple[1],
                    check_signal_parameter_tuple[2],
                    timeout,
                )
                self.bus_comm.ipdu.reset_check_results()
        else:
            raise Exception("check_signal_parameter 参数类型只能为数组和元组")
        sleep(2)

    def set_signal_and_check(
        self,
        set_signal_parameter: Union[tuple, list],
        check_signal_parameter: Union[tuple, list] = (),
        check_service_response: Union[tuple, list] = (),
        check_s2s_event_parameter: Union[tuple, list] = (),
    ):
        if isinstance(check_signal_parameter, list):
            if len(check_signal_parameter_tuple) != 0:
                for check_signal_parameter_tuple in check_signal_parameter:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = bus_msg_list[0]
                    obj_msg = bus_msg_list[1]
                    if (
                        len(check_signal_parameter_tuple) > 3
                        and "timeout" in check_signal_parameter_tuple[3]
                    ):
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    logger.info(
                        "启动检测信号{}({})的进程,期望的信号值是{}".format(
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[0],
                            check_signal_parameter_tuple[2],
                        )
                    )
                    self.bus_comm.check_thread_start(
                        obj_bus,
                        obj_msg,
                        check_signal_parameter_tuple[1],
                        check_signal_parameter_tuple[2],
                        timeout,
                    )

            self.set_signal_value(set_signal_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(2)
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    logger.info(
                        "结束检测信号{}({})的进程,获取实际检测结果".format(
                            check_signal_parameter_tuple[1],
                            check_signal_parameter_tuple[0],
                        )
                    )
                    result = self.bus_comm.check_thread_stop(
                        check_signal_parameter_tuple[1], timeout=5
                    )
                    logger.info("实际检测结果{}".format(result))
                    if result == None:
                        assert False
                    else:
                        assert result[0]

        elif isinstance(check_signal_parameter, tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) != 0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = bus_msg_list[0]
                obj_msg = bus_msg_list[1]
                if (
                    len(check_signal_parameter_tuple) > 3
                    and "timeout" in check_signal_parameter_tuple[3]
                ):
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                logger.info(
                    "启动检测信号{}({})的进程,期望的信号值是{}".format(
                        check_signal_parameter_tuple[1],
                        check_signal_parameter_tuple[0],
                        check_signal_parameter_tuple[2],
                    )
                )
                self.bus_comm.check_thread_start(
                    obj_bus,
                    obj_msg,
                    check_signal_parameter_tuple[1],
                    check_signal_parameter_tuple[2],
                    timeout,
                )

                self.set_signal_value(set_signal_parameter)
                self.check_s2s_event(check_s2s_event_parameter)
                sleep(2)
                logger.info(
                    "结束检测信号{}({})的进程,获取实际检测结果".format(
                        check_signal_parameter_tuple[1], check_signal_parameter_tuple[0]
                    )
                )
                result = self.bus_comm.check_thread_stop(
                    check_signal_parameter_tuple[1], timeout=5
                )
                logger.info("实际检测结果{}".format(result))
                if result == None:
                    assert False
                else:
                    assert result[0]
            else:
                self.set_signal_value(set_signal_parameter)
                self.check_s2s_event(check_s2s_event_parameter)
        else:
            raise Exception("check_signal_parameter 参数类型只能为数组和元组")
        self.send_s2s_request_and_check_response(check_service_response)
        sleep(3)
        self.bus_comm.ipdu.reset_check_results()

    def set_get_battery_tem_sts(self, HvBattCellTInfo: int, sts: bool):
        with allure.step("设置获取电池低温告警"):
            self.bus_comm.set(
                "backbonefr",
                "VddmBackBoneFr19",
                "HvBattCellTInfoHvBattTMin",
                HvBattCellTInfo,
            )
            self.soa.send_request_and_ck_resp(
                "HighVoltageService_client",
                "GetBatteryTemperatureLowState",
                {},
                {"out": sts},
            )

    def set_get_hv_power_sts(self, err_sts: bool, ValidityLevel: ValidityLevel):
        pass

    def set_get_hv_thermal_outof_control(self):
        pass

    def set_get_hv_battery_Fault(self, err_sts: bool, ValidityLevel: ValidityLevel):
        pass

    def parse_excel_to_signal_routing_csv(self, excel_path, csv_path):
        """
        把 信号路由的excel 表处理成需要的csv 文件
        @param self:
        @param excel_path: 原表路径
        @param csv_path: 保存的csv 文件路径
        @return:
        """
        # 读取excel文件
        t1 = time.time()
        workbook = xlrd.open_workbook(excel_path)
        logger.info(f"解析excel 表耗时{time.time() - t1}")
        table = workbook.sheet_by_name("Matrix")
        header_list = [item.strip().replace(" ", "") for item in table.row_values(0)]
        header = []
        for item in header_list:
            if "FrameID" in item:
                header.append("FrameID")
            elif "FrameRate" in item:
                header.append("FrameRate")
            else:
                header.append(item)
        # 经过bgm的 路由信号
        data_info_dict = {
            # "ALM10Flt": {
            #     "TX": {},
            #     "GW": [{}, {}]
            # }
        }
        # 存放crc 的信号名字
        chks_sig_set = set()
        # 存放 counter 的信号名字
        cntr_sig_set = set()
        # 便利该表，使用nrows，和ncols代表当前表的有效行列数。
        for row in range(1, table.nrows):
            row_data = [str(item) for item in table.row_values(row)]
            data_info = dict(zip(header, row_data))
            sig_name = data_info.get("Sig")
            # 判断是不是带crc 或者counter
            if sig_name.endswith("Chks"):
                chks_sig_set.add(sig_name[:-4])
            if sig_name.endswith("Cntr"):
                cntr_sig_set.add(sig_name[:-4])
            tx_type = data_info.get("TxType")
            tx_com_ecu = data_info.get("TxComEcu")
            # 过滤 bgm 发送的，不是路由的信号
            if tx_type.lower() == "tx" and tx_com_ecu.lower() == "bgm":
                continue
            # 过滤非bgm 路由的信号
            if tx_type.lower() == "gw" and tx_com_ecu.lower() != "bgm":
                continue
            if sig_name in data_info_dict:
                if tx_type in data_info_dict[sig_name]:
                    data_info_dict[sig_name][tx_type].append(data_info)
                else:
                    data_info_dict[sig_name][tx_type] = [data_info]
            else:
                data_info_dict[sig_name] = {}
                data_info_dict[sig_name][tx_type] = [data_info]
        csv_header = [
            "SignalName",
            "Tx_BusChannel",
            "Tx_ECUName",
            "Tx_MessageName",
            "Tx_MessageID",
            "Tx_MessageCyclic",
            "EnableUB",
            "crc",
            "counter",
            "Rx_BusChannel",
            "Rx_ECUName",
            "Rx_MessageName",
            "Rx_MessageID",
            "Rx_MessageCyclic",
            "Len",
            "repeat",
        ]
        # 写入 csv 表
        try:
            with open(csv_path, "w", newline="") as csv_f:
                csv_writer = csv.writer(csv_f)
                # 写入 表头
                csv_writer.writerow(csv_header)
                for signal_name, value_info in data_info_dict.items():
                    # print(value_info)
                    send_item_list = value_info.get("Tx")
                    if send_item_list is None:
                        continue
                    recv_item_info = value_info.get("Gw")
                    if recv_item_info is None:
                        continue
                    writer_data = []
                    writer_data.append(signal_name)

                    send_item = send_item_list[0]

                    Tx_BusChannel = send_item["Bus"]
                    writer_data.append(Tx_BusChannel)

                    Tx_ECUName = send_item["TxEcu"]
                    writer_data.append(Tx_ECUName)

                    Tx_MessageName = send_item["Frame"]
                    writer_data.append(Tx_MessageName)

                    Tx_MessageID = str(send_item["FrameID"])
                    Tx_MessageID = Tx_MessageID.replace("-", "=")
                    writer_data.append(Tx_MessageID)

                    Tx_MessageCyclic = (
                        str(send_item["FrameRate"]).replace(",", "").replace("，", "")
                    )

                    if "EventTriggered".lower() in Tx_MessageCyclic.lower():
                        Tx_MessageCyclic = Tx_MessageCyclic
                    elif "/" in Tx_MessageCyclic:
                        Tx_MessageCyclic = [
                            int(float(item) / 1000)
                            for item in Tx_MessageCyclic.split("/")
                        ]
                    else:
                        Tx_MessageCyclic = int(float(Tx_MessageCyclic) / 1000)
                    writer_data.append(Tx_MessageCyclic)

                    EnableUB = str(send_item["SigUB"]).strip()
                    writer_data.append(EnableUB)
                    # 判断带不带 crc
                    crc = ""
                    for name in chks_sig_set:
                        if name in signal_name:
                            crc = True
                            break
                    writer_data.append(crc)
                    # 判断带不带counter
                    counter = ""
                    for name in cntr_sig_set:
                        if name in signal_name:
                            counter = True
                            break
                    writer_data.append(counter)

                    #
                    recv_list = set()
                    for recv_item in recv_item_info:
                        recv_data_list = []
                        Rx_BusChannel = recv_item["Bus"]
                        recv_data_list.append(Rx_BusChannel)

                        Rx_ECUName = recv_item["RxEcu"]
                        recv_data_list.append(Rx_ECUName)
                        if Rx_ECUName.lower() == "S2SReceiver".lower():
                            continue

                        Rx_MessageName = recv_item["Frame"]
                        recv_data_list.append(Rx_MessageName)

                        Rx_MessageID = str(recv_item["FrameID"])
                        Rx_MessageID = Rx_MessageID.replace("-", "=")
                        recv_data_list.append(Rx_MessageID)
                        # Rx_MessageCyclic = recv_item['FrameRate']
                        # recv_data_list.append(Rx_MessageCyclic)
                        Rx_MessageCyclic = (
                            str(recv_item["FrameRate"])
                            .replace(",", "")
                            .replace("，", "")
                        )

                        if "EventTriggered".lower() in Rx_MessageCyclic.lower():
                            Rx_MessageCyclic = Rx_MessageCyclic
                        elif "/" in Rx_MessageCyclic:
                            Rx_MessageCyclic = [
                                int(float(item) / 1000)
                                for item in Rx_MessageCyclic.split("/")
                            ]
                        else:
                            Rx_MessageCyclic = int(float(Rx_MessageCyclic) / 1000)
                        recv_data_list.append(Rx_MessageCyclic)
                        #
                        sig_len = recv_item["Len"]
                        recv_data_list.append(sig_len)
                        # 标记重复的
                        # 接收通道和id 都一样的 算重复
                        temp = (Rx_BusChannel, Rx_MessageID)
                        if temp in recv_list:
                            repeat = "1"
                        else:
                            repeat = "0"
                        recv_list.add(temp)

                        recv_data_list.append(repeat)

                        datd_list = writer_data + recv_data_list
                        csv_writer.writerow(datd_list)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            string_log = f"生成 csv 失败》》{str(e)}"
            logger.error(string_log)
            # 删除csv 文件 必须执行的
            os.system(f"rm -rf {csv_path}")
            assert 0, string_log
        return csv_path

    def read_signal_routing_info(self, path=None, select_cond="cycle"):
        """
        读取信号路由的相关信息
        @param path: csv 文件路径
        @param select_cond: 根据条件筛选 ["cycle", "event", "ub", "crc", "counter"]
        @return: 返回列表
        """
        # csv_header = [
        #     'SignalName',
        #     'Tx_BusChannel',
        #     'Tx_ECUName',
        #     'Tx_MessageName',
        #     'Tx_MessageID',
        #     'Tx_MessageCyclic',
        #     'EnableUB', 'crc','counter',
        #     'Rx_BusChannel',
        #     'Rx_ECUName',
        #     'Rx_MessageName',
        #     'Rx_MessageID',
        #     'Rx_MessageCyclic',
        #     "Len",
        #     "repeat",
        # ]
        condition = ["cycle", "event", "ub", "crc", "counter"]

        select_cond_info = str(select_cond).strip().lower()
        if select_cond_info not in condition:
            assert 0, f"参数不对，select_cond 可以选的有{condition}"
        logger.info(f"过滤数据 select_cond={select_cond_info} ")
        new_dict = dict(zip(condition, [[], [], [], [], []]))
        with open(path, "r") as file:
            csv_data = csv.reader(file)
            csv_data_list = list(csv_data)
            header = csv_data_list[0]
            for row in csv_data_list[1:]:
                dic = dict(zip(header, row))
                # 重复的不执行
                if int(dic["repeat"]):
                    continue
                if dic["SignalName"].endswith("Chks") or dic["SignalName"].endswith(
                    "Cntr"
                ):
                    continue

                item_cycle = dic["Tx_MessageCyclic"]
                item_ub = dic["EnableUB"]
                item_crc = dic.get("crc")
                item_counter = dic.get("counter")
                # 根据周期分类
                if str(item_cycle).lower() == "EventTriggered".lower():
                    new_dict["event"].append(dic)
                else:
                    new_dict["cycle"].append(dic)
                # 根据ub 分类
                if str(item_ub).strip():
                    new_dict["ub"].append(dic)

                # 根据 crc 分类
                if str(item_crc).strip():
                    new_dict["crc"].append(dic)

                # 根据 conter 分类
                if str(item_counter).strip():
                    new_dict["counter"].append(dic)

        return new_dict.get(select_cond_info)
    def get_signal_routing_communication_excel_path(self, excel_path=None):
        """
        获取信号路由通信矩阵的 路径
        返回 True ，CSV文件路径，原表的路径，表示 csv文件存在，无需解析
        返回 Flase ，CSV文件路径，原表的路径，表示 csv文件不存在，需要根据原表解析

        @param excel_path: 存放excel 表的路径
        @return: 返回 BOOL，path，path （True/False，CSV文件路径，原表的路径）
        """

        if excel_path is None:
            excel_path = r"signal_routing_communication/"
        bgm_info_dict = self.ssh.bgm_ssh.get_version()
        version_release = bgm_info_dict.get("version_release", None)  # v1.3.0
        # 获取路径下所有文件
        ccp_string, ccp_list = self.sd_tester.read_ccp()
        # 根据 判断车型  （CCP#950==0x01代表Mars  CCP#950==0x02代表Venus)
        vehicle_model = ccp_list[949]  # Mars  还是 Venus
        # （CCP#962==0x02代表MCA 800v  CCP#962==0x00代表MCA 400v)
        vehicle_mca = ccp_list[962 - 1]  #

        csv_files = [f for f in os.listdir(excel_path)]
        csv_files.sort()
        csv_files.reverse()
        logger.info(f"获取的到存在信号路由版本文件夹有{csv_files}")
        if version_release is None:
            # 取最新的表  v1.3.0
            logger.error(f"当前 BGM 版本未知，默认获取最新的通信表，如有失败需要核对通信矩阵是否和bgm 版本一致")
            csv_file_name = csv_files[0]
            csv_file = os.path.join(excel_path, f"{csv_file_name}/{csv_file_name}.csv")
        else:
            if version_release < "v2.0.0":
                if version_release in csv_files:
                    csv_file_name = version_release
                    logger.info(f"当前 BGM 版本{version_release}，对应{csv_file_name}.csv文件存在")
                else:
                    # 如果不在 取大版本下最新的，如果都不在则取最新的
                    bgm_ver_list = version_release.split(".")[:-1]
                    bgm_ver = ".".join(bgm_ver_list)
                    for item in csv_files:
                        if item.startswith(bgm_ver):
                            csv_file_name = item
                            string=f"当前 BGM 版本{version_release}，对应{version_release}.csv文件不存在,采用临近版本{item}.csv"
                            logger.error(string)
                            break
                    else:
                        csv_file_name = [item for item in csv_files if item < "v2.0.0"][0]
                        string=f"当前 BGM 版本{version_release}，对应{version_release}.csv文件不存在,采用最新{csv_file_name}.csv"
                        logger.error(string)

                csv_file = os.path.join(excel_path, f"{csv_file_name}/{csv_file_name}.csv")
            else:
                if version_release not in csv_files:
                    # 如果不在 取大版本下最新的，如果都不在则取最新的
                    bgm_ver_list = version_release.split(".")[:-1]
                    bgm_ver = ".".join(bgm_ver_list)
                    for item in csv_files:
                        if item.startswith(bgm_ver):
                            csv_file_name = item
                            string = f"当前 BGM 版本{version_release}，对应{version_release}.csv文件不存在,采用临近版本{item}版本"
                            logger.error(string)
                            break
                    else:
                        csv_file_name = [item for item in csv_files if item >= "v2.0.0"][0]
                        string = f"当前 BGM 版本{version_release}，对应{version_release}文件不存在,采用最新{csv_file_name}版本"
                        logger.error(string)
                    #
                    version_release=csv_file_name

                if vehicle_model == 0x01 and vehicle_mca == 0x00:
                    csv_file_name = f"{version_release}_mars.csv"
                    string = f"当前车型是 Mars MCA 400v 采用{csv_file_name}"
                    logger.info(string)

                elif vehicle_model == 0x01 and vehicle_mca == 0x02:
                    csv_file_name = f"{version_release}_mars_mca.csv"
                    string = f"当前车型是 Mars MCA 800v 采用{csv_file_name}"
                    logger.info(string)

                elif vehicle_model == 0x02 and vehicle_mca == 0x00:
                    csv_file_name = f"{version_release}_venus.csv"
                    string = f"当前车型是 Venus MCA 400v 采用{csv_file_name}"
                    logger.info(string)

                elif vehicle_model == 0x02 and vehicle_mca == 0x02:
                    csv_file_name = f"{version_release}_venus_mca.csv"
                    string = f"当前车型是 Venus MCA 800v 采用{csv_file_name}"
                    logger.info(string)
                else:
                    csv_file_name=""
                    string = f"当前车型不存在={vehicle_model}或者vehicle_mca={vehicle_mca}不存在"
                    logger.error(string)
                    assert 0, string

                csv_file = os.path.join(excel_path, f"{version_release}/{csv_file_name}")

        # 判断通信矩阵是否存在
        excel_file = None
        # 判断是否存在解析的csv文件

        if os.path.exists(csv_file):
            logger.info(f"对应{version_release}版本的通信矩阵{csv_file}》》存在,无需再解析")
            return True, csv_file, excel_file
        else:
            error_data = f"对应{version_release}版本的通信矩阵{csv_file}》》不存在"
            logger.error(error_data)
            assert 0, error_data
            
    def send_signal_route_and_check_result(self, item, set_ub_flag=True,check_time=5):
        """
        发送 信号，并校验接收信号，发送的信号有，最大值，最小值，以及中间的一个随机值
        带ub 位的 设置ub位为 True 可以路由
        带ub 位的 设置ub位为 False，不可以路由

        @param item:
        @param set_ub_flag: 设置ub位
        @return:
        """

        signal_name = item["SignalName"]
        # 发送通道
        send_bus = item["Tx_BusChannel"].lower()
        # 发送帧 名字
        send_msg_name = item["Tx_MessageName"]
        # 接收通道
        recv_bus = item["Rx_BusChannel"].lower()
        # 接收帧名字
        recv_msg_name = item["Rx_MessageName"]
        # 发送周期  EventTriggered
        send_cycle = str(item["Tx_MessageCyclic"]).strip().lower()
        signal_len = int(float(item["Len"]))
        # send_obj = eval(f"self.ipdu.{send_bus}.{send_msg_name}")
        # recv_obj = eval(f"self.ipdu.{recv_bus}.{recv_msg_name}")
        max_value = int("1" * signal_len, 2)
        # EnableUB = True if item["EnableUB"] else False

        if send_cycle == "EventTriggered".lower():
            # 事件型
            send_cycle = None
        elif "[" in send_cycle:
            # lin 类型的数据
            send_cycle = eval(send_cycle)
        else:
            send_cycle = int(send_cycle)
        # 接收周期
        recv_cycle = str(item["Rx_MessageCyclic"]).strip().lower()
        if recv_cycle == "EventTriggered".lower():
            # 事件型
            recv_cycle = None
        elif "[" in recv_cycle:
            # lin 类型的数据
            recv_cycle = eval(recv_cycle)
        else:
            recv_cycle = int(recv_cycle)
        
        if isinstance(recv_cycle, int):
            recv_cycle_time = recv_cycle/1000
        else:
            recv_cycle_time = 1 
        
        # 如果是1 则测试0和1
        if max_value == 1:
            send_value_list = [max_value, 0]
        else:
            # 如果最大值大于1  则测试最大值和最小值，以及中间的一个随机值
            send_value_list = [max_value, random.randint(1, max_value - 1), 0]
        if not set_ub_flag:
            for index_ in range(3):
                actual_value = None
                result, actual_value, expected_value = self.bus_comm.check(
                    bus_name=recv_bus,
                    msg_name=recv_msg_name,
                    signal_name=signal_name,
                    sig_value_name=send_value_list[-1],
                    do_assert=False,
                )
                logger.info(f"第{index_}次 {signal_name}的 当前值为{actual_value}")
                if actual_value is not None:
                    break
            if actual_value in send_value_list:
                send_value_list.remove(actual_value)

        start_string_log = f"{signal_name}发送值为：{send_value_list}，发送通道{send_bus} 发送周期{send_cycle}，接收通道{recv_bus}接收周期{recv_cycle}"
        logger.info(start_string_log)
        err_flag = False
        log_lis = []
        
        
        for send_value in send_value_list:
            self.bus_comm.clear_all_bus_buffer()
            logger.info(f"发送生成的随机值{send_value},{float(send_value)}")
            
            send_bus_obj = getattr(self.bus_comm.ipdu, send_bus)
            send_msg_obj = getattr(send_bus_obj, send_msg_name)
            send_msg_signals_obj = getattr(send_msg_obj, signal_name)
            send_sig_value_factor = getattr(send_msg_signals_obj, "sig_value_factor")
            send_sig_value_offset = getattr(send_msg_signals_obj, "sig_value_offset")
            logger.info(f"send_sig_value_factor={send_sig_value_factor} send_sig_value_offset={send_sig_value_offset}")
            # logger.info(f"send_sig_value_offset={send_sig_value_offset}")
            
            if send_sig_value_factor is None and send_sig_value_offset is None:
                     send_value_1= send_value       
            elif send_sig_value_factor is None and send_sig_value_offset is not None:
                send_value_1 = send_value * 1.0 + send_sig_value_offset
            elif send_sig_value_factor is not None and send_sig_value_offset is None:
                send_value_1 = float(send_value * send_sig_value_factor)
            else:
                send_value_1 = float(send_value * send_sig_value_factor + send_sig_value_offset)
            
            if send_cycle is None:
                self.bus_comm.set(
                    bus_name=send_bus,
                    msg_name=send_msg_name,
                    signal_name=signal_name,
                    sig_value_name=send_value_1,
                    ub_flag=set_ub_flag,
                    cycle_time=0,
                )
            else:
                self.bus_comm.set(
                    bus_name=send_bus,
                    msg_name=send_msg_name,
                    signal_name=signal_name,
                    sig_value_name=send_value_1,
                    ub_flag=set_ub_flag,
                )
            # 获取 信号系数
            rec_bus_obj = getattr(self.bus_comm.ipdu, recv_bus)
            msg_obj = getattr(rec_bus_obj, recv_msg_name)
            msg_signals_obj = getattr(msg_obj, signal_name)
            sig_value_factor = getattr(msg_signals_obj, "sig_value_factor")
            sig_value_offset = getattr(msg_signals_obj, "sig_value_offset")
            logger.info(f"recv_sig_value_factor= {sig_value_factor}  recv_sig_value_offset= {sig_value_offset}")
            # logger.info(f"recv_sig_value_offset={sig_value_offset}")
            
            if sig_value_factor is None and sig_value_offset is None:
                     check_value= send_value       
            elif sig_value_factor is None and sig_value_offset is not None:
                check_value = send_value * 1.0 + sig_value_offset
            elif sig_value_factor is not None and sig_value_offset is None:
                check_value = float(send_value * sig_value_factor)
            else:
                check_value = float(send_value * sig_value_factor + sig_value_offset)
            logger.info(f"check_value={check_value}")    

            result, actual_value, expected_value = self.bus_comm.check(
                bus_name=recv_bus,
                msg_name=recv_msg_name,
                signal_name=signal_name,
                sig_value_name=check_value,
                do_assert=False,
                # timeout=recv_cycle_time * 4 ,# check_time
                timeout=check_time,  # check_time
            )
            # logger.info(f"+++++++++++{result}actual_value={actual_value}expected_value={expected_value}")
            if set_ub_flag:
                if not result:
                    err_flag = True
                    string_log = f"ERROR>>>当前路由信号{signal_name} ub位为{set_ub_flag} 发送为{send_value}时候，获取的是{actual_value},{send_bus}通道{send_msg_name}发送给{recv_bus}通道{recv_msg_name}失败"
                    logger.error(string_log)
                    log_lis.append(string_log)
                else:
                    string_log = f"当前路由信号{signal_name} ub位为{set_ub_flag}发送为{send_value}时候，获取的是{actual_value},{send_bus}通道{send_msg_name}发送给{recv_bus}通道{recv_msg_name}成功"
                    logger.info(string_log)
            else:
                if result:
                    err_flag = True
                    string_log = f"ERROR>>>当前路由信号{signal_name} ub位为{set_ub_flag} 发送为{send_value}时候，获取的是{actual_value},{send_bus}通道{send_msg_name}发送给{recv_bus}通道{recv_msg_name}不应成功，实际路由成功"
                    logger.error(string_log)
                    log_lis.append(string_log)
                else:
                    string_log = f"当前路由信号{signal_name} ub位为{set_ub_flag} 发送为{send_value}时候，获取的是{actual_value},{send_bus}通道{send_msg_name}发送给{recv_bus}通道{recv_msg_name}失败"
                    logger.info(string_log)

        if err_flag:
            start_string_log = "**** ERROR ******" + start_string_log
        else:
            start_string_log = "##### SUCCESS ##### " + start_string_log
        with allure.step(start_string_log):
            for log in log_lis:
                with allure.step(log):
                    pass

        return not err_flag, signal_name

    def check_signal_route_items(self, excel_path=None, select_cond="cycle",check_time=2):
        """
         遍历 data_list 里面的路由信号，发送的信号有，最大值，最小值，以及中间的一个随机值

        @param csv_file_path:  csv 路径
        @param select_cond: 根据条件筛选 ["cycle", "event", "ub"]

        @return:
        """
        if excel_path is None:
            excel_path = r"signal_routing_communication/"
        (
            ret,
            csv_file_path,
            excel_file,
        ) = self.get_signal_routing_communication_excel_path(excel_path)
        if not ret:
            self.parse_excel_to_signal_routing_csv(excel_file, csv_file_path)

        select_cond_info = str(select_cond).strip().lower()
        data_list = self.read_signal_routing_info(
            path=csv_file_path, select_cond=select_cond_info
        )
        # data_list = data_list[:3]

        if not isinstance(data_list, list):
            assert 0, "data_list 的参数格式不对，应该为列表"

        info_string = f"总共{len(data_list)}条路由信号"
        with allure.step(info_string):
            logger.info(info_string)

        assert len(data_list), "未过滤到符合条件的数据"
        # 存放路由失败的信号
        err_route_list = []
        for index, item in enumerate(data_list):
            logger.info(f"共{len(data_list)}条，第{index}条路由信息为{item}")
            if not (select_cond_info == "ub"):
                logger.info("正向测试都可以 可以路由")
                # 可以路由
                ret1, signal_name = self.send_signal_route_and_check_result(
                    item, set_ub_flag=True,check_time=check_time
                )
                if not ret1:
                    err_route_list.append(signal_name)

            # todo 不可以路由
            # 带ub 位的 设置ub位为 False，不可以路由
            if select_cond_info == "ub":
                logger.info("带ub 位的 设置ub位为 False，不可以路由")
                ret2, signal_name = self.send_signal_route_and_check_result(
                    item, set_ub_flag=False,check_time=check_time
                )
                if not ret2:
                    err_route_list.append(signal_name)

        err_log = f"路由成功的信号{len(data_list) - len(err_route_list)}个"
        with allure.step(err_log):
            logger.info(err_log)

        err_log = f"存在路由失败的信号{len(err_route_list)}个>>{err_route_list}"
        with allure.step(err_log):
            logger.info(err_log)

        assert not len(err_route_list), err_log

    def ctrl_lock(self, lock_type: LockCmd, ctrl_type: LockSource):
        with allure.step(f"通过{ctrl_type.name}方式控制{lock_type.name}"):
            logger.info(f"通过{ctrl_type.name}方式控制{lock_type.name}")
            self.io.set_bgm_hardware_condition_to_default()
            if ctrl_type.name == "RKE":
                if lock_type.name == "UnLock":
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 0, "source": 0},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem
                    )

                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem
                    )

            elif ctrl_type.name == "Telm":
                if lock_type.name == "UnLock":
                    logger.info("发送远控解锁锁请求")
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 0, "source": 1},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm
                    )

                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3:
                        logger.warning(f"中控锁状态已经是Lock状态,落锁之前先解锁")
                    else:
                        logger.info("发送远控上锁请求")
                        self.soa.send_method_request(
                            "CentralLockService_client",
                            "SetDoorCloseLock",
                            {"cmd": 1, "source": 1},
                        )
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm
                        )

            elif ctrl_type.name == "HMI":
                if lock_type.name == "UnLock":
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 0, "source": 2},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt
                    )

                elif lock_type.name == "Lock":
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 1, "source": 2},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt
                    )

            elif ctrl_type.name == "KV_PEPS":
                self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
                self.sd_tester.write_ccp(ccp={94:0x2})
                if lock_type.name == "UnLock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3:
                        self.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5)
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Unlock,
                            exp_trigsrc=LockTrigerSource.Keyls,
                        )
                    else:
                        logger.warning(f"中控锁状态已经是UnLock状态,无需解锁")

                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1:
                        self.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=3)
                        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")

            elif ctrl_type.name == "NFC":
                logger.warning(f"发送NFC请求")
                self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Pause)
                if lock_type.name == "UnLock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Unlock,
                            exp_trigsrc=LockTrigerSource.NFC,
                        )
                    else:
                        logger.warning(f"中控锁状态已经是UnLock状态,无需解锁")
                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
                elif lock_type.name == "LockCompleteArm":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
            elif ctrl_type.name == "Apprch":
                if lock_type.name == "UnLock":
                    logger.warning(f"发送近车解锁")
                    self.sd_tester.write_ccp(ccp={94:0x80})
                    self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
                    sleep(.5)  # 等设置项生效
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3 or cen_lock_sts == 2:
                        self.bus_comm.dk.send_approach_unlock_cmd()
                    else:
                        logger.warning(f"中控锁状态已经是UnLock状态,无需解锁")
                elif lock_type.name == "Lock":
                    logger.warning(f"发送离车落锁")
                    self.sd_tester.write_ccp(ccp={94:0x80})
                    self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)
                    sleep(.5)
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1 or cen_lock_sts == 2:
                        self.bus_comm.dk.send_walk_away_lock_cmd()
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
                        
            elif ctrl_type.name == "OutsOth":
                if lock_type.name == "UnLock":
                    logger.warning(f"外部方式OutsOth不支持解锁操作")
                elif lock_type.name == "Lock":
                    logger.warning(f"设置整车外部其它方式闭锁")
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 3, "source": 3},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth
                    )
                else:
                    logger.warning(f"中控锁状态已经是Lock状态,无需上锁")

            elif ctrl_type.name == "SpdAut":
                if lock_type.name == "UnLock":
                    logger.warning(f"车速解锁不支持")
                    
                elif lock_type.name == "Lock":
                    logger.warning(f"设置车速自动落锁")
                    self.bus_comm.set_brake_pedal(qf=ValueQf.AccurData,sts= YesOrNo.Yes)
                    self.bus_comm.set_vehspd(value=1.95)
                    self.io.driver_seat_present()
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut
                    )
                else:
                    logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
                    
            elif ctrl_type.name == "InsOth":
                if lock_type.name == "UnLock":
                    logger.warning(f"执行内部其它方式解锁")
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 0, "source": 3},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth
                    )

                elif lock_type.name == "Lock":
                    logger.warning(f"执行内部其它方式闭锁")
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 1, "source": 3},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth
                    )
                    
            elif ctrl_type.name == "TmrAut":
                if lock_type.name == "UnLock":
                    logger.warning(f"自动重锁不支持解锁")
                    
                elif lock_type.name == "Lock":
                    logger.warning(f"执行自动重上锁")
                    self.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
                    self.io.set_hood_sts(sts=HoodSts.Close)
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 1, "source": 1},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm
                    )
                    sleep(.5)
                    self.soa.send_method_request(
                        "CentralLockService_client",
                        "SetDoorCloseLock",
                        {"cmd": 0, "source": 1},
                    )
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm
                    )
                    self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
                    sleep(30)
                    self.bus_comm.check_central_lock_sts(
                        exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut
                    )
                else:
                    logger.warning(f"中控锁状态已经是Lock状态,无需上锁")

    def read_diag_route_excel(self, excel_path, sheet_name=None):
        """
        读取诊断路由的 excle表,
        如果传递 sheet_name 为None 则 读取所有的 sheet 表，返回一个字典,
        字典key 为sheet 名字value 为该sheet的 信息
        字典{
         sheet_name1 :[{}，{}],
         sheet_name1 :[{}，{}],
        }
        如果传递 sheet_name 为 具体的sheet 页，则返回一个列表，[{},{}]
        @param self:
        @param excel_path: 原表路径
        @param sheet_name: 读取的 sheet 名字 或者为None
        @return:
        """

        def change_hex_str2int(string):
            """
            16进制字符传转化为 整数
            @param string:
            @return:
            """
            if not isinstance(string, str):
                assert 0, f"string 格式不对应为str 格式，实际为{type(string)}"
            # 防止读取 表中的数据 带有小数点  '610.0'
            if "." in string:
                int_value = int(string.split(".")[0], 16)
            else:
                int_value = int(string, 16)

            return int_value

        def change_str2int(string):
            """
            字符传转整数
            @param string:
            @return:
            """
            if not isinstance(string, str):
                assert 0, f"string 格式不对应为str 格式，实际为{type(string)}"
            int_value = int(float(string))
            return int_value

        bgm_info_dict = self.ssh.bgm_ssh.get_version()
        version_release = bgm_info_dict.get("version_release", None)
        # 获取路径下所有文件
        files = [f[:-5] for f in os.listdir(excel_path) if f.endswith("xlsx")]
        files.sort()
        files.reverse()
        logger.info(f"获取的到 文件夹{files}")
        if version_release is None:
            # 取最新的表
            logger.info(f"当前 BGM 版本未知，默认获取最新的通信表，如有失败需要核对通信矩阵是否和bgm 版本一致")
            csv_file_name = files[-1]
        else:
            if version_release in files:
                csv_file_name = version_release
                logger.info(f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件存在")
            else:
                # 如果不在 取大版本下最新的，如果都不在则取最新的
                bgm_ver_list = version_release.split(".")[:-1]
                bgm_ver = ".".join(bgm_ver_list)
                for item in files:
                    if item.startswith(bgm_ver):
                        csv_file_name = item
                        logger.error(
                            f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件不存在,采用临{item}.xlsx"
                        )
                        break
                else:
                    csv_file_name = files[0]
                    logger.error(
                        f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件不存在,采用最新{csv_file_name}.xlsx"
                    )
        # 判断通信矩阵是否存在
        excel_file = os.path.join(excel_path, f"{csv_file_name}.xlsx")
        if not os.path.exists(excel_file):
            new_file = files[0]
            string_log = f"对应{version_release}版本的诊断路由表{excel_file}》》不存在，则使用最新{new_file}"
            logger.error(string_log)
            # 不存在则用默认用最新的
            excel_file = os.path.join(excel_path, f"{new_file}.xlsx")
            # assert 0, string_log

        # 读取excel文件
        t1 = time.time()
        workbook = xlrd.open_workbook(excel_file)
        # logger.info(f"读取诊断路由表耗时{time.time() - t1}")
        sheet_name_list = [item.name for item in workbook.sheets()]
        print(sheet_name_list)
        if sheet_name is None:
            sheet_name_list = sheet_name_list
        else:
            if sheet_name not in sheet_name_list:
                assert 0, f"{sheet_name}不存在，可选范围{sheet_name_list}"
            sheet_name_list = [sheet_name]

        sheet_dic = {}
        for sheetname in sheet_name_list:
            table = workbook.sheet_by_name(sheetname)
            header_list = [
                item.strip().replace(" ", "").lower() for item in table.row_values(0)
            ]

            data_info_list = []
            # 便利该表，使用nrows，和ncols代表当前表的有效行列数。
            for row in range(1, table.nrows):
                row_data = [str(item) for item in table.row_values(row)]
                data_info = dict(zip(header_list, row_data))
                if sheet_name in ["doip2docan", "doip2dolin"]:
                    # 十六进制转换
                    data_info["send_address"] = change_hex_str2int(
                        data_info.get("send_address")
                    )
                    data_info["recv_address"] = change_hex_str2int(
                        data_info.get("recv_address")
                    )
                    data_info["request_id"] = change_hex_str2int(
                        data_info.get("request_id")
                    )
                    data_info["response_id"] = change_hex_str2int(
                        data_info.get("response_id")
                    )
                    data_info["padding"] = change_hex_str2int(data_info.get("padding"))
                    # 十进制字符串转换
                    data_info["bs"] = change_str2int(data_info.get("bs"))
                    data_info["st"] = change_str2int(data_info.get("st"))
                    data_info["length"] = change_str2int(data_info.get("length"))
                elif sheet_name == "doip2dofr":
                    # 十六进制转换
                    data_info["send_address"] = change_hex_str2int(
                        data_info.get("send_address")
                    )
                    data_info["recv_address"] = change_hex_str2int(
                        data_info.get("recv_address")
                    )
                    request_id_str = data_info.get("request_id", '').replace('，', ',').strip()
                    if request_id_str:
                        request_id = [int(float(i)) for i in request_id_str.split(',')]
                        data_info["request_id"] = request_id

                    response_id_str = data_info.get("response_id", '').replace('，', ',').strip()
                    if response_id_str:
                        response_id = [int(float(i)) for i in response_id_str.split(',')]
                        data_info["response_id"]=response_id

                    # data_info["padding"] = change_hex_str2int(data_info.get("padding"))
                    # # 十进制字符串转换
                    # data_info["bs"] = change_str2int(data_info.get("bs"))
                    # data_info["st"] = change_str2int(data_info.get("st"))
                    # data_info["length"] = change_str2int(data_info.get("length"))
                elif sheet_name == "docan2docan":
                    # 十六进制转换
                    # data_info["send_address"] = change_hex_str2int(
                    #     data_info.get("send_address")
                    # )
                    # data_info["recv_address"] = change_hex_str2int(
                    #     data_info.get("recv_address")
                    # )
                    data_info["request_id"] = change_hex_str2int(
                        data_info.get("request_id")
                    )
                    data_info["response_id"] = change_hex_str2int(
                        data_info.get("response_id")
                    )
                    data_info["padding"] = change_hex_str2int(data_info.get("padding"))
                    # 十进制字符串转换
                    data_info["bs"] = change_str2int(data_info.get("bs"))
                    data_info["st"] = change_str2int(data_info.get("st"))
                    data_info["length"] = change_str2int(data_info.get("length"))
                    pass
                elif sheet_name == "docan_func":
                    # 十六进制转换
                    # data_info["send_address"] = change_hex_str2int(
                    #     data_info.get("send_address")
                    # )
                    # data_info["recv_address"] = change_hex_str2int(
                    #     data_info.get("recv_address")
                    # )
                    data_info["request_id"] = change_hex_str2int(
                        data_info.get("request_id")
                    )
                    # data_info["response_id"] = change_hex_str2int(data_info.get("response_id"))
                    data_info["padding"] = change_hex_str2int(data_info.get("padding"))
                    # 十进制字符串转换
                    # data_info["bs"] = self.change_str2int(data_info.get("bs"))
                    # data_info["st"] = self.change_str2int(data_info.get("st"))
                    data_info["length"] = change_str2int(data_info.get("length"))
                    # 处理can 接收通道
                    can_recv_channel = (
                        data_info.get("can_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["can_recv_channel"] = [
                        item.strip() for item in can_recv_channel if item.strip()
                    ]
                    # 处理 lin 接收通道
                    lin_recv_channel = (
                        data_info.get("lin_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["lin_recv_channel"] = [
                        item.strip() for item in lin_recv_channel if item.strip()
                    ]
                    # 处理 fr 接收通道
                    fr_recv_channel = (
                        data_info.get("fr_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["fr_recv_channel"] = [
                        item.strip() for item in fr_recv_channel if item.strip()
                    ]
                elif sheet_name == "doip_func":
                    # 十六进制转换
                    data_info["send_address"] = change_hex_str2int(
                        data_info.get("send_address")
                    )
                    data_info["recv_address"] = change_hex_str2int(
                        data_info.get("recv_address")
                    )
                    data_info["request_id"] = change_hex_str2int(
                        data_info.get("request_id")
                    )
                    # data_info["response_id"] = change_hex_str2int(data_info.get("response_id"))
                    data_info["padding"] = change_hex_str2int(data_info.get("padding"))
                    # 十进制字符串转换
                    # data_info["bs"] = self.change_str2int(data_info.get("bs"))
                    # data_info["st"] = self.change_str2int(data_info.get("st"))
                    data_info["length"] = change_str2int(data_info.get("length"))
                    # 处理can 接收通道
                    can_recv_channel = (
                        data_info.get("can_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["can_recv_channel"] = [
                        item.strip() for item in can_recv_channel if item.strip()
                    ]
                    # 处理 lin 接收通道
                    lin_recv_channel = (
                        data_info.get("lin_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["lin_recv_channel"] = [
                        item.strip() for item in lin_recv_channel if item.strip()
                    ]
                    # 处理 fr 接收通道
                    fr_recv_channel = (
                        data_info.get("fr_recv_channel", "")
                        .replace("，", ",")
                        .split(",")
                    )
                    data_info["fr_recv_channel"] = [
                        item.strip() for item in fr_recv_channel if item.strip()
                    ]
                else:
                    pass

                data_info_list.append(data_info)
            sheet_dic[sheet_name] = data_info_list

        return sheet_dic if sheet_name is None else sheet_dic.get(sheet_name, [])

    def log_and_allure_step(self, log_string: str, level=LogLevel.INFO):
        """
        打印日志，并写allure 步骤
        @param log_string:
        @param level:
        @return:
        """
        with allure.step(log_string):
            if level == LogLevel.INFO:
                logger.info(log_string)
            elif level == LogLevel.DEBUG:
                logger.debug(log_string)
            elif level == LogLevel.WARNING:
                logger.warning(log_string)
            elif level == LogLevel.ERROR:
                logger.error(log_string)
            elif level == LogLevel.CRITICAL:
                logger.critical(log_string)
            else:
                logger.info(log_string)
    
    def diag_route_eth2can(self, data_info_list, send_length):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """

        # self.sd_test = Sd_Tester(**self.sd_test_tb_config)
        # self.sd_test.diagnostic_client_sim_start()
        # self.sd_test.tester_present()
        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_address = item_info.get("recv_address")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")
            # 过滤数据
            # if send_channel != "obd":
            #     continue
            # if recv_address != 0x1510:
            #     continue
            # if recv_channel != "connectivitycanfd":
            #     continue
            
            self.bus_comm.filter_msg(recv_channel, request_id)
            self.bus_comm.filter_msg(recv_channel, response_id)

            # 更新逻辑地址，必须
            self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                # 清空 通道缓存
                # self.bus_comm.clear_all_bus_buffer()
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                # 生成随机数据
                # send_data = [random.randint(0, 255) for i in range(send_length)]
                send_data = [random.randint(0xA0, 255)]+[random.randint(0, 255) for i in range(send_length-1)]
                # 发送请求
                string = f"{send_channel}发送数据长度{send_length}"
                logger.info(string)
                send_eth_time = time.time()
                self.sd_tester.send_data(send_data)
                try:
                    # 接受请求
                    string = f"{recv_channel}接收数据"
                    logger.info(string)
                    (
                        recv_msg_data,
                        recv_padding,
                        time_stamp,
                    ) = self.bus_comm.recv_diag_request_msg(
                        recv_channel,
                        request_id=request_id,
                        response_id=response_id,
                        bs=bs,
                        st=st,
                        single_frame_len=length,
                    )
                    if len(recv_padding) > 1 or (
                            recv_padding and recv_padding[0] != padding
                    ):
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败,填充位不对，本应为{padding}实际为{recv_padding}时间差{time_stamp - send_eth_time} 秒"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    elif len(send_data) != len(recv_msg_data):
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败 发送数据长度{len(send_data)}，can接收数据的长度{len(recv_msg_data)}时间差{time_stamp - send_eth_time} 秒"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    elif recv_msg_data != send_data:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败，接收的内容和发送的内容不一样，发送数据{send_data}，can接收数据的{recv_msg_data}时间差{time_stamp - send_eth_time} 秒"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    else:
                        string = f"第{index + 1}条》》》路由长度为{send_length}成功 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由成功,时间差{time_stamp - send_eth_time} 秒"
                        self.log_and_allure_step(string, LogLevel.INFO)
                    # 校验一下其他通道没有收到
                    # recv_no_flag, recv_ch_lis = self.recv_no_request(recv_channel, request_id)
                    # if not recv_no_flag:
                    #     err_item_list.append(hex(recv_address))
                    #     string = f"第{index + 1}条*****路由长度为{send_length}失败，除{recv_channel}通道，其他通道也收到{recv_ch_lis}报文"
                    #     self.log_and_allure_step(string, LogLevel.ERROR)
                    #     continue

                    # todo 发送响应
                    # send_response_msg = [
                    #     random.randint(0, 255) for i in range(send_length)
                    # ]
                    send_response_msg = [random.randint(0xA0, 255)]+[random.randint(0, 255) for i in range(send_length-1)]
                    string = f"{recv_channel}发送响应数据长度{send_length}"
                    logger.info(string)
                    send_can_time = self.bus_comm.send_diag_request_msg(
                        recv_channel,
                        request_id=response_id,
                        response_id=request_id,
                        send_msg=send_response_msg,
                        padding=padding,
                        single_frame_len=length,
                    )
                    # 以太接收响应
                    string = f"{send_channel}接收响应数据"
                    logger.info(string)
                    recv_eth_msg = (
                        self.sd_tester.return_udsdata_and_check_and_print_response_result()
                    )

                    if len(send_response_msg) != len(recv_eth_msg):
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {recv_channel}逻辑地址为{hex(recv_address)}响应{send_channel}请求路由失败 发送数据长度{len(send_response_msg)}，接收数据的长度{len(recv_eth_msg)}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    elif send_response_msg != recv_eth_msg:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {recv_channel}逻辑地址为{hex(recv_address)}响应{send_channel}请求路由失败，接收的内容和发送的内容不一样，发送数据{send_response_msg}，接收数据的{recv_eth_msg}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    else:
                        string = f"第{index + 1}条》》》路由长度为{send_length}成功 {recv_channel}逻辑地址为{hex(recv_address)}响应{send_channel}请求路由成功"
                        self.log_and_allure_step(string, LogLevel.INFO)

                    # 校验一下其他通道没有收到
                    # recv_no_flag, recv_ch_lis = self.recv_no_request(recv_channel, response_id)
                    # if not recv_no_flag:
                    #     err_item_list.append(hex(recv_address))
                    #     string = f"第{index + 1}条*****路由长度为{send_length}失败，除{recv_channel}通道，其他通道也收到{recv_ch_lis}报文"
                    #     self.log_and_allure_step(string, LogLevel.ERROR)

                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    # request_id_hex = hex(request_id)[2:].zfill(3).upper()
                    # response_id_hex = hex(response_id)[2:].zfill(3).upper()
                    # trace_path = os.path.join(str(__file__).split('sat')[0], 'sat/xat_cases/legacy/bgm/Can.asc')
                    # command = f" cat {trace_path}  | grep -E ' {request_id_hex} | {response_id_hex} '"
                    # try:
                    #     # 执行命令
                    #     logger.info(f"开始执行cmd={command}")
                    #     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #     # 等待命令执行完成
                    #     process.wait(60)
                    #     # 获取命令的输出和错误信息
                    #     output = process.stdout.read()
                    #     error = process.stderr.read()
                    #     # 将输出和错误信息解码为字符串
                    #     output = output.decode(encoding="utf-8")
                    #     error = error.decode(encoding="utf-8")
                    # except Exception as e1:
                    #     output = ""
                    #     error = str(e1)
                    # logger.info(f"执行cmd={command} 结束")
                    # # 返回命令的输出和错误信息
                    # result = output.split('\r\n')
                    # asc_data=""
                    # for item in result:
                    #     if item.strip():
                    #         asc_data=item
                    #         logger.info(f"asc>>{item}")

                    err_item_list.append(hex(recv_address))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}逻辑地址为{hex(recv_address)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

            # if err_item_list:
            #     if err_item_list[-1] == hex(recv_address):
                    # request_id_hex=hex(request_id)[2:].zfill(3).upper()
                    # response_id_hex = hex(response_id)[2:].zfill(3).upper()
                    # trace_path= os.path.join(str(__file__).split('sat')[0],'sat/xat_cases/legacy/bgm/Can.asc')
                    # command = f" cat {trace_path}  | grep -E ' {request_id_hex} | {response_id_hex} '"
                    # os.system(command)
                    # try:
                    #     # 执行命令
                    #     logger.info(f"开始执行cmd={command}")
                    #     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #     # 等待命令执行完成
                    #     process.wait(60)
                    #     # 获取命令的输出和错误信息
                    #     output = process.stdout.read()
                    #     error = process.stderr.read()
                    #     # 将输出和错误信息解码为字符串
                    #     output = output.decode(encoding="utf-8")
                    #     error = error.decode(encoding="utf-8")
                    # except Exception as e:
                    #     output = ""
                    #     error = str(e)
                    # logger.info(f"执行cmd={command} 结束")
                    # # 返回命令的输出和错误信息
                    # result=output.split('\r\n')
                    # for item in result:
                    #     logger.info(f"asc>>{item}")


        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string
             
    def set_and_check_low_beam(self, sts: isOn):
        promt_info = f"----------------> 设置并且检测近光灯状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if sts.name == "On":
                self.soa.get_and_set_extilight_mode(
                    target_mode=ExteriorLightMode.LowHeam
                )
                self.bus_comm.check_low_beam_act_sts(
                    actn_sts=isOn.On, extr_light_sts=ExtrLtgSts.On
                )
            elif sts.name == "Off":
                self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
                self.bus_comm.check_low_beam_act_sts(
                    actn_sts=isOn.Off, extr_light_sts=ExtrLtgSts.Off
                )

    def set_lb_off_and_night_mode_sped0(self):  # 近光关夜晚车速零
        self.bus_comm.set_night_mode()
        self.bus_comm.set_vehspd_gear(vehspd=0)
        self.set_and_check_low_beam(sts=isOn.Off)
        sleep(0.5)

    def set_intr_light_auto_and_in_night_mode(self):
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_intr_light_mode()

    def init_boot_per(self):
        try:
            logger.info(
                "初始化进boot环境：车速设置为0 usagemod设置为abandoned carmode设置normal EpbStsEpbSts设置EpbSts_AllAppld 关闭防火墙"
            )
            with allure.step("关闭防火墙"):
                self.sd_tester.close_fireware()
            with allure.step("开始设置EpbStsEpbSts为EpbSts_AllAppld"):
                self.bus_comm.set(
                    "backbonefr",
                    "BcmVddmBackBoneFr00",
                    "EpbStsEpbSts",
                    "EpbSts_AllAppld",
                )
            with allure.step("开始设置车速为0"):
                self.bus_comm.set_vehspd(0)
            with allure.step("开始设置usagemod设置为abandoned carmode设置normal"):
                self.sd_tester.update_serverdoipid(0x1002)
                payload = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF186)
                if payload[-1:] == 2:
                    logger.info("在boot下 无法切换usagemode以及carmode")
                else:
                    logger.info("不在boot下 开始切换usagemode以及carmode")
                    self.bus_comm.set(
                        "backbonefr",
                        "BcmVddmBackBoneFr00",
                        "VehMtnStVehMtnSt",
                        "VehMtnSt2_StandStillVal3",
                    )
                    self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
                    self.sd_tester.change_car_mode(CarMode.NORMAL)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.info(f"初始化环境失败：ERROR：{e}")

    def delete_vehicleInfo_json(self):
        try:
            with allure.step("删除密钥后重启并等待10s"):
                commands = (
                    "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
                )
                with allure.step("删除密钥"):
                    self.ssh.type_commands(DeviceName.BGM, commands)
                with allure.step("重启BGM并等待10s"):
                    self.sd_tester.reset_0x1181()
                    time.sleep(10)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            assert False, f"删除密钥失败,ERROR:{e}"

    def set_low_volt_servse_mode(
        self,
        sys_falt: Union[bool, None] = None,
        low_volt: Union[bool, None] = None,
        serv: Union[bool, None] = None,
        ipm:Union[bool, None] = None,
        time_wait: Union[float, int] = 0,
    ):
        if sys_falt is not None:
            logger.info(f"----------------> 系统故障补电")
            self.bus_comm.set(
                "cem_lin6", "BmsCem_Lin6Fr03", "BattSnsrHwFltRaw", sys_falt
            )
        if low_volt is not None:
            logger.info(f"----------------> 低压补电")
            self.bus_comm.set_low_volt_power_supply()
        if serv is not None:
            logger.info(f"----------------> 服务补电")
            self.soa.send_method_request(
                "HighVoltageService_client", "SetOutput", {"on": serv}
            )
        if ipm is not None:
            logger.info(f"----------------> IPM补电")
            self.bus_comm.set_intelligent_charge_wakeup_sts(IPMLoUWakeUpReq.Chrgn)
        logger.info(f"--------------->等待{time_wait}秒")
        sleep(time_wait)

    
    def set_seats_present_sts(self,
                              drv_seat: Union[SeatPresSts, None] = None,
                              pass_seat: Union[SeatPresSts, None] = None,
                              sec_left: Union[SeatPresSts, None] = None,
                              sec_mid: Union[SeatPresSts, None] = None,
                              sec_right: Union[SeatPresSts, None] = None):
        if drv_seat is not None:
            logger.info(f'设置驾驶位座椅占位为{drv_seat.name}')
            if drv_seat.name == "NoPres":
                self.io.driver_seat_notpresent()
            else:
                self.io.driver_seat_present()
        if pass_seat is not None:
            logger.info(f'设置副驾驶位座椅占位为{pass_seat.name}')
            if pass_seat.name == "NoPres":
                self.bus_comm.set_pass_seat_notpresent()
            else:
                self.bus_comm.set_pass_seat_present()
        if sec_left is not None:
            logger.info(f'设置左后座椅占位为{sec_left.name}')
            if sec_left.name == "NoPres":
                self.bus_comm.set_secle_seat_notpresent()
            else:
                self.bus_comm.set_secle_seat_present()
        if sec_mid is not None:
            logger.info(f'设置后中座椅占位为{sec_mid.name}')
            if sec_mid.name == "NoPres":
                self.bus_comm.set_secmid_seat_notpresent()
            else:
                self.bus_comm.set_secmid_seat_present()
        if sec_right is not None:
            logger.info(f'设置右后座椅占位为{sec_right.name}')
            if sec_right.name == "NoPres":
                self.bus_comm.set_secri_seat_notpresent()
            else:
                self.bus_comm.set_secri_seat_present()

    def set_all_seats_present_sts(self, seat_pres_sts: SeatPresSts):
        logger.info(f'设置所有位座椅占位为{seat_pres_sts.name}')
        self.set_seats_present_sts(drv_seat=seat_pres_sts, pass_seat=seat_pres_sts, sec_left=seat_pres_sts,
                                   sec_mid=seat_pres_sts, sec_right=seat_pres_sts)
        
    
    def s2s_change_car_mode_and_check_result(self, car_mode:CarMode, car_mode_sub:int):
        logger.info(f"----->设置car mode 为{car_mode.name}")
        logger.info(f"------>调用 SetCarMode:(服务:BonnetService;函数名:set:SetCarMode(mode:{car_mode.name}))")
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": car_mode.value})
        logger.info(f"验证切换结果是否为{car_mode.name}:{car_mode_sub}")
        self.bus_comm.check_car_mode_status(car_mode_main=car_mode, car_mode_sub=car_mode_sub)

    
    def trigger_usage_mode_to_abandoned(self,wait_time:Union[int,float] = 180):
        # 2 发送lin 报文 补电
        self.bus_comm.set("cem_lin6","CemCem_Lin6Fr02", "BattSnsrStReq", 1)
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        logger.info("断开诊断激活线")
        self.io.bgm_diag_line_down()
        time.sleep(5)
        self.io.bgm_power_off()
        time.sleep(5)
        self.io.bgm_power_on()
        time.sleep(20)
        self.bus_comm.check("infocanfd", "BgmInfoCanFdFr20", 'DiagcComActv_0_BgmInfoCanFdSignalIPdu20', 0)
        # 3. 四门两盖关闭
        logger.info("关闭四门两盖")
        self.io.set_five_door_sts(Door.close)
        self.io.set_hood_sts(HoodSts.Close)
        # 四门两盖是否关闭
        self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
        # 4. 闭锁
        self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        time.sleep(1)
        # 等待一定时间
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 0)
        logger.info(f"最长等待{wait_time}秒,让 bgm 进入abandoned 模式，超过时间未进入则退出")
        self.bus_comm.check_usage_mode_status(UsageMode.ABANDONED,timeout=wait_time)


    @func_timeout.func_set_timeout(3*60*60)
    def back_fota_to(self, fota_sts: FOTAMasteSts, taskid = 0):
        try:
            if not self.sd_tester.check_mcu_whether_in_boot():
                logger.info("BGM MCU not in BOOT Mode")
            else:
                logger.info("BGM MCU in BOOT Mode, Wait")
                fota_status = self.soa.get_fota_status(MASTER_EVENT.Status)
                ua_status = self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status)
                logger.info(f"FOTA Status = {fota_status}, UA Status = {ua_status}")
                if fota_status == FOTAMasteSts.UPDATE.value and ua_status == UA_Sts.INSTALLING.value:
                    logger.info("BGM in update, need wait")
                    assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Wait BGM MCU back to app, but timeout 1800"
                    assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=1200)
                    logger.info("BGM MCU not in boot, go change VMM")
                else:
                    logger.error(f"Error Status: FOTA Status = {fota_status}, UA Status = {ua_status}")
            self.set_car_mode(CarMode.NORMAL)
            self.set_usage_mode(UsageMode.CONVENIENCE)
        except Exception as error:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(error)
        if fota_sts.name == 'IDLE':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.fota_back_to_idle()
            return True         
        if self.soa.get_fota_status(MASTER_EVENT.Status) == fota_sts.value:
            logger.info(f"FOTA Status is already {fota_sts.name}")
            return True
        elif fota_sts.name == 'QUERY':
            while True:
                status = self.soa.get_fota_status(MASTER_EVENT.Status)
                if status == FOTAMasteSts.IDLE.value:
                    if self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0:
                        self.tsp.trigger_vsp_fota(VSP.Reset, task_id=taskid)
                        self.tsp.trigger_vsp_fota(VSP.Repub, task_id=taskid)
                        self.io.bgm_diag_line_down()
                        time.sleep(20)
                    else:
                        self.io.bgm_diag_line_down()
                        time.sleep(10)
                elif status == FOTAMasteSts.QUERY.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, sleep 120s")
                    return True
                else:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, back to Idle")
                    self.fota_back_to_idle()
        elif fota_sts.name == 'NEW_TASK':
            status = self.soa.get_fota_status(MASTER_EVENT.Status)
            if status == FOTAMasteSts.NEW_TASK.value:
                return True
            self.back_fota_to(FOTAMasteSts.QUERY, taskid=taskid)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=4200)
        elif fota_sts.name == 'DOWNLOADING':
            status = self.soa.get_fota_status(MASTER_EVENT.Status)
            if status == FOTAMasteSts.DOWNLOADING.value:
                return True
            self.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=taskid)
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=30)
        elif fota_sts.name == 'ACTIVE':
            while True:
                status = self.soa.get_fota_status(MASTER_EVENT.Status)
                if status == FOTAMasteSts.IDLE.value:
                    if self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0:
                        self.tsp.trigger_vsp_fota(VSP.Reset, task_id=taskid)
                        self.tsp.trigger_vsp_fota(VSP.Repub, task_id=taskid)
                        self.io.bgm_diag_line_down()
                        time.sleep(20)
                    else:
                        self.io.bgm_diag_line_down()
                        time.sleep(10)
                elif status == FOTAMasteSts.DOWNLOADING.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, sleep 60s")
                    time.sleep(60)
                elif status == FOTAMasteSts.NEW_TASK.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}")
                    self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
                    self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
                    time.sleep(3)
                elif status == FOTAMasteSts.QUERY.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, sleep 20s")
                    time.sleep(20)
                elif status == FOTAMasteSts.ACTIVE.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, pass")
                    return True
                elif status == FOTAMasteSts.REMOTE_UPDATE.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, sleep 60s")
                    self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_HVSOCLow_0x04_0x20.value}})
                elif status == FOTAMasteSts.REACH_APPOINTMENT.value:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, CancelAppointment")
                    self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment, {"taskId": taskid})
                else:
                    logger.info(f"Wish to return Status:{fota_sts.name}, current Status:{status}, back to Idle")
                    self.fota_back_to_idle()
        elif fota_sts.name == 'UPDATE':
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            self.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
            time.sleep(5) #避免 StartUpdate 发太快
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=180), "back fota to Update, fail"
        elif fota_sts.name == 'REMOTE_UPDATE':
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            self.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
            self.soa.trigger_fota_type90(taskid)
        elif fota_sts.name == 'REACH_APPOINTMENT':
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            appoint_time = self.generate_fota_appointment_time(120)
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":taskid, "time":appoint_time})
            assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":taskid}) == appoint_time, "No scheduled events are currently available"
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.REACH_APPOINTMENT.value, 780), "FOTA Status ≠ REACH_APPOINTMENT"
        elif fota_sts.name == 'FAILED_DRIVING':
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            self.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
            self.ssh.type_commands(DeviceName.BGM, "rm -rf /update/ua/* /update/installer/*;sync") 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_DRIVING.value, timeout=120)
        elif fota_sts.name == 'FAILED_NOT_DRIVING':
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            self.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            self.soa.till_UpdateProcess_event_to(MASTER_UpdateProcess_EVENT.state, target_status=Master_UpdateStatusEnum.PRE_UPDATE.value, timeout=240)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=300)
        elif fota_sts.name == 'FACTORY_TASK':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.set_car_mode(car_mode=CarMode.FACTORY)
            self.ssh.copy_factory_packages()
            self.ssh.clear_fota_cache()
            self.sd_tester.reset_bgm()
            sleep(5)#等待启动
            assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_TASK.value and self.soa.get_fota_status(master_event_field=MASTER_EVENT.TaskId) == 1
        elif fota_sts.name == 'FACTORY_UPDATE':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.set_car_mode(car_mode=CarMode.FACTORY)
            self.ssh.copy_factory_packages()
            self.ssh.clear_fota_cache()
            self.sd_tester.reset_bgm()
            sleep(5)#等待启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_UPDATE.value, timeout=300)
        elif fota_sts.name == 'FACTORY_SUCCESSFUL':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.set_car_mode(car_mode=CarMode.FACTORY)
            self.ssh.copy_factory_packages()
            self.ssh.clear_fota_cache()
            self.sd_tester.reset_bgm()
            sleep(5)#等待启动
            self.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            return self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_SUCCESSFUL.value, timeout=1500)
        elif fota_sts.name == 'FACTORY_FAILED':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.set_car_mode(car_mode=CarMode.FACTORY)
            self.ssh.copy_factory_packages()
            self.ssh.clear_fota_cache()
            self.sd_tester.reset_bgm()
            sleep(5)#等待启动
            self.set_factory_ota_condition(display_hv_soc=200,low_volt_power=11.4,local_diag_sts=DiagActLineSts.DisActive) 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            return self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=600)
        elif fota_sts.name == 'SUCCESSFUL':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.back_fota_to(FOTAMasteSts.UPDATE, taskid=taskid)
            return self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=1500)
        elif fota_sts.name == 'RESCUE':
            logger.info(f"Wish to return Status:{fota_sts.name}")
            self.back_fota_to(FOTAMasteSts.ACTIVE, taskid=taskid)
            self.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.TaskType, target_status=FotaTaskType.Rescue.value, timeout=300)
        else:
            logger.error(f"Wrong fota_sts:{fota_sts.name}")

    @func_timeout.func_set_timeout(40*60)
    def fota_back_to_idle(self):
        try:
            if not self.sd_tester.check_mcu_whether_in_boot():
                logger.info("BGM MCU not in BOOT Mode")
            else:
                logger.info("BGM MCU in BOOT Mode, Wait")
                fota_status = self.soa.get_fota_status(MASTER_EVENT.Status)
                ua_status = self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status)
                logger.info(f"FOTA Status = {fota_status}, UA Status = {ua_status}")
                if fota_status == FOTAMasteSts.UPDATE.value and ua_status == UA_Sts.INSTALLING.value:
                    logger.info("BGM in update, need wait")
                    assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Wait BGM MCU back to app, but timeout 1800"
                    assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=1200)
                    logger.info("BGM MCU not in boot, go change VMM")
                else:
                    logger.error(f"Error Status: FOTA Status = {fota_status}, UA Status = {ua_status}")
            self.set_car_mode(CarMode.NORMAL)
            self.set_usage_mode(UsageMode.CONVENIENCE)
        except Exception as error:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(error)
        while True:
            status = self.soa.get_fota_status(MASTER_EVENT.Status)
            taskid = self.soa.get_fota_status(MASTER_EVENT.TaskId)
            if status == FOTAMasteSts.IDLE.value and taskid == 0:
                self.ssh.rm_factory_packages()
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, pass")
                break
            # if status == FOTAMasteSts.IDLE.value and taskid == 0:
            #     self.ssh.rm_factory_packages()
            #     self.soa.trigger_fota_type20(2)
            #     self.io.bgm_diag_line_down()
            #     assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.QUERY.value, timeout=60), "Back fota to query fail, 2_5"
            #     self.sd_tester.diag_cancel()
            #     assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.TaskId, target_status=0, timeout=60), "Back fota to Idle fail, 2_5"
            #     logger.info(f"FOTA Status is {status}, Taskid is {taskid}, pass")
            #     break
            elif status == None:
                logger.info(f"FOTA Status is {status}, reset carmode && usagemode")
                self.set_car_mode(CarMode.NORMAL)
                self.set_usage_mode(UsageMode.CONVENIENCE)
                self.ssh.clear_fota_cache()
                time.sleep(20)
            elif status == FOTAMasteSts.IDLE.value and taskid != 0:
                if taskid == 1:
                    logger.info(f"FOTA Status is {status}, Taskid is {taskid}, factory Idle => normal Idle")
                    self.set_car_mode(CarMode.NORMAL)
                    self.ssh.rm_factory_packages()
                    self.ssh.clear_fota_cache()
                    self.sd_tester.reset_bgm()
                else:
                    logger.info(f"FOTA Status is {status}, Taskid is {taskid}, 1.Diag Online + Query; 2.Successful => Idle")
                    self.io.bgm_diag_line_down() # 断开激活线，针对case1
                    time.sleep(10) #等待状态完全回到Idle，针对case2
            elif status == FOTAMasteSts.QUERY.value:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, relay off and cancel")
                self.io.bgm_diag_line_down()
                time.sleep(5)
                self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
                time.sleep(20)
            elif status == FOTAMasteSts.NEW_TASK.value:
                self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
                self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
                assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=30)
            elif status in [FOTAMasteSts.DOWNLOADING.value, 
                            FOTAMasteSts.ACTIVE.value, 
                            FOTAMasteSts.ROLLBACK.value, 
                            FOTAMasteSts.REACH_APPOINTMENT.value,
                            FOTAMasteSts.FACTORY_UPDATE.value]:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, cancel")
                self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
                time.sleep(20)
            elif status in [FOTAMasteSts.FAILED_NOT_DRIVING.value]:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, sleep 20s then cancel")
                time.sleep(20) # FAILED_NOT_DRIVING 需要等03F7上报上去后再取消，不然会出现（taskId=0 && StateCode=03F7）
                self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
                time.sleep(20)
            elif status in [FOTAMasteSts.UPDATE.value,
                            FOTAMasteSts.REMOTE_UPDATE.value,
                            FOTAMasteSts.FAILED_DRIVING.value,
                            FOTAMasteSts.SUCCESSFUL.value
                          ]:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, wait")
                time.sleep(20)
            elif status == FOTAMasteSts.FACTORY_TASK.value:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, cancel")
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                time.sleep(5)
                self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            elif status in [FOTAMasteSts.FACTORY_SUCCESSFUL.value, FOTAMasteSts.FACTORY_FAILED.value]:
                logger.info(f"FOTA Status is {status}, Taskid is {taskid}, cancel")
                self.set_car_mode(CarMode.NORMAL)
                self.ssh.rm_factory_packages()
                self.ssh.clear_fota_cache()
                self.sd_tester.reset_bgm()
                time.sleep(20)
            else:
                logger.error(FOTAMasteSts.IDLE.value)
                logger.error(f"FOTA Status is {status}, Taskid is {taskid}")
                assert False    

    def set_factory_ota_condition(self, display_hv_soc: Union[int, float], low_volt_power: Union[int, float], local_diag_sts: DiagActLineSts):
        self.bus_comm.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', display_hv_soc)
        logger.info(f"成功设置高压电池显示的SOC值为{display_hv_soc}")
        pdu_data_map = {
            11.4: [0x85, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00],
            11.5: [0x85, 0x03, 0x82, 0x00, 0x00, 0x00, 0x00],
            14: [0x85, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
        }
        if low_volt_power in pdu_data_map:
            self.bus_comm.ipdu.send_pdu("cem_lin6", 0x06, pdu_data_map[low_volt_power])
            logger.info(f"成功设置小电池电量值为{low_volt_power}")
        else:
            logger.error(f"不合法的低电压电量数值：{low_volt_power}，请在 [11.4, 11.5, 14] 中进行选择")
        diag_sts_map = {
            DiagActLineSts.DisActive: self.io.bgm_diag_line_down,
            DiagActLineSts.Active: self.io.bgm_diag_line_up
        }
        if local_diag_sts in diag_sts_map:
            diag_method = diag_sts_map[local_diag_sts]
            diag_method()
            logger.info(f"成功设置本地诊断状态为：{local_diag_sts}")
        time.sleep(12)

    def back_ua_to(self, domain_name: DOMAIN, ua_sts: UA_Sts, downlaod_req=None):
        try:
            if not self.sd_tester.check_mcu_whether_in_boot():
                logger.info("BGM MCU not in BOOT Mode")
                self.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
        except Exception as error:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(error)
        if ua_sts.name == 'READY_TO_INSTALL' and self.soa.get_ua_status(domain_name, UA_EVENT.PreUpdateStatus) != 0:
            logger.info("UA Status is already ready_to_install, but PreUpdateStatus is not 0")
            self.soa.ua_back_to_idle(domain_name=domain_name)
            self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
            return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
        if self.soa.get_ua_status(domain_name, UA_EVENT.Status) == ua_sts.value:
            logger.info(f"{domain_name} UA Status is already {ua_sts.name}")
        elif ua_sts.name == 'IDLE':
            self.soa.ua_back_to_idle(domain_name=domain_name)
            return True
        elif ua_sts.name == 'DOWNLOAD':
            self.soa.ua_back_to_idle(domain_name=domain_name)
            self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
            return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=1, timeout=30)
        elif ua_sts.name == 'INSTALLING':
            cur_ua_status = self.soa.get_ua_status(domain_name, UA_EVENT.Status)
            cur_ua_pre_updates_tatus = self.soa.get_ua_status(domain_name, UA_EVENT.PreUpdateStatus)
            if cur_ua_status == UA_Sts.DOWNLOAD.value:
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=3, timeout=30)
            elif cur_ua_status == UA_Sts.READY_TO_INSTALL.value and cur_ua_pre_updates_tatus == 0:
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=3, timeout=30)
            elif cur_ua_status == UA_Sts.READY_TO_INSTALL.value and cur_ua_pre_updates_tatus != 0:
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=3, timeout=30)
            else:
                self.soa.ua_back_to_idle(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=3, timeout=30)
        elif ua_sts.name == 'UPDATE_FINISH':
            cur_ua_status = self.soa.get_ua_status(domain_name, UA_EVENT.Status)
            if cur_ua_status in [UA_Sts.DOWNLOAD.value,
                                 UA_Sts.READY_TO_INSTALL.value]:
                self.back_ua_to(domain_name=domain_name, ua_sts=UA_Sts.INSTALLING, downlaod_req=downlaod_req)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=4, timeout=900)
            else:
                self.soa.ua_back_to_idle(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=4, timeout=900)
        elif ua_sts.name == 'SYSTEM_ACTIVE':
            cur_ua_status = self.soa.get_ua_status(domain_name, UA_EVENT.Status)
            if cur_ua_status in [UA_Sts.DOWNLOAD.value,
                                 UA_Sts.READY_TO_INSTALL.value,
                                 UA_Sts.INSTALLING.value]:
                self.back_ua_to(domain_name=domain_name, ua_sts=UA_Sts.UPDATE_FINISH, downlaod_req=downlaod_req)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.Activate)
                self.soa.empty_all()
                self.soa.wait_for_service_reconnect(partner_key=f'UpdateAgentService_client_{domain_name.name}_UA_Service', timeout=300)                
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=6, timeout=180)
            else:
                self.soa.ua_back_to_idle(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=4, timeout=900)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.Activate)
                self.soa.empty_all()
                self.soa.wait_for_service_reconnect(partner_key=f'UpdateAgentService_client_{domain_name.name}_UA_Service', timeout=300)                
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=6, timeout=180)
        elif ua_sts.name == 'UPDATE_FAILED':
            cur_ua_status = self.soa.get_ua_status(domain_name, UA_EVENT.Status)
            cur_ua_pre_updates_tatus = self.soa.get_ua_status(domain_name, UA_EVENT.PreUpdateStatus)
            if cur_ua_status == UA_Sts.DOWNLOAD.value:
                logger.info(f"Wish to return Status:{ua_sts.name}, current UA Status:{cur_ua_status}, current UA PreUpdateStatus:{cur_ua_pre_updates_tatus}")
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.ssh.rm_ua_packages(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=9, timeout=60)
            elif cur_ua_status == UA_Sts.READY_TO_INSTALL.value and cur_ua_pre_updates_tatus == 0:
                logger.info(f"Wish to return Status:{ua_sts.name}, current UA Status:{cur_ua_status}, current UA PreUpdateStatus:{cur_ua_pre_updates_tatus}")
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.ssh.rm_ua_packages(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=9, timeout=60)
            elif cur_ua_status == UA_Sts.READY_TO_INSTALL.value and cur_ua_pre_updates_tatus == 2:
                logger.info(f"Wish to return Status:{ua_sts.name}, current UA Status:{cur_ua_status}, current UA PreUpdateStatus:{cur_ua_pre_updates_tatus}")
                self.ssh.rm_ua_packages(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=9, timeout=60)
            else:  
                logger.info(f"Wish to return Status:{ua_sts.name}, current UA Status:{cur_ua_status}, current UA PreUpdateStatus:{cur_ua_pre_updates_tatus}")
                self.soa.ua_back_to_idle(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartDownload, args=downlaod_req)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=2, timeout=1800)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.PreUpdate)
                assert self.soa.till_ua_event_to(domain_name, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600)  #BGM解密最慢可能需要 7-8 min
                self.ssh.rm_ua_packages(domain_name=domain_name)
                self.soa.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.StartUpdate)
                return self.soa.till_ua_event_to(domain_name, UA_EVENT.Status, target_status=9, timeout=60)
        else:
            logger.error("Wrong UA_Sts")
    
    def push_door_outer_switch(self,pos:DoorPos = DoorPos.Dirver,time_interval:Union[int,float] = 2.5,pe_test:bool = False):
        if pe_test == False:
            self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
            sleep(2)

        prompt_info = f"触发模拟按{pos.name}门外开关"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Dirver":
                self.bus_comm.set("bodycan","DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorDrvrOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
                sleep(time_interval)
                self.bus_comm.set("bodycan","DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorDrvrOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)

            elif pos.name == "Pass":
                self.bus_comm.set("bodycan","PpodBodyFr01", 'DoorPassOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorPassOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(Pass =OutSwitchPressSts.Press)
                sleep(time_interval)
                self.bus_comm.set("bodycan","PpodBodyFr01", 'DoorPassOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorPassOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(Pass =OutSwitchPressSts.NoPress)

            elif pos.name == "RearLeft":
                self.bus_comm.set("bodycan","LpodBodyFr01", 'DoorLeReOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorLeReOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(LeRe =OutSwitchPressSts.Press)
                sleep(time_interval)
                self.bus_comm.set("bodycan","LpodBodyFr01", 'DoorLeReOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorLeReOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(LeRe =OutSwitchPressSts.NoPress)

            elif pos.name == "RearRight":
                self.bus_comm.set("bodycan","RpodBodyFr01", 'DoorRiReOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorRiReOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(RiRe =OutSwitchPressSts.Press)
                sleep(time_interval)
                self.bus_comm.set("bodycan","RpodBodyFr01", 'DoorRiReOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorRiReOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(RiRe =OutSwitchPressSts.NoPress)

            elif pos.name == "Tailgate":
                self.io.trigger_door_outswitch_sts(Trunk = OutSwitchPressSts.Press)
                time.sleep(time_interval)
                self.io.trigger_door_outswitch_sts(Trunk=OutSwitchPressSts.NoPress)

    def chk_tcam_ping(self, ping_time=4):
        failed=[]
        chanel_data = self.ssh.chk_net_channel()
        assert len(chanel_data) == 2, f"未检查到两路网卡"
        for i in chanel_data:
            ping_data = self.ssh.tcam_ping_net(i, ping_time=ping_time)
            check_data = f"{ping_time} packets transmitted"
            if check_data in ping_data and "100% packet loss" not in ping_data:
                allure.attach("OK")
            else:
                failed.append(ping_data)
        return failed
    
    def chk_bgm_ping(self, ping_time=4):
        failed = []
        with allure.step("查看BGM联网结果:"):
            data = self.ssh.bgm_ping_net(ping_time=ping_time)
            check_data = f"{ping_time} packets transmitted"
            if check_data in data and "100% packet loss" not in data:
                allure.attach("OK")
            else:
                failed.append("BGM不能联网")
        return failed
    
    def chk_bmg_ping_tcam(self, ping_time=4):
        failed = []
        with allure.step("查看BGM互联tcam结果:"):
            data = self.ssh.bgm_ping_net(ping_time=ping_time)
            check_data = f"{ping_time} packets transmitted"
            if check_data in data and "100% packet loss" not in data:
                allure.attach("OK")
            else:
                failed.append("BGM不通tcam")
        return failed

    def update_version_debug(self, task_id: int, domain_need_flushed_list: list = [DOMAIN.BGM, DOMAIN.TCAM], baseline: str='6100000200 DZ'):
        with open('config/UA_conf.yaml', 'r') as f:
            data = yaml.safe_load(f)
        if DOMAIN.BGM in domain_need_flushed_list and DOMAIN.TCAM in domain_need_flushed_list:
            bgm_hwpn = self.sd_tester.get_bgm_hard_version()
            tcam_hwpn = self.sd_tester.get_tcam_hard_version()
            logger.info("========================================================")
            logger.info("Current domain controller: BGM && TCAM")
            logger.info("========================================================")
            version_debug = data['Version_Debug_Two_Domain']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["ecu"][0]["HWPN"] = bgm_hwpn
            version_debug["data"]["ecu"][1]["HWPN"] = tcam_hwpn
        elif len(domain_need_flushed_list) == 1 and DOMAIN.BGM in domain_need_flushed_list:
            bgm_hwpn = self.sd_tester.get_bgm_hard_version()
            logger.info("========================================================")
            logger.info("Current domain controller: BGM ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_BGM']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["ecu"][0]["HWPN"] = bgm_hwpn
        elif len(domain_need_flushed_list) == 1 and DOMAIN.TCAM in domain_need_flushed_list:
            tcam_hwpn = self.sd_tester.get_tcam_hard_version()
            logger.info("========================================================")
            logger.info("Current domain controller: TCAM ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_TCAM']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["ecu"][0]["HWPN"] = tcam_hwpn
        elif len(domain_need_flushed_list) == 1 and DOMAIN.CDC in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: CDC ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_CDC']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and DOMAIN.ACU in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: ACU ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_ACU']
            version_debug["data"]["taskId"] = task_id    
        elif len(domain_need_flushed_list) == 0:
            logger.info("========================================================")
            logger.info("Current domain controller: ecu ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_Non_Domian']
            version_debug["data"]["taskId"] = task_id        
        elif len(domain_need_flushed_list) == 1 and "CD" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: CD ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_CD']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and "PDM" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: PDM ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_PDM']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and "DDM" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: DDM ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_DDM']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and "SRS" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: SRS ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_SRS']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and "rescueErrorHWPN_BGM" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: Version_rescueErrorHWPN_BGM ")
            logger.info("========================================================")
            version_debug = data['Version_rescueErrorHWPN_BGM']
            version_debug["data"]["taskId"] = task_id
        elif len(domain_need_flushed_list) == 1 and "rescue_BGM" in domain_need_flushed_list:
            bgm_hwpn = self.sd_tester.get_bgm_hard_version()
            bgm_swpn = self.sd_tester.get_bgm_soft_version()
            logger.info("========================================================")
            logger.info("Current domain controller: Version_rescue_BGM ")
            logger.info("========================================================")
            version_debug = data['Version_rescue_BGM']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["ecu"][0]["HWPN"] = bgm_hwpn
            version_debug["data"]["ecu"][0]["SWPN"] = bgm_swpn
        elif len(domain_need_flushed_list) == 1 and "OtherEcu" in domain_need_flushed_list:
            logger.info("========================================================")
            logger.info("Current domain controller: Version_Debug_OtherEcu ")
            logger.info("========================================================")
            version_debug = data['Version_Debug_OtherEcu']
            version_debug["data"]["taskId"] = task_id
        else:
            logger.error(f"Invalid domain control combination: {domain_need_flushed_list}")
        version_debug["data"]["baseLineVer"] = baseline
        config_json = json.dumps(version_debug).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{config_json}" > /update/version_debug.json')
        time.sleep(0.2)
        
    def trigger_call_sos_by_crash(self):
        logger.info("通过切换carmode的方式触发xcall")
        try:
            self.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        except AssertionError as e:
            logger.info(f"切换模式失败，原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("crash切换失败，未能触发xcall")

    
    def set_and_check_pos_lamp(self):
        prompt_info = f"----------> 通过服务开启位置灯，并且通过总线检查位置灯开关状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
            self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On, extr_light_sts=ExtrLtgSts.On)

    def network_sleep(self):
        self.set_car_mode(CarMode.NORMAL)
        self.set_usage_mode(UsageMode.INACTIVE)
        self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        # 断开诊断激活线
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.io.tcam_kl15_down()
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.stop_tester_present()
        # 设置车辆静止
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        # 关闭四门两盖、座椅不占座、门外开关不按、没有踩刹车、危险报警灯不亮
        self.set_seats_present_sts(
            drv_seat=SeatPresSts.NoPres,
            pass_seat=SeatPresSts.NoPres,
            sec_left=SeatPresSts.NoPres,
            sec_mid=SeatPresSts.NoPres,
            sec_right=SeatPresSts.NoPres
        )
        self.io.set_bgm_hardware_condition_to_default()
        self.io.set_hood_sts(HoodSts.Close)
        # 发送lin补电
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(10)
        # 设置NFC锁车
        self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        self.bus_comm.check_central_lock_sts(CenLockSts.Lock, LockTrigerSource.NFC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=60)
        self.bus_comm.stop_dk()
        # 清除缓存
        time.sleep(5)
        # self.bus_comm.ipdu.rx_flag_reset_all()
        # 判断车辆模式是否是ABANDONED
        start_time = time.time()
        while time.time() - start_time < 60 * 7:
            try:
                self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                logger.info(f'当前不为{UsageMode.ABANDONED.value}状态')
            else:
                break
            sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
        time.sleep(20)
        self.bus_comm.pause_all_bus_send()
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(40)
        # 检查CAN LIN FR是否有报文发出
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)
    
    def check_tcam_sleep(self, timeout=120):  
        """  
        检查TCAM是否进入休眠状态  
        """  
        logger.info('检查TCAM休眠')  
        start_time = time.time()  # 记录开始时间  
        while time.time() - start_time < timeout:  
            cmd = "ping 172.16.5.31 -c 1"  
            result = exec_shell(cmd)  
            msg = self.bus_comm.check_bus_recv_message("connectivitycanfd")  
            if ("100% packet loss" in result['output'] or "100% 包丢失" in result['output']) and msg is None:  
                logger.info('TCAM已进入休眠状态')  
                return True  
            time.sleep(1)  # 等待1秒  
        logger.info('TCAM在{}秒内未进入休眠状态'.format(timeout))  
        return False 
    
    def tcam_network_sleep(self,time_out: int = 240):  
        """  
        执行TCAM的休眠动作。若TCAM已经休眠,则直接返回。  
        否则,执行休眠动作并等待TCAM进入休眠状态。  
    
        :param timeout: 检查TCAM是否进入休眠状态的超时时间(秒) 
        """  
        logger.info('检查TCAM是否已休眠')  
        if self.check_tcam_sleep(1):  
            logger.info('TCAM已处于休眠状态')  
            return  
        logger.info('执行TCAM休眠动作')  
        try:  
            self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)  
            self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
            time.sleep(1)  # 等待1秒
            self.io.tcam_kl15_down()  
            self.bus_comm.pause_all_bus_send()  
            logger.info('等待TCAM进入休眠状态')  
            if not self.check_tcam_sleep(time_out):  
                raise Exception('TCAM休眠失败')  
            logger.info('TCAM已成功进入休眠状态')  
        except Exception as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error('执行TCAM休眠动作时发生错误: %s', str(e))  
            raise

    def set_normal_fota_update_condition(self, vehspd: Union[int, float], gear: Union[Gear, None], display_hv_soc: Union[int, float], thermaloutofcontrol: bool, low_volt_soc: Union[int, float], local_diag_sts: DiagActLineSts):
        self.bus_comm.set_vehspd(vehspd)
        logger.info(f"成功设置车速为{vehspd}")
        self.bus_comm.set_gear_pos(gear,ParkLockSts.ParkNotEngd)
        logger.info(f"成功设置挡位为{gear}")
        self.bus_comm.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', display_hv_soc)
        logger.info(f"成功设置高压电池显示的SOC值为{display_hv_soc}")
        pdu_data_map = {
            50: [0xF4, 0x01, 0xB4, 0x00, 0x00, 0x00, 0x00],
            69: [0xB2, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            70: [0xBC, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            71: [0xC6, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            90: [0x84, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
        }
        if low_volt_soc in pdu_data_map:
            self.bus_comm.ipdu.send_pdu("cem_lin6", 0x06, pdu_data_map[low_volt_soc])
            logger.info(f"成功设置小电池电量SOC值为{low_volt_soc}")
        else:
            logger.error(f"不合法的小电池电量SOC值：{low_volt_soc}，请在 [50, 69, 70, 71, 90] 中进行选择")
        diag_sts_map = {
            DiagActLineSts.DisActive: self.io.bgm_diag_line_down,
            DiagActLineSts.Active: self.io.bgm_diag_line_up
        }
        if local_diag_sts in diag_sts_map:
            diag_method = diag_sts_map[local_diag_sts]
            diag_method()
            logger.info(f"成功设置本地诊断状态为：{local_diag_sts}")
        if thermaloutofcontrol:
            self.bus_comm.ipdu.send_pdu("propulsioncan", 0x142, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        else:
            self.bus_comm.ipdu.send_pdu("propulsioncan", 0x142, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        logger.info(f"成功设置电池热失控状态为：{thermaloutofcontrol}")
        time.sleep(3)
    
    def check_ccp_data_resp(self, check_type:CheckType, bus_name, id: Union[str, int], data_index=0):
        ccp_dict = {}
        start = time.time()
        # 阻塞等待第一帧的01序号报文发出并存储第一帧报文
        while (time.time() - start < 30):
            id, time_stamp, length, data, = self.bus_comm.recv_pdu(bus_name, id)
            if data and data[data_index] == 1:
                ccp_dict[data[data_index]] = time_stamp
                break
        before = time.time()
        if check_type.value == 1:
            with allure.step(f"判断一个周期的ccp信号值是否在9s内"):
                while (len(ccp_dict) < 72 and (time.time() - before < 30)):
                    id, time_stamp, length, data, = self.bus_comm.recv_pdu(bus_name, id)
                    ccp_dict[data[data_index]] = time_stamp
                if len(ccp_dict) < 72:
                    assert False, '超时30s仍未发送一轮ccp信号'
                elif len(ccp_dict) == 72:
                    logger.info(f'ccp_dict的值为:{ccp_dict}')
                    first_pdu_time = ccp_dict[1]
                    finally_pdu_time = ccp_dict[72]
                    ccp_interval_time = finally_pdu_time - first_pdu_time
                    logger.info(f'ccp_interval_time的值为:{ccp_interval_time / 1000000}s')
                    assert ccp_interval_time / 1000000 <= 9, f'超时{ccp_interval_time}s仍未发送一轮ccp信号'
                else:
                    assert False, 'ccp_dict长度大于72'
        if  check_type.value == 2:
            with allure.step(f"判断30s有多少周期ccp"):
                ccp_dict['1+1'] = ccp_dict.pop(1)
                num = 2
                while (time.time() - before <= 30):
                    id, time_stamp, length, data, = self.bus_comm.recv_pdu(bus_name, id)
                    ccp_dict[str(data[data_index]) + f'+{num}'] = time_stamp
                    num += 1
                logger.info(f'ccp_dict的值为{ccp_dict}')
                ccp_keys = list(ccp_dict.keys())
                ccp_count = 0
                while len(ccp_keys) >= 72:
                    start_time = ccp_dict[ccp_keys[0]]
                    for ccp in ccp_keys:
                        if '72+' in ccp:
                            ccp_keys = ccp_keys[ccp_keys.index(ccp) + 1:]
                            while '72+' in ccp_keys[0]:
                                ccp_keys = ccp_keys[1:]
                            end_time = ccp_dict[ccp]
                            ccp_count += 1
                            logger.info(f'当前轮次为第{ccp_count}轮,所用时间为{(end_time - start_time)/1000000}s')
                            break
                    ccp_keys_num = [ccp_num.split('+')[0] for ccp_num in ccp_keys]
                    if '72' not in ccp_keys_num:
                        break
                assert ccp_count >= 2, f'30S内一共有{ccp_count}轮次的ccp'
        if  check_type.value == 3:
            with allure.step(f"判断一个周期的cpp报文是否完整"):
                while (time.time() - before < 30):
                    id, time_stamp, length, data, = self.bus_comm.recv_pdu(bus_name, id)
                    ccp_dict[data[data_index]] = time_stamp
                    if data[data_index] == 72:
                        break
                if len(ccp_dict) == 72 and list(ccp_dict.keys()) == list(range(1, 73)):
                    logger.info("报文帧连续，未丢帧")
                else:
                    logger.info(f'报文帧不连续,ccp_dict的信号内容为{ccp_dict}')

    def get_mcu_cpuload_save_data(self, path='/root/bgm_log/cpu_load',run_status='', **kwargs):
        '''
        读取mcu cpu load 保存在csv 文件
        @param path: 保存路径
        @param run_status: 运行状态
        @param kwargs:
        @return:
        '''
        mcu_version = kwargs.get('mcu_version', None)
        boot_version = kwargs.get('boot_version', None)
        mpu_version = kwargs.get('mpu_version', None)
        run_status = kwargs.get('run_status', '')

        try:
            save_data_head = ['日期', "mpu版本",  "mcu版本","mcu boot版本",
                              "核0 50ms内mcu当前负载", "核0 50ms内mcu峰值负载", "核0 500ms内mcu当前负载",
                              "核0 500ms内mcu峰值负载",
                              "核1 50ms内mcu当前负载", "核1 50ms内mcu峰值负载", "核1 500ms内mcu当前负载",
                              "核1 500ms内mcu峰值负载",
                              "运行状态"
                              ]

            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            print(otherStyleTime)
            save_data_list = [otherStyleTime]
            if not os.path.exists(path):
                os.makedirs(path)
            save_csv_path = os.path.join(path, 'mcu_cpu_load.csv')
            try:
                if mpu_version is None:
                    self.sd_tester.update_serverdoipid(0x1001)
                    boot_version,mpu_version = self.sd_tester.read_bgm_mpu_version()
                # 读取mcu 版本
                if mcu_version is None:
                    mcu_version = self.sd_tester.read_bgm_mcu_version()
                if boot_version is None:
                    boot_version = self.sd_tester.read_bgm_boot_version()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                logger.warning(f"读取版本号失败{str(e)}")
            save_data_list.append(mpu_version)
            save_data_list.append(mcu_version)
            save_data_list.append(boot_version)

            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_data([0x22, 0xdb, 0x02])
            return_result_list = self.sd_tester.return_udsdata_and_check_and_print_response_result()
            cpuload_list = return_result_list[3:]
            cpuload1 = cpuload_list[0]
            cpuload2 = cpuload_list[1]
            cpuload3 = cpuload_list[2]
            cpuload4 = cpuload_list[3]
            string = f'核0:50ms内mcu当前负载:{cpuload1}%  50ms内mcu峰值负载:{cpuload2}% 500ms内mcu当前负载:{cpuload3}% 500ms内mcu峰值负载:{cpuload4}%'
            with allure.step(string):
                logger.info(string)

            save_data_list.append(cpuload1)
            save_data_list.append(cpuload2)
            save_data_list.append(cpuload3)
            save_data_list.append(cpuload4)

            cpuload1 = cpuload_list[4]
            cpuload2 = cpuload_list[5]
            cpuload3 = cpuload_list[6]
            cpuload4 = cpuload_list[7]
            string = f'核1:50ms内mcu当前负载:{cpuload1}%  50ms内mcu峰值负载:{cpuload2}% 500ms内mcu当前负载:{cpuload3}% 500ms内mcu峰值负载:{cpuload4}%'
            with allure.step(string):
                logger.info(string)
            save_data_list.append(cpuload1)
            save_data_list.append(cpuload2)
            save_data_list.append(cpuload3)
            save_data_list.append(cpuload4)
            #
            save_data_list.append(run_status)
            try:
                # 写入 csv 文件
                if os.path.exists(save_csv_path):
                    with open(save_csv_path, "a+", newline="",encoding='gbk') as csv_f:
                        csv_writer = csv.writer(csv_f)
                        csv_writer.writerow(save_data_list)
                else:
                    with open(save_csv_path, "a+", newline="",encoding='gbk') as csv_f:
                        csv_writer = csv.writer(csv_f)
                        csv_writer.writerow(save_data_head)
                        csv_writer.writerow(save_data_list)
                logger.info(f"cpu load 数据保存在{run_status}下")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                logger.error(f"保存cpu load 数据失败{str(e)}")

            return cpuload_list
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(f"读取cpu load 失败 ERROR：{e}")
            return []
    
    def service_change_usage_mode_and_check_result(self, usagemode:UsageMode):
        USAGE_MODE_MAP = {
        0: "ABANDONED",
        1: "INACTIVE",
        2: "CONVENIENCE",
        11: "ACTIVE",
        13: "DRIVING"}
        curren_usage_mode = self.bus_comm.get_usage_mode_status()
        curren_usage_mode_name = USAGE_MODE_MAP.get(curren_usage_mode)
        logger.info(f"当前模式为 为{curren_usage_mode_name}:{curren_usage_mode}")
        if curren_usage_mode < usagemode.value:
            self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            method_name = "SetUsageModeUp"
        elif curren_usage_mode > usagemode.value:
            method_name = "SetUsageModeDown"
        else:
            # 已经是所需要模式，无需切换，直接返回
            return 1, curren_usage_mode, usagemode.value
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client', method_name,{"mode": usagemode.value})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=usagemode)

    
    def wti_sig_set_and_get_and_event_check_warning_light_sts(self,func:WTI_Func,sig_value:Union[int,float], prom_name: str, prom_state: str):
        self.bus_comm.set_wti_signal(func = func,value = sig_value)
        self.soa.get_and_event_check_warning_light_list(name = prom_name,state = prom_state)
        

    def wti_sig_set_and_get_and_event_check_warning_info_list(self,func:WTI_Func,sig_value:Union[int,float], prom_name: str, prom_state: str):
        self.bus_comm.set_wti_signal(func = func,value = sig_value)
        self.soa.get_and_event_check_warning_info_list(name = prom_name,info = prom_state)
                                                              

    
    def diag_route_doip2can_func(self, data_info_list, send_length, **kwargs):
        """
        发送 以太到 can canfd 的诊断路由
        @param data_info_list:
        @param send_length:
        @return:
        """
        max_len = kwargs.get('max_len', 6)

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        name_list, index_list, can_map = self.bus_comm.get_all_can_channel_info()

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_address = item_info.get("recv_address")

            can_recv_channel = item_info.get("can_recv_channel")
            lin_recv_channel = item_info.get("lin_recv_channel")
            fr_recv_channel = item_info.get("fr_recv_channel")
            request_id = item_info.get("request_id")
            padding = item_info.get("padding")
            length = item_info.get("length")

            # 更新逻辑地址，必须
            self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                try:
                    # 接受请求
                    string = f"长度小于等于{max_len}，can/canfd 通道 {can_recv_channel}可以接收数据"
                    logger.info(string)
                    self.bus_comm.clear_recv_pdu_d_buffer('bodycan')

                    # 生成随机数据
                    send_data = [random.randint(0, 255) for i in range(send_length)]
                    # 发送请求
                    string = f"{send_channel}发送数据长度{send_length}"
                    logger.info(string)
                    self.sd_tester.send_data(send_data)

                    recv_data_map = self.bus_comm.recv_mul_can_channel_msg(can_chnanel_lis=index_list, msg_id=0x7ff,
                                                                           unexpect_msg=[0x02, 0x3e, 0x80])
                    for recv_channel in can_recv_channel:
                        can_index = self.bus_comm.get_can_channel_index_by_name(recv_channel)
                        recv_mg_dic = recv_data_map.get(can_index)
                        if len(recv_mg_dic) == 1:
                            recv_mg_list = recv_mg_dic.get(request_id)
                            if len(recv_mg_list) == 1:
                                msg_ifo = recv_mg_list[0]
                                can_len = msg_ifo[0]
                                recv_msg_data = msg_ifo[1:can_len + 1]
                                recv_padding = list(set(msg_ifo[can_len + 1:]))

                                if len(recv_padding) > 1 or (
                                        recv_padding and recv_padding[0] != padding
                                ):
                                    err_item_list.append(hex(recv_address))
                                    string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败,填充位不对，本应为{padding}实际为{recv_padding}"
                                    self.log_and_allure_step(string, LogLevel.ERROR)

                                elif len(send_data) != len(recv_msg_data):
                                    err_item_list.append(hex(recv_address))
                                    string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败 发送数据长度{len(send_data)}，can接收数据的长度{len(recv_msg_data)}"
                                    self.log_and_allure_step(string, LogLevel.ERROR)

                                elif recv_msg_data != send_data:
                                    err_item_list.append(hex(recv_address))
                                    string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败，接收的内容和发送的内容不一样，发送数据{send_data}，can接收数据的{recv_msg_data}"
                                    self.log_and_allure_step(string, LogLevel.ERROR)

                                else:
                                    string = f"第{index + 1}条》》》路由长度为{send_length}成功 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由成功"
                                    self.log_and_allure_step(string, LogLevel.INFO)
                            else:
                                err_item_list.append(hex(recv_address))
                                string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败 发送数据长度{send_data}，can接收数据的长度{recv_mg_list}"
                                self.log_and_allure_step(string, LogLevel.ERROR)
                        else:
                            err_item_list.append(hex(recv_address))
                            string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(recv_address)}路由失败 发送数据长度{send_data}，can接收数据的{recv_mg_dic}"
                            self.log_and_allure_step(string, LogLevel.ERROR)

                    for unrecv_channel in name_list:
                        if unrecv_channel in can_recv_channel:
                            continue
                        can_index = self.bus_comm.get_can_channel_index_by_name(unrecv_channel)
                        recv_mg_list = recv_data_map.get(can_index)

                        if recv_mg_list:
                            err_item_list.append(hex(recv_address))
                            string = f"第{index + 1}条*****路由长度为{send_length}失败 {unrecv_channel}本不应收到，实际收到{recv_mg_list}"
                            self.log_and_allure_step(string, LogLevel.ERROR)
                        else:
                            logger.info(f"{unrecv_channel}本不应收到，实际未收到")
                    # 接受请求
                    string = f"lin 通道 {lin_recv_channel}接收数据"
                    logger.info(string)
                    for recv_channel in lin_recv_channel:
                        pass
                    string = f"fr 通道 {fr_recv_channel}接收数据"
                    logger.info(string)
                    for recv_channel in fr_recv_channel:
                        pass
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(recv_address))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{can_recv_channel}逻辑地址为{hex(recv_address)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)

        assert not len(err_item_list), string

    def diag_route_eth2can_unrecv(self, data_info_list, send_length, all_can=False):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length
        name_list, index_list, can_map = self.bus_comm.get_all_can_channel_info()

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_address = item_info.get("recv_address")
            recv_channel = item_info.get("recv_channel")

            # 更新逻辑地址，必须
            self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                # 清空 通道缓存
                # self.bus_comm.clear_all_bus_buffer()
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                # 生成随机数据
                send_data = [random.randint(0, 255) for i in range(send_length)]
                # 发送请求
                string = f"{send_channel}发送数据长度{send_length}"
                logger.info(string)
                send_eth_time = time.time()
                self.sd_tester.send_data(send_data)
                try:
                    recv_data_map = self.bus_comm.recv_mul_can_channel_msg(can_chnanel_lis=index_list,
                                                                           msg_id=(0x700, 0x7ff),
                                                                           unexpect_msg=[0x02, 0x3e, 0x80])
                    for unrecv_channel in name_list:
                        if not all_can and unrecv_channel == recv_channel:
                            continue
                        can_index = self.bus_comm.get_can_channel_index_by_name(unrecv_channel)
                        recv_msg_dic = recv_data_map.get(can_index)
                        if recv_msg_dic:
                            err_item_list.append(hex(recv_address))

                            string = f"第{index + 1}条*****路由长度为{send_length}失败，obd 发送给{hex(recv_address)} {unrecv_channel}本不应收到，实际收到{recv_msg_dic}"
                            with allure.step(string):
                                logger.error(string)
                                for can_id, can_msg in recv_msg_dic.items():
                                    string2 = f"{unrecv_channel}通道，接收到id为{hex(can_id)[2:].upper()} 内容为{can_msg}的报文"
                                    with allure.step(string2):
                                        logger.error(string2)
                        else:
                            string = f"第{index + 1}条obd 发送给{hex(recv_address)} {unrecv_channel}本不应收到，实际未收到"
                            logger.info(string)

                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(recv_address))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}逻辑地址为{hex(recv_address)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)
        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def SetConvenienceForAppAction_and_check_usagemode(self, time1: int , usagemode: UsageMode):
        self.soa.send_method_request(
            'VehicleSetStatusService_client', "SetConvenienceForAppAction", {"time": time1}
        )
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=usagemode)
    
    def wait_time_in_usagemde(self, num, usagemode: UsageMode):
        for i in range(num):
            time.sleep(60)
            self.bus_comm.check_usage_mode_status(usage_mode=usagemode)
            logger.info(f'当前时间为{60*i+60}s')
    
    def wait_time_exit_usagemde_a_to_b(self, num, usagemode1: UsageMode, usagemode2: UsageMode):
        self.wait_time_in_usagemde(num-1, usagemode=usagemode1)
        time.sleep(50)
        self.bus_comm.check_usage_mode_status(usage_mode=usagemode1)
        time.sleep(10)
        self.bus_comm.check_usage_mode_status(usage_mode=usagemode2)
          
    def creat_diag_route_doip2can_phy_invalid_data_item(self,data_info_list_phy):
        '''
        构造 以太到can的 物理寻址的，无效数据
        @return:
        '''
        # data_info_list_phy = self.mix.read_diag_route_excel(self.excel_path, 'doip2docan')
        new_dic = {}
        temp = None
        # 分类
        for item in data_info_list_phy:
            recv_name = item['recv_channel']
            recv_address = item['recv_address']
            request_id = item['request_id']
            if recv_name in new_dic:
                new_dic[recv_name].append(recv_address)
            else:
                new_dic[recv_name] = [recv_address]
            temp = item

        new_data_list = []
        # 构造非法逻辑地址,组装新数据
        for name, address_list in new_dic.items():
            address = hex(address_list[0])[2:].zfill(4)
            min_address = int(address[:2] + '00', 16)
            max_address = int(address[:2] + 'FF', 16)
            add_lis = [i for i in range(min_address, max_address + 1) if i not in address_list]
            lis = random.sample(add_lis, 5)
            for add in lis:
                new_item = copy.deepcopy(temp)
                new_item['recv_channel'] = name
                new_item['recv_address'] = add
                new_item['request_id'] = int("7" + hex(add)[2:].zfill(4)[2:], 16)
                new_item['response_id'] = int("6" + hex(add)[2:].zfill(4)[2:], 16)
                new_data_list.append(new_item)
        return new_data_list
    
    def generate_dtc_fault(self,dtc_fault:DTCFault,last_time:Union[int,float] = 0):
        prompt_info = f"---------->引入{dtc_fault.name}故障来制造DTC:{dtc_fault.value} 故障持续时间设为{last_time}s"
        with allure.step(prompt_info):
            logger.info(prompt_info)

            if dtc_fault.name == "AWMSensorFail_A":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallAFlt',1)
            elif dtc_fault.name == "AWMSensorFail_B":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallBFlt',1)
            elif dtc_fault.name == "CommunicationFail_CEM_and_RSLM":
                self.bus_comm.stop_send_pdu("cem_lin1","RlsmCem_Lin1Fr01")
            elif dtc_fault.name == "NoSignalFromWMM":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe',random.choice([0, 3]))
            elif dtc_fault.name == "ActvReSplrHallSnsrFltHallOutpFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallOutpFlt',1)
            elif dtc_fault.name =="ActvReSplrUFltLoVoltDetdFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltLoVoltDetdFlt',1)
            elif dtc_fault.name =="ActvReSplrUFltHiVoltDetdFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt',1)
            elif dtc_fault.name =="CalStsAWM":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM',0)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt3":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt3',1)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt5":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt5',1)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt2":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt2',1)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt1":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt1',1)
            elif dtc_fault.name =="ActvReSplrIntFltActrFlt4":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt4',1)
            elif dtc_fault.name =="RainSensorFault":
                self.bus_comm.set_rain_sensor_fault_sts(type=RainSensorFaultType.SensorFault,sts=True)
            elif dtc_fault.name =="RainSensorCalibrationFault":
                self.bus_comm.set_rain_sensor_fault_sts(type=RainSensorFaultType.CalibrationFault,sts=True)
            elif dtc_fault.name =="BMSCommunicationFault":
                self.bus_comm.pause_ecu_send('cem_lin6','BMS')
            elif dtc_fault.name =="BMSHardwareFault":
                self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 1)
            elif dtc_fault.name =="IPMBattSocSts":
                self.bus_comm.stop_send_pdu("bodycan", "IpmBodyFr01")
            elif dtc_fault.name =="RSLMCommunicationFault":
                self.bus_comm.pause_ecu_send('cem_lin1','RSLM')
            elif dtc_fault.name =="Rainerror":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainDetnErrRainDetnErr', 1)
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrRainDetnErrActv',1)
            elif dtc_fault.name =="Raincalibrationerror":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrCalErr', 1)
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrCalErrActv',1)
            elif dtc_fault.name == "WiperError":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe',2)
            elif dtc_fault.name == "WiperVoltage":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotLoVoltDetd',2)
            elif dtc_fault.name == "WiperOverVoltage":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotHiVoltDetd',2)
            elif dtc_fault.name == "WiperOverload":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotOvldDetd',2)
            elif dtc_fault.name == "RelHumSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',1)
            elif dtc_fault.name == "NoresponseBMS":
                self.bus_comm.pause_ecu_send('cem_lin6','BMS')
            elif dtc_fault.name == "WMMresponseLIN":
                self.bus_comm.pause_ecu_send('cem_lin1','WMM')
            elif dtc_fault.name == "SolarSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',1)
            elif dtc_fault.name =="SunSensorFault":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',1)
            elif dtc_fault.name =="RelHumSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',1)
            elif dtc_fault.name =="Switch_Right":
                self.bus_comm.pause_ecu_send('bodycan','SWTR')
                self.bus_comm.pause_ecu_send('bodycan','SWTL') 
            elif dtc_fault.name =="Switch_Left":
                self.bus_comm.pause_ecu_send('bodycan','SWTR')
                self.bus_comm.pause_ecu_send('bodycan','SWTL')    
                
            logger.info(f"--------->等待{last_time}")
            sleep(last_time)
        
        

    def remove_dtc_fault(self,dtc_fault:DTCFault,last_time:Union[int,float] = 0):
        prompt_info = f"---------->移除{dtc_fault.name}故障，移除故障之后等待{last_time}s"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if dtc_fault.name == "AWMSensorFail_A":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallAFlt',0)
            elif dtc_fault.name == "AWMSensorFail_B":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallBFlt',0)
            elif dtc_fault.name == "CommunicationFail_CEM_and_RSLM":
                self.bus_comm.resume_send_pdu("cem_lin1","RlsmCem_Lin1Fr01")
            elif dtc_fault.name == "NoSignalFromWMM":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe',1)
            elif dtc_fault.name == "ActvReSplrHallSnsrFltHallOutpFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallOutpFlt',0)
            elif dtc_fault.name =="ActvReSplrUFltLoVoltDetdFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltLoVoltDetdFlt',0)
            elif dtc_fault.name =="ActvReSplrUFltHiVoltDetdFlt":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt',0)
            elif dtc_fault.name =="CalStsAWM":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM',2)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt3":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt3',0)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt5":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt5',0)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt2":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt2',0)
            elif dtc_fault.name == "ActvReSplrIntFltActrFlt1":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt1',0)
            elif dtc_fault.name =="ActvReSplrIntFltActrFlt4":
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt4',0)
            elif dtc_fault.name =="RainSensorFault":
                self.bus_comm.set_rain_sensor_fault_sts(type=RainSensorFaultType.SensorFault,sts=False)
            elif dtc_fault.name =="RainSensorCalibrationFault":
                self.bus_comm.set_rain_sensor_fault_sts(type=RainSensorFaultType.CalibrationFault,sts=False)
            elif dtc_fault.name =="BMSCommunicationFault":
                self.bus_comm.resume_ecu_send('cem_lin6','BMS')
            elif dtc_fault.name =="BMSHardwareFault":
                self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 0)
            elif dtc_fault.name =="IPMBattSocSts":
                self.bus_comm.resume_send_pdu("bodycan", "IpmBodyFr01")
            elif dtc_fault.name =="RSLMCommunicationFault":
                self.bus_comm.resume_ecu_send('cem_lin1','RSLM')
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainDetnErrRainDetnErr', 0)
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainDetnErrRainDetnErr', 1)
            elif dtc_fault.name =="Rainerror":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainDetnErrRainDetnErr', 0)
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrRainDetnErrActv',0)
            elif dtc_fault.name =="Raincalibrationerror":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrCalErr', 0)
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr01', 'RainSnsrErrCalErrActv',0)
            elif dtc_fault.name == "WiperError":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe',1)
            elif dtc_fault.name == "WiperVoltage":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotLoVoltDetd',1)
            elif dtc_fault.name == "WiperOverVoltage":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotHiVoltDetd',1)
            elif dtc_fault.name == "WiperOverload":
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotOvldDetd',1)
            elif dtc_fault.name == "RelHumSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',0)
            elif dtc_fault.name == "NoresponseBMS":
                self.bus_comm.resume_ecu_send('cem_lin6','BMS')
            elif dtc_fault.name == "WMMresponseLIN":
                self.bus_comm.resume_ecu_send('cem_lin1','WMM')
            elif dtc_fault.name == "SolarSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',0)
            elif dtc_fault.name =="SunSensorFault":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',0)
            elif dtc_fault.name =="RelHumSnsrErr":
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',0)
            elif dtc_fault.name =="Switch_Right":
                self.bus_comm.resume_ecu_send('bodycan','SWTR')
                self.bus_comm.resume_ecu_send('bodycan','SWTL')
            elif dtc_fault.name =="Switch_Left":
                self.bus_comm.resume_ecu_send('bodycan','SWTR')
                self.bus_comm.resume_ecu_send('bodycan','SWTL')  
                 
            logger.info(f"--------->等待{last_time}")
            sleep(last_time)

    
    def set_dtc_precontion(self):
        prompt_info = f"---------->设置测试DTC前提条件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.bus_comm.set_vehspd_gear(vehspd=0.0)    
            self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
            self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
            sleep(.5)
            self.sd_tester.change_car_mode(CarMode.NORMAL)
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            sleep(5)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])#写normal电压
            sleep(1)


    def keep_lin_wake_up(self,channel,usage_mode=UsageMode.INACTIVE,speed=0,duration=20):
        self.set_usage_mode(usage_mode)
        self.bus_comm.set_vehspd(speed)
        #清除缓存
        self.bus_comm.clear_all_bus_buffer()
        res = ""
        start_time = time.time()
        while time.time() - start_time < duration:
            res = self.bus_comm.check_bus_recv_message(channel)  
            if res != True:
                logger.info(f"{channel} {time.time() - start_time - 5}S后进入了休眠")
                break   
        assert res,f"{channel},未收到报文"

    def lin_sleep(self,channel,usage_mode=UsageMode.INACTIVE,speed=0,duration=20):
        self.set_usage_mode(usage_mode)
        self.bus_comm.set_vehspd(speed)
        #清除缓存
        self.bus_comm.clear_all_bus_buffer()
        res = ""
        end_time = None
        start_time = time.time()
        while time.time() - start_time < duration:
            res = self.bus_comm.check_bus_recv_message(channel)
            if res == None:
                end_time = time.time() - start_time -5
                logger.info(f"{channel} {usage_mode} {end_time}S后进入了休眠")
                break

        bgm_mcu_version = self.sd_tester.read_bgm_mcu_version()
        if usage_mode == UsageMode.ABANDONED and speed == 0 and "130" in bgm_mcu_version:
            if res != None or end_time > 5.5:
                assert False,f"{channel} 车速小于7km/h 5.5s 未进入休眠"
        else:
            if res != None or end_time > 12.5:
                assert False,f"{channel} 车速小于7km/h 12.5s 未进入休眠"

    def pc_ping_BGM_and_vlan(self, count=10, err_count=3, condition="boot 下", dst_tar="tcam", ip='172.16.5.31',ping="get_ping"):
        '''

        @param count: 总共ping 几次
        @param err_count: 几次不通 报错
        @return:
        '''
        global test_count
        # todo 进入bgm ping tcam  10次
        err_count_index = 0
        for _ in range(count):
            # ret = self.bgm_ssh.get_ping(ip=ip, num=1)
            if ping == "get_arping":
                ret = self.ssh.get_arping(ip=ip,num=4)
            else:
                ret = self.ssh.get_ping(ip=ip, num=1)
            if not ret:
                logger.error(f"在{condition} bgm ping {dst_tar} 出现一次不通")
                err_count_index += 1

        with allure.step(
                f"第{test_count}轮 在{condition} bgm ping {dst_tar} {count}次，有{count - err_count_index}次可以ping通，{err_count_index}次ping不通"):
            pass

        return not err_count_index >= err_count

    def change_ip_and_id(self,ip,id,vlan):
        file_path = os.path.join(os.getcwd(),"mcu/config_data/vlan/switch_vlan5.sh")
        logger.info(f"============333333 {file_path}")
        li = []
        with open(file_path,"r") as file:
            file_content = file.readlines()
            for index,data in enumerate(file_content):
                old_ip = re.findall("ip addr add (.*?)/24",data)
                old_id = re.findall("hw ether (.*?);",data)
                if vlan == "eth0.5" and "eth0.5" in data:
                    file_content[index] = file_content[index].replace(old_ip[0],ip)
                    file_content[index] = file_content[index].replace(old_id[0],id)
                    li.append(file_content[index])

                elif vlan == "eth0.32" and "eth0.32" in data:
                    file_content[index] = file_content[index].replace(old_ip[0],ip)
                    file_content[index] = file_content[index].replace(old_id[0],id)
                    li.append(file_content[index])

                elif vlan == "eth0.9" and "eth0.9" in data:
                    file_content[index] = file_content[index].replace(old_ip[0],ip)
                    file_content[index] = file_content[index].replace(file_content[index][-17:],id)
                    li.append(file_content[index])
                else:
                    li.append(data)

        logger.info(f"888888 {li}")
        #将修改后的ip和id写入vlan文件中
        with open(file_path,"w") as new_file:
            for i in li:
                new_file.write(i)
        os.popen(f"chmod 777 {file_path}")
        #删除vlan原来的配置，并执行修改后的配置
        os.popen("cd ~")
        res1 = os.popen("ifconfig").read()
        if "eth0.32" in res1:
            os.popen(f"ip link delete eth0.32")
            for i in ["eth0.5","eth0.9","eth0.21","eth0.22"]:
                os.popen(f"ip link delete {i}")
        else:
            for i in ["eth0.5","eth0.9","eth0.21","eth0.22"]:
                os.popen(f"ip link delete {i}")
        subprocess.run(file_path,shell=True)
        res2 = os.popen("ifconfig").read()
        logger.info(f"ifconfig 执行结果999999 {res2}")
        if ip not in res2 and id not in res2:
            assert False,f"{vlan} {ip} {id} 未设置成功"

    def ping_bgm_ip_and_vlan_ip(self,bgm_ip,other_ip=None,ping="get_ping"):
        try:
            if other_ip != None:
                logger.info(f"开始执行arping {bgm_ip}")
                err_count = self.pc_ping_BGM_and_vlan(count=10,err_count=3,condition=f"修改ip为{bgm_ip}后",dst_tar="bgm",ip=bgm_ip)
                assert err_count,f"ping {bgm_ip} 失败次数超过3次"
                logger.info(f"开始执行arping {other_ip}")
                err_count = self.pc_ping_BGM_and_vlan(count=10,err_count=3,condition=f"修改ip为{other_ip}后",dst_tar="bgm",ip=other_ip)
                assert err_count,f"ping {other_ip} 失败次数超过3次"
            else:
                if ping == "get_arping":
                    logger.info(f"开始执行arping {bgm_ip}")
                    err_count = self.pc_ping_BGM_and_vlan(count=10,err_count=3,condition=f"修改ip为{bgm_ip}",dst_tar="bgm",ip=bgm_ip,ping="get_arping")
                    assert err_count,f"arping {other_ip} 失败次数超过3次"
                else:
                    logger.info(f"开始执行ping {bgm_ip}")
                    err_count = self.pc_ping_BGM_and_vlan(count=10,err_count=3,condition=f"修改ip为{bgm_ip}",dst_tar="bgm",ip=bgm_ip)
                    assert err_count,f"ping {other_ip} 失败次数超过3次"

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(f"失败>>>{str(e)}")
            assert 0, str(e)
    
    def set_PtActvnReq(self, up_type:UpType):
        '''
        触发PtActvnReq置位
        up_type:0 gear, 1 geatAuto, 2 gearCdc ,3 setusagemodeup = 13, 4 setusagemodewithoutkey = 2
        '''
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.check('infocanfd', 'BgmInfoCanFdDevFr02', 'FOTAStatus', 0)
        self.bus_comm.check('infocanfd', 'BgmInfoCanFdDevFr02', 'StartInhibitSts', 0)
        self.bus_comm.set('backbonefr', 'VddmBackBoneFr08', 'ImobEngSts1', 2)
        if up_type.value == 0:
            self.bus_comm.trigger_gear_by_manual()
            time.sleep(0.7)
        elif up_type.value == 1:
            self.bus_comm.trigger_gear_by_auto()
            time.sleep(0.7)
        elif up_type.value == 2:
            self.bus_comm.trigger_gear_by_cdc()
        elif up_type.value == 3:
            self.soa.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 13})
        elif up_type.value == 4:
            self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        time.sleep(0.3)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_StrtgInProgs)
        time.sleep(5)
        self.bus_comm.check('backbonefr', 'CemBackBoneFr25', 'PtActvnReq1WdPtActvnReq', 1)

    def filter_vehicle_announcement_fun(self, pack):
        '''
        回调函数，过滤 车辆公告
        @param pack: 以太报文包
        @return:
        '''
        # logger.info(pack, pack.time) filter_vehicle_announcement
        string = bytes(pack).hex()
        # "02fd0004000000205c2e0b5cd05dd775e8dcd8e2bbe10f6584100102000000101100000000000100"
        if len(string) == 164 and "02fd000400000020" in string:
            self.first_veh_ann_time = pack.time
            logger.info(f'第一帧车辆公告时间戳为={self.first_veh_ann_time}')
            self.sniffpack.sniff_flag = True

    def get_veh_ann_time_under_app_mode_send_func_1181(self,iface, max_time=30, do_assert=True):
        '''
        APPMode下_功能寻址_1181重启后车辆公告发出时长
         @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert: 是否会报错，默认报错
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X86])
        if recv_data_list[3] == 2:
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
            time.sleep(20)
        elif recv_data_list[3] == 3:
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        else:
            pass
        self.first_veh_ann_time = 0
        self.sniffpack = SniffPacket(iface=iface)
        self.sniffpack.set_callback(self.filter_vehicle_announcement_fun)
        self.sniffpack.start_sniff()
        time.sleep(2)
        self.sd_tester.update_serverdoipid(0x1fff)
        self.sd_tester.send_data([0x11, 0x81])
        t = time.time()
        logger.info(f"APPMode下,发送0x11, 0x81 的时间戳为{t}")
        while time.time() - t < 35:
            time.sleep(1)
            if self.first_veh_ann_time:
                break
        tem = self.first_veh_ann_time - t
        self.sniffpack.stop_sniff()
        #
        if do_assert:
            if tem > max_time:
                string = f"APPMode下_功能寻址_1181重启后车辆公告发出时长>>{tem}，超过{max_time}秒"
                with allure.step(string):
                    logger.error(string)
                    assert 0, string
        string = f"APPMode下_功能寻址_1181重启后车辆公告发出时长>>{tem}，不能超过{max_time}秒"
        with allure.step(string):
            logger.info(string)
        return tem

    def get_veh_ann_time_under_app_mode_send_func_1082(self,iface, max_time=15, do_assert=True):
        '''
        APPMode下_功能寻址_1082重启后车辆公告发出时长
        @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert: 是否会报错，默认报错
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X86])
        if recv_data_list[3] == 1:
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
            time.sleep(20)
        elif recv_data_list[3] == 3:
            self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        else:
            pass
        self.first_veh_ann_time = 0
        self.sniffpack = SniffPacket(iface=iface)
        self.sniffpack.set_callback(self.filter_vehicle_announcement_fun)
        self.sniffpack.start_sniff()
        time.sleep(2)
        self.sd_tester.update_serverdoipid(0x1fff)
        self.sd_tester.send_data([0x10, 0x82])
        t = time.time()
        logger.info(f"APPMode下 发送0x10, 0x82 的时间戳为{t}")
        while time.time() - t < 20:
            time.sleep(1)
            if self.first_veh_ann_time:
                break

        tem = self.first_veh_ann_time - t
        self.sniffpack.stop_sniff()
        # 退boot
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        #
        if do_assert:
            if tem > max_time:
                string = f"APPMode下_功能寻址_1082重启后车辆公告发出时长>>{tem}，超过{max_time}秒"
                with allure.step(string):
                    logger.error(string)
                    assert 0, string
        string = f"APPMode下_功能寻址_1082重启后车辆公告发出时长>>{tem}，不能超过{max_time}秒"
        with allure.step(string):
            logger.info(string)
        return tem

    def get_veh_ann_time_under_boot_mode_send_func_1181(self,iface, max_time=20, do_assert=True):
        '''
            BootMode下_功能寻址_1181重启后车辆公告发出时长
        @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert:
        @return:
        '''
        self.init_boot_per()
        self.sd_tester.update_serverdoipid(0x1002)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X86])
        if recv_data_list[3] != 2:
            # self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.enter_boot()

        self.first_veh_ann_time = 0
        self.sniffpack = SniffPacket(iface=iface)
        self.sniffpack.set_callback(self.filter_vehicle_announcement_fun)
        self.sniffpack.start_sniff()
        time.sleep(2)
        self.sd_tester.update_serverdoipid(0x1fff)
        self.sd_tester.send_data([0x11, 0x81])
        t = time.time()
        logger.info(f"BootMode下,发送0x11, 0x81 的时间戳为{t}")
        while time.time() - t < 35:
            time.sleep(1)
            if self.first_veh_ann_time:
                break
        tem = self.first_veh_ann_time - t
        self.sniffpack.stop_sniff()
        if do_assert:
            if tem > max_time:
                string = f"BootMode下_功能寻址_1181重启后车辆公告发出时长>>{tem}，超过{max_time}秒"
                with allure.step(string):
                    logger.error(string)
                    assert 0, string
        string = f"BootMode下_功能寻址_1181重启后车辆公告发出时长>>{tem}，不能超过{max_time}秒"
        with allure.step(string):
            logger.info(string)
        return tem
    
    def set_precon_to_abandon(self):
        self.bus_comm.set("bodycan", "CcmBodyFr34", "ClimaOvrHeatPrtSts", 0)
        self.bus_comm.set("connectivitycanfd", "BncmConnectivityFr17", "UsgModChgReqFromBLE", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr09", "HvEgyLoadFctReq", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr28", "HvOnMaiReq", 0)
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 0)
        self.bus_comm.set("bodycan", "LpodBodyFr01", "DoorLeReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq", 0)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 0)
        self.bus_comm.set("infocanfd", "CdcInfoCanFdFr03", "MmedHdPwrMod", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr00", "PtCoolgPostRunActv", 0)
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr12", "RemHvStrtActvReq", 0)
        self.bus_comm.set("propulsioncan", "EgsmPropFr01", "DrvrGearShiftParkReq1", 0)
        self.bus_comm.set("bodycan", "PpodBodyFr01", "DoorPassOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.NoPress)
        self.bus_comm.set("bodycan", "RpodBodyFr01", "DoorRiReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(RiRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "RrdmBodyFr01", "DoorRiReOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "RpodBodyFr01", "DoorRiReOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "RldmBodyFr01", "DoorLeReOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "LpodBodyFr01", "DoorLeReOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "PdmBodyFr01", "DoorPassOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "PpodBodyFr01", "DoorPassOpenReqInsdSwt2", 0)
        self.soa.send_method_request( 'LightService_client','SetExteriorLightMode',{"mode": 0})

    def set_fota_RemoteUpdate_condition(self, usagemode:UsageMode, lock_cmd:LockCmd):
        self.set_usage_mode(usagemode)
        logger.info(f"成功设置UsageMode为:{usagemode}")
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd, LockSource.HMI)
        time.sleep(5) # 等待中控锁状态的更新
        logger.info(f"成功设置Lock Status为:{lock_cmd}")
    
    def generate_fota_appointment_time(self, delay_seconds: int = 300):
        appiont_time = get_current_time_delayed_timestamp(delay_seconds = delay_seconds)
        logger.info(f"============== generates a delay {delay_seconds} time: {appiont_time} ==============")
        return appiont_time
    
    def return_when_reach_target_time(self, target_time: int, monitor_cycle: int = 1):
        while True:
            cur_time = datetime.datetime.now().timestamp()
            logger.info(f"current time is {cur_time}, target time is {target_time}, left time is {target_time- cur_time}")
            if cur_time > target_time:
                break
            else:
                time.sleep(monitor_cycle)
    
    def check_fota_keep_awake(self,
                              log_type=" fota:",
                              pnc29=None, 
                              acu_keep_alive=None,
                              up_inactive=None,
                              hv_active=None,
                              startInhibit=None,
                              ):
        keywords = []
        unexpect_keywords = []
        if pnc29 is not None:
            if pnc29:
                keywords.append('VfcType :23')
            else:
                unexpect_keywords.append('VfcType :23')
        if acu_keep_alive is not None:
            if acu_keep_alive:
                keywords.append('KeepAliveCb')
            else:
                unexpect_keywords.append('KeepAliveCb')
        if up_inactive is not None:
            if up_inactive:
                keywords.append('SetUsageModeUpAsyncCb')
            else:
                unexpect_keywords.append('SetUsageModeUpAsyncCb')
        if hv_active is not None:
            if hv_active:
                keywords.append('OnSetOutputCb Fail_Type:0')
            else:
                unexpect_keywords.append('OnSetOutputCb Fail_Type:0')
        if startInhibit is not None:
            if startInhibit:
                keywords.append('OnSetStartInhibitCb')
            else:
                unexpect_keywords.append('OnSetStartInhibitCb')
        with self.log_manage.check_jetlog_by_keywords(log_type=log_type, 
                                                      keywords=keywords if keywords else None, 
                                                      unexpect_keywords=unexpect_keywords if unexpect_keywords else None, 
                                                      timeout=10):
            pass
        return True 
            
    def set_enter_boot_condition(self, usagemode: UsageMode, low_volt_power: Union[int, float], vehspd: Union[int, float]):
        self.set_usage_mode(usagemode)
        logger.info(f"BGM MCU 进boot条件: 1.Usagemode 不等于 Driving; 当前成功设置当前Usagemode为 {usagemode}")
        pdu_data_map = {
            11.4: [0x85, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00],
            11.5: [0x85, 0x03, 0x82, 0x00, 0x00, 0x00, 0x00],
            14: [0x85, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
        }
        if low_volt_power in pdu_data_map:
            self.bus_comm.ipdu.send_pdu("cem_lin6", 0x06, pdu_data_map[low_volt_power])
            logger.info(f"BGM MCU 进boot条件: 2.小电池电压 大于 9V; 当前成功设置当前小电池电压为 {low_volt_power}")
        else:
            logger.error(f"不合法的低电压电量数值：{low_volt_power}，请在 [11.4, 11.5, 14] 中进行选择")
        logger.info(f"BGM MCU 进boot条件: 3.车速 等于 0; 当前成功设置当前车速为 {vehspd}")
        self.bus_comm.set_vehspd(vehspd)

    def wait_appoint_until_excut_time(self, task_time):
        # 在指定时间之前，等待至指定时间
        task_time = datetime.datetime.strptime(task_time.strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        while True:
            current_time = datetime.datetime.now()
            time_difference = (task_time - current_time).total_seconds()  - 15 * 60
            if time_difference <= 0:
                logger.info(f"已等待时间至{task_time}前15分钟, 开始检查各种请求")
                break
            else:
                time.sleep(time_difference)
    
    def wait_appoint_until_use_time(self, task_time):
        # 等待至用户上车后15min
        task_time = datetime.datetime.strptime(task_time.strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        while True:
            current_time = datetime.datetime.now()
            time_difference = (task_time - current_time).total_seconds() + 15 * 60
            if time_difference <= 0:
                logger.info(f"已等待时间至{task_time}后15分钟, 开始检查各种请求")
                break
            else:
                time.sleep(time_difference)
    
    def chk_rvc_cock_reserv_pnc(self):
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC26, NMSts.valid, timeout=20)
    
    def chk_rvc_cock_reserv_taskupload(self, task_time, message):
        logger.info("开始检查TCAM上报预约任务的上报协议是否正确")
        use_vehicle_time_match = re.search(r'useVehicleTime:(\d+)', message)
        use_vehicle_time_formatted = datetime.datetime.fromtimestamp(int(use_vehicle_time_match.group(1))).strftime("%H:%M")
        logger.info(f"检查到预约座舱用户上车时间为{use_vehicle_time_formatted}")
        assert task_time == use_vehicle_time_formatted
        # 定义要校验的字段列表
        fields_to_check = ['steering_wheel_heat:{level:SwhLevel1}', 'driver_seat_heat:{level:ShLevel1}', 'passenger_seat_heat:{level:ShLevel1}', 'battery_pack_heat:{op:BphOpen}']
        pattern = re.compile("ac_control:{op:AcOpen.*temp:230}")
        if pattern.search(message):
            for field in fields_to_check:
                if field not in message:
                    assert False, f"检查TCAM上报预约任务的上报协议错误字段为{field}" 
            logger.info("检查TCAM上报预约任务的上报协议结果为正确")
        else:
            assert False,f"检查TCAM上报预约任务的上报协议错误，缺少字段: ac_control"
    
    def chk_rvc_vent_reserv_taskupload(self, message, fields_to_check = ["ac_control", "rear_right_seat_vent", "rear_left_seat_vent", "driver_seat_vent", "passenger_seat_vent"],expected_msg: str = "Success", success=True):
        logger.info("开始检查上报座椅通风任务的预约执行结果是否正确")
        if not message:
            assert False, f"检查TCAM上报预约任务的上报协议错误，未找到关键词{expected_msg}"
        else:
            for cmd_code in fields_to_check:
                if success:
                    pattern = re.compile(f"cmdCode:{cmd_code}.*msg:\"{expected_msg}\"")
                else:
                    pattern = re.compile(f"cmdCode:{cmd_code}.*code:1.*msg:\"{expected_msg}\"")
                if not pattern.search(message[1]):
                    assert False,f"检查TCAM上报预约任务的上报协议错误，缺少字段: cmdCode:{cmd_code} msg:\"{expected_msg}\""
            logger.info("检查上报座椅通风任务的预约执行结果为正确")

    
    def chk_rvc_vent_reserv_threads(self, ids: List[str], timeout: int = 1800):
        logger.info("开始启动检查预约座椅通风关闭请求的线程")
        threads = []
        for id_value in ids:
            logger.info(f"通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求，id: {id_value}")
            args = ("SeatService_server", "SetVentingLevel",
                            {"params": [{"id": id_value, "uint8Info": 0}], "source": 2}, timeout)
            t = Thread(target=self.soa.ck_s2s_req, args=args)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        logger.info("所有预约座椅通风关闭请求的线程检查完成")

    def chk_rvc_threads(self, target: callable, args: List[Any]):
        logger.info("开始启动检查远控服务请求的线程")
        threads = []
        results = [] 
        for partner_key, interface_name, ck_info, timeout in args:
            def get_thread_result(partner_key, interface_name, ck_info, timeout):
                try:
                    result = target(partner_key, interface_name, ck_info, timeout)
                    results.append(result)    
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"线程执行时发生异常: {e}")
                    results.append(e)
            t = Thread(target=get_thread_result, args=(partner_key, interface_name, ck_info, timeout))
            t.start()
            threads.append(t)  
        for t in threads:
            t.join()
        assert "未获取到期望" not in str(results), f"存在{results}情况"
        logger.info(f"相关远控服务请求的线程检查结果为{results}")
    

    def check_convenience_mode_duration(self, duration=255, do_assert=True, **kwargs):
        '''
        @return: 返回 True 是驻车舒享设置与预期一致，False 是驻车舒享设置与预期不一致
        '''
        ck_info = {'out': duration}
        method_name = 'GetConvenienceModeDuration'
        ret = self.soa.send_request_and_ck_resp(
            'VehicleModeService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleModeService ck_info={ck_info}       ret={ret}")
        logger.info(F"当前为  {'驻车舒享设置与预期一致' if ret else '驻车舒享设置与预期不一致'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"
        if ret:
            self.bus_comm.check("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", duration)
            return True
        else:
            return False
    
    def set_keep_power_and_check_notify(self, flag:KeepPowerFlag):
        #flag: 0 open, 1 close_服务， 2 close_hvsoc , 3 close_gear, 4 close_carmode, 5 close_fota, 6 close_other
        if flag.value == 0:
            self.soa.send_method_request(
                'VehicleSetStatusService_client', "SetParkingComfortMode", {"modeSts": 1}
            )
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 255})
        elif flag.value == 1:
            self.soa.send_method_request(
                'VehicleSetStatusService_client', "SetParkingComfortMode", {"modeSts": 0}
            )
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 2:
            self.bus_comm.set_singal("propulsioncan", "EcmPropFr04", "DispHvBattLvlOfChrg", 19.0)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 3:
            self.bus_comm.set("propulsioncan", "EcmPropFr24", "GearLvrIndcn_1_EcmPropSignalIPdu24", 2)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 4:
            self.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 5:
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 6:
            self.soa.send_method_request('VehicleModeService_client','SetUsageModeDown', {"mode": 1},)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        else:
            logger.info(f"非预期的flag{flag}")
    
    def eth2can_send_response_recv_flow_frame(self, data_info_list, **kwargs):
        '''
        不发送请求，can 节点直接发送多帧响应，bgm 回复流控帧
        @param data_info_list: 
        @param kwargs: 
        @return: 
        '''
        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        send_length = 8
        error_list = []
        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            # time.sleep(1)
            send_channel = item_info.get("send_channel")
            recv_address = item_info.get("recv_address")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")
            send_response_msg = [0x10, 0x08, 1, 2, 3, 4, 5, 6]
            string = f"{recv_channel}发送响应数据长度{send_length}"
            logger.info(string)
            self.bus_comm.send_msg_by_id_func(recv_channel, response_id, send_response_msg)
            # 接收流控帧
            recv_flow_control_frame, time_stamp = self.bus_comm.recv_msg_by_id_func(recv_channel, request_id)
            if recv_flow_control_frame:
                first_byte = recv_flow_control_frame[0]
                if first_byte != 0x30:
                    log_string = f"{recv_channel}id={hex(response_id)}发送首帧后未收到流控帧或者流控帧收个字节不为0x30"
                    with allure.step(log_string):
                        logger.error(log_string)
                        error_list.append(log_string)
                    # assert 0, log_string
            else:
                log_string = f"{recv_channel}id={hex(response_id)}发送首帧后未收到流控帧"
                with allure.step(log_string):
                    logger.error(log_string)
                    # assert 0, log_string
                error_list.append(log_string)

        assert not len(error_list)

    def make_can_communicate_err(self,bus_name,send_node_name,make_fault_msg,make_fault_before_expect_res,make_fault_after_expect_res):
        """
        制造can 某个节点故障
        """
        self.bus_comm.pause_ecu_send(bus_name,send_node_name)
        time.sleep(5)
        self.sd_tester.send_data_and_check(0x1002,make_fault_msg,make_fault_before_expect_res,diagnostic_action="检查故障是否制造成功")
        self.bus_comm.resume_all_bus_send()
        time.sleep(5)
        self.sd_tester.send_data_and_check(0x1002,make_fault_msg,make_fault_after_expect_res,diagnostic_action="检查是否有存历史故障")

    def get_all_log_info_awakeup(self,time_to_sleep):
        sleep(time_to_sleep)
        self.bus_comm.resume_all_bus_send()
        global bgm_log_awakeup,awakeup_source
        if awakeup_source == "source_1":
            with allure.step(f"Step:执行网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源03")
                self.bus_comm.send_pdu("bodycan",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
        elif awakeup_source == "source_3":
            with allure.step(f"Step:执行唤醒源03唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源03")
                self.bus_comm.send_pdu("bodycan",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
        elif awakeup_source == "source_4":
            with allure.step(f"Step:执行唤醒源04唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源04")
                self.bus_comm.send_pdu("bodyexposedcanfd",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
        elif awakeup_source == "source_5":
            with allure.step(f"Step:执行唤醒源05唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源05")
                self.bus_comm.send_pdu("connectivitycanfd",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
        elif awakeup_source == "source_6":
            with allure.step(f"Step:执行唤醒源06唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源06")
                self.bus_comm.send_pdu("passivesafetycan",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
        elif awakeup_source == "source_7":
            with allure.step(f"Step:执行唤醒源07唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源07")
                self.bus_comm.send_pdu("propulsioncan",0x500, "00 40 00 00 00 01 00 00")
                sleep(10)
                
                
    def check_lin_wakeup_time(self,bus_name:str,msg_name:str,signal:str,value:any,timeout=12):
        self.bus_comm.check_signal_thread_start(bus_name,msg_name, signal, timeout)
        logger.info(f"检测通道唤醒 {msg_name} {signal}: 发送 发送3S之后休眠")
        result_ori_1 = self.bus_comm.check_signal_thread_stop(signal,2*timeout)
        logger.info(f"result_original_1({signal}):{result_ori_1}")
        if result_ori_1 == None:
            assert False
        else:
            if check_all_value_is(result_ori_1, value):
                result_1 = calculate_signal_times_and_duration(result_ori_1)
                frame_times = result_1[0]
                duration_time = result_1[1]
                logger.info(f"{msg_name}{signal}=1持续发送{frame_times}帧，持续时间为{duration_time}s")
                if abs(duration_time-timeout)<=0.5:
                    assert True
                else:
                    logger.info("帧发送时间误差大于500ms")
                    assert False
            else:
                logger.info(f"不是所有的{signal}值为1")
                assert False

                
    def get_request_and_send_response_to_tcam(self, check_req_list: list):
        error_function = []
        # 0 构建自己的服务和方法字典
        soa_func_dict = {k:[] for k in check_req_list}
            
        while True:
            if self.get_request_and_send_response_to_tcam_flag:
                logger.info('stop !!!')
                break
            # 1. 查找收到的新的请求
            for server_name, func_list in soa_func_dict.items():
                rcv_req_list = self.soa.soa_partner.partner_infos[server_name].req_queue.queue
                new_func_list = []
                if len(rcv_req_list) == 0:
                    # 代表req_list被调用清空了
                    soa_func_dict[server_name] = []
                    continue
                elif len(rcv_req_list) == len(func_list):
                    # 代表没有收到新的func请求
                    continue
                elif len(rcv_req_list) < len(func_list):
                    # 代表req_list被调用清空了，且收到了新的func请求
                    new_func_list = rcv_req_list.copy()
                    soa_func_dict[server_name] = rcv_req_list.copy()
                elif len(rcv_req_list) > len(func_list):
                    # 代表收到了新的func请求
                    num = len(rcv_req_list) - len(func_list)
                    new_func_list = rcv_req_list[-num:]  # 截取新的function_list
                    soa_func_dict[server_name] = rcv_req_list.copy()
                    
                # 2. 根据收到新的请求进行响应
                logger.info("Get new requests from TCAM: {0}".format(new_func_list))
                for req in new_func_list:
                    # 处理请求名。可能需要拼接server-name
                    server_function_name = "_".join(server_name.split('_')[:-1]) + f"_{req['function']}"
                    if server_function_name in error_function:
                        # 如果已经发现不存在该方法，则直接跳过
                        continue

                    if req['function'] in self.ignore_func or server_function_name in self.ignore_func: 
                        # 若存在待忽略的方法，则自动忽略
                        continue
                    
                    if hasattr(self.soa, f"response_to_{req['function']}_req"):
                        # 判断是function存在与否
                        func = getattr(self.soa, f"response_to_{req['function']}_req")
                            
                    elif hasattr(self.soa, f"response_to_{server_function_name}_req"):
                        # 判断server_function是否存在
                        func = getattr(self.soa, f"response_to_{server_function_name}_req")
                    else:
                        # function未定义
                        logger.warning(f'soa类中存在未定义的function "response_to_{req["function"]}_req" or "response_to_{server_function_name}_req"')
                        error_function.append(server_function_name)
                        continue
                    
                    if req['function'] in self.func_param or server_function_name in self.func_param:
                        # 判断是否存在默认参数传递
                        try:
                            func(**self.func_param[req['function']])
                        except TypeError:
                            logger.warning(f'{func.__name__}方法提供的参数有误!')
                            # raise TypeError(f'{func.__name__}方法提供的参数有误!')
                    else:
                        try:
                            func()
                        except Exception:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                            logger.warning(f'{func.__name__} 方法没有设定默认值！')
                time.sleep(0.1)
            time.sleep(0.1)

    def start_get_request_and_send_response_to_tcam_thread(self, check_req_list: list, func_param: dict= {}, ignore_func: list = []):
        self.get_request_and_send_response_to_tcam_flag = False
        self.func_param = func_param
        self.ignore_func = ignore_func
        self.get_request_tcam_thread = Thread(target=self.get_request_and_send_response_to_tcam, args=(check_req_list,))
        self.get_request_tcam_thread.start()

    
    def stop_get_request_and_send_response_to_tcam_thread(self):
        self.get_request_and_send_response_to_tcam_flag=True
        self.get_request_tcam_thread.join()
        self.func_param = {}
        self.ignore_func = []

    def set_func_param(self, func_param:dict):
        self.func_param.update(func_param)
        logger.info(f'更新后的func_param: {self.func_param}')


    def default_func_param(self,func_names:list):
        for func_name in func_names:
            if func_name in self.func_param:
                self.func_param.pop(func_name)

    
    def make_can_communicate_err(self,bus_name,send_node_name,make_fault_msg,make_fault_before_expect_res,make_fault_after_expect_res):
        """
        制造can 某个节点故障
        """
        self.bus_comm.pause_ecu_send(bus_name,send_node_name)
        time.sleep(5)
        self.sd_tester.send_data_and_check(0x1002,make_fault_msg,make_fault_before_expect_res,diagnostic_action="检查故障是否制造成功")
        self.bus_comm.resume_all_bus_send()
        time.sleep(5)
        self.sd_tester.send_data_and_check(0x1002,make_fault_msg,make_fault_after_expect_res,diagnostic_action="检查是否有存历史故障")
        
    def filter_switch_port_fun(self, packet):
        '''
        回调函数，过滤 switch_port
        测试工具发送 start test 请求（31 01 DC05），SOC 收到请求后，以周期 1s 发送广播 UDP 消息（255.255.255.255， port: 7000）with payload
            0102030405060708090A
        @param pack: 以太报文包
        @return:
        '''
        # logger.info(pack, pack.time) filter_vehicle_announcement
        string = bytes(packet).hex()
        # "ffffffffffff0200000010010800450000264a104000401133b8a9fe1301ffffffffb8721b58001255e20102030405060708090a0000000000000000"
        dst_ip_hex = string[60:68]
        dst_port_hex = string[72:76]
        data_hex = string[84:104]
        if dst_ip_hex == 'ffffffff' and dst_port_hex == '1b58' and data_hex == '0102030405060708090a':
            self.switch_port_msg_list.append(packet.time)
            logger.info(f'{packet.time},{time.time()}获取的报文为={string}')

    def bgm_soc_switch_port(self, iface='any', do_assert=True, ):
        '''
        测试工具发送 start test 请求（31 01 DC05），SOC 收到请求后，以周期 1s 发送广播 UDP 消息（255.255.255.255， port: 7000）with payload
        0102030405060708090A
        测试工具监控 5s(TBD)内所有 ports 是否收到了广播消息并 check payload
        收到后，测试工具发送 stop test 请求（31 02 DC05），SOC 收到请求后，停止发送 UDP 消息
        @param do_assert:
        @return:
        '''
        # 获取 bgm 内部的 ip
        ret_msg = self.ssh.type_commands(DeviceName.BGM, "ifconfig")
        ip_list = re.findall('inet (.*?)  netmask', ret_msg)
        logger.info(f"获取bgm 内部的ip={ip_list}")
        if '127.0.0.1' in ip_list:
            ip_list.remove('127.0.0.1')
        # ip_list = ['172.16.5.1', '172.16.11.1', '172.16.32.1', '172.16.9.1', '172.16.19.1']
        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.ssh.start_bgm_tcpdump(iface="eth0")
        self.switch_port_msg_list = []
        self.sniffpack = SniffPacket(iface=iface)
        self.sniffpack.set_callback(self.filter_switch_port_fun)
        self.sniffpack.start_sniff()

        self.sd_tester.update_serverdoipid(0x1001)
        send_data = [0x31, 0x01, 0xDC, 0x05]
        expect_recv = [0x71, 0x01, 0xDC, 0x05, 0x10]
        start_time = time.time()
        self.sd_tester.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)
        #
        time.sleep(5)
        # 停止bgm 内部抓包
        self.ssh.stop_bgm_tcpdump()
        # 停止抓包obd 口
        self.sniffpack.stop_sniff()
        # 把 bgm 的日志 拉取到本地，并删除bgm内部的 pcap 包
        pacp_file_path = self.ssh.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)
        read_data = rdpcap(pacp_file_path)
        logger.info("开始解析文件，会耗时一段时间。。。。。")
        data_dict = {}
        for packet_index in range(len(read_data)):
            packet = read_data[packet_index]
            line = bytes(packet).hex()
            packet_time = float(packet.time)
            src_ip_hex = line[60:68]
            dst_ip_hex = line[68:76]
            dst_port_hex = line[80:84]
            data_hex = line[92:112]
            if dst_ip_hex == 'ffffffff' and dst_port_hex == '1b58' and data_hex == '0102030405060708090a':
                logger.info(f"data={line}")
                if src_ip_hex in data_dict:
                    data_dict[src_ip_hex].append(packet_time)
                else:
                    data_dict[src_ip_hex] = [packet_time]

        logger.info(f"data_dict={data_dict}")
        assert len(data_dict), 'bgm 内部未抓到 UDP 消息 with payload0102030405060708090A'

        # 校验 内部抓包发出数据
        for ip in ip_list:
            ip_hex = bytes([int(item) for item in ip.split('.')]).hex().lower()
            data_list = data_dict.get(ip_hex)
            string = f'bgm 内部抓到{ip} UDP 消息 {data_list}'
            logger.info(string)
            assert data_list, string
            # 判断第一帧 在5秒内
            first_frame = data_list[0]
            temp = first_frame - start_time
            string = f'bgm 内部抓到{ip} 第一帧UDP 消息 在{temp}秒内发出,应该在5秒发出'
            logger.info(string)
            assert temp < 5, string
            for indx in range(1, len(data_list)):
                t1 = data_list[indx - 1]
                t2 = data_list[indx]
                temp = t2 - t1
                assert abs(temp - 1) < 0.2, f"udp 周期大于1，实际为{temp}秒"

        # 检查周期
        assert len(
            self.switch_port_msg_list), '未收到发送广播 UDP 消息 with payload0102030405060708090A'
        logger.info(f"self.switch_port_msg_list={self.switch_port_msg_list}")
        for indx in range(1, len(self.switch_port_msg_list)):
            t1 = self.switch_port_msg_list[indx - 1]
            t2 = self.switch_port_msg_list[indx]
            temp = t2 - t1
            assert abs(temp - 1) < 0.2, f"udp 周期大于1，实际为{temp}秒"

        # 收到后，测试工具发送 stop test 请求（31 02 DC05），SOC 收到请求后，停止发送 UDP 消息
        send_data = [0x31, 0x02, 0xDC, 0x05]
        expect_recv = [0x71, 0x02, 0xDC, 0x05, 0x10]
        self.sd_tester.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)
        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.ssh.start_bgm_tcpdump(iface="eth0")

        self.switch_port_msg_list = []
        self.sniffpack = SniffPacket(iface=iface)
        self.sniffpack.set_callback(self.filter_switch_port_fun)
        self.sniffpack.start_sniff()
        time.sleep(5)
        # # 停止
        self.sniffpack.stop_sniff()
        # 停止bgm 内部抓包
        self.ssh.stop_bgm_tcpdump()
        assert not len(self.switch_port_msg_list), "不应该收到udp 报文的实际收到"

        # 把 bgm 的日志 拉取到本地，并删除bgm内部的 pcap 包
        pacp_file_path = self.ssh.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)
        read_data = rdpcap(pacp_file_path)
        logger.info("开始解析文件，会耗时一段时间。。。。。")
        data_dict = {}
        for packet_index in range(len(read_data)):
            packet = read_data[packet_index]
            line = bytes(packet).hex()
            packet_time = float(packet.time)
            src_ip_hex = line[60:68]
            dst_ip_hex = line[68:76]
            dst_port_hex = line[80:84]
            data_hex = line[92:112]
            if dst_ip_hex == 'ffffffff' and dst_port_hex == '1b58' and data_hex == '0102030405060708090a':
                if src_ip_hex in data_dict:
                    data_dict[src_ip_hex].append(packet_time)
                else:
                    data_dict[src_ip_hex] = [packet_time]
        assert not len(data_dict), 'bgm 内部抓到 UDP 消息 with payload0102030405060708090A 本不应抓到'

    def bgm_soc_check_mcu_mpu_comm_link_status(self, do_assert=True):
        '''
        如果收到 OK, 说明测试通过
        SOC 监控 MCU 发送的周期心跳请求，如果 1s 收不到就认为 link 有问题
        BGMIntEthPDU20020 MCU->SOC Cyclic-100ms 20020 1 HeartbeatMonitorUp
        BGMIntEthPDU20021 SOC->MCU Cyclic-100ms 20021 1 HeartbeatMonitorDown
        @param do_assert:
        @return:
        '''
        send_data = [0x22, 0xDA, 0x01]
        expect_recv = [0x62, 0xDA, 0x01, 0x00]
        start_time = time.time()
        self.sd_tester.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)
        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.ssh.start_bgm_tcpdump(iface="eth0")
        time.sleep(5)
        # 停止bgm 内部抓包
        self.ssh.stop_bgm_tcpdump()
        # 把 bgm 的日志 拉取到本地，并删除bgm内部的 pcap 包
        pacp_file_path = self.ssh.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)
        read_data = rdpcap(pacp_file_path)
        logger.info("开始解析文件，会耗时一段时间。。。。。")
        #
        mpu2mcu_lis = []
        mcu2mpu_lis = []
        data_dict = {'4e28': [],
                     "4e34": []}
        for packet_index in range(len(read_data)):
            packet = read_data[packet_index]
            string = bytes(packet).hex()
            packet_time = float(packet.time)

            src_ip_hex = string[60:68]
            dst_ip_hex = string[68:76]
            src_port_hex = string[76:80]
            dst_port_hex = string[80:84]
            data_hex = string[144:148]

            if (dst_ip_hex == 'ac100502' and src_ip_hex == 'ac100501' and
                    dst_port_hex == '7724' and src_port_hex == '7728' and
                    data_hex == '4e28'):
                logger.info(f"mpu2mcu={string}")
                mpu2mcu_lis.append(packet_time)
            elif (dst_ip_hex == 'ac100501' and src_ip_hex == 'ac100502' and
                  dst_port_hex == '7729' and src_port_hex == '7725' and
                  data_hex == '4e34'):
                logger.info(f"mcu2mpu={string}")
                mcu2mpu_lis.append(packet_time)
            else:
                pass
        logger.info(f"mpu2mcu_lis=={mpu2mcu_lis}")
        logger.info(f"mcu2mpu_lis=={mcu2mpu_lis}")
        assert mpu2mcu_lis, "未抓到mpu2mcu的心跳"

        assert mcu2mpu_lis, "未抓到 mcu2mpu 的心跳"


        for indx in range(1, len(mpu2mcu_lis)):
            t1 = mpu2mcu_lis[indx - 1]
            t2 = mpu2mcu_lis[indx]
            temp = t2 - t1
            logger.info(f"MCU 监控 SOC 发送的周期心跳请求，周期为{temp}秒")
            assert temp < 1, f"MCU 监控 SOC 发送的周期心跳请求，{temp}秒未收到"

        for indx in range(1, len(mcu2mpu_lis)):
            t1 = mcu2mpu_lis[indx - 1]
            t2 = mcu2mpu_lis[indx]
            temp = t2 - t1
            logger.info(f"SOC 监控 MCU 发送的周期心跳请求，周期为{temp}秒")
            assert temp < 1, f"SOC 监控 MCU 发送的周期心跳请求，{temp}秒未收到"
    
    def check_exhibition_mode(self, status: bool):
        '''
        status 为 True 校验 当前模式是展车模式，
        status 为 False 校验 当前模式非展车模式，
        '''
        method_name = 'GetExhibitionModeSts'
        if status:
            ck_info = {'out': {'isOpen': True, 'isValid': True}}
        else:
            ck_info = {'out': {'isOpen': False, 'isValid': True}}
        ret = self.soa.send_request_and_ck_resp(
            'VehicleModeService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleModeService ck_info={ck_info}       ret={ret}")
        if status:
            logger.info(F"当前为  {'展车模式，与预期一致' if ret else '非展车模式，与预期不一致'}")
        else:
            logger.info(F"当前为  {'展车模式，预期不一致' if not ret else '非展车模式， 与预期一致'}")
    
    def set_and_check_exhibition_mode(self, status: bool):
        self.bus_comm.set_epb_sts(sts=3)
        self.soa.set_exhibition_mode(is_open=status)
        self.check_exhibition_mode(status=status)
    
    def set_tcam_bgm_to_wakeup(self):
        self.io.bgm_diag_line_up()
        sleep(5)
        self.io.tcam_kl15_up()
        sleep(10)
    
    def chk_tcam_reboot_or_not(self, time:int=15):
        """
        检查time周期内tcam是否重启,默认检查15min,time单位是1min
        """
        for i in range(time):
            result = self.chk_tcam_ping()
            if len(result) != 0:
                logger.info(f"第{i}次检查时TCAMping不通，出现重启")
                assert False
            else:
                logger.info(f"第{i}次检查tcam未重启, 继续等待60s")
                sleep(60)
    
    def network_wakeup(self, wakeup_reason: Wakeup_Reasons = Wakeup_Reasons.NO_WAKEUP, **kwargs):
        # 连接诊断激活线
        mn_msg = kwargs.get("mn_msg", True)
        if wakeup_reason.name == "WAKEUP_BY_BODYCAN":
            if mn_msg:
                with allure.step(f"Step:执行bodycan网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：bodycan 502 02 40 00 80 00 00 00 00 唤醒源03")
                    self.bus_comm.send_awakeup_msg("bodycan", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                # 应用报文
                can_name="bodycan"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)

        elif wakeup_reason.name == "WAKEUP_BY_PROPULSIONCAN":
            if mn_msg:
                with allure.step(f"Step:执行propulsioncan网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：propulsioncan CANFD 526 26 40 00 80 00 00 00 00 唤醒源07")
                    self.bus_comm.send_awakeup_msg("propulsioncan", 0x526, "26 40 00 00 00 01 00 00", 20, 20)
            else:
                can_name = "propulsioncan"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_CLASSICCAN1":
            with allure.step(f"Step:执行网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：chassiscan1 CANFD 529 29 40 00 80 00 00 00 00 唤醒源08")
                self.bus_comm.send_awakeup_msg("chassiscan1",0x529, "29 40 00 00 00 01 00 00",20,20)
        elif wakeup_reason.name == "WAKEUP_BY_CLASSICCAN2":
            with allure.step(f"Step:执行网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：chassiscan2 CANFD 522 22 40 00 80 00 00 00 00 唤醒源09")
                self.bus_comm.send_awakeup_msg("chassiscan2",0x522, "22 40 00 00 00 01 00 00",20,20)

        elif wakeup_reason.name == "WAKEUP_BY_PASSIVESAFETYCAN":
            with allure.step(f"Step:执行网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：passivesafetycan CANFD 50B 0B 40 00 80 00 00 00 00 唤醒源06")
                self.bus_comm.send_awakeup_msg("passivesafetycan",0x50B, "0B 40 00 00 00 01 00 00",20,20)

        elif wakeup_reason.name == "WAKEUP_BY_DIAGCAN":
            with allure.step(f"Step:执行diagnosticcan网络NM帧唤醒BGM"):
                self.bus_comm.ipdu.add_msg("diagnosticcan", 0x502,
                                           [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                logger.info("仿真网络管理报文唤醒如：diagnosticcan CANFD 502 02 40 00 80 00 00 00 00 唤醒源11")
                self.bus_comm.send_awakeup_msg("diagnosticcan", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_INFOCAN":
            if mn_msg:
                with allure.step(f"Step:执行infocanfd网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：infocanfd CANFD 502 02 40 00 80 00 00 00 00 唤醒源10")
                    self.bus_comm.send_awakeup_msg("infocanfd", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                can_name = "infocanfd"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_BODYEXPCANCANFD":
            if mn_msg:
                with allure.step(f"Step:执行bodyexposedcanfd网络NM帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg("bodyexposedcanfd", 0x502,
                                               [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info("仿真网络管理报文唤醒如：Body Exposed CANFD 0x502 31 40 00 80 00 00 00 00 唤醒源04")
                    self.bus_comm.send_awakeup_msg("bodyexposedcanfd", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                # 应用报文
                can_name = "bodyexposedcanfd"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_ADCAN":
            if mn_msg:
                with allure.step(f"Step:执行adcanfd 网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：adcanfd CANFD 502 02 40 00 80 00 00 00 00 唤醒源12")
                    self.bus_comm.send_awakeup_msg("adcanfd", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                # 应用报文
                can_name = "adcanfd"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_CONNCANFD":
            if mn_msg:
                with allure.step(f"Step:执行connectivitycanfd网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：connectivitycanfd CANFD 502 09 40 00 80 00 00 00 00 唤醒源05")
                    self.bus_comm.ipdu.add_msg("connectivitycanfd", 0x502,
                                               [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    self.bus_comm.send_awakeup_msg("connectivitycanfd", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                can_name = "connectivitycanfd"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_ALM1":
            if mn_msg:
                with allure.step(f"Step:执行 bodyalmcanfd1 网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：bodyalmcanfd1  502 02 40 00 80 00 00 00 00 唤醒源13")
                    self.bus_comm.send_awakeup_msg("bodyalmcanfd1", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                # 应用报文
                # self.send_app_msg("bodyalmcanfd1")
                can_name = "bodyalmcanfd1"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)

        elif wakeup_reason.name == "WAKEUP_BY_ALM2":
            if mn_msg:
                with allure.step(f"Step:执行 bodyalmcanfd2 网络NM帧唤醒BGM"):
                    logger.info("仿真网络管理报文唤醒如：bodyalmcanfd2  502 02 40 00 80 00 00 00 00 唤醒源14")
                    self.bus_comm.send_awakeup_msg("bodyalmcanfd2", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
            else:
                # 应用报文
                can_name = "bodyalmcanfd2"
                with allure.step(f"Step:执行 {can_name} 节点 应用帧唤醒BGM"):
                    self.bus_comm.ipdu.add_msg(can_name, 0x1, [0x02, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
                    logger.info(f"仿真应用报文唤醒如：{can_name} id=0x1 唤醒源0")
                    self.bus_comm.send_awakeup_msg(can_name, 0x100, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_FLEXRAY":
            with allure.step(f"Step:执行 backbonefr 网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：backbonefr  502 02 40 00 80 00 00 00 00 唤醒源15")
                self.bus_comm.send_awakeup_msg("backbonefr", 0x502, "02 40 00 00 00 01 00 00", 20, 20)
        elif wakeup_reason.name == "WAKEUP_BY_LIN1":
            with allure.step(f"Step:仿真Lin1从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin1从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN1)
        elif wakeup_reason.name == "WAKEUP_BY_LIN2":
            with allure.step(f"Step:仿真Lin2从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin2从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        elif wakeup_reason.name == "WAKEUP_BY_LIN3":
            with allure.step(f"Step:仿真Lin3从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin3从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN3)
        elif wakeup_reason.name == "WAKEUP_BY_LIN4":
            with allure.step(f"Step:仿真Lin4从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin4从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN4)
        elif wakeup_reason.name == "WAKEUP_BY_LIN5":
            with allure.step(f"Step:仿真Lin5从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin5从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN5)
        elif wakeup_reason.name == "WAKEUP_BY_LIN6":
            with allure.step(f"Step:仿真Lin6从节点唤醒发送PM波1000us"):
                logger.info(f"仿真Lin6从节点唤醒发送PM波1000us 唤醒源{wakeup_reason.value}")
                self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN6)
        # ####   硬线唤醒
        elif wakeup_reason.name == "WAKEUP_BY_ACTIVATION_LINE":
            with allure.step(f"Step:诊断激活线唤醒"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                self.io.bgm_diag_line_up()
                # self.io.bgm_diag_line_down()
        elif wakeup_reason.name == "WAKEUP_BY_HAZARD":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"打开危险报警灯 唤醒源{wakeup_reason.value}")
                self.io.hazard_light_open()
        elif wakeup_reason.name == "WAKEUP_BY_CHARGELID":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"打开充电口盖 唤醒源{wakeup_reason.value}")
                self.io.io.charge_lid_open()
        elif wakeup_reason.name == "WAKEUP_BY_BRAKE":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                self.io.io.brake_down()
        elif wakeup_reason.name == "WAKEUP_BY_HOOD1":
            with allure.step(f"Step:执行网络NM帧唤醒BGM"):
                logger.info("仿真网络管理报文唤醒如：开副驾们 唤醒源23")
                self.io.set_hood_sts(HoodSts.Open)
                sleep(1)
                self.io.set_hood_sts(HoodSts.Close)
        elif wakeup_reason.name == "WAKEUP_BY_HOOD2":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                # self.io.set_hood_sts(HoodSts.Open)
                # self.io.set_hood_sts(HoodSts.Close)
                self.io.io.hood_door2_close()

        elif wakeup_reason.name == "WAKEUP_BY_FLDOOR_SW":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                self.io.io.drvr_door_outswitch_pressed()
                sleep(1)
                # self.io.set_door(Drvr=Door.open)
                # self.io.set_door(Drvr=Door.close)
        elif wakeup_reason.name == "WAKEUP_BY_FLDOOR_LOCK_SW":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                self.io.io.drvr_door_open()
                sleep(1)

        elif wakeup_reason.name == "WAKEUP_BY_FRDOOR_SW":
            with allure.step(f"Step:{wakeup_reason.name}"):
                logger.info(f"{wakeup_reason.name} 唤醒源{wakeup_reason.value}")
                self.io.set_door(Pass=Door.open)
                self.io.set_door(Pass=Door.close)
        else:
            assert 0, f"不存在当前唤醒源{wakeup_reason}"
        sleep(0.5)
        logger.info(f'连接诊断激活线')
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        sleep(35)  # 等待日志打印完整，否则日志获取不全
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        # self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        self.set_usage_mode(UsageMode.INACTIVE)

    
       
    def check_keywords_in_version_collect_results(self, taskid=None, expect_keywords=None, unexpect_keywords=None):
        self.back_fota_to(FOTAMasteSts.NEW_TASK, taskid)
        # json_log = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /update/version.json")
        # ecu_info = eval(json_log)["data"]["ecu"]
        jet_log = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /log/jetlog_messages |grep ' fota:' | tail -n 2000")
        result = re.findall(r'version json string: (.*?)\n', jet_log, re.S)[-1]
        ecu_info = eval(result)["data"]["ecu"]
        logger.info(f"版本收集结果为：{ecu_info}")
        if expect_keywords:
            for ck in expect_keywords:
                if f"'{str(ck)}'" not in str(ecu_info):
                    assert False, f"'{ck}'未出现在版本收集结果中"
        if unexpect_keywords:
            for ck in unexpect_keywords:
                if f"'{str(ck)}'" in str(ecu_info):
                    assert False, f"'{ck}'出现在版本收集结果中"

    def check_factory_F154_results(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='factory_exit_ota => factory_ota_finish', timeout=2000):
            pass
        jet_log = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /log/jetlog_messages |grep ' fota:' | tail -n 2000")
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_data([0x22, 0xF1, 0X54])
        payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        logger.info(f"诊断F154返回结果为：{payload}")
        if self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_SUCCESSFUL.value:
            assert int(payload[3]) == 1
        elif self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_FAILED.value:
            assert int(payload[3]) == 2
        result = re.findall(r"SaveUpgradeResult:status:\d* , code:\d*\n(.*?)\d+-\d+-\d+ \d+:\d+:\d+.\d+ \d+ \d+ I fota: \d+: \[fota_assist_service.cpp:\d*]SaveUpgradeResult:F154::", jet_log, re.S)[-1]
        ecuInfo = re.findall(r"getErrorEcuInfo:name:.*? , err code:(\d+) , ecuId: (\d+)\n", result, re.S)
        logger.info(f"jetlog中正则匹配到的ecuInfo为：{ecuInfo}")
        checklist = []
        for errCode, ecuId in ecuInfo:
            if ecuId in ['1011', '6011', '3011', '2011']:
                continue
            checklist.clear()
            checklist.append(int(ecuId[:2], 16))
            checklist.append(int(ecuId[2:], 16))
            if int(errCode) == 4096:
                checklist.extend([16, 0])
            else:
                checklist.extend([0, int(errCode)])
            assert any((checklist == payload[i:i + len(checklist)]) for i in range(len(payload) - len(checklist) + 1)), f'ecuId：{ecuId}校验失败'

    def check_remote_diag_results(self, remote_diag_res:CheckRemoteDiagRes):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=':UploadRemoteDiagResult:', timeout=600):
            pass
        sleep(5)
        with open("config/remote_diag_lua.yaml", encoding="utf-8") as fn:
            yaml_content = yaml.safe_load(fn)
        check_list = yaml_content[remote_diag_res.value]
        jet_log = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /log/jetlog_messages |grep ' LUA_' | tail -n 200")
        dict_keys = [f"{addr}_{cmd}" for addr, cmd_l in check_list.items() for cmd in cmd_l]
        ck_dic = dict.fromkeys(dict_keys, False)
        result = re.findall(r':UploadRemoteDiagResult:(.*?)\n', jet_log, re.S)[-1]
        logger.info(result)
        for addr, cmd_list in check_list.items():
            for cmd in cmd_list:
                res = result.replace('\\', '').replace('"{', '{').replace('}"', '}')
                res_list = json.loads(res)['para']['data']
                for data in res_list:
                    li = [str(hex(i)[2:].zfill(2)) for i in data["cmd"]]
                    cmd_str = ''.join(li)
                    if cmd.lower() == "3e80":
                        if data['addr'] == int(addr, 16) and cmd_str == cmd.lower():
                            ck_dic[f"{addr}_{cmd}"] = True
                            logger.info(f"addr：{int(addr, 16)}，rsp_addr：{data['addr']}，cmd：{cmd.lower()}，rsp_cmd：{cmd_str}，rsp：{data['rsp']}")
                    else:
                        if data['addr'] == int(addr, 16) and cmd_str == cmd.lower() and data['rsp']:
                            ck_dic[f"{addr}_{cmd}"] = True
                            logger.info(f"addr：{int(addr, 16)}，rsp_addr：{data['addr']}，cmd：{cmd.lower()}，rsp_cmd：{cmd_str}，rsp：{data['rsp']}")
        logger.info(ck_dic)
        for check_key, check_result in ck_dic.items():
            ecu_id, diag_cmd = check_key.split('_')
            assert check_result, f'ecu_id：{ecu_id}，远程诊断指令：{diag_cmd}，结果校验失败'

    def get_bus_send_recv_info(self, ipdu, channel_name: str, **kwargs):
        '''
         根据通道获取当前通道的，发送节点和接收节点的数据
         @param ipdu:  对象 self.ipdu
         @param channel_name: 通道   bodycan 等等
         @param kwargs:
         @return: {}
        {
             "发送节点": {
                 "周期发送": {
                     "BGM": [ {"msg_name": msg_name,
                             "msg_id": msg_id,
                             "msg_type": msg_type,
                             "msg_tx_method": msg_tx_method,
                             "msg_cycle": msg_cycle,
                             "msg_length": msg_length,
                             "rx_nodes": rx_nodes,
                             "tx_node": tx_node,
                             "msg_base_cycle": msg_base_cycle,
                             "msg_repetition": msg_repetition}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },
             "接收节点": {
                 "周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },

         }
        '''

        channel_name = channel_name.strip().replace(" ", '').lower()
        # 先判断是不是解析过了，如果已经解析过，直接从缓存里取
        # if channel_name in self.__all_bus_data_info:
        #     return self.__all_bus_data_info[channel_name]
        bus_obj = getattr(ipdu, channel_name)
        msg_obj_lis = [i for i in dir(bus_obj) if not i.startswith("_")]
        # 存放所有 接收节点
        rx_nodes_dict = {}
        # 存放所有发送节点
        tx_nodes_dict = {}
        for name in msg_obj_lis:
            # obj = eval(f"{ipdu}.{channel_name}.{name}")
            if name =="lin_scheduleTable":
                continue
            obj = getattr(bus_obj, name)
            msg_name = getattr(obj, "msg_name")
            msg_id = getattr(obj, "msg_id")
            msg_tx_method = getattr(obj, "msg_tx_method")
            msg_cycle = getattr(obj, "msg_cycle")
            msg_length = getattr(obj, "msg_length")
            # 接收端
            rx_nodes = getattr(obj, "rx_nodes")
            # 发送端
            tx_node = getattr(obj, "tx_node")
            # fr 报文
            try:
                msg_slotid = getattr(obj, "msg_slotid")
                msg_base_cycle = getattr(obj, "msg_base_cycle")
                msg_repetition = getattr(obj, "msg_repetition")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_slotid = None
                msg_base_cycle = None
                msg_repetition = None

            try:
                # lin fr 没有这个
                msg_type = getattr(obj, "msg_type")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_type = None

            if msg_slotid is not None:
                msg_id = msg_slotid

            dic = {
                "msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": rx_nodes,
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition,
            }
            # 分类 接收节点

            if msg_tx_method in tx_nodes_dict:
                if tx_node in tx_nodes_dict[msg_tx_method]:
                    tx_nodes_dict[msg_tx_method][tx_node].append(dic)
                else:
                    tx_nodes_dict[msg_tx_method][tx_node] = [dic]
            else:
                tx_nodes_dict[msg_tx_method] = {}
                tx_nodes_dict[msg_tx_method][tx_node] = [dic]

            for item in rx_nodes:
                if msg_tx_method in rx_nodes_dict:
                    if item in rx_nodes_dict[msg_tx_method]:
                        rx_nodes_dict[msg_tx_method][item].append(dic)
                    else:
                        rx_nodes_dict[msg_tx_method][item] = [dic]
                else:
                    rx_nodes_dict[msg_tx_method] = {}
                    rx_nodes_dict[msg_tx_method][item] = [dic]

        new_dict = {"rx_nodes": rx_nodes_dict, "tx_nodes": tx_nodes_dict}
        # 添加缓存，防止每次都去解析数据库，浪费时间
        # self.__all_bus_data_info[channel_name] = new_dict
        return new_dict

    def check_app_busoff_channel_recv_msg(self,channel_name):
        for channel in ["bodycan","propulsioncan","chassiscan1","chassiscan2","passivesafetycan","infocanfd","bodyexposedcanfd","adcanfd"]:
            self.io.close_control_can_busoff(channel)
            msgs = self.bus_comm.ipdu.check_bus_recv_message(channel)
            logger.info(f"8888888888888888 {msgs}")
            if msgs != True:
                assert False,f"{channel} 通道接受报文失败"
        #进入busoff
        self.io.open_control_can_busoff(channel_name)
        self.bus_comm.clear_all_bus_buffer()
        msgs = self.bus_comm.ipdu.check_bus_recv_message(channel_name)
        if msgs != None:
            assert False,f"{channel_name} 通道，busoff后还能收到报文" 

        #busoff恢复后
        self.io.close_control_can_busoff(channel_name)
        self.bus_comm.clear_all_bus_buffer()
        msgs2 = self.bus_comm.ipdu.check_bus_recv_message(channel_name)
        if msgs2 != True:
            assert False,f"{channel_name} 通道，busoff恢复后收不到报文"



    def check_boot_busoff_channel_recv_msg(self,channel_name):
        for channel in ["bodycan","propulsioncan","chassiscan1","chassiscan2","passivesafetycan","infocanfd","bodyexposedcanfd","adcanfd"]:
            self.io.close_control_can_busoff(channel)
            msgs = self.bus_comm.ipdu.check_bus_recv_message(channel)
            logger.info(f"8888888888888888 {msgs}")
            if msgs != True:
                assert False,f"{channel} 通道接受报文失败"
        #进入boot
        self.bus_comm.clear_all_bus_buffer()
        self.bus_comm.set_vehspd(0)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_boot()
        logger.info("=================== 进入boot ========================")
        msgs1 = self.bus_comm.ipdu.check_bus_recv_message(channel_name)
        if msgs1 != True:
            assert False,f"{channel_name} 通道，进入boot后，收到不报文"

        #进入busoff
        self.io.open_control_can_busoff(channel_name)
        msgs2 = self.bus_comm.ipdu.check_bus_recv_message(channel_name)
        if msgs2 != None:
            assert False,f"{channel_name} 通道，进入bussoff后，还能收到报文"

        #busoff恢复后
        self.io.close_control_can_busoff(channel_name)
        msgs3 = self.bus_comm.ipdu.check_bus_recv_message(channel_name)
        #退出boot
        logger.info("=================== 退出boot ========================")
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.quit_boot()
        if msgs3 != True:
            assert False,f"{channel_name} 通道，busoff恢复后收不到报文"

    def network_sleep_by_single_tcam(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        time.sleep(60)

    def check_tcam_process_status(self, proecess_list: list, cmd: str = "ps -ef|grep -E 'usr|app|oem|mode=260'"):
        '''
        检查TCAM进程是否正常运行：
        :param proecess_list: 进程列表，要检查的进程集合，元素为字符串类型；
        :param cmd: 字符串类型，查询TCAM进程的指令
        '''
        outmsg = self.ssh.tcam_ssh.type_commands(commands=cmd, output=False, root_permission=True, timeout=60)
        for process in proecess_list:
            logger.info("Check the process work status of {0}".format(process))
            assert process in outmsg
    
    def set_strt_req(self, up_type:UpType):
        '''
        触发start_req置位
        up_type:0 gear, 1 geatAuto, 2 gearCdc ,3 setusagemodeup = 13, 4 setusagemodewithoutkey = 2
        '''
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.check('infocanfd', 'BgmInfoCanFdDevFr02', 'FOTAStatus', 0)
        self.bus_comm.check('infocanfd', 'BgmInfoCanFdDevFr02', 'StartInhibitSts', 0)
        self.bus_comm.set('backbonefr', 'VddmBackBoneFr08', 'ImobEngSts1', 2)
        if up_type.value == 0:
            self.bus_comm.trigger_gear_by_manual()
            time.sleep(0.7)
        elif up_type.value == 1:
            self.bus_comm.trigger_gear_by_auto()
            time.sleep(0.7)
        elif up_type.value == 2:
            self.bus_comm.trigger_gear_by_cdc()
        elif up_type.value == 3:
            self.soa.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 13})
        elif up_type.value == 4:
            self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        time.sleep(0.3)

    def clear_pnc(self,pnc:BGMPNC):
        promt_info = f"---------------->清除PCN：{pnc.name}置位"
        with allure.step(promt_info):
            logger.info(promt_info)    
            if pnc.name == "PNC16":
                self.io.set_five_door_sts(Door.close)
                self.io.set_hood_sts(HoodSts.Close)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, NMSts.no_valid)
            elif pnc.name == "PNC17":
                self.io.set_five_door_sts(Door.close)
                self.io.set_hood_sts(HoodSts.Close)
                self.set_common_precontion()
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, NMSts.no_valid)
                pass
            elif pnc.name == "PNC18":
                self.set_usage_mode(UsageMode.INACTIVE)
                self.io.set_bgm_hardware_condition_to_default()
                self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, NMSts.no_valid,60.0)
            elif pnc.name == "PNC19":
                self.io.set_five_door_sts(Door.close)
                self.io.set_hood_sts(HoodSts.Close)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, NMSts.no_valid)
                pass
            elif pnc.name == "PNC20":
                self.set_usage_mode(UsageMode.INACTIVE)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, NMSts.no_valid)
                pass
            elif pnc.name == "PNC21":
                self.set_usage_mode(UsageMode.INACTIVE)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, NMSts.no_valid,20.0)
                pass
            elif pnc.name == "PNC22":
                pass
            elif pnc.name == "PNC23":
                self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
                self.sd_tester.update_serverdoipid(0x1002)
                self.sd_tester.send_data([0x11, 0x01])
                sleep(30)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.no_valid, 480.0)
                pass
            elif pnc.name == "PNC24":
                self.set_usage_mode(UsageMode.INACTIVE)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid, 60.0)
                pass
            elif pnc.name == "PNC25":
                self.set_usage_mode(UsageMode.INACTIVE)
                self.bus_comm.set_battery_stop_intelligent_charge(time_wait=7)
                self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
                self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
            elif pnc.name == "PNC26":
                self.set_usage_mode(UsageMode.INACTIVE)
                self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)
                self.io.set_bgm_hardware_condition_to_default()
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid)
            elif pnc.name == "PNC27":
                pass
            elif pnc.name == "PNC28":
                self.set_usage_mode(UsageMode.INACTIVE)
                self.bus_comm.set_battery_stop_intelligent_charge(time_wait=7)
                self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
                self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC28, NMSts.no_valid)
            elif pnc.name == "PNC29":
                self.set_usage_mode(UsageMode.INACTIVE)
                self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
                # 断开诊断激活线
                self.io.bgm_diag_line_down()
                logger.info(f'断开诊断激活线')
                sleep(30)
                self.io.tcam_kl15_down()
                self.sd_tester.update_serverdoipid(0x1FFF)
                self.sd_tester.send_data([0x11, 0x01])
                sleep(30)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC30":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC30, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC31":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC31, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC32":
                self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
                self.io.set_five_door_sts(Door.close)
                self.io.set_hood_sts(HoodSts.Close)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC33":
                self.set_usage_mode(UsageMode.CONVENIENCE)
                self.io.set_bgm_hardware_condition_to_default()
                sleep(10)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, NMSts.no_valid, timeout=10)
                pass
            elif pnc.name == "PNC34":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC34, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC35":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC35, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC36":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC36, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC37":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC38":
                self.set_common_precontion(usage_mode=UsageMode.INACTIVE)
                self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
                self.sd_tester.update_serverdoipid(0x1FFF)
                self.sd_tester.send_data([0x11, 0x01])
                sleep(30)
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, NMSts.no_valid, timeout=10)
                pass
            elif pnc.name == "PNC39":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC40":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC40, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC41":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC41, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "PNC42":
                self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC42, NMSts.no_valid, timeout=60)
                pass
            elif pnc.name == "All":
                pass

    def diag_route_can2can(self, data_info_list, send_length):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_can_type = item_info.get("send_can_type")
            recv_can_type = item_info.get("recv_can_type")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")
            # 过滤数据
            # if send_channel != "obd":
            #     continue
            # if recv_address != 0x1510:
            #     continue
            # if recv_channel != "connectivitycanfd":
            #     continue

            # 更新逻辑地址，必须
            except_flag = False
            for send_length in send_length_list:
                # 清空 通道缓存
                # self.bus_comm.clear_all_bus_buffer()
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                # 生成随机数据
                # send_data = [random.randint(0, 255) for i in range(send_length)]
                send_data = [random.randint(0xA0, 255)] + [random.randint(0, 255) for i in range(send_length - 1)]
                # 发送请求
                string = f"{send_channel}发送数据长度{send_length}"
                logger.info(string)
                send_eth_time = time.time()

                recv_flag = False
                except_flag = False
                try:
                    send_can_time = self.bus_comm.send_diag_request_msg(
                        send_channel,
                        request_id=request_id,
                        response_id=response_id,
                        send_msg=send_data,
                        padding=padding,
                        single_frame_len=length,
                    )
                    recv_flag = False
                    # 接受请求
                    string = f"{recv_channel}接收数据"
                    logger.info(string)
                    (
                        recv_msg_data,
                        recv_padding,
                        time_stamp,
                    ) = self.bus_comm.recv_diag_request_msg(
                        recv_channel,
                        request_id=request_id,
                        response_id=response_id,
                        bs=bs,
                        st=st,
                        single_frame_len=length,
                    )
                    if len(recv_padding) > 1 or (
                            recv_padding and recv_padding[0] != padding
                    ):
                        err_item_list.append(hex(request_id))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}请求id为{hex(request_id)}路由失败,填充位不对，本应为{padding}实际为{recv_padding} 秒"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    elif len(send_data) != len(recv_msg_data):
                        err_item_list.append(hex(request_id))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}请求id为{hex(request_id)}路由失败 发送数据长度{len(send_data)}，can接收数据的长度{len(recv_msg_data)}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    elif recv_msg_data != send_data:
                        err_item_list.append(hex(request_id))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}请求id为{hex(request_id)}路由失败，接收的内容和发送的内容不一样，发送数据{send_data}，can接收数据的{recv_msg_data}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break

                    else:
                        string = f"第{index + 1}条》》》路由长度为{send_length}成功 {send_channel}到{recv_channel}请求id为{hex(request_id)}路由成功"
                        self.log_and_allure_step(string, LogLevel.INFO)

                    self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                    recv_flag = True
                    send_response_msg = [random.randint(0xA0, 255)] + [random.randint(0, 255) for i in
                                                                       range(send_length - 1)]
                    string = f"{recv_channel}发送响应数据长度{send_length}"
                    logger.info(string)
                    send_can_time = self.bus_comm.send_diag_request_msg(
                        recv_channel,
                        request_id=response_id,
                        response_id=request_id,
                        send_msg=send_response_msg,
                        padding=padding,
                        single_frame_len=length,
                    )
                    # 以太接收响应
                    string = f"{send_channel}接收响应数据"
                    logger.info(string)
                    (
                        recv_can_msg,
                        recv_padding,
                        time_stamp,
                    ) = self.bus_comm.recv_diag_request_msg(
                        send_channel,
                        request_id=response_id,
                        response_id=request_id,
                        bs=bs,
                        st=st,
                        single_frame_len=length,
                    )

                    if len(send_response_msg) != len(recv_can_msg):
                        err_item_list.append(hex(response_id))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {recv_channel}响应id为{hex(response_id)}响应{send_channel}请求路由失败 发送数据长度{len(send_response_msg)}，接收数据的长度{len(recv_can_msg)}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    elif send_response_msg != recv_can_msg:
                        err_item_list.append(hex(response_id))
                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {recv_channel}响应id为{hex(response_id)}响应{send_channel}请求路由失败，接收的内容和发送的内容不一样，发送数据{send_response_msg}，接收数据的{recv_can_msg}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    else:
                        string = f"第{index + 1}条》》》路由长度为{send_length}成功 {recv_channel}响应id为{hex(response_id)}响应{send_channel}请求路由成功"
                        self.log_and_allure_step(string, LogLevel.INFO)


                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    except_flag = True
                    logger.error(f"异常》》{str(e)}")
                    # request_id_hex = hex(request_id)[2:].zfill(3).upper()
                    # response_id_hex = hex(response_id)[2:].zfill(3).upper()
                    # trace_path = os.path.join(str(__file__).split('sat')[0], 'sat/xat_cases/legacy/bgm/Can.asc')
                    # command = f" cat {trace_path}  | grep -E ' {request_id_hex} | {response_id_hex} '"
                    # try:
                    #     # 执行命令
                    #     logger.info(f"开始执行cmd={command}")
                    #     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #     # 等待命令执行完成
                    #     process.wait(60)
                    #     # 获取命令的输出和错误信息
                    #     output = process.stdout.read()
                    #     error = process.stderr.read()
                    #     # 将输出和错误信息解码为字符串
                    #     output = output.decode(encoding="utf-8")
                    #     error = error.decode(encoding="utf-8")
                    # except Exception as e1:
                    #     output = ""
                    #     error = str(e1)
                    # logger.info(f"执行cmd={command} 结束")
                    # # 返回命令的输出和错误信息
                    # result = output.split('\r\n')
                    # asc_data = ""
                    # for item in result:
                    #     if item.strip():
                    #         asc_data = item
                    #         logger.info(f"asc>>{item}")

                    err_item_list.append(hex(response_id))
                    if recv_flag:
                        can_id = response_id
                    else:
                        can_id = request_id
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}can id 为{hex(can_id)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

            # if err_item_list and not except_flag:
                # if err_item_list[-1] == hex(response_id) or err_item_list[-1] == hex(request_id):
                #     request_id_hex = hex(request_id)[2:].zfill(3).upper()
                #     response_id_hex = hex(response_id)[2:].zfill(3).upper()
                #     trace_path = os.path.join(str(__file__).split('sat')[0], 'sat/xat_cases/legacy/bgm/Can.asc')
                #     command = f" cat {trace_path}  | grep -E ' {request_id_hex} | {response_id_hex} '"
                #     os.system(command)
                #     try:
                #         # 执行命令
                #         logger.info(f"开始执行cmd={command}")
                #         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #         # 等待命令执行完成
                #         process.wait(60)
                #         # 获取命令的输出和错误信息
                #         output = process.stdout.read()
                #         error = process.stderr.read()
                #         # 将输出和错误信息解码为字符串
                #         output = output.decode(encoding="utf-8")
                #         error = error.decode(encoding="utf-8")
                #     except Exception as e:
                #         output = ""
                #         error = str(e)
                #     logger.info(f"执行cmd={command} 结束")
                #     # 返回命令的输出和错误信息
                #     result = output.split('\r\n')
                #     for item in result:
                #         logger.info(f"asc>>{item}")

        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def diag_route_can2can_unrecv(self, data_info_list, send_length, all_can=False,**kwargs):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """
        #
        under_boot = kwargs.get("under_boot", False)
        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length
        name_list, index_list, can_map = self.bus_comm.get_all_can_channel_info()

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_can_type = item_info.get("send_can_type")
            recv_can_type = item_info.get("recv_can_type")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")

            # 更新逻辑地址，必须
            # self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                # 清空 通道缓存
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                # 生成随机数据
                send_data = [random.randint(0, 255) for i in range(send_length)]
                # 发送请求
                logger.info(f"{send_channel}发送数据长度{send_length}")
                if under_boot:
                    # 在boot 下 can2can 单帧不转
                    if send_length<=7:
                        send_can_time = self.bus_comm.send_diag_request_msg(
                            send_channel,
                            request_id=request_id,
                            response_id=response_id,
                            send_msg=send_data,
                            padding=padding,
                            single_frame_len=length,
                        )
                    else:
                        # 多帧 发送首帧 不会回复流控帧
                        send_msg_len=len(send_data)
                        multi_head = '1' + hex(send_msg_len)[2:].zfill(3)
                        first_frame_msg = send_data[:length - 2]
                        first_frame = [int(multi_head[i:i + 2], 16) for i in range(0, len(multi_head), 2)] + first_frame_msg
                        # 发送 首帧
                        self.bus_comm.send_msg_by_id_func(send_channel, request_id, first_frame)

                        recv_flow_control_frame, time_stamp = self.bus_comm.recv_msg_by_id_func(send_channel, response_id)
                        logger.info(f"{send_channel}发送首帧，接收流控帧{recv_flow_control_frame}")
                        if recv_flow_control_frame:
                            logger.info(f"{send_channel}发送首帧，接收流控帧{recv_flow_control_frame}")
                            err_item_list.append(hex(request_id))
                            string = f"第{index + 1}条***** 发送首帧后，不应该接收流控帧，实际接收到{recv_flow_control_frame}"
                            self.log_and_allure_step(string, LogLevel.ERROR)
                            continue
                else:
                    send_can_time = self.bus_comm.send_diag_request_msg(
                        send_channel,
                        request_id=request_id,
                        response_id=response_id,
                        send_msg=send_data,
                        padding=padding,
                        single_frame_len=length,
                    )
                try:
                    recv_data_map = self.bus_comm.recv_mul_can_channel_msg(can_chnanel_lis=index_list,
                                                                           msg_id=(0x700, 0x7ff),
                                                                           unexpect_msg=[0x02, 0x3e, 0x80])
                    for unrecv_channel in name_list:
                        if not all_can and unrecv_channel == recv_channel:
                            continue
                        can_index = self.bus_comm.get_can_channel_index_by_name(unrecv_channel)
                        recv_msg_dic = recv_data_map.get(can_index)
                        if recv_msg_dic:
                            err_item_list.append(hex(request_id))

                            string = f"第{index + 1}条*****路由长度为{send_length}失败，{send_channel}发送给{recv_channel} {unrecv_channel}本不应收到，实际收到{recv_msg_dic}"
                            with allure.step(string):
                                logger.error(string)
                                for can_id, can_msg in recv_msg_dic.items():
                                    string2 = f"{unrecv_channel}通道，接收到id为{hex(can_id)[2:].upper()} 内容为{can_msg}的报文"
                                    with allure.step(string2):
                                        logger.error(string2)
                        else:
                            string = f"第{index + 1}条{send_channel}发送给{recv_channel}  {unrecv_channel}本不应收到，实际未收到"
                            logger.info(string)

                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(request_id))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}请求id 为{hex(request_id)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)
        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def creat_diag_route_can2can_phy_invalid_data_item(self, data_info_list_phy):
        '''
        构造无效数据
        @param data_info_list_phy:
        @return:
        '''
        # 下面修改了内容，要处理下
        data_info_list = copy.deepcopy(data_info_list_phy)
        func_id = [0x7df]
        new_item_list = []
        send_channel_id_dict = {}
        diag_id_list = [i for i in range(0x700, 0x800)]
        new_list = []
        for item_info in data_info_list:
            send_channel = item_info.get("send_channel")
            request_id = item_info.get("request_id")
            if send_channel in send_channel_id_dict:
                send_channel_id_dict[send_channel].append(request_id)
            else:
                send_channel_id_dict[send_channel] = [request_id]
                new_list.append(item_info)

        for item_info in new_list:
            curr_channel_name = item_info['send_channel']
            curr_channel_id = send_channel_id_dict.get(item_info["send_channel"], [])
            logger.info(f"{curr_channel_name}自带的诊断id为{[hex(i) for i in curr_channel_id]}")
            diag_id_list1 = copy.deepcopy(diag_id_list)
            invalid_req_id = [i for i in diag_id_list1 if i not in func_id + curr_channel_id]

            num = 10 if len(invalid_req_id) > 10 else len(invalid_req_id)
            invalid_req_id_select = random.sample(invalid_req_id, num)
            logger.info(
                f"{curr_channel_name}随机上产生的{num}个无效诊断id为{[hex(i) for i in invalid_req_id_select]}")

            for canid in invalid_req_id_select:
                item_info["request_id"] = canid
                iteminfo = copy.deepcopy(item_info)
                new_item_list.append(iteminfo)

        return new_item_list


    def diag_route_can2can_unsend_flow_frame(self, data_info_list, send_length):
        """
        发送多帧到下挂 ，下挂节点接收首帧，不回复流控帧，则收不到连续帧
        @param data_info_list:
        @param send_length:
        @return:
        """

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_can_type = item_info.get("send_can_type")
            recv_can_type = item_info.get("recv_can_type")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")
            # 更新逻辑地址，必须
            for send_length in send_length_list:
                # 清空 通道缓存
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                # 生成随机数据
                send_data = [random.randint(0xA0, 255)] + [random.randint(0, 255) for i in range(send_length - 1)]
                # 发送请求
                string = f"{send_channel}发送数据长度{send_length}"
                logger.info(string)
                try:
                    self.bus_comm.send_diag_request_msg(
                        send_channel,
                        request_id=request_id,
                        response_id=response_id,
                        send_msg=send_data,
                        padding=padding,
                        single_frame_len=length,
                    )
                    # 接受请求
                    logger.info(f"{recv_channel}接收数据")
                    # 接收首帧数据
                    recv_first_data, time_stamp = self.bus_comm.recv_msg_by_id_func(recv_channel, request_id, timeout=1)
                    logger.info(f"{recv_channel}接收首帧数据为{recv_first_data}")
                    recv_seq_data, time_stamp = self.bus_comm.recv_msg_by_id_func(recv_channel, request_id, timeout=1)
                    logger.info(f"未发送流控帧，{recv_channel}接收数据为{recv_seq_data}")
                    if recv_seq_data:
                        err_item_list.append(hex(request_id))
                        string = f"第{index + 1}条*****{recv_channel}接收首帧,未发送流控帧，也收到连续帧，本不应收到连续帧"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(response_id))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}can id 为{hex(request_id)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def diag_route_eth2can_unsend_flow_frame(self, data_info_list, send_length):
        """
        发送多帧到下挂 ，下挂节点接收首帧，不回复流控帧，则收不到连续帧
        @param data_info_list:
        @param send_length:
        @return:
        """

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            recv_address = item_info.get("recv_address")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")

            # 更新逻辑地址，必须
            self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                # 清空 通道缓存
                self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                send_data = [random.randint(0xA0, 255)] + [random.randint(0, 255) for i in range(send_length - 1)]
                # 发送请求
                string = f"{send_channel}发送数据长度{send_length}"
                logger.info(string)
                send_eth_time = time.time()
                self.sd_tester.send_data(send_data)
                try:
                    # 接受请求
                    logger.info(f"{recv_channel}接收数据")
                    # 接收首帧数据
                    recv_first_data, time_stamp = self.bus_comm.recv_msg_by_id_func(recv_channel, request_id, timeout=1)
                    logger.info(f"{recv_channel}接收首帧数据为{recv_first_data}")
                    recv_seq_data, time_stamp = self.bus_comm.recv_msg_by_id_func(recv_channel, request_id, timeout=1)
                    logger.info(f"未发送流控帧，{recv_channel}接收数据为{recv_seq_data}")
                    if recv_seq_data:
                        err_item_list.append(hex(request_id))
                        string = f"第{index + 1}条*****{recv_channel}接收首帧,未发送流控帧，也收到连续帧，本不应收到连续帧"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(recv_address))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}逻辑地址为{hex(recv_address)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def diag_route_can2can_func(self, data_info_list, send_length, **kwargs):
        """
        发送 can 到 can canfd 的诊断路由  功能寻址
        @param data_info_list:
        @param send_length:
        @return:
        """
        max_len = kwargs.get('max_len', 6)
        recv_able = kwargs.get('recv_able', True)
        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        err_item_list = []
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length

        name_list, index_list, can_map = self.bus_comm.get_all_can_channel_info()
        logger.info(f"name_list={name_list}  index_list={index_list} can_map={can_map}")
        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            response_id = item_info.get("response_id")
            can_recv_channel = item_info.get("can_recv_channel")
            # lin_recv_channel = item_info.get("lin_recv_channel")
            # fr_recv_channel = item_info.get("fr_recv_channel")
            request_id = item_info.get("request_id")
            padding = item_info.get("padding")
            length = item_info.get("length")

            # 更新逻辑地址，必须
            # self.sd_tester.update_serverdoipid(recv_address)
            for send_length in send_length_list:
                try:
                    # 接受请求
                    string = f"长度小于等于{max_len}，can/canfd 通道 {can_recv_channel}可以接收数据"
                    logger.info(string)
                    self.bus_comm.clear_recv_pdu_d_buffer('bodycan')
                    # 生成随机数据
                    send_data = [random.randint(0, 255) for i in range(send_length)]
                    # 发送请求
                    string = f"{send_channel} 发送数据长度{send_length} data={[hex(i)[2:].zfill(2) for i in send_data]}"
                    logger.info(string)
                    send_can_time = self.bus_comm.send_diag_request_msg(
                        send_channel,
                        request_id=request_id,
                        response_id=response_id,
                        send_msg=send_data,
                        padding=padding,
                        single_frame_len=length,
                    )

                    recv_data_map = self.bus_comm.recv_mul_can_channel_msg(can_chnanel_lis=index_list, msg_id=0x7Df,
                                                                           unexpect_msg=[0x02, 0x3e, 0x80])
                    if recv_able:
                        for recv_channel in can_recv_channel:
                            can_index = self.bus_comm.get_can_channel_index_by_name(recv_channel)
                            logger.info(f"获取的{recv_channel} 对应的索引为{can_index}")
                            recv_mg_dic = recv_data_map.get(can_index, {})
                            if len(recv_mg_dic) == 1:
                                recv_mg_list = recv_mg_dic.get(request_id)
                                if len(recv_mg_list) == 1:
                                    msg_ifo = recv_mg_list[0]
                                    can_len = msg_ifo[0]
                                    recv_msg_data = msg_ifo[1:can_len + 1]
                                    recv_padding = list(set(msg_ifo[can_len + 1:]))

                                    if len(recv_padding) > 1 or (
                                            recv_padding and recv_padding[0] != padding
                                    ):
                                        err_item_list.append(hex(request_id))
                                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}canid为{hex(request_id)}路由失败,填充位不对，本应为{padding}实际为{recv_padding}"
                                        self.log_and_allure_step(string, LogLevel.ERROR)

                                    elif len(send_data) != len(recv_msg_data):
                                        err_item_list.append(hex(request_id))
                                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}canid为{hex(request_id)}路由失败 发送数据长度{len(send_data)}，can接收数据的长度{len(recv_msg_data)}"
                                        self.log_and_allure_step(string, LogLevel.ERROR)

                                    elif recv_msg_data != send_data:
                                        err_item_list.append(hex(request_id))
                                        string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}canid为{hex(request_id)}路由失败，接收的内容和发送的内容不一样，发送数据{send_data}，can接收数据的{recv_msg_data}"
                                        self.log_and_allure_step(string, LogLevel.ERROR)

                                    else:
                                        string = f"第{index + 1}条》》》路由长度为{send_length}成功 {send_channel}到{recv_channel}canid为{hex(request_id)}路由成功"
                                        self.log_and_allure_step(string, LogLevel.INFO)
                                else:
                                    err_item_list.append(hex(request_id))
                                    string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}canid为{hex(request_id)}路由失败 发送数据长度{send_data}，can接收数据的长度{recv_mg_list}"
                                    self.log_and_allure_step(string, LogLevel.ERROR)
                            else:
                                err_item_list.append(hex(request_id))
                                string = f"第{index + 1}条*****路由长度为{send_length}失败 {send_channel}到{recv_channel}逻辑地址为{hex(request_id)}路由失败 发送数据长度{send_data}，can接收数据的{recv_mg_dic}"
                                self.log_and_allure_step(string, LogLevel.ERROR)

                    for unrecv_channel in name_list:
                        if recv_able:
                            if unrecv_channel in can_recv_channel:
                                continue
                        can_index = self.bus_comm.get_can_channel_index_by_name(unrecv_channel)
                        recv_mg_list = recv_data_map.get(can_index)
                        if recv_mg_list:
                            err_item_list.append(hex(request_id))
                            string = f"第{index + 1}条*****路由长度为{send_length}失败 {unrecv_channel}本不应收到，实际收到{recv_mg_list}"
                            self.log_and_allure_step(string, LogLevel.ERROR)
                        else:
                            logger.info(f"{unrecv_channel}本不应收到，实际未收到")
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(request_id))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{can_recv_channel}canid为{hex(request_id)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)

        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)

        assert not len(err_item_list), string

    def send_diag_route_eth2fr(self,data_info_list,send_length):
        '''
        发送诊断路由 以太到fr的
        @param data_info_list: 列表格式，里面是字典，包含每条信息的具体内容
        @param send_length: 发送数据长度
        @return:
        '''

        string = f"总共{len(data_info_list)}条路由信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        if isinstance(send_length, int):
            send_length_list = [send_length]
        else:
            send_length_list = send_length
        # 存放失败的
        err_item_list = []
        for index, item_info in enumerate(data_info_list):
            string = f"共{len(data_info_list)}条，第{index + 1}条路由信息{item_info}"
            logger.info(string)
            send_channel = item_info.get("send_channel")
            send_address = item_info.get("send_address")
            recv_address = item_info.get("recv_address")
            recv_channel = item_info.get("recv_channel")
            request_id = item_info.get("request_id")
            response_id = item_info.get("response_id")
            if isinstance(response_id,list):
                response_id=response_id[0]
            padding = item_info.get("padding")
            bs = item_info.get("bs")
            st = item_info.get("st")
            length = item_info.get("length")

            for send_length in send_length_list:
                try:
                    logger.info("************** doip2fr  以太发送诊断请求***********************************")
                    self.sd_tester.update_serverdoipid(recv_address)
                    # if send_length <= 255:
                    #     send_data = [k for k in range(send_length)]
                    # else:
                    #     send_data = [random.randint(0, 255) for k in range(send_length)]
                    send_data = [random.randint(0, 255) for k in range(send_length)]
                    logger.info(f"obd 发送请求数据 >>{bytes(send_data).hex().upper()}")
                    self.sd_tester.send_data(send_data)
                    msg = self.bus_comm.recv_fr_msg(fr_id_list=request_id, fr_response_id=response_id, send_address=send_address,
                                           recv_address=recv_address, )
                    logger.info(f"fr 接收到的请求数据>>{bytes(msg).hex().upper()}")
                    if len(msg) != send_length:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度{send_length}失败，以太到fr 地址为{hex(recv_address)}长度不对 本应为{send_length}实际为{len(msg)}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    elif msg != send_data:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度{send_length}失败，以太到fr 地址为{hex(recv_address)}内容不对 本应为{send_data}实际为{msg}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    else:
                        string = f"第{index + 1}条》》》》路由长度{send_length}成功，以太到fr 地址为{hex(recv_address)}成功"
                        self.log_and_allure_step(string, LogLevel.INFO)

                    # assert len(msg) == send_length, f"长度不对 本应为{send_length}实际为{len(msg)}"
                    # assert msg == send_data, f"内容不对 本应为{send_data}实际为{msg}"

                    logger.info("************** doip2fr  fr响应诊断请求***********************************")
                    # if send_length <= 255:
                    #     send_data = [k for k in range(send_length)]
                    # else:
                    #     send_data = [random.randint(0, 255) for k in range(send_length)]
                    send_data = [random.randint(0, 255) for k in range(send_length)]
                    res_recv_id = request_id[0]
                    res_send_id = response_id
                    logger.info(f"fr 发送的响应数据长度为{len(send_data)} 内容为={bytes(send_data).hex().upper()}")
                    self.bus_comm.send_fr_msg(send_data, send_id=res_send_id, recv_id=res_recv_id, send_address=recv_address,
                                     recv_address=send_address, )
                    recv_eth_msg = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                    logger.info(f"obd 接收的响应为 recv_eth_msg 长度为{len(recv_eth_msg)} 内容={bytes(recv_eth_msg).hex().upper()}")
                    # assert send_data == recv_eth_msg, "接收数据不一样"

                    if len(recv_eth_msg) != send_length:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度{send_length}失败，fr 地址为{hex(recv_address)}到以太,长度不对 本应为{send_length}实际为{len(msg)}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    elif recv_eth_msg != send_data:
                        err_item_list.append(hex(recv_address))
                        string = f"第{index + 1}条*****路由长度{send_length}失败，fr 地址为{hex(recv_address)}到以太 ,内容不对 本应为{send_data}实际为{msg}"
                        self.log_and_allure_step(string, LogLevel.ERROR)
                        break
                    else:
                        string = f"第{index + 1}条》》》》路由长度{send_length}成功，fr到eth 地址为{hex(recv_address)}成功"
                        self.log_and_allure_step(string, LogLevel.INFO)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                    logger.error(f"异常》》{str(e)}")
                    err_item_list.append(hex(recv_address))
                    string = f"第{index + 1}条*****路由长度为{send_length}失败{recv_channel}逻辑地址为{hex(recv_address)} 异常》》{str(e)}"
                    self.log_and_allure_step(string, LogLevel.ERROR)


        string = (
            f"总共{len(data_info_list)}条路由,失败{len(err_item_list)}条路由>>{err_item_list}"
        )
        self.log_and_allure_step(string, LogLevel.INFO)
        assert not len(err_item_list), string

    def set_digital_key_pre_condition(self):
        promt_info = f"---------------->设置数字钥匙测试的公共前提条件"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
            self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20","EntityKeyWhiteListVers",self.bus_comm.dk.last_sync_time_entity)
            self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20","BLESlotKeyWhiteListVers",self.bus_comm.dk.last_sync_time_ble)
            self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr17","BLEKeyPrsntStsZone7",0)
            
            self.bus_comm.set_gear_pos(gear=Gear.Park)
            self.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
            self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)
            sleep(0.5)
            self.bus_comm.reset_bncm_digital_keyinfo()
            self.io.set_bgm_hardware_condition_to_default()
            self.io.bgm_diag_active_line_ctrl(sts=DiagActLineSts.Active)
            self.soa.hmi_set_key_config_info(key_type=KeyConfigType.SetPEKeySearchDedicateZone,value=0)


    def s2s_change_car_mode(self, car_mode:CarMode):
        logger.info(f"----->设置car mode 为{car_mode.name}")
        logger.info(f"------>调用 SetCarMode:(服务:BonnetService;函数名:set:SetCarMode(mode:{car_mode.name}))")
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": car_mode.value})



    def check_turn_lamp_flash(self,pos:GeneralPos,sts:isOn,last_time:int):
        start_time = time.time()
        logger.info(f"----------->Check Start{start_time}")
        for num in range(last_time):
            if sts.name == "On":
                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)

                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            
            if sts.name == "Off":
                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
                sleep(0.9)

        stop_time = time.time()
        logger.info(f"----------->Check Stop{stop_time}")
        test_duration = stop_time - start_time 
        logger.info(f"----------->Check 信号跳变执行时间{test_duration},时间差为{test_duration - last_time}")
        # if abs(test_duration - last_time) > 2:
        #     assert False

    def test_check_ping_tcam_success(self,bgm_wait_time:int,tcam_wait_time:int,expect_value:int):
        """
        bgm与tcam通讯正常
        """
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(bgm_wait_time)
        current_time = datetime.datetime.now()
        logger.info(f"当前时间： {current_time}")
        time.sleep(tcam_wait_time)
        outmsg = self.ssh.type_commands(DeviceName.BGM,"ls /log/jetlog_message*")
        jie_log_list = [j for i in outmsg.split("\n") for j in i.split(" ") if len(j) != 0]
        #找出当天日志中打印 Ping 172.16.9.31 success
        logger.info(f"7777777777 {jie_log_list}")
        ping_success_msg_lis = []
        for i in [i for i in jie_log_list[1:] if str(datetime.datetime.now()).replace("-", "").split(" ")[0] in i]:
            ping_success_msg_lis.append(self.ssh.type_commands(DeviceName.BGM,f'/app/bin/zstdcat {i} | grep "Ping 172.16.9.31 success"'))

        logger.info(f"666666666666 {len(ping_success_msg_lis)}")
        #处理过滤出来的日志
        all_log_msg = []
        for j in ping_success_msg_lis:
            if "\n" in j:
                for msg in j.split("\n"):
                    if datetime.datetime.strptime(msg[:23],'%Y-%m-%d %H:%M:%S.%f') >= current_time:
                        all_log_msg.append(msg)
            else:
                logger.info(f"333333333333 {j}")
        logger.info(f"9999999999999 {all_log_msg}")
        if len(all_log_msg) < expect_value:
            assert False,f"ping 172.16.5.31 要求ping的次数为：大于等于2次，实际ping的次数为：{len(all_log_msg)}"


    def test_check_ping_tcam_fail(self,bgm_wait_time,tcam_wait_time,expect_value,phy_reset_count,phy_quit=0):
        """
        bgm与tcam通讯异常
        """
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(bgm_wait_time)
        res = self.ssh.get_ping(ip="172.16.5.31", num=3)
        res2 = self.ssh.get_ping(ip="www.baidu.com", num=3) 
        if res and res2:
            logger.info("=============== tcam下电 =============== ")
            self.io.tcam_power_off()
            current_time = datetime.datetime.now()
            logger.info(f"当前时间： {current_time}")
            time.sleep(tcam_wait_time)
            outmsg = self.ssh.type_commands(DeviceName.BGM,"ls /log/jetlog_message*")
            logger.info(f"22222222222 {outmsg}")
            jie_log_list = [j for i in outmsg.split("\n") for j in i.split(" ") if len(j) != 0]
            logger.info(f"7777777777 {jie_log_list}")
            #找出当天日志中打印 Check ping count fail 及 phy hard reset
            ping_success_msg_lis = []
            for i in [i for i in jie_log_list[1:] if str(datetime.datetime.now()).replace("-", "").split(" ")[0] in i]:
                ping_success_msg_lis.append(self.ssh.type_commands(DeviceName.BGM,f'/app/bin/zstdcat {i} | grep -E "Check ping count | Phy hard reset | Check phy Failed, quit"'))
            #处理过滤出来的日志
            all_log_msg = []
            for j in ping_success_msg_lis:
                if "\n" in j:
                    for msg in j.split("\n"):
                        if datetime.datetime.strptime(msg[:23],'%Y-%m-%d %H:%M:%S.%f') >= current_time:
                            all_log_msg.append(msg)
                else:
                    logger.info(f"333333333333 {j}")
            logger.info(f"9999999999999 {all_log_msg}")
            new_list = [i[-16:] if "Phy hard reset" in i else i[-25:] for i in all_log_msg]
            count_ping_fail = 0
            phy_hard_reset_count = 0
            for i in all_log_msg:
                if "Check ping count" in i:
                    count_ping_fail += 1
                elif "Phy hard reset" in i:
                    phy_hard_reset_count += 1
       
            if count_ping_fail < expect_value:
                assert False,f"期望ping fail 的次数为：{expect_value}，实际ping fail 的次数为{count_ping_fail}"
            
            if phy_hard_reset_count < phy_reset_count:
                assert False,f"期望复位 的次数为：{phy_reset_count}，实际复位 的次数为{phy_hard_reset_count}"

            count_fial = [i for i in new_list if "Check ping count" in i]
            logger.info(f"888888888888 {count_fial}")
            for i in range(1,expect_value+1):
                if expect_value %6 == 0:
                    if i > 6:
                        if i%6 == 0:
                            if count_fial[i-1].strip(" ") != f"Check ping count {i%6+6} Failed":
                                assert False,f"第{i-1}的期望值为：Check ping count {i%6+6} Failed，实际值为：{count_fial[i-1]}"
                        else:
                            if count_fial[i-1].strip(" ") != f"Check ping count {i%6} Failed":
                                assert False,f"第{i-1}的期望值为：Check ping count {i%6} Failed，实际值为：{count_fial[i-1]}"
                    else: 
                        if count_fial[i-1] != f'Check ping count {i} Failed':
                            assert False,f"第{i-1}的期望值为：Check ping count {i} Failed，实际值为：{count_fial[i-1]}"
                else:
                    if i > 6:
                        if i%6 == 0:
                            if count_fial[i-1].strip(" ") != f"Check ping count {i%6+6} Failed":
                                assert False,f"第{i-1}的期望值为：Check ping count {i%6+6} Failed，实际值为：{count_fial[i-1]}"
                        else:
                            if count_fial[i-1].strip(" ") != f"Check ping count {i%6} Failed":
                                assert False,f"第{i-1}的期望值为：Check ping count {i%6} Failed，实际值为：{count_fial[i-1]}"
                    else: 
                        if count_fial[i-1] != f'Check ping count {i} Failed':
                            assert False,f"第{i-1}的期望值为：Check ping count {i} Failed，实际值为：{count_fial[i-1]}"

            for i in range(1,phy_reset_count+1):
                if i == 1:
                    if "Phy hard reset 1" not in all_log_msg[6]:
                        assert False,f"第6次ping count fail 后，未执行复位操作"
                if i == 2:
                    if "Phy hard reset 2" not in all_log_msg[13]:
                        assert False,f"第12次ping count fail 后，未执行复位操作"
                if i == 3:
                    if "Phy hard reset 3" not in all_log_msg[20]:
                        assert False,f"第18次ping count fail 后，未执行复位操作"
                if i == 4:
                    if "Phy hard reset 4" not in all_log_msg[27]:
                        assert False,f"第24次ping count fail 后，未执行复位操作"
                if i == 5:
                    if "Phy hard reset 5" not in all_log_msg[34]:
                        assert False,f"第30次ping count fail 后，未执行复位操作"
                if i == 6:
                    if "Phy hard reset 6" not in all_log_msg[41]:
                        assert False,f"第36次ping count fail 后，未执行复位操作"

            if phy_quit == 1 and "Check phy Failed, quit" not in all_log_msg[42]:
                assert False,"复位6次失败后，未停止检测"
                
        else:
            assert False,f"tcam下电前还ping不通tcam 或者tcam上不了网"
                
                    

    def write_vehicle_model_ccp(self, vehicle_model: VehicleType = VehicleType.Mars,
                                vehicle_mca: VehicleMca = VehicleMca.Mca_400v,
                                ccp_value: [list, str, None] = None, **kwargs):
        '''
          写入 车型
        @param vehicle_model: （CCP#950==0x01代表 Mars  CCP#950==0x02代表 Venus) 默认 Mars
        @param vehicle_mca:    (CCP#962==0x00代表MCA 400v CCP#962==0x02代表MCA 800v)  默认400v
        @param ccp_value: 传入的ccp 值 ，不传则采用默认的值
        @return:
        '''
        ccp_len = kwargs.get('ccp_len', 1556)  # 纯粹 ccp 内容
        ret_vehicle_model, ret_vehicle_mca = self.sd_tester.get_vehicle_model()
        if vehicle_model.value == ret_vehicle_model and vehicle_mca.value == ret_vehicle_mca:
            logger.info("当前模式已经满足，不需要写入")
            return
        bgm_info_dict = self.ssh.bgm_ssh.get_version()
        version_release = bgm_info_dict.get("version_release", None)
        assert version_release, "未获取BGM 版本号"
        self.bgm_version_release = int(version_release[1:].replace('.', ""))
        if ccp_value is None:
            if vehicle_model == VehicleType.Mars:
                # 代表 Mars
                ccp_value = "A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8C 80 09 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 02 01 80 00 01 00 81 80 11 80 03 04 01 01 01 01 02 01 03 01 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 81 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 02 04 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 02 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 02 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 02 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 01 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 01 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 02 01 02 01 01 01 02 01 01 02 01 01 01 01 01 01 01 01 01 01 02 02 01 01 02 01 01 01 01 00 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 02 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 01 01 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 0E"
            else:
                # 代表 Venus
                ccp_value = "A3 01 81 06 FD 03 01 01 A2 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 01 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 80 89 02 03 01 01 03 02 73 72 03 01 01 01 01 01 01 01 03 01 02 02 02 02 0A 01 01 02 01 02 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 00 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 80 01 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 82 03 03 04 01 14 03 0A 80 01 04 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 05 02 01 01 00 03 02 02 03 04 02 02 02 01 01 01 02 00 01 01 01 01 01 01 01 01 01 80 03 0A 01 01 04 06 07 07 0A 0A 07 07 0A 0A 00 00 04 00 00 02 01 01 01 01 01 02 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 00 01 01 02 00 00 00 01 03 00 00 01 00 00 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00 00 00 00 01 00 01 01 00 00 02 00 00 00 80 00 00 00 00 84 03 01 01 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 01 01 01 01 01 05 03 80 02 06 01 03 01 10 00 00 02 03 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 02 01 00 00 00 00 00 85 04 01 02 02 02 01 02 02 02 04 85 01 02 01 01 02 80 04 03 01 01 02 02 01 03 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 00 00 00 01 80 02 02 01 01 02 02 01 02 02 02 01 02 01 03 02 02 01 01 01 01 01 01 01 01 00 01 03 01 02 01 01 05 02 03 03 04 01 01 01 01 03 01 01 04 02 01 02 01 01 01 01 02 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 01 02 01 01 03 01 04 01 04 01 01 01 01 01 02 01 03 01 05 02 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 01 01 01 01 01 02 01 01 01 01 02 06 00 00 01 01 04 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 03 02 02 08 01 00 00 01 02 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 01 01 02 02 02 02 02 02 02 02 01 02 02 01 02 01 02 02 02 02 01 02 02 02 02 01 02 02 02 02 02 02 01 02 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 00 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 02 02 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 01 02 02 02 01 02 02 01 01 01 02 02 01 01 02 02 02 02 02 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"

        if isinstance(ccp_value, str):
            ccp_data = ccp_value.replace(' ', "")
            ccp_data_list = [int(ccp_data[i:i + 2], 16) for i in range(0, len(ccp_data), 2)]
        elif isinstance(ccp_value, (list, tuple)):
            ccp_data_list = list(ccp_value)
        else:
            assert 0, "ccp 数据格式不对，本应为列表或者字符串"
        # logger.info(f'写入的的ccp={bytes(ccp_data_list).hex()}')
        if ccp_data_list[0:3] == [0x2E, 0XF1, 0X06]:
            ccp_data_list = ccp_data_list[3:ccp_len + 3]

        # 处理是多少v
        ccp_data_list[949] = vehicle_model.value
        ccp_data_list[961] = vehicle_mca.value
        write_ccp_value = copy.deepcopy(ccp_data_list)
        if vehicle_model == VehicleType.Mars and vehicle_mca == VehicleMca.Mca_400v:
            string = f"需要写入车型是 Mars MCA 400v "
            logger.info(string)
        elif vehicle_model == VehicleType.Mars and vehicle_mca == VehicleMca.Mca_800v:
            string = f"需要写入车型是 Mars MCA 800v "
            logger.info(string)
            if self.bgm_version_release < 200:
                # v200 版本以前没有 800v的项目
                logger.warning("v200 版本以前没有 800v的项目")
                assert 0, "v200 版本以前没有 800v的项目"
        elif vehicle_model == VehicleType.Venus and vehicle_mca == VehicleMca.Mca_400v:
            string = f"需要写入车型是 Venus MCA 400v"
            logger.info(string)
        elif vehicle_model == VehicleType.Venus and vehicle_mca == VehicleMca.Mca_800v:
            string = f"需要写入车型是 Venus MCA 800v "
            logger.info(string)
            if self.bgm_version_release < 200:
                # v200 版本以前没有 800v的项目
                logger.warning("v200 版本以前没有 800v的项目")
                assert 0, "v200 版本以前没有 800v的项目"

        # 写入
        with allure.step(f'写入{vehicle_model.name} {vehicle_mca.name}'):
            self.sd_tester.write_ccp_value(write_ccp_value)
            time.sleep(5)
            self.sd_tester.reset_bgm()
        #
        ret_vehicle_model, ret_vehicle_mca = self.sd_tester.get_vehicle_model()
        assert vehicle_model.value == ret_vehicle_model and vehicle_mca.value == ret_vehicle_mca, "写入ccp的和读取的不一致"

    def exit_crash(self):
        curren_car_mode = self.bus_comm.get_car_mode_status()
        if curren_car_mode == 3:
            #crash下需要等待15s，防止后续解闭锁报错
            time.sleep(15)
            self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
            self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
            self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
            self.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
            self.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)


            
        
    def back_ccp_status_to_Idle(self):
        self.ssh.rm_ccp_persist()
        self.sd_tester.reset_bgm()
        self.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        time.sleep(15) #删除持久文件回idel时，为避免72H上报CCP和下发FOD任务冲突
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State, target_status=CCPMasteSts.IDLE.value, timeout=150), "CCP Status ≠ Idle"
        
    def rain_auto_windows(self):
        self.set_common_precontion()
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(0.5)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.wakeup_lin1()
        sleep(1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
    
    def set_keep_power_by_source_and_check_notify(self, flag:KeepPowerFlag, source: str = "PetMode"):
        #flag: 0 open, 1 close_服务， 2 close_hvsoc , 3 close_gear, 4 close_carmode, 5 close_fota, 6 close_other
        if flag.value == 0:
            self.soa.send_method_request(
                'VehicleSetStatusService_client', "SetParkingComfortBaseFunctionByApp", {"cmd": {'modeSts': 1, 'source': source}}
            )
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 255})
        elif flag.value == 1:
            self.soa.send_method_request(
                'VehicleSetStatusService_client', "SetParkingComfortBaseFunctionByApp", {"cmd": {'modeSts': 0, 'source': source}}
            )
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 2:
            self.bus_comm.set_singal("propulsioncan", "EcmPropFr04", "DispHvBattLvlOfChrg", 19.0)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 3:
            self.bus_comm.set("propulsioncan", "EcmPropFr24", "GearLvrIndcn_1_EcmPropSignalIPdu24", 2)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 4:
            self.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 5:
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        elif flag.value == 6:
            self.soa.send_method_request('VehicleModeService_client','SetUsageModeDown', {"mode": 1},)
            self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        else:
            logger.info(f"非预期的flag{flag}")

    def set_ccp(self,ccp_vlaue:dict):
        self.sd_tester.write_ccp(ccp_vlaue)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(10)

    def set_control_power_door_precondition(self, doorid:DoorPos, door_status: DoorStatus):
        with allure.step(f"设置{doorid.name}开关状态为{door_status.name}"):
            logger.info(f"设置{doorid.name}开关状态为{door_status.name}")
            if doorid.name == "Dirver":
                if door_status.name == "kOpened":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Opened)

                elif door_status.name == "kClosed":
                    self.io.set_door(Drvr=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Closed)

                elif door_status.name == "kClosing":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgIn)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Closing)

                elif door_status.name == "kOpening":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Opening)

                else:
                    logger.warning(f"当前侧门状态不支持无需控制")
                    
            elif doorid.name == "Pass":
                if door_status.name == "kOpened":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Opened)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(Pass=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Closed)

                elif door_status.name == "kClosing":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgIn)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Closing)

                elif door_status.name == "kOpening":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgOut)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Opening)
                else:
                    logger.warning(f"当前侧门状态不支持无需控制")

            elif doorid.name == "RearLeft":
                if door_status.name == "kOpened":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Opened)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(LeRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 2)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Closed)
                    
                elif door_status.name == "kClosing":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgIn)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Closing)

                elif door_status.name == "kOpening":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOut)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Opening)
                else:
                    logger.warning(f"当前侧门状态不支持无需控制")

            elif doorid.name == "RearRight":
                if door_status.name == "kOpened":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Opened)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(RiRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 2)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Closed)
                    
                elif door_status.name == "kClosing":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgIn)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Closing)

                elif door_status.name == "kOpening":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Opening)
                else:
                    logger.warning(f"当前侧门状态不支持无需控制")

            elif doorid.name == "All":
                if door_status.name == "kOpened":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Opened)
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Opened)
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Opened)
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Opened)
                    sleep(.5)

                elif door_status.name == "kClosed":
                    self.io.set_door(Drvr=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontLeft, DoorMoveStatus.Closed)
                    self.io.set_door(Pass=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorFrontRight, DoorMoveStatus.Closed)
                    self.io.set_door(LeRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 2)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearLeft, DoorMoveStatus.Closed)
                    self.io.set_door(RiRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 2)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
                    self.soa.notify_and_get_door_movests(DoorId.kDoorRearRight, DoorMoveStatus.Closed)
                else:
                    logger.warning(f"当前侧门状态不支持无需控制")

    def check_stop_light_flicker(self, num=3):
        promt_info = f"--------------->Check 刹车灯闪烁，检查3次"
        with allure.step(promt_info):
            logger.info(promt_info)
            for i in range(num):
                self.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
                self.check_brake_light_sts(sts=ExtrLtgSts.On)
                time.sleep(0.15)
                self.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
                self.check_brake_light_sts(sts=ExtrLtgSts.Off)
    
    def read_check_e2e_excel(self, excel_path, **kwargs):
        '''
        读取需要校验的e2e的信息表
        根据bgm的版本去匹配使用哪个版本的表

        @param excel_path: 表的路径
        @param kwargs:
        @return:
        '''

        bgm_info_dict = self.ssh.bgm_ssh.get_version()
        version_release = bgm_info_dict.get("version_release", None)
        # 获取路径下所有文件
        files = [f[:-5] for f in os.listdir(excel_path) if f.endswith("xlsx")]
        files.sort()
        files.reverse()
        logger.info(f"获取的到 文件夹{files}")
        if version_release is None:
            # 取最新的表
            csv_file_name = files[0]
            logger.info(f"当前 BGM 版本未知，默认获取最新的e2e表 {csv_file_name}.xlsx")

        else:
            if version_release in files:
                csv_file_name = version_release
                logger.info(f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件存在")
            else:
                # 如果不在 取大版本下最新的，如果都不在则取最新的
                bgm_ver_list = version_release.split(".")[:-1]
                bgm_ver = ".".join(bgm_ver_list)
                for item in files:
                    if item.startswith(bgm_ver):
                        csv_file_name = item
                        string = f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件不存在,采用临近{item}.xlsx"
                        logger.error(string)
                        break
                else:
                    csv_file_name = files[0]
                    string = f"当前 BGM 版本{version_release}，对应{version_release}.xlsx 文件不存在,采用最新{csv_file_name}.xlsx"
                    logger.error(string)
        # 判断通信矩阵是否存在
        excel_file = os.path.join(excel_path, f"{csv_file_name}.xlsx")
        if not os.path.exists(excel_file):
            new_file = files[0]
            string_log = f"对应{version_release}版本的e2e表{excel_file}》》不存在，则使用最新{new_file}"
            logger.error(string_log)
            # 不存在则用默认用最新的
            excel_file = os.path.join(excel_path, f"{new_file}.xlsx")
            # assert 0, string_log

        # 读取excel文件
        t1 = time.time()
        workbook = xlrd.open_workbook(excel_file)
        logger.info(f"读取诊断路由表耗时{time.time() - t1}")
        table = workbook.sheet_by_name('e2e_data_info')
        header_list = [
            item.strip().replace(" ", "").lower() for item in table.row_values(0)
        ]
        data_info_list = []
        # 便利该表，使用nrows，和ncols代表当前表的有效行列数。
        for row in range(1, table.nrows):
            row_data = [str(item) for item in table.row_values(row)]
            data_info = dict(zip(header_list, row_data))
            data_info_list.append(data_info)
        return data_info_list

    def check_e2e_func(self, data_list, **kwargs):
        '''
        校验e2e 是否正常
        @param data_list:
        @param kwargs:
        @return:
        '''
        error_list = []
        count = len(data_list)
        string = f"总共{count} 带e2e的信息"
        self.log_and_allure_step(string, LogLevel.INFO)
        for index, item in enumerate(data_list):
            signalname = item.get('signalname')
            targetmsgname = item.get('targetmsgname')
            targetbus = item.get('targetbus')
            portrx = item.get('portrx')

            string_log = f"共{count}条 第{index + 1}条 BGM 通过{targetbus} 发给{portrx} msg_nme={targetmsgname} signalname={signalname}"
            logger.info(string_log)
            try:
                # 接收bgm 发出的信号
                captured_msgdata = self.bus_comm.recv_pdu(targetbus, targetmsgname, timeout=5)
                logger.info(f'接收到bgm发出的数据为 {captured_msgdata}')
                result, actual_crc, expected_crc = self.bus_comm.check_crc_from_pdu(targetbus, targetmsgname,
                                                                                    signalname,
                                                                                    captured_msgdata[-1],
                                                                                    do_assert=False)
                if actual_crc != expected_crc:
                    string_log = f"》》》》失败《《《《  第{index + 1}条 BGM 通过{targetbus} 发给{portrx} actual_crc={actual_crc}, expected_crc={expected_crc}  msg_nme={targetmsgname} signalname={signalname}"
                    self.log_and_allure_step(string_log, LogLevel.ERROR)
                    error_list.append(item)
                else:
                    string_log = f"成功 第{index + 1}条 BGM 通过{targetbus} 发给{portrx} actual_crc={actual_crc}, expected_crc={expected_crc}  msg_nme={targetmsgname} signalname={signalname}"
                    self.log_and_allure_step(string_log, LogLevel.INFO)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                string_log = f"》》》》失败《《《《  第{index + 1}条 BGM 通过{targetbus} 发给{portrx}   msg_nme={targetmsgname} signalname={signalname} erroe>>{str(e)}"
                self.log_and_allure_step(string_log, LogLevel.ERROR)
                error_list.append(item)

        assert not len(error_list), f"总共有{len(error_list)}未校验通过"

    def set_open_close_door_precondition(self, doorid:DoorPos, door_status: DoorStatus):
        with allure.step(f"设置{doorid.name}开关状态为{door_status.name}"):
            logger.info(f"设置{doorid.name}开关状态为{door_status.name}")
            if doorid.name == "Dirver":
                if door_status.name == "kOpened":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)

                elif door_status.name == "kClosed":
                    self.io.set_door(Drvr=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)

                elif door_status.name == "kClosing":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgIn)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True,antipinch=False)

                elif door_status.name == "kOpening":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opening,isopen=True, antipinch=False)
                    
                else:
                    logger.warning(f"当前侧门状态异常")
                    
            elif doorid.name == "Pass":
                if door_status.name == "kOpened":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(Pass=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                   
                elif door_status.name == "kClosing":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgIn)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True, antipinch=False)

                elif door_status.name == "kOpening":
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgOut)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opening,isopen=True, antipinch=False)
                else:
                    logger.warning(f"当前侧门状态异常")

            elif doorid.name == "RearLeft":
                if door_status.name == "kOpened":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(LeRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 2)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                    
                elif door_status.name == "kClosing":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgIn)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True, antipinch=False)

                elif door_status.name == "kOpening":
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOut)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opening, isopen=True, antipinch=False)
                    
                else:
                    logger.warning(f"当前侧门状态异常")

            elif doorid.name == "RearRight":
                if door_status.name == "kOpened":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    
                elif door_status.name == "kClosed":
                    self.io.set_door(RiRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 2)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed, isopen=False, antipinch=False)
                   
                elif door_status.name == "kClosing":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgIn)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True, antipinch=False)
                    
                elif door_status.name == "kOpening":
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening,isopen=True, antipinch=False)
                else:
                    logger.warning(f"当前侧门状态异常")

            elif doorid.name == "All":
                if door_status.name == "kOpened":
                    self.io.set_door(Drvr=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    self.io.set_door(Pass=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    self.io.set_door(LeRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    self.io.set_door(RiRe=Door.open)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False)
                    sleep(.5)

                elif door_status.name == "kClosed":
                    self.io.set_door(Drvr=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)  
                    self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                    self.io.set_door(Pass=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)  
                    self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                    self.io.set_door(LeRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 2)  
                    self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                    self.io.set_door(RiRe=Door.close)
                    self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 2)  
                    self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
                    self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)
                else:
                    logger.warning(f"当前侧门状态异常")
    
    def cycle_write_ccp(self,json_data,v1,v2,bus_name,id):
        for i in json_data:
            ccp_id=i['ccp_id']
            if v1<= ccp_id <= v2:
                userful_value=i['userful_value'].split('/')
                for j in userful_value:
                    userful_value_hexint = int(j,16)
                    self.sd_tester.write_ccp({ccp_id: int(j,16)})
                    before_time = time.time()
                    while(time.time() - before_time >=9 ):
                        captur_packet=self.bus_comm.recv_pdu(bus_name,id)
                        if captur_packet:
                            group_id= ccp_id/7 if ccp_id % 7 ==0 else  ccp_id/7 +1
                            if captur_packet[0] == group_id:
                                ccp_pos = (ccp_id) -(group_id -1 )*7  -1 
                                assert captur_packet[ccp_pos]==userful_value_hexint ,f'写入的ccp:{hex(ccp_id)}与总线上面的值不符和'
    
    def restart_bgm_and_connect_service(self, partner_name, pause_all_bus=True, resume_all_bus=True):
        """
        bgm重启并连接服务
        @param partner_name: 待连接的服务
        @param pause_all_bus: 是否在下电的时候停止总线
        @param resume_all_bus: 是否在上电之后恢复总线
        """
        if pause_all_bus:
            self.bus_comm.pause_all_bus_send()
        sleep(1)  # 下电前等待1s，否则之前的日志可能还没有落盘，造成有效日志丢失
        self.sd_tester.stop_tester_present()
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_data([0x11,0x81])
        self.soa.empty_all()
        if resume_all_bus:
            self.bus_comm.resume_all_bus_send()
        self.soa.wait_for_service_reconnect(partner_name)

    def get_restart_bgm_wait_until_fr_alive_time(self, pause_all_bus=False, resume_all_bus=False, time_out=2):
        """
        获取bgm重启后fr接收到BGM的第一帧数据时间
        @param pause_all_bus: 是否在下电的时候停止总线
        @param resume_all_bus: 是否在上电之后恢复总线
        @param time_out: 接受信号第一帧超时时间为2秒
        @return 返回收到BGM重启后接收到fr的第一帧数据的时间
        """
        if pause_all_bus:
            self.bus_comm.pause_all_bus_send()
        sleep(1)  # 下电前等待1s，否则之前的日志可能还没有落盘，造成有效日志丢失
        self.io.bgm_power_off()
        time.sleep(3)
        self.bus_comm.bus_app.bus_dict["tosun_tc1034"].set_listen_frame_with_0x27(time.time())
        self.bus_comm.bus_app.bus_dict["tosun_tc1034"].set_listen_frame_first_flag_with_0x27(False)
        self.io.bgm_power_on()
        time_start = time.time()
        while not self.bus_comm.bus_app.bus_dict["tosun_tc1034"].listen_frame_first_flag_with_0x27:
            time.sleep(0.001)
            if time.time() - time_start > time_out:
                raise AssertionError(f"在 {time_out}时间内，没有发现BGM发出第一帧fr数据")

        if resume_all_bus:
            self.bus_comm.resume_all_bus_send()

    def set_soc_and_wait_tme_check_keep_power_mode_time(self, soc_value: Union[int, float] = 0, wait_time: Union[int, float] = 0.1, displaytime:DisplayLeftTime=DisplayLeftTime.kUnknown):
        if soc_value != 0:
            self.bus_comm.set_SOC_display_value(soc_value=soc_value)
        time.sleep(wait_time)
        self.soa.check_keep_power_mode_and_time(True, exit_reason=KeepPowerFlag.open, displaytime=displaytime)
        self.check_convenience_mode_duration(255)

    def times_set_soc_and_wait_tme_check_keep_power_mode_time(self, soc_sz = [], displaytimesz = []):
        displaytime_sz= [DisplayLeftTime.kUnknown, DisplayLeftTime.kCharging, DisplayLeftTime.kCalulating, DisplayLeftTime.kWithin15Min, DisplayLeftTime.kWithin30Min, DisplayLeftTime.kWithin1Hour,
        DisplayLeftTime.kWithin2Hour,DisplayLeftTime.kWithin3Hour,DisplayLeftTime.kWithin4Hour,DisplayLeftTime.kWithin5Hour,DisplayLeftTime.kWithin6Hour,DisplayLeftTime.kWithin7Hour,DisplayLeftTime.kWithin8Hour,
        DisplayLeftTime.kWithin9Hour,DisplayLeftTime.kWithin10Hour,DisplayLeftTime.kWithin11Hour,DisplayLeftTime.kWithin12Hour,DisplayLeftTime.kWithin13Hour,DisplayLeftTime.kWithin14Hour,DisplayLeftTime.kWithin15Hour,
        DisplayLeftTime.kWithin16Hour,DisplayLeftTime.kWithin17Hour,DisplayLeftTime.kWithin18Hour,DisplayLeftTime.kWithin19Hour,DisplayLeftTime.kWithin20Hour,DisplayLeftTime.kWithin21Hour,DisplayLeftTime.kWithin22Hour,
        DisplayLeftTime.kWithin23Hour,DisplayLeftTime.kWithin24Hour,DisplayLeftTime.k24HourPlus]
        k = len(soc_sz)
        for i in range(k):
            self.set_soc_and_wait_tme_check_keep_power_mode_time(soc_value=soc_sz[i], wait_time = 30, displaytime = displaytime_sz[displaytimesz[i]])

    def set_fota_rescue_condition(self, gear: Union[Gear, None], hv_actice_sts: HVActiveSts, display_hv_soc: Union[int, float]):
        self.bus_comm.set_gear_pos(gear,ParkLockSts.ParkNotEngd)
        self.bus_comm.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', display_hv_soc)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', hv_actice_sts.value)
        logger.info(f"成功设置挡位为{gear}\n成功设置高压状态为{hv_actice_sts}\n成功设置高压电池显示的SOC值为{display_hv_soc}")

    def diag_not_change_car_mode(self, mode_type: int, do_assert=True, **kwargs):
        '''
        前置条件不满足时不能切换 car mode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        # 读取did
        ret_code, local_date = self.sd_tester.send_request_and_recv_response([0x22, 0xD1, 0x34])
        logger.info(f'------------------->{ret_code}')
        curr_mode = local_date[3:]
        if curr_mode == mode_type:
            return curr_mode
        # 检查当前会话，判断是否需要重新进入
        ret_code, local_date = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x86])
        curr_status = local_date[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            ret_code, local_date = self.sd_tester.send_request_and_recv_response([0x10, 0x03])
            if do_assert and local_date[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level(level=3)
        else:
            # 判断是否需要解锁
            ret_code, local_date = self.sd_tester.send_request_and_recv_response([0x27, 0x03])
            curr_le = local_date[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level(level=3)
        # 设置 car 模式
        send_data = [0x2F, 0xD1, 0x34, 0x03, mode_type]
        self.sd_tester.send_data(send_data)
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        assert result[0] != 0x6F, '不应切换成功'

    def set_parkingComfortMode(self, parkingComfortMode: bool=None):
        if parkingComfortMode is None:
            pass
        elif parkingComfortMode:
            self.bus_comm.set_vehmtn()
            self.bus_comm.set_vehspd()
            self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
            self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
            time.sleep(1)
            self.sd_tester.write_ccp(ccp={566: 25})
            self.bus_comm.set_dtc_pre()
            self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
            self.bus_comm.set_charging_sts(ChargingSts.Default)
            self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
            self.bus_comm.set_gear_pos(gear=Gear.Park)
            self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
            self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
            self.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
            self.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)    
            self.set_usage_mode(UsageMode.CONVENIENCE)
            time.sleep(1)
            self.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
            time.sleep(1)
            self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
            self.check_convenience_mode_duration(255)
            assert self.soa.send_request_and_return_resp(
                    'VehicleSetStatusService_client', "GetParkingComfortModeSts", {}
                )['out']['modeSts'] == 1
        else:
            self.bus_comm.set_vehmtn()
            self.bus_comm.set_vehspd()
            self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
            self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
            time.sleep(1)
            self.sd_tester.write_ccp(ccp={566: 25})
            self.bus_comm.set_dtc_pre()
            self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
            self.bus_comm.set_charging_sts(ChargingSts.Default)
            self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
            self.bus_comm.set_gear_pos(gear=Gear.Park)
            self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
            self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
            self.set_usage_mode(UsageMode.CONVENIENCE)
            time.sleep(1)
            self.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
            time.sleep(0.3)
            self.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
            time.sleep(1)
            self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_service)
            self.check_convenience_mode_duration(0)
            assert self.soa.send_request_and_return_resp(
                    'VehicleSetStatusService_client', "GetParkingComfortModeSts", {}
                )['out']['modeSts'] == 0
            
    def set_normal_fota_update_condition_new(self, vehspd: Union[int, float], gear: Union[Gear, None], display_hv_soc: Union[int, float], thermaloutofcontrol: bool, 
                                             low_volt_soc: Union[int, float], is_jidu_charger: bool, local_diag_sts: DiagActLineSts, usage_mode: UsageMode, 
                                             is_hw_ver_match: bool, maintenance_mode_sts: bool, park_comfort_mode_sts: bool, pet_mode_sts: str):
        self.bus_comm.set_vehspd(vehspd)
        logger.info(f"成功设置车速为{vehspd}")

        self.bus_comm.set_gear_pos(gear,ParkLockSts.ParkNotEngd)
        logger.info(f"成功设置挡位为{gear}")

        display_hv_soc  *= 10
        self.bus_comm.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', display_hv_soc)
        logger.info(f"成功设置高压电池显示的SOC值为{display_hv_soc}")

        # TODO, 连续调用set_JiduCharger会报错，等待更新
        # self.set_JiduCharger(is_jidu_charger)
        # logger.info(f"成功设置集度充电桩")

        pdu_data_map = {
            50: [0xF4, 0x01, 0xB4, 0x00, 0x00, 0x00, 0x00],
            69: [0xB2, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            70: [0xBC, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            71: [0xC6, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            90: [0x84, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
        }
        if low_volt_soc in pdu_data_map:
            self.bus_comm.ipdu.send_pdu("cem_lin6", 0x06, pdu_data_map[low_volt_soc])
            logger.info(f"成功设置小电池电量SOC值为{low_volt_soc}")
        else:
            logger.error(f"不合法的小电池电量SOC值：{low_volt_soc}，请在 [50, 69, 70, 71, 90] 中进行选择")
        
        diag_sts_map = {
            DiagActLineSts.DisActive: self.io.bgm_diag_line_down,
            DiagActLineSts.Active: self.io.bgm_diag_line_up
        }
        if local_diag_sts in diag_sts_map:
            diag_method = diag_sts_map[local_diag_sts]
            diag_method()
            logger.info(f"成功设置本地诊断状态为：{local_diag_sts}")
        
        if thermaloutofcontrol:
            self.bus_comm.ipdu.send_pdu("propulsioncan", 0x142, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        else:
            self.bus_comm.ipdu.send_pdu("propulsioncan", 0x142, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        logger.info(f"成功设置电池热失控状态为：{thermaloutofcontrol}")
        time.sleep(3)

        self.soa.set_maintenanceMode(maintenance_mode_sts)
        logger.info(f"成功设置维修模式状态为{maintenance_mode_sts}")

        self.set_parkingComfortMode(park_comfort_mode_sts)
        logger.info(f"成功设置维持上电模式状态为{park_comfort_mode_sts}")

        self.soa.update_InteractiveService_response(pet_mode_sts)
        logger.info(f"成功设置宠物模式状态为{pet_mode_sts}")

        self.set_usage_mode(usage_mode)
        if usage_mode in (UsageMode.DRIVING, UsageMode.ACTIVE):
            self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetUsageModeDownCb:result:1', timeout=60)
        logger.info(f"成功设置usagmode为{usage_mode}")
        
        time.sleep(.5)
    
    
    def set_JiduCharger(self, is_JiduCharger: bool=None):
        if is_JiduCharger is None:
            pass
        elif is_JiduCharger:
            self.bus_comm.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 2)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 2)   
            time.sleep(0.5)
            assert 2 not in self.soa.send_request_and_return_resp("HighVoltageService_client", "getEquipmentInfo", {})["out"]["equipmentTypes"], "Not Equip with JiduCharger"
            # self.bus_comm.ipdu.resume_all_bus_send()
        else:
            self.bus_comm.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 0)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 0)
            # self.partner.empty_all(1)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
            # logger.info(f"---发送信号={X}")
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 1)
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 1)       
            sleep(0.5)            
            assert 2 in self.soa.send_request_and_return_resp("HighVoltageService_client", "getEquipmentInfo", {})["out"]["equipmentTypes"], "Equip with JiduCharger"
            # self.bus_comm.ipdu.resume_all_bus_send()

    def set_wiper_test_before(self,usagemode,carmode,wash_func_sts,maintain_pos,wiper_mode):
        self.set_common_precontion(usage_mode=usagemode, car_mode=carmode,)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)
    
    def check_wipe_safety_monitor_on_500385(self,wipe_mode):
        if wipe_mode == "high":
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
            self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
            
        elif wipe_mode == "low":
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
            self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
        elif wipe_mode == "active_wiper_washer":
            with allure.step("进入扩展会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
            with allure.step("通过安全访问L5"):
                self.sd_tester.security_access_level(UnLock.L5)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x02],recv=[0x6F, 0x42, 0X0A])
            self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x00],recv=[0x6F, 0x42, 0X0A])
            
    def check_wipe_safety_monitor_off_500385(self,wipe_mode):
        if wipe_mode == "high":
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
            self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
            
        elif wipe_mode == "low":
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
            self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
        elif wipe_mode == "active_wiper_washer":
            with allure.step("进入扩展会话"):
                self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
            with allure.step("通过安全访问L5"):
                self.sd_tester.security_access_level(UnLock.L5)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x02],recv=[0x6F, 0x42, 0X0A])
            self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
            sleep(2)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
            self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x00],recv=[0x6F, 0x42, 0X0A])
            
    def check_fota_setStartInhibit(self, 
                                   startInhibit: bool = False):
        if startInhibit is not None:
            if startInhibit:
                with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='OnSetStartInhibitCb', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='OnSetStartInhibitCb', timeout=10):
                    pass
        return True  
    
    def set_rear_defrost_sts(self, sts: bool):
        promt_info = f"----------------> 设置并且检测后除霜状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
            self.sd_tester.change_car_mode(CarMode.NORMAL)
            self.sd_tester.write_multi_ccp({182: 0x3, 13: 0x4})        
            self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideQly",3)
            self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideAmbTVal",320.0)
            self.bus_comm.set("bodycan","DdmBodyFr02","MirrDefrstAtDrvSts",1)
            self.bus_comm.set("bodycan","PdmBodyFr03","MirrDefrstAtPassSts",1)
            
            if sts == "True":
                self.soa.hmi_set_outview_heat_mode(sts=True)
                self.bus_comm.check("bodycan","CcmBodyFr25","ElecDefrstReqWinDefrstReReq",1) 
                
            elif sts == "False":
                self.soa.hmi_set_outview_heat_mode(sts=False)
                self.bus_comm.check("bodycan","CcmBodyFr25","ElecDefrstReqWinDefrstReReq",0) 

    def set_and_check_findkey_sts(self, sts: bool):
        promt_info = f"----------------> 发出寻钥匙请求为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
         
            if sts == "True":
                self.soa.set_findkey_req(findzone=FindZone.ZoneAllInSide)      
                self.bus_comm.check_keysearch_req(key_zone=KeyZone.KeyLocnAllInt)
                self.soa.set_findkey_req(findzone=FindZone.ZoneAllOutSide)      
                self.bus_comm.check_keysearch_req(key_zone=KeyZone.KeyLocnAllExt)   
                
            elif sts == "False":
                self.soa.set_findkey_req(findzone=FindZone.ZoneNa)      
                self.bus_comm.check_keysearch_req(key_zone=KeyZone.KeyLocnIdle)

    def update_version_debug_bridge(self, task_id: int, domain_need_flushed_list: list = [{"SWPN": "6160110200 AA,2960110200 BB", "name": "BGM"}]):
        with open('config/UA_conf.yaml', 'r') as f:
            data = yaml.safe_load(f)
        if len(domain_need_flushed_list) == 1:
            version_debug = data['Version_Debug_BGM']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["baseLineVer"] = '6100000200CCC'
            domian_name = domain_need_flushed_list[0]['name']
            version_debug["data"]["ecu"][0]["name"] = domian_name
            version_debug["data"]["ecu"][0]["SWPN"] = domain_need_flushed_list[0]['SWPN']
            if domian_name == "BGM":
                version_debug["data"]["ecu"][0]["HWPN"] = self.sd_tester.get_bgm_hard_version()
            elif domian_name == "TCAM":    
                version_debug["data"]["ecu"][0]["HWPN"] = self.sd_tester.get_tcam_hard_version()
            elif domian_name == "CDC":
                version_debug["data"]["ecu"][0]["HWPN"] = '6608010818  F'
            else:
                logger.error(f"Not Support {domian_name}")
        elif len(domain_need_flushed_list) == 2:
            version_debug = data['Version_Debug_Two_Domain']
            version_debug["data"]["taskId"] = task_id
            version_debug["data"]["baseLineVer"] = '6100000200CCC'
            for i in range(2):
                version_debug["data"]["ecu"][i]["name"] = domain_need_flushed_list[i]['name']
                version_debug["data"]["ecu"][i]["SWPN"] = domain_need_flushed_list[i]['SWPN']
                current_ecu = version_debug["data"]["ecu"][i]
                ecu_name = current_ecu["name"]
                if ecu_name == "BGM":
                    current_ecu["ecuId"] = '6011'
                    current_ecu["HWPN"] = self.sd_tester.get_bgm_hard_version()
                elif ecu_name == "TCAM":
                    current_ecu["ecuId"] = '1011'
                    current_ecu["HWPN"] = self.sd_tester.get_tcam_hard_version()
                elif ecu_name == "CDC":
                    current_ecu["ecuId"] = '3011'
                    current_ecu["HWPN"] = '6608010818  F'
                elif ecu_name == "PDM":
                    current_ecu["ecuId"] = '6031'
                    current_ecu["HWPN"] = '8892362699  A'
                else:
                    logger.error(f"Not Support: {ecu_name}")
        else:
            logger.error(f"Not Support version_debug lenth: {len(domain_need_flushed_list)}")
        config_json = json.dumps(version_debug).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{config_json}" > /update/version_debug.json')
        time.sleep(0.2)

    def set_lock_unlock_visible_feedback_precondition(self,lockstate:LockState, time_wait = 0):
        prompt_info = f"---------->设置当前{lockstate.name}灯效反馈前置条件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.io.set_five_door_sts(Door.close)
            self.io.set_hood_sts(HoodSts.Close)
            if lockstate.name == "UnLock":
                self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Unlckd, time_wait=0.5)
              
            elif lockstate.name == "Lock":
                self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Lockd, time_wait=0.5)

            elif lockstate.name == "SafeLock":
                self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.SafeLockd, time_wait=0.5)
            
            else:
                logger.info(f"The request type is not supported")
                assert False
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)     
    def check_remoteRescue_wakeup_and_Inhibit(self,
                              pnc29: bool = False, 
                              acu_keep_alive: bool = False,
                              up_inactive: bool = False,
                              hv_active: bool = False,
                              startInhibit: bool = False,
                              ):
        if pnc29 is not None:
            if pnc29:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='VfcType :23', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", unexpect_keywords='VfcType :23', timeout=10):
                    pass
        if acu_keep_alive is not None:
            if acu_keep_alive:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='KeepAliveCb', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", unexpect_keywords='KeepAliveCb', timeout=10):
                    pass
        if up_inactive is not None:
            if up_inactive:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='SetUsageModeUpAsyncCb', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", unexpect_keywords='SetUsageModeUpAsyncCb', timeout=10):
                    pass
        if hv_active is not None:
            if hv_active:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='OnSetOutputCb Fail_Type:0', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", unexpect_keywords='OnSetOutputCb Fail_Type:0', timeout=10):
                    pass
        if startInhibit is not None:
            if startInhibit:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='OnSetStartInhibitCb', timeout=10):
                    pass
            else:
                with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", unexpect_keywords='OnSetStartInhibitCb', timeout=10):
                    pass
        return True 

    def set_seat_occpt_sts(self, occupysts: OccupySts,  time_wait = 0):
        promt_info = f"设置座椅占位状态为{occupysts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if occupysts.name == "NotOccupied":
                self.io.driver_seat_notpresent()
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","PassSeatSts", 0) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecLe", 0) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecMid", 0) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecRi", 0) 
            elif occupysts.name  == "Occupied":
                self.io.driver_seat_present()
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","PassSeatSts", 2) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecLe", 2) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecMid", 2) 
                self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecRi", 2) 

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def update_skip_debug_nokill(self, debug_list: list):
        if not debug_list:
            self.type_commands(DeviceName.BGM, f'echo -n "[]" > /update/skip_debug')
            time.sleep(0.5)
        else:
            debug_str = str(debug_list).replace('\'', '\\"').replace(',', ',\n')
            self.type_commands(DeviceName.BGM, f'echo -e "{debug_str}" > /update/skip_debug')
            time.sleep(0.5)
    
    def set_usagemode_inactive_to_convenience(self, set_usagemode_type: set_usagemode_type, check_selftest_flag: bool = False, time1:int = 1, selftest_fail1_flg:bool = False, selftest_fail2_flg:bool = False):
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        if set_usagemode_type.value == 0:
            self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeUp', {"mode": UsageMode.CONVENIENCE.value})
        elif set_usagemode_type.value == 1:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.io.set_door(Drvr=Door.open)
        elif set_usagemode_type.value == 2:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.io.set_door(Pass=Door.open)
        elif set_usagemode_type.value == 3:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.io.set_door(LeRe=Door.open)
        elif set_usagemode_type.value == 4:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.io.set_door(RiRe=Door.open)    
        elif set_usagemode_type.value == 5:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.io.driver_seat_present()
        elif set_usagemode_type.value == 6:
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.bus_comm.set_brake_pedal()
        elif set_usagemode_type.value == 7:
            self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
            self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
            self.soa.send_method_request(
            'VehicleSetStatusService_client', "SetConvenienceForAppAction", {"time": time1}
        )
        if check_selftest_flag:
            self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
            self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
            self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
            if selftest_fail1_flg:
                logger.info(f"成功上切convenience,且自检相关信号满足预期")
            else:
                time.sleep(0.3)
                self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
                self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.Reqd)
                self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
                if selftest_fail2_flg:
                    logger.info(f"成功触发自检上切Active,且自检相关信号满足预期")
                else:
                    time.sleep(5.5)
                    self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
                    self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
                    self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
        else:
            time.sleep(6) 
            self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    def wait_time_in_chrgild_req(self, num: int, req: ChrgLidReq):
        for i in range(num):
            self.bus_comm.check_chrgild_req(req)
            time.sleep(0.1)
            logger.info(f'当前时间为{0.1*i}s')

    def vehicle_sleep(self):
        time_start = time.time()
        while True:
            UsageMode = self.tsp.get_tcam_power_status()
            logger.info("当前车辆状态为：{}".format(UsageMode["powerStatus"]))
            time_end = time.time()
            if UsageMode["powerStatus"] == 2:
                sleep(20)
                break
            elif time_end - time_start > 1200:
                logger.info("车辆长时间未休眠")
                assert False
            else:
                time.sleep(30)
    
    def kill_s2s_and_reconnect_service(self, partner_key=None):
        """
        kill S2S进程，等待EM2拉起S2S并等待partner重新连接服务
        仅用于SIL环境测试
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """
        self.ssh.rerun_bgm_process(BgmApp.s2s_service)
        self.soa.empty_all()
        if partner_key is not None:
            self.soa.wait_for_service_reconnect(partner_key)
    
    def update_bgm_s2s_json(self, update_info: dict, partner_key=None):
        """
        更新本地s2s.json文件，并同步更新bgm的s2s.json并落盘
        仅用于SIL环境测试
        @param update_info: 更新的字段内容
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """
        write_s2s_json(update_info)
        self.ssh.bgm_ssh.scp_local_file_to_bgm(s2s_path, bgm_path="/app/etc/")
        self.ssh.bgm_ssh.type_commands("sync")
        self.ssh.bgm_ssh.type_commands("cat /app/etc/s2s.json")
        self.kill_s2s_and_reconnect_service(partner_key)

    def set_and_get_wash_mode_sts(self, sts: isOn, time_wait = 0):
        promt_info = f"设置洗车模式状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if sts.name == "On":
                self.soa.hmi_set_wash_mode(sts=isOn.On)
                self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr21", 'WashModeSts', 1)
            elif sts.name == "Off":
                self.soa.hmi_set_wash_mode(sts=isOn.Off)
                self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr21", 'WashModeSts', 0)
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def set_inside_open_door_flag(self, scene: VehicleInsideOutside,  time_wait = 0):
        promt_info = f"设置开门方式为{scene.name}方式"
        with allure.step(promt_info):
            logger.info(promt_info)
            if scene.name == "VehicleInSide":
                self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
                self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
                self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
                self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
            elif scene.name == "VehicleOutSide":
                self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
                self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleOutSide)
                self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI)
                self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def set_and_check_door_resist_cmd(self, resist: ResistMode, time_wait: Union[float, int] = 1):
        if resist.name == "CloseDoor":
            with allure.step(f'通过关闭四门撤销开门阻力'):
                logger.info(f'通过关闭四门撤销开门阻力')
                self.io.set_door(Drvr= Door.close, Pass= Door.close, LeRe= Door.close, RiRe= Door.close)
                self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
                self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
                
        elif resist.name == "DoorOpenWarning":
            with allure.step(f'通过清除侧方开门保护撤销开门阻力'):
                logger.info(f'通过清除侧方开门保护撤销开门阻力')
                self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NotUsed, time_wait=2)
                self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
                self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
        
    def check_upload_log_to_cloud_consistency(self, ecu_name: str = 'bgm', duration: int = 1800):
        def extract_json_or_return_line(line):
            start_index = line.find('{')
            end_index = line.find('}')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                try:
                    json_content = line[start_index:end_index + 1]
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    return line
            return line

        def filter_log_with_keywords_and_extract_json(lines, keywords):
            # with open(log_file_path, 'r') as file:
            lines = lines.splitlines()
            filtered_lines = {}
            for line in lines:
                for keyword in keywords:
                    if keyword in line:
                        filtered_content = extract_json_or_return_line(line.strip())
                        if keyword in filtered_lines:
                            filtered_lines[keyword].append(filtered_content)
                        else:
                            filtered_lines[keyword]=[]
                            filtered_lines[keyword].append(filtered_content)
                        break
            uploaded_files = []
            fileinfos = {}
            fileinfo_success = []
            if 'UploadFileList' in filtered_lines:
                for v in filtered_lines['UploadFileList']:
                    if isinstance(v, dict):
                        uploaded_files = v.get('files')
                        logger.info(f"上传的文件列表: {uploaded_files}")
                        break
                if '[UPLOADER]FileInfo' in filtered_lines:
                    for v in filtered_lines['[UPLOADER]FileInfo']:
                        for f in uploaded_files:
                            if f in v:
                                pattern = r'FileInfo:{file=(.*?)\.[^/.]+,size=(\d+),.*?modify_time:(\d+)'
                                match = re.search(pattern, v)
                                # 如果找到匹配项，则提取文件名称和大小
                                if match:
                                    file_name = match.group(1)
                                    file_size = match.group(2)
                                    modify_time = match.group(3)
                                    logger.info(f"文件名称: {file_name}")
                                    logger.info(f"文件大小: {file_size}")
                                    logger.info(f"修改时间: {modify_time}")
                                    fileinfos[file_name]=[file_size, modify_time]
                                else:
                                    logger.warning("未找到文件名称和大小")               
                if '[UPLOADER]Success' in filtered_lines:
                    for v in filtered_lines['[UPLOADER]Success']:
                        for f in uploaded_files:
                            if f in v:
                                fileinfo_success.append(v)
            if 'utimestamp: Log-upload-timestamp:' in filtered_lines:
                utimestamp_str_list = []
                utimestamp_str = filtered_lines['utimestamp: Log-upload-timestamp:']
                for stamp in utimestamp_str:
                    pattern = r'Log-upload-timestamp: (\d+)'
                    match = re.search(pattern, stamp)
                    # 如果找到匹配项，则提取Log-upload-timestamp的值
                    if match:
                        log_upload_timestamp = match.group(1)
                        utimestamp_str_list.append(f"Log-upload-timestamp: {log_upload_timestamp}")
                logger.info(f"上传时间戳列表: {utimestamp_str_list}")  
            return filtered_lines, uploaded_files, fileinfos, fileinfo_success, utimestamp_str_list
        
        if ecu_name == 'bgm':
            log = self.ssh.bgm_ssh.type_commands('/app/bin/zstdcat /log/jetlog_messages | grep RLog')
        elif ecu_name == 'tcam':
            log = self.ssh.tcam_ssh.type_commands('/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages |grep RLog')
        else:
            raise ValueError(f"Invalid ECU name: {ecu_name}. Please use 'bgm' or 'tcam'.")
        keywords=["trigger source", 'UploadFileList', 'utimestamp: Log-upload-timestamp:', '[UPLOADER]FileInfo', '[UPLOADER]Success']
        filtered_lines, uploaded_files, fileinfos, fileinfo_success, utimestamp_str_list = filter_log_with_keywords_and_extract_json(log, keywords)

        # 查询触发方式
        self.tsp.uplaod_log_search_result(index='jidulogapp-staging-*-serverlog', begin_time=int(time.time())-duration, 
                                          fuzzy_query=[filtered_lines.get('trigger source')[0].get("event"), 
                                                       filtered_lines.get('trigger source')[0].get("request_id")])
        # 查询上传时间戳
        for timestamp in utimestamp_str_list:
            self.tsp.uplaod_log_search_result(index='jidulogapp-staging-*-serverlog', begin_time=int(time.time())-duration, fuzzy_query=[timestamp])
        # 查询文件信息，文件名称，大小，修改时间
        for file_name, info in fileinfos.items():
            self.tsp.uplaod_log_search_result(index='jidulogapp-staging-*-serverlog', begin_time=int(time.time())-duration, fuzzy_query=[file_name, info[0], info[1]])
        # 查询文件上传成功信息
        for file_name, info in fileinfos.items():
            self.tsp.uplaod_log_search_result(index='jidulogapp-staging-*-serverlog', begin_time=int(time.time())-duration, fuzzy_query=[file_name, 'success', 'upload'])
    
    def exit_vehicle_inside_person(self):
        logger.info(f"退出车内有人状态")
        self.io.set_door(Drvr=Door.open)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        time.sleep(3)
        self.io.set_door(Drvr=Door.close)
    
    def ck_rvc_DefrostHvRunTime(self, start_time:float, ck_time:int):
        # start_time = time.time()  # 记录开始时间
        while True:
            try:
                self.soa.soa_partner.ck_s2s_req("HighVoltageService_server", "SetOutput", timeout=3)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                logger.error(e)
                current_time = time.time()
                if ck_time < current_time - start_time < 100:
                    logger.info(f"远控参数配置_RemElecDefrostHvRunTime配置有效，RemElecDefrostHvRunTime={current_time - start_time}秒")
                    break
                else:
                    logger.info(f"远控参数配置_RemElecDefrostHvRunTime配置失效，RemElecDefrostHvRunTime={current_time - start_time}秒")
                    assert False
                    
    def clean_soa_all(self, wait_time=0):
        """清空partner所有缓存数据"""
        time.sleep(wait_time)
        logger.info("清除partner所有缓存数据")
        self.sd_tester.write_single_ccp(973, 2)
        self.ssh.type_commands(DeviceName.BGM,"rm -f /data/SOAApp/SOAApp.db3",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"rm -f /data/s2s_service/s2s_service.db3",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"sync",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"ls -l /data/SOAApp/",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"ls -l /data/s2s_service/",timeout=30)
        sleep(3)
        self.sd_tester.reset_bgm()
        self.bus_comm.resume_all_bus_send()
        sleep(10)

    def get_default_time(self): 
        # 获取当前时间
        now = datetime.datetime.now()
        # 获取当前日期
        today = now.date()
        # 设置今天夜晚10点的时间
        night_10pm = datetime.datetime.combine(today, datetime.datetime.min.time())
        night_10pm = night_10pm.replace(hour=22, minute=0, second=0, microsecond=0)
        # 输出结果
        logger.info("今天夜晚10点的时间: %s", night_10pm)
        # 计算明天的时间
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow = tomorrow.date()  # 确保是日期类型
        # 设置明天6点的时间
        tomorrow_night_6am = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())
        tomorrow_night_6am = tomorrow_night_6am.replace(hour=6, minute=0, second=0, microsecond=0)
        # 输出结果
        logger.info("明日6点的时间: %s", tomorrow_night_6am)
        dt = datetime.datetime.strptime(str(night_10pm), "%Y-%m-%d %H:%M:%S")
        # 将datetime对象转换为时间戳
        timestamp = int(time.mktime(dt.timetuple()))
        dt = datetime.datetime.strptime(str(tomorrow_night_6am), "%Y-%m-%d %H:%M:%S")
        # 将datetime对象转换为时间戳
        timestamp1 = int(time.mktime(dt.timetuple()))
        logger.info("今天夜晚10点的时间: %s", timestamp)
        logger.info("明日6点的时间: %s", timestamp1)
        return timestamp,timestamp1


    def write_did_and_check(self,ta:int,did:int,session=SESSION.EMPTY,unlock_level=UnLock.L0,write_data='',check_data='',check_length=0,check_range=[],check_in=[],check_method=Check_Method.reset,recover=True):   
        pass_status = True
        try:
            result_data = None
            did_str = hex(did)[2:].zfill(4)
            raw_data=self.sd_tester.read_did_and_check(ta,did,session)
            unlock_check_data =  '67' if isinstance(ta,int) else  ['67']*len(ta)
            self.sd_tester.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data=unlock_check_data)
            write_data = f'2E{did_str}{write_data}'
            
            with allure.step(f"写入DID:{did_str} 写入值:{write_data}"):
                if check_method == Check_Method.read:
                    wirte_checkdata= f'6e{did_str}' if isinstance(ta,int) else [f'6e{did_str}'] * len(ta)
                    self.sd_tester.send_data_and_check(ta,write_data,wirte_checkdata)
                    time.sleep(0.5)  #写入值后加等待0.5s时间再读 保证值已经被存储
                    result_data=self.sd_tester.read_did_and_check(ta,did,SESSION.EMPTY,check_data,check_length,check_range,check_in)    
                elif check_method == Check_Method.reset:
                    wirte_checkdata= f'6e{did_str}' if isinstance(ta,int) else [f'6e{did_str}'] * len(ta)
                    self.sd_tester.send_data_and_check(ta,write_data,wirte_checkdata)
                    self.sd_tester.reset_0x1181()
                    self.sd_tester.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data='67')
                    result_data=self.sd_tester.read_did_and_check(ta,did,SESSION.EMPTY,check_data,check_length,check_range,check_in)
                elif check_method ==Check_Method.response:
                    result_data=self.sd_tester.send_data_and_check(ta,write_data,check_data)
                elif check_method == Check_Method.kl30:
                    wirte_checkdata= f'6e{did_str}' if isinstance(ta,int) else [f'6e{did_str}'] * len(ta)
                    self.sd_tester.send_data_and_check(ta,write_data,wirte_checkdata)
                    self.io.io_reset_bgm(times=3)
                    time.sleep(20)
                    self.sd_tester.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data='67')
                    result_data=self.sd_tester.read_did_and_check(ta,did,SESSION.EMPTY,check_data,check_length,check_range,check_in)
                else:
                    assert False,'请填入正确的检查方式'
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(f'ERROR:{e}')
            pass_status = False
        finally:            
            if recover:
                with allure.step(f"将DID:{did_str}值恢复为写入前的值"):
                    write_data = f'2E{did_str}{raw_data[6:]}'
                    self.sd_tester.send_data_and_check(ta,write_data,f'6e{did_str}')
                    time.sleep(0.5)  #写入值后加等待0.5s时间再读 保证值已经被存储
                    recover_data=self.sd_tester.read_did_and_check(ta,did,SESSION.EMPTY,raw_data)
                    if recover_data != raw_data:
                        logger.error(f'恢复值失败，返回数据为{recover_data},而期望数据为{raw_data},返回值与预期不一致')
            assert pass_status

        return result_data
                
    def set_lock_and_door_restore_default(self,  anti_pinch: Union[bool, None] = None, 
                                          door_opener: Union[DoorOpenerSts, None] = None,
                                          engine: Union[EngSt1WdStsEngSt1WdSts, None] = None,
                                          door_sts: Union[Door, None] = None):
        
        if anti_pinch is not None:
            with allure.step("四门防夹状态恢复默认值"):
                logger.info(f"--------->四门防夹状态恢复默认值")
                self.bus_comm.set_four_door_anti_pnch_sts(anti_pnch_sts=False)
            
        elif door_opener is not None:
            with allure.step("设置四门运动状态恢复默认值"):
                logger.info(f"--------->设置四门运动状态恢复默认值")
                self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.Ukwn)
            
        elif engine is not None:
            with allure.step("设置发动机状态恢复默认值"):
                logger.info(f"--------->设置发动机状态恢复默认值")
                self.bus_comm.set('backbonefr', 'VddmBackBoneFr00', 'EngSt1WdStsEngSt1WdSts', engine.value)
            
        elif door_sts is not None:
            with allure.step("设置四门及尾门全关"):
                logger.info(f"--------->设置四门及尾门全关")
                self.io.set_five_door_sts(sts=Door.close)

        else:
            logger.info(f"The request type is not supported")
            assert False

    def whether_auto_creat_task(self, ecu, vin):
        self.vin = vin
        self.fota_version = ecu.get("fota_version")
        if self.fota_version:
            logger.info("自动提测&&创建任务")
            self.tcam_version = self.tcam_version = eval(self.fota_version)[1]
            appStatus, appId= self.tsp.check_appStatus(self.tcam_version)
            if appStatus == 0:
                #app上库，但未提测
                assert False, "软件未提测, 周期提测JOB失效"
            elif appStatus == 10:
                #app上库，且已提测
                self.auto_soft_id = self.tsp.get_softid_by_app_name(app_name=self.tcam_version) #找soft id，正常情况下整车包已经打包好了
                if self.auto_soft_id != 0:
                    #找到可用soft id, 继续判断是否有存在的任务
                    check_result = self.tsp.check_task_existence(vin=self.vin, soft_id=self.auto_soft_id)
                    if check_result[0]:
                        #当前存在有效任务, 非第一次run
                        self.auto_task_id = check_result[1]
                        consuming_flag = self.tsp.is_task_consuming(task_id=self.auto_task_id, vin=self.vin)
                        if consuming_flag:
                            logger.info(f"当前有效任务:{self.auto_task_id}正在消费")
                            self.taskid = self.auto_task_id #传递给后续
                        else: 
                            assert False, f"{self.vin} 非当前任务正在消费"
                    else:
                        #当前不存在有效任务, 第一次run
                        self.tsp.create_vsp_task(vin=self.vin,
                                            skip_ecu=get_skip_ecu_list(vin=self.vin),
                                            target_soft_id=self.auto_soft_id)
                        cur_taskid = self.tsp.check_task_existence(vin=self.vin, soft_id=self.auto_soft_id)[1]
                        logger.info(f"{self.vin}: {self.auto_soft_id} 新建有效任务:{cur_taskid}")
                        self.taskid = cur_taskid #传递给后续
                        consuming_flag = self.tsp.is_task_consuming(task_id=cur_taskid, vin=self.vin)
                        if consuming_flag:
                            logger.info(f"新建，当前有效任务:{cur_taskid}正在消费")
                        else: 
                            assert False, f"{self.vin} 非当前任务正在消费" 
                else:
                    #未找到可用soft id
                    assert False, "整车软件未打包, VSP集成失败"
            elif appStatus == None:
                #app未上库，直接报错
                assert False, f"{self.fota_version} 未上库"
            else:                 
                assert False, f"app状态错误 {self.tcam_version}: {appStatus}"
            logger.info(f"传递taskid:{self.taskid}")
            return True, self.taskid
            # ecu["task_id"] = self.taskid
        else:
            logger.info("手动传taskid")
            return False, 0

    def check_wiper_maintenance_mode_signal(self,status="deactive"):
        if status != "deactive":
            self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
            sleep(0.7)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",1)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        else:
            self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
            sleep(0.7)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",0)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    def get_mcu_ver(self, sd_test=None, timeout=10):
        '''
        @param sd_test:
        @return:
        '''
        os.system("ifconfig")
        logger.info(f'************ifconfig==========')
        try:
            self.sd_tester.send_data([0x22, 0xF1, 0x86])
            recv_data_list = (
                self.sd_tester.return_udsdata_and_check_and_print_response_result()
            )
            t = time.time()
            self.sd_tester.update_serverdoipid(0x1002)
            while time.time() - t < timeout:
                # 0x22, 0xF1, 0xF0
                self.sd_tester.sd_tester.information_check_f1f0()
                recv_data_list = (
                    self.sd_tester.return_udsdata_and_check_and_print_response_result()
                )
                if recv_data_list[:3] == [0x62, 0xF1, 0xF0]:
                    break
                time.sleep(5)

            mcu_version = self.sd_tester.sd_tester.read_mcu_version_or_check()
            logger.info(f'获取 mcu_version 的版本{mcu_version}')
            boot_version = self.sd_tester.sd_tester.read_boot_version_or_check()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
            logger.error(f"读取mcu 版本号失败{str(e)}")
            mcu_version = None
            boot_version = None
        finally:
            if mcu_version is None:
                assert 0, " 读取mcu 版本失败"
        return mcu_version, boot_version

    def get_bus_send_recv_info(self, channel_name: str, **kwargs):
        '''
         根据通道获取当前通道的，发送节点和接收节点的数据
         @param ipdu:  对象 self.ipdu
         @param channel_name: 通道   bodycan 等等
         @param kwargs:
         @return: {}
        {
             "发送节点": {
                 "周期发送": {
                     "BGM": [ {"msg_name": msg_name,
                             "msg_id": msg_id,
                             "msg_type": msg_type,
                             "msg_tx_method": msg_tx_method,
                             "msg_cycle": msg_cycle,
                             "msg_length": msg_length,
                             "rx_nodes": rx_nodes,
                             "tx_node": tx_node,
                             "msg_base_cycle": msg_base_cycle,
                             "msg_repetition": msg_repetition}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },
             "接收节点": {
                 "周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },

         }
        '''
        channel_name = channel_name.strip().replace(" ", '').lower()
        # 先判断是不是解析过了，如果已经解析过，直接从缓存里取
        if channel_name in self.all_bus_data_info:
            return self.all_bus_data_info[channel_name]
        bus_obj = getattr(self.bus_comm.ipdu, channel_name)
        #该对象的所有非私有属性（即不以_开头的属性）
        msg_obj_lis = [i for i in dir(bus_obj) if not i.startswith("_")]
        # 存放所有 接收节点
        rx_nodes_dict = {}
        # 存放所有发送节点
        tx_nodes_dict = {}
        mcu_version = int(re.findall("\d+",self.get_mcu_ver()[0])[0][-3:])
        for name in msg_obj_lis:
            # obj = eval(f"{ipdu}.{channel_name}.{name}")
            if name =="lin_scheduleTable":
                continue
            obj = getattr(bus_obj, name)
            msg_name = getattr(obj, "msg_name")
            msg_id = getattr(obj, "msg_id")

            msg_tx_method = getattr(obj, "msg_tx_method")
            if channel_name == "cem_lin1" and mcu_version >= 140:
                if any([msg_id==0x5,msg_id==0x15,msg_id==0x25,msg_id==0x27]):
                    msg_cycle = 0.165/2
                else:
                    msg_cycle = 0.165
            elif channel_name == "cem_lin2" and mcu_version >= 140:
                msg_cycle = 0.11
            elif channel_name == "cem_lin3" and mcu_version >= 140:
                if msg_id==0x20:
                    msg_cycle = 0.135/3
                else:
                    msg_cycle = 0.135
            elif channel_name == "cem_lin4" and mcu_version >= 140:
                msg_cycle = 0.075
            elif channel_name == "cem_lin5" and mcu_version >= 140:
                msg_cycle = 0.315
            elif channel_name == "cem_lin6" and mcu_version >= 140:
                if msg_id==0x2 and msg_id==0x6:
                    msg_cycle = 0.170/2
                else:
                    msg_cycle = 0.170
            else:
                msg_cycle = getattr(obj, "msg_cycle")
            msg_length = getattr(obj, "msg_length")
            # 接收端
            rx_nodes = getattr(obj, "rx_nodes")
            # 发送端
            tx_node = getattr(obj, "tx_node")
            # fr 报文
            try:
                msg_slotid = getattr(obj, "msg_slotid")
                msg_base_cycle = getattr(obj, "msg_base_cycle")
                msg_repetition = getattr(obj, "msg_repetition")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_slotid = None
                msg_base_cycle = None
                msg_repetition = None

            try:
                # lin fr 没有这个
                msg_type = getattr(obj, "msg_type")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_type = None

            if msg_slotid is not None:
                msg_id = msg_slotid

            dic = {
                "msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": rx_nodes,
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition,
            }
            # 分类 接收节点

            if msg_tx_method in tx_nodes_dict:
                if tx_node in tx_nodes_dict[msg_tx_method]:
                    tx_nodes_dict[msg_tx_method][tx_node].append(dic)
                else:
                    tx_nodes_dict[msg_tx_method][tx_node] = [dic]
            else:
                tx_nodes_dict[msg_tx_method] = {}
                tx_nodes_dict[msg_tx_method][tx_node] = [dic]

            for item in rx_nodes:
                if msg_tx_method in rx_nodes_dict:
                    if item in rx_nodes_dict[msg_tx_method]:
                        rx_nodes_dict[msg_tx_method][item].append(dic)
                    else:
                        rx_nodes_dict[msg_tx_method][item] = [dic]
                else:
                    rx_nodes_dict[msg_tx_method] = {}
                    rx_nodes_dict[msg_tx_method][item] = [dic]

        new_dict = {"rx_nodes": rx_nodes_dict, "tx_nodes": tx_nodes_dict}
        # 添加缓存，防止每次都去解析数据库，浪费时间
        self.all_bus_data_info[channel_name] = new_dict
        return new_dict

    def get_bus_send_msg_info(
        self,
        data_dic,
        send_nodes=None,
        send_type="cyclic",
    ):
        '''

        获取 当前bus通道， send_nodes 节点 send_type 发送数据；区分bgm 发送和 非bgm 发送

        @param data_dic: 根据bus 处理得到的数据  只是单个 bus
        @param send_nodes: 如果 send_nodes 为None 表示所有节点,除去bgm的 所有节点
        @param send_type:  cyclic  ，spontaneous
        @return: 非bgm 发送 列表，bgm发送的数据 列表
         [ {"msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": [BGM,.],
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition
                    },
                    {
                    ....
                    }
                ]
            ，
         [{}，{}]
        '''
        
        if send_nodes is not None:
            tx_nodes_data_list = (
                data_dic["tx_nodes"].get(send_type, {}).get(send_nodes, {})
            )
            bgm_tx_nodes_data_list = (
                data_dic["tx_nodes"].get(send_type, {}).get("BGM", {})
            )
            return tx_nodes_data_list, bgm_tx_nodes_data_list
        else:
            # 获取所有 发送节点的，除去BGM 自己发送
            tx_nodes_data_dic = data_dic["tx_nodes"].get(send_type, {})
            # 非bgm 发送 信息
            lis_info = []
            # bgm 发送
            bgm_send_info = []
            for nodes_name, info in tx_nodes_data_dic.items():
                if str(nodes_name).upper() == "BGM":
                    bgm_send_info.extend(info)
                else:
                    lis_info.extend(info)
            return lis_info, bgm_send_info

    def parse_one_eth_packet(self, data_info_string, packet_index, time_string):
        '''
        解析 一条 eth 报文的数据
        UDP Payload格式： 总线编号+报文ID+ 毫秒时间戳 +报文长度 Data…总线编号 + 报文ID + 毫秒时间戳+ 报文长度+ Data… 结束符（0xFE）
        @param data_info_string:
        @param packet_index:
        @param time_string:
        @return:
        '''
        can_map_dic = {
            2: "Info CANFD",
            3: "AD CANFD",
            4: "Propulsion CAN",
            5: "Chassis CAN1",
            6: "Chassis CAN2",
            7: "PassiveSafety CAN",
            8: "Connectivity CANFD",
            9: "Body CAN",
            10: "BodyExposed CANFD",
            11: "BodyALM CANFD1",
            12: "BodyALM CANFD2",
        }
        lin_map_dic = {
            41: "CEM_LIN1",
            42: "CEM_LIN2",
            43: "CEM_LIN3",
            44: "CEM_LIN4",
            45: "CEM_LIN5",
            46: "CEM_LIN6",
            47: "CEM_LIN7",
        }
        one_udp_data_list = []
        while 1:
            # 通道 一个字节
            channel_index_string = data_info_string[:2]
            channel_index = int(channel_index_string, 16)
            # 报文ID：LIN报文ID占1个字节；
            # CAN/CANFD报文ID占2bytes；
            # FlexRay 报文ID（ SLOT ID（2Byte） +BASE CYCLE（1Byte）+ Repetition（1Byte）)共占4Byte；报文ID从报文接收模块获取。
            if channel_index == 1:
                # fr   FlexRay
                channel_name = "backbonefr"
                count = 8
            elif 2 <= channel_index <= 12:
                # can
                channel_name = can_map_dic.get(channel_index)
                count = 4
            elif 41 <= channel_index <= 47:
                # lin
                channel_name = lin_map_dic.get(channel_index)
                count = 2
            else:
                # 异常总线
                channel_name = None
                count = None

            # id  1  2  4 字节
            msg_id_string = data_info_string[2 : 2 + count]
            base_cycle = None
            repetition = None
            if len(msg_id_string) == 8:
                msg_id = msg_id_string[:4]
                base_cycle = int(msg_id_string[4:6], 16)
                repetition = int(msg_id_string[6:8], 16)
            else:
                msg_id = msg_id_string
            # 时间毫秒 2
            ms_time_string = data_info_string[2 + count : 6 + count]
            # 数据长度 1个字节
            msg_len = data_info_string[6 + count : 6 + count + 2]
            msg_len_int = int(msg_len, 16) * 2
            # 数据内容
            msg_content = data_info_string[6 + count + 2 : 8 + count + msg_len_int]
            # 剩余部分
            left_data = data_info_string[8 + count + msg_len_int :]
            # [所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
            # base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）]
            # print(time_string, channel_name, msg_id, ms_time_string, msg_len, msg_content, base_cycle, repetition)

            channel_name = channel_name.strip().replace(" ", "").lower()
            dic = {
                "packet_index": packet_index + 1,
                "timestamp": time_string,
                "channel_name": channel_name,
                "msg_id": int(msg_id, 16),
                "ms_timestamp": int(ms_time_string, 16),
                "msg_len": msg_len_int // 2,
                "msg": msg_content,
                "msg_base_cycle": base_cycle,
                "msg_repetition": repetition,
            }

            one_udp_data_list.append(dic)
            if not left_data:
                break
            data_info_string = copy.deepcopy(left_data)

        return one_udp_data_list

    def parse_pdu_msg(self, file_path, **kwargs):
        '''
        参考文档
        https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46

        解析pud 的报文
        :param file_path: pcap 包路径
        :return:  packet_list ,packet_list
        data_list=[{所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
                     base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）}]
        packet_list=[{所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str),时间戳 （float）}]

        '''

        src_ip = kwargs.get("src_ip", "172.16.5.2")
        des_ip = kwargs.get("des_ip", "172.16.5.1")
        # 时差 默认无
        hours_diff = kwargs.get("hours_diff", 0)
        # 走的udp  还是tcp 协议
        proto = kwargs.get("proto", None)
        # 处理下 tcp 或者udp
        if proto is None:
            proto_str = None
        elif proto.lower() == "udp":
            proto_str = "11"
        else:
            proto_str = "06"
        # 处理ip
        ip_str = (
            bytes([int(i) for i in src_ip.split('.')]).hex()
            + bytes([int(i) for i in des_ip.split('.')]).hex()
        )
        # 处理返回值
        logger.info(f"开始读取pcap文件，会耗时一段时间{file_path}。。。。。")
        t1 = time.time()
        read_data = rdpcap(file_path)
        logger.info(f"读取pcap文件，耗时 {time.time() - t1}秒")
        # 存放所有的can lin fr 数据
        data_list = []
        # 存放 udp 报文的信息
        packet_list = []
        logger.info("开始解析文件，会耗时一段时间。。。。。")
        start_time = time.time()
        for packet_index in range(len(read_data)):
            packet = read_data[packet_index]
            line = bytes(packet).hex()
            packet_time = float(packet.time)
            if ip_str in line:
                # ip 方向对，再判断那种报文
                # 需要判断 带不带vlan  0200000010010200000010028100
                vlan = int(line[24 : 24 + 4], 16)
                if vlan == 0x8100:
                    packet_proto_str = line[54:56]
                    payload_start = 92
                else:
                    payload_start = 84
                    packet_proto_str = line[46:48]
                if proto_str and packet_proto_str != proto_str:
                    continue
                # 解析 数据
                payload_string = line[payload_start:]
                # UDP Payload格式：全局时钟（年月日时分秒）+ 总线编号+报文ID+ 毫秒时间戳 +报文长度 Data…总线编号 + 报文ID + 毫秒时间戳+ 报文长度+ Data… 结束符（0xFE）
                # pload 长度
                payload_string_len = len(payload_string) // 2
                # 时间戳  全局时间戳：年（1byte，只表示年份的后两位，如2022的22；） 月（1byte) 日（1byte) 时（1byte) 分（1byte) 秒（1byte)
                time_string1 = payload_string[0:12]
                time_string_list = [
                    str(int(time_string1[i : i + 2], 16)).zfill(2)
                    for i in range(0, len(time_string1), 2)
                ]
                UTC_FORMAT = r"%Y:%m:%d:%H:%M:%S"
                current_year = str(datetime.datetime.now().year)
                string = current_year[:2] + ':'.join(time_string_list)
                utc_time = datetime.datetime.strptime(string, UTC_FORMAT)
                time_string = utc_time + datetime.timedelta(hours=hours_diff)

                # 结束符
                end_string = payload_string[-2:]
                # 数据部分
                data_info_string = payload_string[12:-2]
                # 所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str)，格式化时间，时间戳 （float）
                # udp_packet_info = (packet_index + 1, payload_string_len, end_string, packet_time)
                otherStyleTime = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(int(packet_time))
                )
                udp_packet_info = {
                    "packet_index": packet_index + 1,
                    "payload_len": payload_string_len,
                    "end_string": end_string,
                    "packet_time": otherStyleTime,
                    "packet_timestamp": packet_time,
                }
                packet_list.append(udp_packet_info)

                one_udp_data_lis = self.parse_one_eth_packet(
                    data_info_string, packet_index, time_string
                )
                data_list.extend(one_udp_data_lis)
        # packet_list=[所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str),时间戳 （float）]
        # data_list=[所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
        # base_cycle（针对fr，can lin 为None）,
        # repetition（针对fr，can lin 为None）]8100
        string = f"解析耗时》》》{time.time() - start_time}秒"
        logger.info(string)
        return data_list, packet_list

    def get_bus_msgid_info(self, channel_name: str, **kwargs):
        '''
        根据通道获取当前通道的，发送节点和接收节点的数据
        @param ipdu:  对象 self.ipdu
        @param channel_name: 通道   bodycan 等等
        @param kwargs:
        @return: {}

        '''

        channel_name = channel_name.strip().replace(" ", '').lower()
        # 先判断是不是解析过了，如果已经解析过，直接从缓存里取
        if channel_name in self.all_bus_msgid_info:
            return self.all_bus_msgid_info[channel_name]
        bus_obj = getattr(self.bus_comm.ipdu, channel_name)
        msg_obj_lis = [i for i in dir(bus_obj) if not i.startswith("_")]
        nodes_dict = {}
        for name in msg_obj_lis:
            # obj = eval(f"{ipdu}.{channel_name}.{name}")
            if name == "lin_scheduleTable":
                continue
            obj = getattr(bus_obj, name)
            msg_name = getattr(obj, "msg_name")
            msg_id = getattr(obj, "msg_id")

            msg_tx_method = getattr(obj, "msg_tx_method")

            msg_cycle = getattr(obj, "msg_cycle")
            msg_length = getattr(obj, "msg_length")
            # 接收端
            rx_nodes = getattr(obj, "rx_nodes")
            # 发送端
            tx_node = getattr(obj, "tx_node")
            # fr 报文
            try:
                msg_slotid = getattr(obj, "msg_slotid")
                msg_base_cycle = getattr(obj, "msg_base_cycle")
                msg_repetition = getattr(obj, "msg_repetition")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_slotid = None
                msg_base_cycle = None
                msg_repetition = None

            try:
                # lin fr 没有这个
                msg_type = getattr(obj, "msg_type")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                msg_type = None

            if msg_slotid is not None:
                msg_id = msg_slotid

            dic = {
                "msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": rx_nodes,
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition,
            }
            # 分类 接收节点
            nodes_dict[msg_id] = dic
            #添加缓存，防止每次都去解析数据库
            self.all_bus_msgid_info[channel_name] = nodes_dict

        return nodes_dict

    def restore_poweroutlet_relay_simulation_environment(self):
        with allure.step(f"12v电源继电器case结束连接诊断激活线且退诊断关五门"):
            logger.info(f"----------------> 恢复诊断激活线连接状态, 退出42 9D 429E诊断, 关闭五门")
            self.io.bgm_diag_line_up()
            logger.info(f'诊断激活线连接')
            self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
            # self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False) # 退诊断
            # self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d', check_method=Check_Method.response, recover=False)
            self.io.set_five_door_sts(sts=Door.close)
            sleep(2)    
    def start_mock_cdc_wifi(self):
        with allure.step('模拟InteractiveService通知其他域控的network manager进程'):
            self.soa.start_send_InteractiveService_response_wifi()
            self.soa.send_event_notify_thread_start("InteractiveService_server", "WifiStsChanged",{"values": [{"id": "WifiSts", "data": "1"}]}, 20)
            self.soa.send_event_notify_thread_start("InteractiveService_server", "WifiStsChanged",{"values": [{"id": "NetWorkAccess", "data": '{"type": "1", "hasAccessibility": "true"}'}]}, 20)
        with allure.step('上位机配置vlan11'):
            cmds_v11 = ['ip link add link enp89s0 name eth0.11 type vlan id 11',
                        'ip addr add 172.16.11.13/24 dev eth0.11',
                        'ip link set dev eth0.11 address 02:00:00:00:10:13',
                        'ifconfig eth0.11 up']
            for cmd in cmds_v11:
                res = exec_shell(cmd)
                error = res.get('error')
                if error:
                    raise Exception(f"配置vlan11错误，原因：{error}")
        with allure.step('上位机配置转发策略配置'):
            cmds_forwards = ['iptables -P FORWARD ACCEPT', 
                            'iptables -t nat -I POSTROUTING -s 172.16.11.0/24 -o wlo1 -j MASQUERADE']
            for cmd in cmds_forwards:
                res = exec_shell(cmd)
                error = res.get('error')
                if error:
                    raise Exception(f"配置FORWARD错误，原因：{error}")
            time.sleep(10)
        with allure.step('检查模拟cdc wifi配置是否ok'):
            wifi_route = self.ssh.type_commands(DeviceName.TCAM, "ip route")
            wifi_line = wifi_route.strip().splitlines()[0]
            assert "eth0.11" in wifi_line, f"连接wifi后，默认路由未切换至eth11"
            logger.info(f"======================= 执行ping baidu操作 =======================")
            commands = f"ping baidu.com -c 10"
            ping_data = self.ssh.type_commands(DeviceName.TCAM, commands)
            check_data = "10 packets transmitted"
            if check_data in ping_data and "100% packet loss" not in ping_data:
                logger.info('模拟cdc wifi配置ok')
            else:
                raise Exception(f"模拟cdc wifi配置失败")        
           
    def stop_mock_cdc_wifi(self):
        with allure.step('停止模拟InteractiveService通知其他域控的network manager进程'):
            self.soa.send_event_notify_thread_stop('InteractiveService_server')
            self.soa.stop_send_InteractiveService_response_wifi()
        with allure.step("删除vlan11"):
            res = exec_shell('ip link delete eth0.11')
            error = res.get('error')
            if error:
                raise Exception(f"删除vlan11错误，原因：{error}")
        time.sleep(30)
        with allure.step('检查模拟cdc 配置是否ok'):
            wifi_route = self.ssh.type_commands(DeviceName.TCAM, "ip route")
            wifi_line = wifi_route.strip().splitlines()[0]
            assert "rmnet_data" in wifi_line, f"默认路由未切换至rmnet_data"
            logger.info(f"======================= 执行tcam ping操作 =======================")
            self.chk_tcam_ping()

    def network_sleep_unlock(self, unlock: bool = False, door_open: DoorSts = DoorSts.Close):
        self.set_car_mode(CarMode.NORMAL)
        self.set_usage_mode(UsageMode.INACTIVE)
        self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        if door_open.value == 1:
            self.io.set_door(Drvr=Door.open)
        elif door_open.value == 2:
            self.io.set_door(Pass=Door.open)
        elif door_open.value == 3:
            self.io.set_door(RiRe=Door.open)
        elif door_open.value == 4:
            self.io.set_door(LeRe=Door.open)
        else:
            pass
        # 断开诊断激活线
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.io.tcam_kl15_down()
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.stop_tester_present()
        # 设置车辆静止
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        # 关闭四门两盖、座椅不占座、门外开关不按、没有踩刹车、危险报警灯不亮
        self.set_seats_present_sts(
            drv_seat=SeatPresSts.NoPres,
            pass_seat=SeatPresSts.NoPres,
            sec_left=SeatPresSts.NoPres,
            sec_mid=SeatPresSts.NoPres,
            sec_right=SeatPresSts.NoPres
        )
        if door_open.value == 5:
            self.io.set_bgm_hardware_condition_to_default()
            self.io.set_hood_sts(HoodSts.Close)
        else:
            pass
        # 发送lin补电
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(10)
        if unlock == False:
            self.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
            self.bus_comm.check_central_lock_sts(CenLockSts.Lock, LockTrigerSource.NFC)
        else:
            pass
        if door_open.value == 5:
            self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        else:
            pass
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=60)
        self.bus_comm.stop_dk()
        # 清除缓存
        time.sleep(5)
        # self.bus_comm.ipdu.rx_flag_reset_all()
        # 判断车辆模式是否是ABANDONED
        start_time = time.time()
        while time.time() - start_time < 60 * 15:
            try:
                self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/mix.py")
                logger.info(f'当前不为{UsageMode.ABANDONED.value}状态')
            else:
                break
            sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
        time.sleep(20)
        self.bus_comm.pause_all_bus_send()
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(40)
        # 检查CAN LIN FR是否有报文发出
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)

    def set_door_and_seat_status(self,motion_state,seat_status,door_status):
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",motion_state)
        self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        if seat_status == "yes":
            self.io.driver_seat_present()
        else:
            self.io.driver_seat_notpresent()

        if door_status == "open":
            self.io.set_door(Drvr=Door.open)
        else:
            self.io.set_door(Drvr=Door.close)

    def set_wiper_mode_and_get_wiper_mode(self,mode):
        sleep(1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,mode)
        sleep(0.7)
        self.soa.get_wiper_mode(WiperPos.Front,mode)

    def check_wiper_maintanance_signal(self,status):
        if status == "active":
            self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
            sleep(0.7)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",1)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        else:
            self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
            sleep(0.7)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",0)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
