#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :soa.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :soa通信能力模拟 实现接口
"""
from typing import Union, List, Dict
from xat_ecu import reporting as allure
import uuid, base64
from time import sleep
import time, datetime
import json

from xat_ecu.api import CommonSoa
from xat_ecu.api.constants.common import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from threading import Thread
from xat_ecu.legacy.common.logger import logger
import hashlib

start_get_service_flag = 1
start_get_light_inhibit_sts_flag = 1


class Soa(CommonSoa):
    def update(self, partner_member: str):
        self.soa_partner.start_soa(partner_member)

    def ck_event_and_resp(self, partner_key: str, event_name: str, event_info: dict,
                          method_name=None, method_args=None, resp_info=None,
                          timeout=3, fuzz_match=True):
        """
        校验历史event，并调用get获取结果
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param event_info: 待校验event的数据
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param resp_info: 请求的预期响应结果
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        """
        return self.soa_partner.ck_event_and_resp(partner_key, event_name, event_info, method_name, method_args,
                                                  resp_info, timeout, fuzz_match)

    def send_event_notify(self, partner_key: str, event_name: str, args: dict):
        return self.soa_partner.send_event_notify(partner_key, event_name, args)

    def ck_s2s_req(self, partner_key: str, interface_name: str, ck_info: Union[dict, None] = None, timeout=1):
        return self.soa_partner.ck_s2s_req(partner_key, interface_name, ck_info, timeout)

    def ck_s2s_req_v20(self, partner_key: str, interface_name_list: list, ck_info_list=None, timeout=1):
        return self.soa_partner.ck_s2s_req_v20(partner_key, interface_name_list, ck_info_list, timeout)

    def chk_notify(self, partner_key: str, method_name: str, ck_info: Union[dict, None] = None, timeout=1,
                   fuzz_match=True):
        return self.soa_partner.chk_notify(partner_key, method_name, ck_info, timeout, fuzz_match)

    def send_request_and_ck_failtype(self, partner_key: str, method_name: str, args: dict,
                                     failtype: Union[FailType, str], timeout=6, is_async=False):
        return self.soa_partner.send_request_and_ck_failtype(partner_key, method_name, args, failtype, timeout,
                                                             is_async)

    def send_request_and_ck_resp(self, partner_key: str, method_name: str, args: dict,
                                 ck_info: dict, timeout=1, cycle_time=0.2, is_async=False, fuzz_match=True):
        return self.soa_partner.send_request_and_ck_resp(partner_key, method_name, args, ck_info, timeout, cycle_time,
                                                         is_async, fuzz_match)

    def send_request_and_return_resp(self, partner_key: str, method_name: str, args: dict,
                                     timeout=1, is_async=False):
        return self.soa_partner.send_request_and_return_resp(partner_key, method_name, args, timeout, is_async)

    def wait_for_service_reconnect(self, partner_key: str, timeout=20):
        return self.soa_partner.wait_for_service_reconnect(partner_key, timeout)

    def ck_s2s_event(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        return self.soa_partner.ck_s2s_event(partner_key, interface_name, ck_info, timeout, fuzz_match)

    def return_latest_event(self, partner_key: str, interface_name: str, pop_event: bool = False):
        return self.soa_partner.return_latest_event(partner_key, interface_name, pop_event)

    def ck_no_event(self, partner_key: str, interface_name: str, timeout=1):
        return self.soa_partner.ck_no_event(partner_key, interface_name, timeout)

    def ck_no_specific_event(self, partner_key: str, interface_name: str, hint: str, timeout=1):
        return self.soa_partner.ck_no_specific_event(partner_key, interface_name, hint, timeout)

    def ck_no_req(self, partner_key: str, interface_name: str, timeout=1):
        return self.soa_partner.ck_no_req(partner_key, interface_name, timeout)

    def register_event(self, partner_key: str, event_list: Union[None, List[Dict]] = None):
        if event_list is None:
            event_list = [{"all": 1}]
        return self.soa_partner.register_event(partner_key, event_list)

    def unregister_event(self, partner_key: str, event_list: Union[None, List] = None):
        if event_list is None:
            event_list = ["all"]
        return self.soa_partner.unregister_event(partner_key, event_list)

    def send_method_request(self, partner_key: str, method_name: str, args: dict, is_async=False):
        return self.soa_partner.send_method_request(partner_key, method_name, args, is_async)

    def send_event_notify_thread_start(self, partner_key: str, event_name: str, args: dict, cycle_time: float = 1):
        return self.soa_partner.send_event_notify_thread_start(partner_key, event_name, args, cycle_time)

    def send_event_notify_thread_stop(self, partner_key):
        return self.soa_partner.send_event_notify_thread_stop(partner_key)

    def send_event_notify_thread_update(self, partner_key: str, event_name: str, args: dict, cycle_time=None):
        return self.soa_partner.send_event_notify_thread_update(partner_key, event_name, args, cycle_time)

    def send_response_to_req_start(self, partner_key: str, func):
        return self.soa_partner.register_callback(partner_key=partner_key, func=func)

    def send_response_to_req_stop(self, partner_key: str, func):
        return self.soa_partner.unregister_callback(partner_key=partner_key, func=func)

    def register_auto_response(self, partner_key: str, func_name: str):
        self.soa_partner.register_auto_response(partner_key, func_name)

    def unregister_auto_response(self, partner_key: str, func_name: str):
        self.soa_partner.unregister_auto_response(partner_key, func_name)

    def send_method_response(self, partner_key: str, method_name: str, args: dict):
        self.soa_partner.send_method_response(partner_key=partner_key, method_name=method_name, args=args)

    def start_send_GetHVSOCInfo_response(self):
        self.send_response_to_req_start(partner_key=f'HighVoltageService_server',
                                        func=self.on_GetHVSOCInfo)

    def start_send_GetHVBatterySOH_response(self):
        self.send_response_to_req_start(partner_key=f'HighVoltageService_server',
                                        func=self.on_GetHVBatterySOH)

    def start_send_GetRange_response(self):
        self.send_response_to_req_start(partner_key=f'HighVoltageService_server',
                                        func=self.on_GetRange)

    def start_send_GetBatteryStatus_response(self):
        self.send_response_to_req_start(partner_key=f'LowVoltageService_server',
                                        func=self.on_GetBatteryStatus)

    def on_GetHVSOCInfo(self, partner_key, msg):
        logger.info(f'msg: {msg}')
        if partner_key == "HighVoltageService_server" and msg["function"] == "GetHVSOCInfo":
            self.send_method_response(partner_key, "GetHVSOCInfo", {'calculateDTESOC': 80,"displaySoc": 90,"realSoc": 92})

    def on_GetHVBatterySOH(self, partner_key, msg):
        logger.info(f'msg: {msg}')
        if partner_key == "HighVoltageService_server" and msg["function"] == "GetHVBatterySOH":
            self.send_method_response(partner_key, "GetHVBatterySOH", 100)

    def on_GetRange(self, partner_key, msg):
        logger.info(f'msg: {msg}')
        if partner_key == "HighVoltageService_server" and msg["function"] == "GetRange":
            self.send_method_response(partner_key, "GetRange", {"source": 0,"CLTCRange":500,"estimatedRange":999,"CLTCRangeIncrease":300,"estimatedRangeIncrease":280})

    def on_GetBatteryStatus(self, partner_key, msg):
        logger.info(f'msg: {msg}')
        if partner_key == "LowVoltageService_server" and msg["function"] == "GetBatteryStatus":
            self.send_method_response(partner_key, "GetBatteryStatus", {"isValid":True,"calculatedSoc": 90,"calculatedSoh": 99})

    def hmi_set_wash_mode(self, sts: isOn, time_wait: Union[float, int] = 0):
        with allure.step(f"调用接口 SetWashMode  设置洗车模式为{sts}"):
            logger.info(f"调用接口 SetWashMode 设置洗车模式为{sts}")
            self.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": sts.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def hmi_set_start_adjust_viewmirror(self, viewPos: ViewPos, direction: Direction, time_wait: Union[float, int] = 0):
        with allure.step(f"调用接口StartAdjustViewMirror 向{direction}调节{viewPos}视镜"):
            logger.info(f"调用接口StartAdjustViewMirror 向{direction}调节{viewPos}视镜")
            self.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror",
                                     {"params": [{"id": viewPos.value, "direction": direction.value}]})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def hmi_set_door_close_lock(self, lock_cmd: LockCmd, source: LockSource,
                                find_key_type: Union[FindKeyType, None] = None, time_wait: Union[float, int] = 0):
        with allure.step(f"调用接口SetDoorCloseLock 执行{lock_cmd.name}操作"):
            logger.info(f"调用接口SetDoorCloseLock 执行{lock_cmd.name}操作")
            if find_key_type == None:
                self.send_method_request("CentralLockService_client", "SetDoorCloseLock",
                                         {"cmd": lock_cmd.value, "source": source.value})
            else:
                self.send_method_request("CentralLockService_client", "SetDoorCloseLock",
                                         {"cmd": lock_cmd.value, "source": source.value, "findKeyTyp": find_key_type})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def get_alrm_info(self, sys_fault: SysFault, sys_sts: SysDefenSts, alm_src: AlmSrc, timeout=5):
        with allure.step(
                f"调用接口 getAlarmInfo 获取期望的告警信息,期望的'sysFault': {sys_fault.name}, 'sysSts': {sys_sts.name}, 'almSrc': {alm_src.name}"):
            logger.info(
                f"调用接口 getAlarmInfo 获取期望的告警信息,期望的'sysFault': {sys_fault.name}, 'sysSts': {sys_sts.name}, 'almSrc': {alm_src.name}")
            self.send_request_and_ck_resp("CTDService_client", "getAlarmInfo", {},
                                          {"out": {"sysFault": sys_fault.value, "sysSts": sys_sts.value,
                                                   "almSrc": alm_src.value}},
                                          timeout=5)
        sleep(0.5)

    def get_wiper_switch_sts(self):
        global start_get_service_flag
        while start_get_service_flag == 1:
            self.send_request_and_return_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0})
            sleep(1)

    def start_get_wiper_switch_sts(self):
        receiver_thread = Thread(target=self.get_wiper_switch_sts, args=())
        receiver_thread.start()

    def stop_get_wiper_switch_sts(self):
        global start_get_service_flag
        start_get_service_flag = 0

    def hmi_set_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        logger.info(f"调用接口 SetWiperMode 将雨刮设置为{mode.name}模式")
        with allure.step(f"调用接口 SetWiperMode 将雨刮设置为{mode.name}模式"):
            self.send_method_request("WiperService_client", "SetWiperMode",
                                     {'wipers': [{'id': pos.value, 'mode': mode.value}]})

    def hmi_set_wiper_wash_func(self, pos: WiperPos, sts: isOn):
        logger.info(f"调用接口 SetSparyWashing 将雨刮洗涤状态设置为{sts.value}")
        with allure.step(f"调用接口 SetSparyWashing 将雨刮洗涤状态设置为{sts.value}"):
            self.send_method_request("WiperService_client", "SetSparyWashing",
                                     {"wipers": [{"id": pos.value, "on": sts.value}]})

    def hmi_set_wiper_maintaince_pos(self, sts: isOn):
        logger.info(f"调用接口 SetWiperMaintainceMode 将雨刮维修服务设置为{sts.value}")
        with allure.step(f"调用接口 SetWiperMaintainceMode 将雨刮维修服务设置为{sts.value}"):
            self.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': sts.value})

    def get_wiper_maintaince_pos(self, sts: isOn):
        logger.info(f"调用接口 GetWiperMaintainceMode 获取雨刮维修服务是否为{sts.name}")
        with allure.step(f"调用接口 GetWiperMaintainceMode 获取雨刮维修服务是否为{sts.name}"):
            self.send_method_request("WiperService_client", "GetWiperMaintainceMode", {}, {"out": sts.value})

    def event_check_wiper_maintaince_pos(self, sts: isOn):
        self.soa_partner.empty_event_list()
        logger.info(f"调用接口 MaintainceMode 获取雨刮维修服务事件上上报")
        with allure.step(f"调用接口 MaintainceMode 获取雨刮维修服务事件上上报"):
            self.ck_s2s_event("WiperService_client", "MaintainceMode", {"on": sts.value})

    def get_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        logger.info(f"调用接口 GetWiperMode 获取雨刮模式是否为{mode.name}")
        with allure.step(f"调用接口 GetWiperMode 获取雨刮模式是否为{mode.name}"):
            self.send_request_and_ck_resp("WiperService_client", "GetWiperMode", {"wipers": [pos.value]},
                                          {"out": [{"id": pos.value, "mode": mode.value}]})

    def event_check_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        logger.info(f"调用接口 Mode 查看雨刮模式改变事件")
        with allure.step(f"调用接口 Mode 查看雨刮模式改变事件"):
            self.ck_s2s_event("WiperService_client", "Mode", {"mode": {"id": pos.value, "mode": mode.value}})

    def hmi_set_wiper_move_inhibit(self, pos: WiperPos, sts: isOn):
        logger.info(f"S2S设置前雨刮动作禁用状态为{sts.name}")
        with allure.step(f"S2S设置前雨刮动作禁用状态为{sts.name}"):
            self.send_method_request("WiperService_client", "SetWiperMoveInhibit",
                                     {"wipers": pos.value, "isOn": sts.value})

    def get_wiper_inhibit_sts(self, pos: WiperPos, move_inhibit: isOn, wash_inhibit: isOn):
        logger.info(f"S2S获取雨刮动作禁用状态")
        with allure.step(f"S2S获取雨刮动作禁用状态"):
            self.send_request_and_ck_resp("WiperService_client", "GetWiperInhibitStatus", {},
                                          {"out": {"id": pos.value, "MoveInhibit": move_inhibit.value,
                                                   "WashInhibit": wash_inhibit.value}})

    def event_check_wiper_inhibit_sts(self, pos: WiperPos, move_inhibit: isOn, wash_inhibit: isOn):
        logger.info(f"S2S获取雨刮动作禁用事件通知")
        with allure.step(f"S2S获取雨刮动作禁用事件通知"):
            self.ck_s2s_event("WiperService_client", "NotifyWiperInhibitStatus",
                              {"inhibit": {"id": pos.value, "MoveInhibit": move_inhibit.value,
                                           "WashInhibit": wash_inhibit.value}})

    def hmi_set_wiper_wash_inhibit(self, pos: WiperPos, sts: isOn):
        logger.info(f"S2S设置雨刮洗刷模式禁用状态为{sts.value}")
        with allure.step(f"S2S设置雨刮洗刷模式禁用状态为{sts.value}"):
            self.send_method_request("WiperService_client", "SetWiperWashInhibit",
                                     {"wipers": pos.value, "isOn": sts.value})

    def get_wiper_wash_sts(self, pos: WiperPos, sts: isOn):
        logger.info(f"S2S获取雨刮洗刷状态是否为{sts.value}")
        with allure.step(f"S2S获取雨刮洗刷状态{sts.value}"):
            self.send_request_and_ck_resp("WiperService_client", "GetSparyWashing", {"wipers": [pos.value]},
                                          {"out": [{"id": pos.value, "on": sts.value}]})

    def event_check_wiper_wash_sts(self, pos: WiperPos, sts: isOn):
        logger.info(f"S2S获取雨刮洗刷事件通知{sts.value}")
        with allure.step(f"S2S获取雨刮洗刷事件通知{sts.value}"):
            self.ck_s2s_event("WiperService_client", "SparyWashing", {"info": {"id": pos.value, "on": sts.value}})

    def get_charging_info(self, isTempHigh: bool):
        self.soa_partner.empty_event_list()
        with allure.step(f"获取充电信息为{isTempHigh}"):
            self.ck_s2s_event('HighVoltageService_client', "ChargingInfo", {"info": {"isTempHigh": isTempHigh}})
            self.send_request_and_ck_resp('HighVoltageService_client', "GetChargingInfo", {},
                                          {"out": {"isTempHigh": isTempHigh}})
            logger.info(f"获取充电信息为{isTempHigh}成功")

    def get_batterylow_mode(
            self,
            BatteryLowTelltale: BatteryLowTelltale,
            isFirstWarn: bool,
            isSecondWarn: bool
    ):
        self.soa_partner.empty_event_list()
        with allure.step(f"获取电量低报警信息,  {BatteryLowTelltale.name}"):
            self.ck_s2s_event('HighVoltageService_client', "batteryLowWarnInfo",
                              {"info": {"lowTeLSts": BatteryLowTelltale.value,
                                        "isFirstWarn": isFirstWarn, "isSecondWarn": isSecondWarn}})
            self.send_request_and_ck_resp('HighVoltageService_client', "getBatteryLowWarnInfo", {},
                                          {"out": {"lowTeLSts": BatteryLowTelltale.value,
                                                   "isFirstWarn": isFirstWarn, "isSecondWarn": isSecondWarn}})
            logger.info(f"获取电量低报警信息, {BatteryLowTelltale.name}成功")

    def get_battery_low_warn_info(self,
                                  BatteryLowTelltale: BatteryLowTelltale,
                                  isFirstWarn: bool,
                                  isSecondWarn: bool):
        with allure.step(f"获取电量低报警信息,  {BatteryLowTelltale.name}"):
            self.send_request_and_ck_resp('HighVoltageService_client', "getBatteryLowWarnInfo", {},
                                          {"out": {"lowTeLSts": BatteryLowTelltale.value,
                                                   "isFirstWarn": isFirstWarn, "isSecondWarn": isSecondWarn}})
            logger.info(f"获取电量低报警信息, {BatteryLowTelltale.name}成功")

    def s2s_set_usage_mode(self, usage_mode: UsageMode):
        with allure.step(f"通过SOA 发送  usagemode为  {usage_mode.name}   事件"):
            self.send_event_notify("VehicleModeService_server", 'UsageModeChanged', {"mode": usage_mode.value})
            logger.info(f"通过SOA 发送  usagemode为  {usage_mode.name}   事件")

    def s2s_set_car_mode(self, car_mode: CarMode):
        with allure.step(f"通过SOA 发送  carmode为  {car_mode.name}   事件"):
            self.send_event_notify("VehicleModeService_server", 'CarModeChanged', {"mode": car_mode.value})
            logger.info(f"通过SOA 发送  carmode为  {car_mode.name}   事件")

    def s2s_set_gear(self, gear: Gear):
        with allure.step(f"通过SOA 发送  Gear为  {gear.name}   事件"):
            self.send_event_notify("ChassisService_server", 'Gear', {"gear": gear.value})
            logger.info(f"通过SOA 发送  Gear为  {gear.name}   事件")

    def hmi_set_tailwing_mode(self, mode: TailWindMode, time_wait: Union[float, int] = 0):
        with allure.step(f"设置尾翼工作模式为{mode.name}"):
            logger.info(f"设置尾翼工作模式为{mode.name}")
            self.send_method_request('TailWingService_client', 'SetTailwingMode', {"mode": mode.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def hmi_set_tailgate_mode(self, cmd: TailGateMode, time_wait: Union[float, int] = 0):
        with allure.step(f"设置尾门动作为{cmd.name}"):
            logger.info(f"设置尾门动作为{cmd.name}")
            self.send_method_request("TailGateService_client", "SetTailGate", {"cmd": cmd.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
#o_fan.liu edit
    def hmi_set_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId,time_wait: Union[float, int] = 0):
        with allure.step(f"设置方向盘加热等级为{level.name},加热源为{source.name}"):
            logger.info(f"设置方向盘加热等级为{level.name},加热源为{source.name}")
            self.send_method_request("SteerWheelService_client", "SetHeat", {"status": level.value,"source": source.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
#o_fan.liu edit 
    def get_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId):
        with allure.step(f"获取方向盘加热等级为{level.name}, 获取方向盘加热源为{source.name}"):
            logger.info(f"获取方向盘加热等级为{level.name}, 获取方向盘加热源为{source.name}")
            self.send_request_and_ck_resp("SteerWheelService_client", "GetHeat", {}, {"out": {"level":level.value, "source":source.value}})
            
#o_fan.liu edit
    def event_check_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId):
        with allure.step(f"获取方向盘加热等级事件上报，Check上报的加热等级是否为{level.name}, Check上报的加热源是否为{source.name}"):
            logger.info(f"获取方向盘加热等级事件上报，Check上报的加热等级是否为{level.name}, Check上报的加热源是否为{source.name}")
            self.ck_s2s_event("SteerWheelService_client", "Heat", {"sts": {"level":level.value, "source":source.value}})

    def get_belt_warning(self, seats: SeatsAlrm, seat_id: SeatId, warn_sts: BeltWarning, time_wait: Union[float, int] = 0):
        with allure.step(f"获取安全带未系报警状态 ,期望获取的安全带未系报警状态{seats.name},期望获取的座椅位置{seat_id.name},期望获取的告警状态{warn_sts.name}"):
            logger.info(f"获取安全带未系报警状态 ,期望获取的安全带未系报警状态{seats.name},期望获取的座椅位置{seat_id.name},期望获取的告警状态{warn_sts.name}")
            self.send_request_and_ck_resp("SeatService_client", "GetBeltWarning", {"seats": [seats.value]},
                                          {"out": [{"id": seat_id.value, "status": warn_sts.value}]})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def event_check_belt_warning(self, seat_id: SeatId, warn_sts: BeltWarning):
        with allure.step(
                f"获取安全带未系报警事件通知 ,期望获取通知的座椅位置{seat_id.name},期望获取的告警状态{warn_sts.name}"):
            logger.info(
                f"获取安全带未系报警事件通知 ,期望获取通知的座椅位置{seat_id.name},期望获取的告警状态{warn_sts.name}")
            self.ck_s2s_event("SeatService_client", "BeltWarning", {"id": seat_id.value, "warn": warn_sts.value})

    def get_warning_msg_List(self, name: str, info: str):
        with allure.step(f"获取告警提示消息列表 ,提示的名字:{name},提示的信息:{info}"):
            logger.info(f"获取告警提示消息列表 ,提示的名字:{name},提示的信息:{info}")
            self.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                          {"out": [{"name": name, "info": info}]})

    def s2s_set_mntnmode(self, mntnmode: bool):
        with allure.step(f"通过SOA 发送车辆维修模式设置为{mntnmode}事件"):
            self.send_event_notify("VehicleSetStatusService_server", 'NotifyMaintenanceMode', {"mode": mntnmode})
            logger.info(f"通过SOA 发送车辆维修模式设置为{mntnmode}事件")

    def send_SetBookEvent_req(self, ser_name: str = "low_temp_protect",book_type: str = "8",sch_time: int = 120):
        current_time = int(time.time())
        schedule_time = (current_time - int(current_time % 60)) + sch_time
        logger.info("当前时间:{0}".format(int(time.time())))
        param = {"bookEventInfo": {
            "serviceName": ser_name,
            "repeatType": 0,
            "weekDay": 0,
            "rtcTime": schedule_time,
            "timerFlag": "qwer",
            "bookInfo": {
                "bookType": book_type,
                "repeatType": 0,
                "weekDay": 0,
                "startTime": schedule_time,
                "stopTime": 0
            },
            "timerHandler": "",
            "rtcFlag": True
        }}
        with allure.step(f'通过SOA Partner发送SetBookEvent请求'):
            self.send_method_request("RtcAlarmService_client", "SetBookEvent", param)
        return (schedule_time - current_time)

    def check_GetHeat_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SteerWheelService_server:GetHeat请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SteerWheelService_server:GetHeat请求")
            self.ck_s2s_req("SteerWheelService_server", "GetHeat", timeout=timeout)

    def response_to_GetHeat_req(self, heatlevel: HeatLevel=HeatLevel.Off,source: SourceId = SourceId.Idle):
        prompt_info = f"----------> 通过SOA Partner发送SteerWheelService_server:GetHeat请求的响应,响应的参数heatlevel为:{heatlevel.name},{source.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("SteerWheelService_server", "GetHeat", 
                                                  {"level":heatlevel.value,
                                                   "source":source.value
                                                      })

    def check_GetRemotePowerStatus_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetRemotePowerStatus请求"):
            self.ck_s2s_req("ClimateControlService_server", "GetRemotePowerStatus", timeout=timeout)

    def check_NotifyTimeUpEventInfo_event(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出 RtcAlarmService_client:NotifyTimeUpEventInfo事件"):
            self.chk_notify("RtcAlarmService_client", "NotifyTimeUpEventInfo", timeout=timeout)

    def response_to_GetRemotePowerStatus_req(self, rem_pow_sts: RemClimateSts):
        prompt_info = f"----------> 通过SOA Partne发送ClimateControlService:GetRemotePowerStatus请求的响应,响应的关键参数远程空调状态为:{rem_pow_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("ClimateControlService_server", "GetRemotePowerStatus",
                                                  rem_pow_sts.value)

    def check_GetDefrostSts_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetDefrostSts请求"):
            self.ck_s2s_req("ClimateControlService_server", "GetDefrostSts", timeout=timeout)

    def response_to_GetDefrostSts_req(self, defrostmax: bool, climatedefrost: bool):
        with allure.step("通过SOA Partner发送ClimateControlService:GetDefrostSts请求的响应"):
            self.soa_partner.send_method_response("ClimateControlService_server", "GetDefrostSts", 
                                                  args = {"defrostMax": defrostmax, "climateDefrost": climatedefrost})

    def check_GetChargingInfo_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:GetChargingInfo请求"):
            self.ck_s2s_req("HighVoltageService_server", "GetChargingInfo", timeout=timeout)

    def response_to_GetChargingInfo_req(self, charg_sts: ChargingSts = ChargingSts.Default,
                                        plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                                        charg_complete_sts: bool = True,
                                        book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                        is_charging_pre: bool = True):
        with allure.step("通过SOA Partner发送HighVoltageService:GetChargingInfo请求的响应"):
            self.soa_partner.send_method_response("HighVoltageService_server", "GetChargingInfo",
                                                  {
                                                      "chargingState": charg_sts.value,
                                                      "chargingSpeed": 0,
                                                      "remainChargingTime": 0,
                                                      "isConnect": True,
                                                      "isTempHigh": True,
                                                      "bookChargeResp": 0,
                                                      "bookStateFeedBack": 0,
                                                      "chargeTargetSoc": tar_soc,
                                                      "pluggerStatus": plug_sts.value,
                                                      "chargePower": 0,
                                                      "totalChargeEnergy": 0,
                                                      "chargeEnergyThisTime": 0,
                                                      "chargeSpeedCalculate": 0,
                                                      "recentChargeStartTime": 0,
                                                      "recentChargeEndTime": 0,
                                                      "chargingCompleteStatus": charg_complete_sts,
                                                      "bookChargests": book_charg_sts.value,
                                                      "isChargingPreparing": is_charging_pre
                                                  }
                                                  )

    def check_SetOutput_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetOutput请求"):
            self.ck_s2s_req("HighVoltageService_server", "SetOutput", timeout=timeout)

    def response_to_SetOutput_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetOutput响应"):
            logger.info('"通过SOA Partner监听TCAM是否发出HighVoltageService:SetOutput响应"')
            self.soa_partner.send_method_response("HighVoltageService_server", "SetOutput")


    def check_GethvActiveSts_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:GethvActiveSts请求"):
            self.ck_s2s_req("HighVoltageService_server", "GethvActiveSts", timeout=timeout)

    def response_to_GethvActiveSts_req(self, hv_act_sts: HVActiveSts):
        prompt_info = f"----------> 通过SOA Partner发送HighVoltageService:GethvActiveSts请求的响应,设置响应的高压激活状态为:{hv_act_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageService_server", "GethvActiveSts",
                                                  hv_act_sts.value)

    def check_SetBatteryHeating_req(self, req_type: ThermalRequestType = ThermalRequestType.kNoRequest,
                                          on: bool = True, value: float = 28.0, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求
        
        Args:
            req_type (ThermalRequestType, optional): 请求类型，默认为ThermalRequestType.kNoRequest.
            on (bool, optional): 是否开启电池加热，默认为True.
            value (float, optional): 电池加热目标温度值，默认为28.0.
            timeout (Union[float, int], optional): 超时时间，单位为秒，默认为1.
        
        Returns:
            None
        
        """
        logger.info(f"通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求")
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求"):
            self.ck_s2s_req("HighVoltageService_server", "SetBatteryHeating", 
                            {"type": req_type.value, "on": on, "value": value}, timeout=timeout)


    def check_SetBatteryHeating_exit_req(self, type: ThermalRequestType = 5,on: bool = False, value: int = -40, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求"):
            self.ck_s2s_req("HighVoltageService_server", "SetBatteryHeating",{"type":type,"on":on,"value":value},timeout=timeout)

    def check_GetSeatHeatVentStatus_req(self, seats: list = [12], timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:GetSeatHeatVentStatus请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SeatService:GetSeatHeatVentStatus请求")
            self.ck_s2s_req("SeatService_server", "GetSeatHeatVentStatus", {"seats": seats}, timeout=timeout)

    def response_to_GetSeatHeatVentStatus_req(self, work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                              pass_work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                              dri_heat_level: HeatLevel = HeatLevel.Off,
                                              pass_heat_level: HeatLevel = HeatLevel.Off):
        with allure.step(f"通过SOA Partner响应 SeatService_server:GetSeatHeatVentStatus 请求,响应的座椅通风工作状态"):
            logger.info(f"通过SOA Partner响应 SeatService_server:GetSeatHeatVentStatus 请求,响应的座椅通风工作状态")
            seat_heatventsts_list = [
                {"id": 0,
                 "status": {
                     "heatLevel": dri_heat_level.value,
                     "heatTime": 0,
                     "heatWorkStatus": 2,
                     "ventLevel": 0,
                     "ventTime": 0,
                     "ventWorkStatus": work_sts.value}
                 },
                {"id": 1,
                 "status": {
                     "heatLevel": pass_heat_level.value,
                     "heatTime": 0,
                     "heatWorkStatus": 2,
                     "ventLevel": 0,
                     "ventTime": 0,
                     "ventWorkStatus": pass_work_sts.value}
                 }
            ]
            self.soa_partner.send_method_response("SeatService_server", "GetSeatHeatVentStatus", seat_heatventsts_list)

    def check_GetBatteryTemperatureInfo_req(self, timeout=1):
        with allure.step(f"通过SOA Partner监听TCAM是否发出HighVoltageService:GetBatteryTemperatureInfo"):
            logger.info(f"通过SOA Partner监听TCAM是否发出HighVoltageService:GetBatteryTemperatureInfo")
            self.ck_s2s_req("HighVoltageService_server", "GetBatteryTemperatureInfo", timeout=timeout)

    def response_to_GetBatteryTemperatureInfo_req(self, min_temp: float = -50, max_temp: float = 80,
                                                  average_temp: float = 0):
        with allure.step(f"通过SOA Partner响应HighVoltageService:GetBatteryTemperatureInfo请求"):
            logger.info(f"通过SOA Partner响应HighVoltageService:GetBatteryTemperatureInfo请求")
            self.soa_partner.send_method_response("HighVoltageService_server", "GetBatteryTemperatureInfo",
                                                  {"maxTemperature": max_temp, "minTemperature": min_temp,
                                                   "averageTemperature": average_temp})

    def notify_BatteryHeatingInfo(self, current_sts: BatteryThermalSts = BatteryThermalSts.kIdle,
                                  req_sts: ThermalReqSts = ThermalReqSts.Default,
                                  estimate_time: int = 0):
        with allure.step(f"通过SOA Partner发出HighVoltageService:BatteryHeatingInfo事件通知"):
            logger.info(f"通过SOA Partner发送HighVoltageService:BatteryHeatingInfo事件通知")
            self.soa_partner.send_event_notify("HighVoltageService_server", "BatteryHeatingInfo",
                                               {"sts": {"currentState": current_sts.value, "reqState": req_sts.value,
                                                        "estimateTime": estimate_time}})

    def check_high_voltage_setoutput_request(self, check_time: float):
        self.soa_partner.empty_all()
        check_times = int(check_time / 3.0)
        with allure.step(f"检查TCAM是否2s周期发送上高压请求，检查{check_times}次"):
            logger.info(f"检查TCAM是否2s周期发送上高压请求，检查{check_times}次")
            time_start = time.time()
            for i in range(0, check_times):
                self.check_SetOutput_req(timeout=3.1)
                if time.time() - time_start < 3:
                    time_start = time.time()
                else:
                    assert False

    def notify_HVSOCInfo(self, realSoc: float = 90.5, calDTESOC: float = 90, displaySoc: float = 90.2):
        with allure.step(
                f"模拟发送高压电池SOC值改变通知，通知的参数:真实SOC:{realSoc}，计算续航里程的SOC:{calDTESOC}，显示SOC:{displaySoc}"):
            logger.info(
                f"模拟发送高压电池SOC值改变通知，通知的参数:真实SOC:{realSoc}，计算续航里程的SOC:{calDTESOC}，显示SOC:{displaySoc}")
            self.soa_partner.send_event_notify("HighVoltageService_server", "HVSOCInfo", {
                'info': {'realSoc': realSoc, 'displaySoc': displaySoc, 'calculateDTESOC': calDTESOC}})

    def notify_VehicleTimeInfo(self, time_zone: TimeZone = TimeZone.EAST_8,
                               sync_sts: TimeSyncSts = TimeSyncSts.Default,
                               poli_time_zone: str = "Asia/Shanghai"):

        time_now = str(datetime.datetime.now())
        [day, time_str] = time_now.split(" ")
        day_list = day.split('-')
        utc_day = int(day_list[2] + day_list[1] + day_list[0][2:])
        time_now = time.time()
        logger.info("当前日期:{0}".format(utc_day))
        with allure.step(f"模拟发时间同步通知,同步状态为{sync_sts.name}"):
            logger.info(f"模拟发时间同步通知,同步状态为{sync_sts.name}")
            self.soa_partner.send_event_notify("VehicleTimeService_server", "VehicleTimeInfo", {
                'info': {'UTCDate': utc_day, 'UTCTime': int(time.time()), 'timeZone': time_zone.value,
                         'SynchronizationStatus': sync_sts.value, 'politicalTimeZone': poli_time_zone}})

    def check_GetSeatHeatVentStatus_req_and_feedback_resp(self, seats: list = [12],
                                                          work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                                          pass_work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                                          dri_heat_level: HeatLevel = HeatLevel.Off,
                                                          pass_heat_level: HeatLevel = HeatLevel.Off,
                                                          timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取SeatService_server:GetSeatHeatVentStatus请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req(seats=seats, timeout=timeout)  # 监听TCAM发送获取座椅加热通风状态请求
            self.response_to_GetSeatHeatVentStatus_req(work_sts=work_sts, pass_work_sts=pass_work_sts,
                                                       dri_heat_level=dri_heat_level, pass_heat_level=pass_heat_level)

    def check_steerwheel_GetHeat_req_and_feedback_resp(self, heatlevel: HeatLevel, source: SourceId = SourceId.Idle,timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取SteerWheelService_server:GetHeat请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetHeat_req(timeout)  # 监听TCAM发送获取方向盘加热请求
            self.response_to_GetHeat_req(heatlevel,source)

    def check_climate_GetRemotePowerStatus_req_and_feedback_resp(self, rem_pow_sts: RemClimateSts,
                                                                 timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取ClimateControlService:GetRemotePowerStatus请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetRemotePowerStatus_req(timeout)
            self.response_to_GetRemotePowerStatus_req(rem_pow_sts)

    def check_GetDefrostSts_req_and_feedback_resp(self, defrostmax: bool, climatedefrost: bool,
                                                  timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取ClimateControlService:GetDefrostSts请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetDefrostSts_req(timeout)  # 监听TCAM发送获取除霜状态请求
            self.response_to_GetDefrostSts_req(defrostmax, climatedefrost)

    def check_GetBatteryTemperatureInfo_req_and_feedback_resp(self, min_temp: float = -50, max_temp: float = 80,
                                                              average_temp: float = 0,
                                                              timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取HighVoltageService:GetBatteryTemperatureInfo请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetBatteryTemperatureInfo_req(timeout)
            self.response_to_GetBatteryTemperatureInfo_req(min_temp=min_temp, max_temp=max_temp,
                                                           average_temp=average_temp)

    def check_GetChargingInfo_req_and_feedback_resp(self, charg_sts: ChargingSts = ChargingSts.Default,
                                                    plug_sts: PluggerSts = PluggerSts.Disconnected,
                                                    tar_soc: float = 0.0,
                                                    charg_complete_sts: bool = True,
                                                    book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                                    is_charging_pre: bool = True, timeout: Union[float, int] = 0.5):

        prompt_info = f"---------->获取HighVoltageService:GetChargingInfo请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetChargingInfo_req(timeout)  # 监听TCAM发送获取充电状态请求
            self.response_to_GetChargingInfo_req(charg_sts=charg_sts, plug_sts=plug_sts, tar_soc=tar_soc,
                                                 charg_complete_sts=charg_complete_sts,
                                                 book_charg_sts=book_charg_sts, is_charging_pre=is_charging_pre)

    def check_GethvActiveSts_req_and_feedback_resp(self, hv_act_sts: HVActiveSts, timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取HighVoltageService:GethvActiveSts请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GethvActiveSts_req(timeout)
            self.response_to_GethvActiveSts_req(hv_act_sts=hv_act_sts)

    def get_ua_status(self, domain_name: DOMAIN, ua_event_field: UA_EVENT):
        time.sleep(3)
        if domain_name.value == 0:
            ua_status = self.return_latest_event("UpdateAgentService_client_BGM_UA_Service", "Status")['status']
        elif domain_name.value == 1:
            ua_status = self.return_latest_event("UpdateAgentService_client_TCAM_UA_Service", "Status")['status']
        else:
            logger.error(f"Not support {domain_name.name} yet")
        if ua_event_field.value == 0:
            value = ua_status['status']
        elif ua_event_field.value == 1:
            value = ua_status['downloadStatus']['status']
        elif ua_event_field.value == 2:
            value = ua_status['preUpdateStatus']['status']
        elif ua_event_field.value == 3:
            value = ua_status['updateStatus']['status']
        elif ua_event_field.value == 4:
            value = ua_status['errorCode']
        elif ua_event_field.value == 5:
            value = ua_status['downloadStatus']['downloadFileSize']
        elif ua_event_field.value == 6:
            value = ua_status['downloadStatus']['totalFileSize']
        elif ua_event_field.value == 7:
            value = ua_status['downloadStatus']['downloadSpeed']
        elif ua_event_field.value == 8:
            value = ua_status['preUpdateStatus']['progress']
        elif ua_event_field.value == 9:
            value = ua_status['updateStatus']['updateFileSize']
        elif ua_event_field.value == 10:
            value = ua_status['updateStatus']['totalFileSize']
        else:
            logger.error("Wrong UA event field name !!!")
        logger.info(f"Current {domain_name.name} UA {ua_event_field.name} = {value}")
        return value

    def get_fota_status(self, master_event_field: MASTER_EVENT, wait: bool=True):
        if wait:
            time.sleep(4)
        fota_master_status = self.return_latest_event("FotaMasterService_client", "Status")['status']
        if master_event_field.value == 0:
            value = fota_master_status['state']
        elif master_event_field.value == 1:
            value = fota_master_status['taskId']
        elif master_event_field.value == 2:
            value = fota_master_status['errorCode']
        elif master_event_field.value == 3:
            value = fota_master_status['serialNumber']
        elif master_event_field.value == 4:
            value = fota_master_status['taskType']
        else:
            logger.error("Wrong FOTA Master event field name !!!")
        logger.info(f"Current FOTA Master {master_event_field.name} = {value}")
        return value

    def send_fota_request(self, master_request: MASTER_REQUEST, args={}):
        if self.soa_partner.partner_infos[f'FotaMasterService_client'].service_status != "START":
            # 发起请求之前做 服务在线 判断，避免 进/退boot 重启影响
            self.soa_partner.empty_all()
            self.soa_partner.wait_for_service_reconnect(f'FotaMasterService_client')
        re = {}
        if master_request.value < 20:
            self.send_method_request(partner_key='FotaMasterService_client', method_name=master_request.name, args={})
        elif master_request.name == 'CheckTask' and 'cmd' in args:
            self.send_method_request(partner_key='FotaMasterService_client', method_name=master_request.name, args=args)
        elif master_request.name == 'GetAppointment' and 'taskId' in args:
            time.sleep(2) # 等待2s，确保预约event发出才可get
            re = self.send_request_and_return_resp(partner_key='FotaMasterService_client', method_name=master_request.name, args=args).get("out")
        elif master_request.name == 'CancelAppointment' and 'taskId' in args:
            self.send_method_request(partner_key='FotaMasterService_client', method_name=master_request.name, args=args)
        elif master_request.name == 'SetAppointment' and 'taskId' in args and 'time' in args:
            self.send_method_request(partner_key='FotaMasterService_client', method_name=master_request.name, args=args)
        elif master_request.name == 'SetFirstCheckResult' and 'sts' in args:
            self.send_method_request(partner_key='FotaMasterService_client', method_name=master_request.name, args=args)
        elif master_request.name == 'CancelServiceBookEvent' and 'RtcAlarmService' in args:
            self.send_method_request(partner_key='RtcAlarmServicee_client', method_name=master_request.name, args=args)
        else:
            logger.error(f"Wrong master_request: {master_request} or Wrong args: {args}")
        logger.info(f"send FOTA Master request: {master_request.name} with args: {args}")
        return re

    def send_ua_request(self, domain_name: DOMAIN, ua_request: UA_REQUEST, args={}, retry: bool=True):
        if self.soa_partner.partner_infos[f'UpdateAgentService_client_{domain_name.name}_UA_Service'].service_status != "START":
            # 发起请求之前做 服务在线 判断，避免 进/退boot 重启影响
            self.soa_partner.empty_all()
            self.soa_partner.wait_for_service_reconnect(f'UpdateAgentService_client_{domain_name.name}_UA_Service')
        if ua_request.value < 20:
            self.send_method_request(partner_key=f'UpdateAgentService_client_{domain_name.name}_UA_Service',
                                     method_name=ua_request.name, args={})
        elif ua_request.name == 'StartDownload' and 'downloadReq' in args:
            self.send_method_request(partner_key=f'UpdateAgentService_client_{domain_name.name}_UA_Service',
                                     method_name=ua_request.name, args=args)
            if retry:
                time.sleep(5)
                if self.get_ua_status(domain_name, UA_EVENT.Status) != 1:
                    self.send_ua_request(domain_name, ua_request, args)
        else:
            logger.error(f"Wrong master_request: {ua_request} or Wrong args: {args}")
        logger.info(f"send UA request: {ua_request.name} with args: {args}")

    def ua_back_to_idle(self, domain_name: DOMAIN):
        while True:
            ua_status = self.get_ua_status(domain_name, UA_EVENT.Status)
            if ua_status == 0:
                logger.info(f"{domain_name} UA Status is already Idle")
                break
            elif ua_status == 1:
                self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelDownload)
                sleep(10)
            elif ua_status == 3:
                logger.info(f"{domain_name} UA Status is still Installing, wait 60s")
                sleep(60)
            elif ua_status == 6:
                self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelUpdate)
                sleep(60)
            elif ua_status == 5:
                self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelUpdate)
                sleep(300)  # TCAM update finish => roll back => Idle 需要4分半
            elif ua_status == 4:
                if domain_name.name == 'TCAM':
                    self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelUpdate)
                    sleep(300)  # TCAM update finish => roll back => Idle 需要4分半
                else:
                    self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelUpdate)
                    sleep(60)
            else:
                self.send_ua_request(domain_name=domain_name, ua_request=UA_REQUEST.CancelUpdate)
                sleep(10)

    def notify_fota_status(self, state: FOTAMasteSts, errorCode: int = 0):
        with allure.step(
                f"通过SOA Partner发出 FotaMasterService:Status事件通知,FOTAMasteSts:{state.name},ErrorCode:{errorCode}"):
            logger.info(
                f"通过SOA Partner发出 FotaMasterService:Status事件通知,FOTAMasteSts:{state.name},ErrorCode:{errorCode}")
            self.soa_partner.send_event_notify("FotaMasterService_server", "Status", {"status": {"taskId": 123456,
                                                                                                 'state': state.value,
                                                                                                 'errorCode': errorCode}})

    def start_send_ua_event(self, domain_name: DOMAIN, event_args):
        self.send_event_notify_thread_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                            event_name='Status', args=event_args, cycle_time=2)
        logger.info(f"Start send {domain_name.name} UA event: 【{event_args}】")

    def stop_send_ua_event(self, domain_name: DOMAIN):
        self.send_event_notify_thread_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service')
        logger.info(f"Stop send {domain_name.name} UA event")

    def update_ua_event(self, domain_name: DOMAIN, event_args):
        self.send_event_notify_thread_update(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                             event_name='Status', args=event_args, cycle_time=2)
        logger.info(f"Update send {domain_name.name} UA event: 【{event_args}】")

    def pack_ua_status_args(self, ua_sts: UA_Sts, errorCode=0):
        ua_dict = json.loads(json.dumps(UA_Status_Event))
        if ua_sts.name == 'IDLE':
            pass
        elif ua_sts.name == 'DOWNLOAD':
            ua_dict['status'] = 1
            ua_dict['downloadStatus']['downloadFileSize'] = 4000000000
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 10
            ua_dict['downloadStatus']['status'] = 0
        elif ua_sts.name == 'READY_TO_INSTALL':
            ua_dict['status'] = 2
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 0
        elif ua_sts.name == 'INSTALLING':
            ua_dict['status'] = 3
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4000000000
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 0
        elif ua_sts.name == 'UPDATE_FINISH':
            ua_dict['status'] = 4
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4704677392
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 3
        elif ua_sts.name == 'ACTIVATING':
            ua_dict['status'] = 8
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4704677392
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 3
        elif ua_sts.name == 'SYSTEM_ACTIVE':
            ua_dict['status'] = 6
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4704677392
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 3
        elif ua_sts.name == 'ROLLING_BACK':
            ua_dict['status'] = 5
            ua_dict['downloadStatus']['downloadFileSize'] = 4000000000
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4000000000
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 4
        elif ua_sts.name == 'ERROR':
            ua_dict['status'] = 7
        elif ua_sts.name == 'UPDATE_FAILED':
            ua_dict['status'] = 9
            ua_dict['downloadStatus']['downloadFileSize'] = 4000000000
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4000000000
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = 2
        else:
            logger.error("Illegal UA Status")
        ua_dict['errorCode'] = errorCode if errorCode != 0 else ua_dict['errorCode']
        logger.info(f"Pack UA status args: 【{ua_dict}】")
        return ua_dict

    def hmi_set_climate_power_sts(self, zone: ClimateZone, sts: isOn, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:请求,控制区域{zone.name}状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if sts.name == "Off":
                self.send_method_request("ClimateControlService_client", "Off", {"zoneId": zone.value})
            elif sts.name == "On":
                self.send_method_request("ClimateControlService_client", "On", {"zoneId": zone.value})
            sleep(timeout)

    def get_climate_ac_sts(self, sts: bool, timeout: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:GetAC 获取A/C开关状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("ClimateControlService_client", "GetAC", {}, {"out": sts})
        sleep(timeout)

    def hmi_set_acinhibit_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetACInhibit 设置A/C禁用开关状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetACInhibit", {"isOn": sts})
        logger.info(f"---------------->等待{time_wait}")
        sleep(time_wait)
        
    def hmi_set_climate_windspeed(self, zone: ClimateZone, speed: WindSpeed, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetWindSpeed,设置区域{zone.name}风速为{speed.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetWindSpeed",
                                     {"zoneId": zone.value, "speed": speed.value})
        sleep(timeout)

    def hmi_set_climate_cycle_mode(self, mode: CycleMode, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetCycleMode,设置循环模式{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetCycleMode", {"mode": mode.value})
        sleep(timeout)

    def get_climate_ac_mode(self, sts: bool, timeout: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:GetAC,获取空调模式，期望的模式为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("ClimateControlService_client", "GetAC", {}, {"out": sts})
        sleep(timeout)

    def hmi_set_climate_auto_mode(self, zone: ClimateZone, sts: bool, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetClimateAuto,设置区域{zone.name}自动模式为为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetClimateAuto",
                                     {"zoneId": zone.value, "on": sts})
        sleep(timeout)

    def hmi_set_climate_sync_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetAutoSyncMode,设置温度同步为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetAutoSyncMode",
                                     {"on": sts})
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def get_climate_sync_mode(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:GetAutoSyncMode,获取温度同步状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("ClimateControlService_client", "GetAutoSyncMode",{},
                                     {"out": sts})
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
        
    def get_climate_mode(self, mode: ClimateMode, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:GetClimateMode,获取状态机{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("ClimateControlService_client", "GetClimateMode",{},
                                     {"out": mode.value})
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)        

    def get_extilight_mode(self, mode: ExteriorLightMode):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:GetExteriorLightMode,获取当前的外灯模式是否为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("LightService_client", "GetExteriorLightMode", {}, {"out": mode.value})

    def hmi_set_extilight_mode(self, mode: ExteriorLightMode, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:SetExteriorLightMode,设置当前的外灯模式是为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("LightService_client", "SetExteriorLightMode", {"mode": mode.value})

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def event_check_extilight_mode(self, mode: ExteriorLightMode):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:ExteriorLightMode,期望外灯模式改变事件上报，期望是为模式为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ck_s2s_event("LightService_client", "ExteriorLightMode", {"mode": mode.value})

    def get_and_set_extilight_mode(self, target_mode: ExteriorLightMode):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:GetExteriorLightMode,获取当前的外灯模式是否为{target_mode.name},如果不一致会自动重设"
        with allure.step(promt_info):
            logger.info(promt_info)
            current_mode = self.send_request_and_return_resp("LightService_client", "GetExteriorLightMode", {})[
                "out"]  # 获取当前的灯模式
            if current_mode != target_mode.value:  # 如果当前的模式不等于请求的模式
                logger.info("\033[0;35;40m当前外灯模式不等设置值,开始切换模式\033[0m")
                self.send_method_request("LightService_client", "SetExteriorLightMode", {"mode": target_mode.value})
                # logger.info("\033[0;35;40m外灯模式设置成功等待通知返回\033[0m")
                # self.ck_s2s_event("LightService_client", "ExteriorLightMode", {"mode": target_mode.value})
                sleep(0.5)
                logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
                self.send_request_and_ck_resp("LightService_client", "GetExteriorLightMode", {},
                                              {"out": target_mode.value})
                logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
            else:
                logger.info("\033[0;35;40m当前外灯模式等于设置值,重新设置当前模式\033[0m")
                self.send_method_request("LightService_client", "SetExteriorLightMode",
                                         {"mode": target_mode.value})  # 设置近光mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
                logger.info("\033[0;35;40m外灯模式设置成功无通知等待300ms获取当前模式\033[0m")
                sleep(0.5)
                self.send_request_and_ck_resp("LightService_client", "GetExteriorLightMode", {}, {"out": target_mode.value})  # 获取外灯模式mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
                logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")

    def get_and_event_check_low_beam_sts(self, mode: ExteriorLightMode):
        promt_info = f"----------------> 通过SOA Partner发出LightService_client:GetExteriorLightMode 和 ExteriorLightMode,检查近光灯事件上报和获取近光灯状态,检测的期望模式为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.event_check_extilight_mode(mode)
            self.get_extilight_mode(mode)

    def get_high_beam_sts(self, sts: HighBeamSts, clientId: LowBeamClientId):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:GetHighBeamStatus,获取当前的远光灯状态是否为{sts.name},触发源是否为{clientId.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_request_and_ck_resp("LightService_client", "GetHighBeamStatus", {},
                                          {"out": {'sts': sts.value, 'clientId': clientId.value}})

    def event_check_auto_high_beam_sts(self, auto_sts: AutoHighBeamSts):
        promt_info = f"----------------> 通过SOA Partner发出 LightService_client:AutoHighBeamStatus,来检测是否有自动远光灯事件上报，期望状态为:{auto_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ck_s2s_event("LightService_client", "AutoHighBeamStatus", {"sts": auto_sts.value})

    def event_check_high_beam_sts(self, sts: Union[HighBeamSts,None], clientId: LowBeamClientId):
        if sts is not None:
            promt_info = f"----------------> 通过SOA Partner发出 LightService_client:ExteriorLightMode,来检测是否有远光灯事件上报，期望状态为:{sts.name},触发源为{clientId.name}"
            with allure.step(promt_info):
                logger.info(promt_info)
                self.ck_s2s_event("LightService_client", "HighBeamStatus",
                                {"sts": {"sts": sts.value, "clientId": clientId.value}})
        else:
            promt_info = f"----------------> 通过SOA Partner发出 LightService_client:ExteriorLightMode,来检测是否有远光灯事件上报,触发源为{clientId.name}"
            with allure.step(promt_info):
                logger.info(promt_info)
                self.ck_s2s_event("LightService_client", "HighBeamStatus",{"sts": {"clientId": clientId.value}})

    def get_and_event_check_high_beam_sts(self, auto_sts: AutoHighBeamSts, sts: HighBeamSts, clientId: LowBeamClientId):
        promt_info = f"----------------> 通过SOA Partner发出LightService_client:GetExteriorLightMode 和 ExteriorLightMode,检查远光灯事件上报和获取远光灯状态,检测的期望状态是为{sts.name},触发源为{clientId.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.event_check_auto_high_beam_sts(sts=auto_sts)
            self.event_check_high_beam_sts(sts=sts, clientId=clientId)
            self.get_high_beam_sts(sts=sts, clientId=clientId)

    def hmi_set_climate_power_sts(self, zone: ClimateZone, sts: isOn, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:请求,控制区域{zone.name}状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if sts.name == "Off":
                self.send_method_request("ClimateControlService_client", "Off", {"zoneId": zone.value})
            elif sts.name == "On":
                self.send_method_request("ClimateControlService_client", "On", {"zoneId": zone.value})
            sleep(timeout)

    def hmi_set_climate_ac_sts(self, sts: bool, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetAC 设置A/C开关状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetAC", {"on": sts})
        sleep(timeout)

    def hmi_set_climate_windspeed(self, zone: ClimateZone, speed: WindSpeed, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetWindSpeed,设置区域{zone.name}风速为{speed.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetWindSpeed",
                                     {"zoneId": zone.value, "speed": speed.value})
        sleep(timeout)

    def hmi_set_climate_cycle_mode(self, mode: CycleMode, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetCycleMode,设置循环模式{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetCycleMode", {"mode": mode.value})
        sleep(timeout)

    def hmi_set_climate_auto_mode(self, zone: ClimateZone, sts: bool, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetClimateAuto,设置区域{zone.name}自动模式为为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetClimateAuto",
                                     {"zoneId": zone.value, "on": sts})
        sleep(timeout)

    def pack_ua_event_args(self, ua_sts: UA_Sts, errorCode=0):
        ua_status = self.pack_ua_status_args(ua_sts=ua_sts, errorCode=errorCode)
        ua_event_dict = {
            "status": ua_status
        }
        logger.info(f"Pack UA event args: 【{ua_event_dict}】")
        return ua_event_dict


    def on_ua_start_download(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'StartDownload':
            self.send_method_response(partner_key=partner_key, method_name='StartDownload', args=0)

    def on_ua_suspend_download(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'SuspendDownload':
            self.send_method_response(partner_key=partner_key, method_name='SuspendDownload', args=0)

    def on_ua_resume_download(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'ResumeDownload':
            self.send_method_response(partner_key=partner_key, method_name='ResumeDownload', args=0)

    def on_ua_cancel_download(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'CancelDownload':
            self.send_method_response(partner_key=partner_key, method_name='CancelDownload', args=0)

    def on_ua_pre_update(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'PreUpdate':
            self.send_method_response(partner_key=partner_key, method_name='PreUpdate', args=0)

    def on_ua_start_update(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'StartUpdate':
            self.send_method_response(partner_key=partner_key, method_name='StartUpdate', args=0)

    def on_ua_cancel_update(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'CancelUpdate':
            self.send_method_response(partner_key=partner_key, method_name='CancelUpdate', args=0)

    def on_ua_rollback(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'Rollback':
            self.send_method_response(partner_key=partner_key, method_name='Rollback', args=0)

    def on_ua_activate(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'Activate':
            self.send_method_response(partner_key=partner_key, method_name='Activate', args=0)

    def on_ua_finishupdate(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'FinishUpdate':
            self.send_method_response(partner_key=partner_key, method_name='FinishUpdate', args=0)

    def on_ua_rescue(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'Rescue':
            self.send_method_response(partner_key=partner_key, method_name='Rescue', args=0)

    def on_ua_get_status(self, partner_key, msg):
        if 'UpdateAgentService_server_CDC_UA_Service' in partner_key and msg["function"] == 'GetStatus':
            if not hasattr(self.soa_partner.partner_infos[partner_key], "args"):
                ua_resp = self.pack_ua_status_args(UA_Sts.IDLE, errorCode=0)
                setattr(self.soa_partner.partner_infos[partner_key], "args", ua_resp)
            self.send_method_response(partner_key=partner_key, method_name='GetStatus',
                                      args=self.soa_partner.partner_infos[partner_key].args)

    def start_send_ua_response(self, domain_name: DOMAIN):
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_get_status)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_start_download)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_suspend_download)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_resume_download)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_cancel_download)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_pre_update)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_start_update)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_cancel_update)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_rollback)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_activate)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_finishupdate)
        self.send_response_to_req_start(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                        func=self.on_ua_rescue)

    def stop_send_ua_response(self, domain_name: DOMAIN):
        try:
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_get_status)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_start_download)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_suspend_download)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_resume_download)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_cancel_download)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_pre_update)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_start_update)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_cancel_update)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_rollback)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_activate)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_finishupdate)
            self.send_response_to_req_stop(partner_key=f'UpdateAgentService_server_{domain_name.name}_UA_Service',
                                           func=self.on_ua_rescue)
            # delattr(self.soa_partner.partner_infos[f'UpdateAgentService_server_{domain_name.name}_UA_Service'], "args")
        except KeyError:
            logger.error("当前服务未注册,无法调用stop")

    def update_ua_response(self, domain_name: DOMAIN, get_status_args):
        self.stop_send_ua_response(domain_name=domain_name)
        self.soa_partner.partner_infos[
            f'UpdateAgentService_server_{domain_name.name}_UA_Service'].args = get_status_args
        self.start_send_ua_response(domain_name=domain_name)

    def change_ua_event_and_getstatus(self, domain_name: DOMAIN, ua_sts: UA_Sts, errorCode=0):
        self.empty_all()
        self.update_ua_event(domain_name=domain_name,
                             event_args=self.pack_ua_event_args(ua_sts=ua_sts, errorCode=errorCode))
        self.update_ua_response(domain_name=domain_name,
                                get_status_args=self.pack_ua_status_args(ua_sts=ua_sts, errorCode=errorCode))

    def till_ua_event_to(self, domain_name: DOMAIN, ua_event_field: UA_EVENT, target_status=None, timeout=60):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.get_ua_status(domain_name=domain_name, ua_event_field=ua_event_field)
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current {domain_name} UA {ua_event_field} is {curr_status}")

    def event_check_warning_light_list(self, name: str, state: str):
        prompt_info = f"----------> 通过SOA Partner发送 WTIService_client:TelltaleList 获取告警灯通知，检测的告警{name}状态是否为{state}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("WTIService_client", "TelltaleList", {"list": [{"name": name, "state": state}]},timeout=5)

    def get_warning_light_list(self, name: str, state: str):
        prompt_info = f"----------> 通过SOA Partner发送 WTIService_client:GetTelltaleList 获取警示灯列表信息，检测的告警{name}状态是否为{state}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("WTIService_client", "GetTelltaleList", {},
                                          {"out": [{"name": name, "state": state}]})

    def get_and_event_check_warning_light_list(self, name: str, state: str):
        self.event_check_warning_light_list(name=name, state=state)
        self.get_warning_light_list(name=name, state=state)
        self.empty_all()

    def event_check_warning_info_list(self, name: str, info: str):
        prompt_info = f"----------> 通过SOA Partner发送 WTIService_client:WarningMsgList 获取告警信息事件上报，检测的告警{name}信息是否为{info}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("WTIService_client", "WarningMsgList", {"list": [{"name": name, "info": info}]},timeout=5)

    def get_warning_info_list(self, name: str, info: str):
        prompt_info = f"----------> 通过SOA Partner发送 WTIService_client:GetWarningMsgList 获取警示信息列表，检测的告警{name}信息是否为{info}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                          {"out": [{"name": name, "info": info}]})

    def get_and_event_check_warning_info_list(self, name: str, info: str):
        self.event_check_warning_info_list(name=name, info=info)
        self.get_warning_info_list(name=name, info=info)
        self.empty_all()

    def get_and_event_check_seatbelt_sign_warning_light_list(self, name: str = "Seat Belt", state: str = ""):
        self.get_and_event_check_warning_light_list(name=name, state=state)

    def get_and_event_check_airbag_sign_warning_light_list(self, name: str = "Airbag", state: str = ""):
        self.get_and_event_check_warning_light_list(name=name, state=state)

    def get_and_event_check_seatbelt_warning_sts_list(self, name: str = "Driver Seat Belt Warning", state: str = ""):
        self.get_and_event_check_warning_light_list(name=name, state=state)

    def get_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool, is_valid: bool):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:GetAirbagWarning获取安全气囊系统报警信息，检测气囊故障灯状态是否为{trouble_light_sts.name}，是否为故障状态是否为{is_fault}，故障有效状态是否为{is_valid}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("PassiveSafetyService_client", "GetAirbagWarning", {},
                                          {"out": {"troubleLightStatus": trouble_light_sts.value, "isFault": is_fault,
                                                   "isValid": is_valid}})

    def event_check_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool,
                                                     is_valid: bool):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:AirbagWarning 安全气囊系统报警信息事件上报，检测气囊故障灯状态是否为{trouble_light_sts.name}，是否为故障状态是否为{is_fault}，故障有效状态是否为{is_valid}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("PassiveSafetyService_client", "AirbagWarning",
                              {"warn": {"troubleLightStatus": trouble_light_sts.value, "isFault": is_fault,
                                        "isValid": is_valid}})

    def get_and_event_check_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool,
                                                             is_valid: bool):
        self.get_airbag_trouble_light_sts(trouble_light_sts=trouble_light_sts, is_fault=is_fault, is_valid=is_valid)
        self.event_check_airbag_trouble_light_sts(trouble_light_sts=trouble_light_sts, is_fault=is_fault,
                                                  is_valid=is_valid)

    def get_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool, is_valid: bool):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:GetPedestrianProtectionWarning 获取行人保护告警状态，是否为系统故障状态是否为{is_sys_fault}，是否为is_impact_warn是否为{is_impact_warn}，故障有效状态是否为{is_valid}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("PassiveSafetyService_client", "GetPedestrianProtectionWarning", {}, {
                "out": {"isSysFault": is_sys_fault, "isImpactWarning": is_impact_warn, "isValid": is_valid}})

    def event_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool, is_valid: bool):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:PedestrianProtectionWarning 行人保护告警状态事件上报，是否为系统故障状态是否为{is_sys_fault}，是否为is_impact_warn是否为{is_impact_warn}，故障有效状态是否为{is_valid}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("PassiveSafetyService_client", "PedestrianProtectionWarning",
                              {"warn": {"isSysFault": is_sys_fault, "isImpactWarning": is_impact_warn,
                                        "isValid": is_valid}})

    def get_and_event_check_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool,
                                                              is_valid: bool):
        self.event_pedestrian_protection_warning_sts(is_sys_fault=is_sys_fault, is_impact_warn=is_impact_warn,
                                                     is_valid=is_valid)
        self.get_pedestrian_protection_warning_sts(is_sys_fault=is_sys_fault, is_impact_warn=is_impact_warn,
                                                   is_valid=is_valid)

    def get_vehicle_collision_warning_sts(self, roll_over_crash: bool = False, front_crash: bool = False,
                                          rear_crash: bool = False, left_crash: bool = False,
                                          right_crash: bool = False):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:GetVehicleCrashStatus 获取车辆碰撞状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("PassiveSafetyService_client", "GetVehicleCrashStatus", {}, {"out": [
                {"RollOverCrash": roll_over_crash, "FrontCrash": front_crash, "RearCrash": rear_crash,
                 "LeftCrash": left_crash, "RightCrash": right_crash}]})

    def event_vehicle_collision_warning_sts(self, roll_over_crash: bool = False, front_crash: bool = False,
                                            rear_crash: bool = False, left_crash: bool = False,
                                            right_crash: bool = False):
        prompt_info = f"----------> 通过SOA发送 PassiveSafetyService:PedestrianProtectionWarning 通知车辆碰撞状态改变事件上报"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("PassiveSafetyService_client", "NotifyVehicleCrashStatus", {
                "crash": {"RollOverCrash": roll_over_crash, "FrontCrash": front_crash, "RearCrash": rear_crash,
                          "LeftCrash": left_crash, "RightCrash": right_crash}})

    def get_and_event_check_vehicle_collision_warning_sts(self, roll_over_crash: bool = False,
                                                          front_crash: bool = False, rear_crash: bool = False,
                                                          left_crash: bool = False, right_crash: bool = False):
        self.event_vehicle_collision_warning_sts(roll_over_crash=roll_over_crash, front_crash=front_crash,
                                                 rear_crash=rear_crash, left_crash=left_crash, right_crash=right_crash)
        self.get_vehicle_collision_warning_sts(roll_over_crash=roll_over_crash, front_crash=front_crash,
                                               rear_crash=rear_crash, left_crash=left_crash, right_crash=right_crash)

    def hmi_light_control(self, type: LightType, zone: LightZone, mode: LightMode, brightness: int = 0,
                          color: dict = {"R": 0, "G": 0, "B": 0}):
        prompt_info = f"----------> 通过SOA发送LightService:LightControl来设置灯,类型设为{type.name},区域设为{zone.name},模式设为{mode.name},亮度设为{brightness},颜色设为{color}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("LightService_client", "LightControl", {"lights": [
                {"light": {"type": type.value, "zoneId": zone.value}, "mode": mode.value, "brightness": brightness,
                 "color": {"cRed": color["R"], "cGreen": color["G"], "cBlue": color["B"]}}]})

    def hmi_control_ai_and_alm_light(self, type: LightType, zone: LightZone, pixel_data: list = [0],
                                     pixel_type: PixelType = PixelType.RgbBmp, brightness: int = 0,
                                     color: dict = {"R": 0, "G": 0, "B": 0}):
        prompt_info = f"----------> 通过SOA发送LightService:LightShowControlWithLightDevice来设置AI灯和氛围灯的控制,类型设为{type.name},区域设为{zone.name},亮度设为{brightness},颜色设为{color}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("LightService_client", "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": type.value, "zoneId": zone.value}, "PixelData": pixel_data, "type": pixel_type.value,
                 "color": [{"brightness": brightness,
                            "color": {"cRed": color["R"], "cGreen": color["G"], "cBlue": color["B"]}}]}]})

    def hmi_set_intr_light_mode(self, mode: LightMode = LightMode.Auto):
        logger.info("将内灯为Auto模式")
        self.hmi_light_control(type=LightType.LightCourtesy, zone=LightZone.LightZoneAllOrSingle, mode=mode)

    def set_alm_color_brightness(self, brightness: int = 0, color: dict = {"R": 255, "G": 0, "B": 0}):
        self.hmi_control_ai_and_alm_light(type=LightType.LightGeneralAmbient, zone=LightZone.LightZoneFrontLeft,
                                          brightness=brightness, color=color)

    def notify_SeatOccupyStatus(self, seatid: list = [0, 1, 4, 5, 6], rawsensorstatus: list = [0, 0, 0, 0, 0],
                                status: list = [0, 0, 0, 0, 0]):
        prompt_info = f"----------> 通过SOA发送 SeatService:SeatOccupyStatus座椅占位信息，MarsOne支持主副驾及后排座椅"
        with allure.step(prompt_info):
            logger.info(prompt_info)
        occupied_status = [
            {"seatId": 0, "rawSensorStatus": 0, "status": 0},
            {"seatId": 1, "rawSensorStatus": 0, "status": 0},
            {"seatId": 2, "rawSensorStatus": 0, "status": 0},
            {"seatId": 3, "rawSensorStatus": 0, "status": 0},
            {"seatId": 4, "rawSensorStatus": 0, "status": 0},
            {"seatId": 5, "rawSensorStatus": 0, "status": 0},
            {"seatId": 6, "rawSensorStatus": 0, "status": 0}
        ]
        for id in range(0, len(seatid)):
            occupied_status[seatid[id]]["rawSensorStatus"] = rawsensorstatus[id]
            occupied_status[seatid[id]]["status"] = status[id]
        self.soa_partner.send_event_notify("SeatService_server", "SeatOccupyStatus", {'infos': occupied_status})


    # def notify_SeatOccupyStatus_new(self,fr_le:Union[SeatOccupySts,None] = None,fr_ri:Union[SeatOccupySts,None] = None,
    #                                 fr_mid:Union[SeatOccupySts,None] = None,fr_all:Union[SeatOccupySts,None] = None,
    #                                 re_le:Union[SeatOccupySts,None] = None,re_ri:Union[SeatOccupySts,None] = None,
    #                                 re_mid:Union[SeatOccupySts,None] = None,re_all:Union[SeatOccupySts,None] = None
    #                                 ):
    #     prompt_info = f"----------> 通过SOA发送 SeatService:SeatOccupyStatus座椅占位信息，MarsOne支持主副驾及后排座椅"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         occupied_status = []
    #         if fr_le is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 前排左座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 0, "rawSensorStatus": fr_le.sensor_sts.value, "status": fr_le.sts.value})
    #         if fr_ri is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 前排右座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 1, "rawSensorStatus": fr_ri.sensor_sts.value, "status": fr_ri.sts.value})
    #         if fr_mid is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 前排中座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 2, "rawSensorStatus": fr_mid.sensor_sts.value, "status": fr_mid.sts.value})
    #         if fr_all is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 第一排全部座椅座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 3, "rawSensorStatus": fr_all.sensor_sts.value, "status": fr_all.sts.value})
    #         if re_le is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 后排左座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 4, "rawSensorStatus": re_le.sensor_sts.value, "status": re_le.sts.value})
    #         if re_ri is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 后排右座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 5, "rawSensorStatus": re_ri.sensor_sts.value, "status": re_ri.sts.value})
    #         if re_mid is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 后排中座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 6, "rawSensorStatus": re_mid.sensor_sts.value, "status": re_mid.sts.value})
    #         if re_all is not None:
    #             logger.info(f"通过SOA发送 SeatService:SeatOccupyStatus 后排全部座椅座椅占位传感器状态为{fr_le.sensor_sts.name},座椅占位信息为{fr_le.sts.name}")
    #             occupied_status.append({"seatId": 7, "rawSensorStatus": re_all.sensor_sts.value, "status": re_all.sts.value})

    #     for id in range(0, len(seatid)):
    #         occupied_status[seatid[id]]["rawSensorStatus"] = rawsensorstatus[id]
    #         occupied_status[seatid[id]]["status"] = status[id]
    #     self.soa_partner.send_event_notify("SeatService_server", "SeatOccupyStatus", {'infos': occupied_status})

    def check_getEquipmentInfo_req(self, timeout: Union[float, int]):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService_server:getEquipmentInfo请求"):
            logger.info("通过SOA Partner监听TCAM是否发出HighVoltageService_server:getEquipmentInfo请求")
            self.ck_s2s_req("HighVoltageService_server", "getEquipmentInfo", timeout=timeout)

    def response_to_getEquipmentInfo_req(self, max_current: float, equipment_types: list, actual_current: float):
        prompt_info = f"----------> 通过SOA Partne发送HighVoltageService_server:getEquipmentInfo请求的响应,\
                        响应的关键参数充电桩信息为:{max_current}, {equipment_types}, {actual_current}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageService_server", "getEquipmentInfo",
                                                  {
                                                      "maxCurrent": max_current,
                                                      "actualCurrent": actual_current,
                                                      "equipmentTypes": equipment_types
                                                  })

    def check_getEquipmentInfo_req_and_feedback_resp(self, max_current: float, equipment_types: list,
                                                     actual_current: float, timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取HighVoltageService_server:getEquipmentInfo请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_getEquipmentInfo_req(timeout)  # 监听TCAM发送获取方向盘加热请求
            self.response_to_getEquipmentInfo_req(max_current, equipment_types, actual_current)

    def check_SetCharging_req(self, req: bool, timeout: Union[float, int]):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService_server:SetCharging请求"):
            logger.info("通过SOA Partner监听TCAM是否发出HighVoltageService_server:SetCharging请求")
            self.ck_s2s_req("HighVoltageService_server", "SetCharging", {"on": req}, timeout=timeout)

    def set_tcam_rvc_common_preconditions(self):
        prompt_info = f"----------> 通过SOA设置TCAM单域远程车控通用前置条件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.s2s_set_car_mode(car_mode=CarMode.NORMAL)
            self.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
            self.s2s_set_gear(gear=Gear.Park)
            self.notify_fota_status(state=FOTAMasteSts.IDLE)
            self.s2s_set_mntnmode(mntnmode=False)
            self.notify_HVSOCInfo(displaySoc=90)
            self.notify_VehicleTimeInfo(sync_sts=TimeSyncSts.NTP)
            self.notify_SeatOccupyStatus()

    def notify_BattMaintReqSts(self, battmaintreqsts: BattMaintReqSts):
        with allure.step(f"通过SOA Partner发送HighVoltageService:BattMaintReqSts事件通知"):
            logger.info(f"通过SOA Partner发送HighVoltageService:BattMaintReqSts事件通知sts: {battmaintreqsts.value}")
            self.soa_partner.send_event_notify("HighVoltageService_server", "BattMaintReqSts",
                                               {"sts": battmaintreqsts.value})

    def start_battery_heating_success_plan_a(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟正常开启电池加热插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=29.9, actual_current=29, equipment_types=[1],timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=29.9, actual_current=29, equipment_types=[1],timeout=10)
            self.check_SetBatteryHeating_req(timeout=5)
            self.check_SetCharging_req(req=True, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=10)
            time.sleep(1)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件

    def start_battery_heating_success_plan_b_b1(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟正常开启电池加热非插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=10)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(1)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件

    def start_battery_heating_success_plan_b_b2(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟正常开启电池加热非集度桩插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[2],timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[2],timeout=10)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(1)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件

    def start_battery_heating_success_plan_b_b3(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟正常开启电池加热非集度桩插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[1],timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[2],timeout=10)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(1)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件

    def check_climate_heat_status_and_get_mintemp(self, mintemp: float):
        prompt_info = f"----------> 通过SOA监听climate请求并返回响应, 监听获取最低温度请求并返回响应, 监听获取充电信息请求并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)

    def check_climate_heat_status_and_get_mintemp_and_get_charginfo(self, mintemp: float,
                                                                    plug_sts: PluggerSts = PluggerSts.ConnectedWithoutPower,
                                                                    charg_sts: ChargingSts = ChargingSts.NoCharging):
        prompt_info = f"----------> 通过SOA监听climate请求并返回响应, 监听获取最低温度请求并返回响应, 监听获取充电信息请求并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=charg_sts, plug_sts=plug_sts, timeout=5)

    def event_check_steer_wheel_sts(self, stalk_id: StalkId, press_type: PressType, is_valid: bool):
        prompt_info = f"----------> 通过SteerWheelService: StalkStatus 查看是否有拨杆状态改变的通知.期望的方向盘拨杆ID{stalk_id.name},拨杆拨动类型{press_type.name},有效状态为{is_valid}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("SteerWheelService_client", "StalkStatus",
                              {"infos": [{"stalkId": stalk_id.value, "state": press_type.value, "isValid": is_valid}]})

    def hmi_set_climate_defrost_mode(self, mode: bool):
        prompt_info = f"----------> 通过SteerWheelService: SetFastDefrostMode 设置强力除霜模式为{mode}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "SetFastDefrostMode", {"on": mode})

    def check_SetRemoteClimateSwitchToHV_req(self, isOn: bool = True, keep_time: int = 30,
                                             timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetRemoteClimateSwitchToHV",
                            {"isOn": isOn, "time": keep_time}, timeout=timeout)

    def response_to_SetRemoteClimateSwitchToHV_req(self):
        prompt_info = f"----------> 通过SOA Partner发送远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("ClimateControlService_server", "SetRemoteClimateSwitchToHV", args=None)

    def check_SetRemoteClimateSwitchToHV_req_feedback_resp(self, isOn: bool = True, keep_time: int = 30,
                                             timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req(isOn=isOn, keep_time=keep_time, timeout=timeout)
            self.response_to_SetRemoteClimateSwitchToHV_req()


    def check_SetRemoteClimateSwitchToHVDelay_req(self, extendtime: int = 30, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetRemoteClimateSwitchToHVDelay",
                            {"extendtime": extendtime}, timeout=timeout)

    def notify_RemoteClimateHVStatus(self, remote_climate_Status: RemoteClimateStatus):
        prompt_info = f"----------> 通过SOA Partner发送远程上高压状态事件:ClimateControlService:RemoteClimateHVStatus sts: {remote_climate_Status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ClimateControlService_server", "RemoteClimateHVStatus",
                                               {'sts': remote_climate_Status.value})

    def check_RemoteOn_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程开启空调请求:ClimateControlService:RemoteOn"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "RemoteOn", timeout=timeout)

    def response_to_RemoteOn_req(self):
        prompt_info = f"----------> 通过SOA Partner发送远程开启空调请求:ClimateControlService:RemoteOn的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("ClimateControlService_server", "RemoteOn", args=None)

    def check_RemoteOn_req_and_feedback_resp(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程开启空调请求:ClimateControlService:RemoteOn,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_RemoteOn_req(timeout=timeout)
            self.response_to_RemoteOn_req()

    def check_RemoteOff_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭空调请求:ClimateControlService:RemoteOff"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "RemoteOff", timeout=timeout)

    def response_to_RemoteOff_req(self):
        prompt_info = f"----------> 通过SOA Partner发送远程关闭空调请求:ClimateControlService:RemoteOff的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("ClimateControlService_server", "RemoteOff", args=None)

    def check_RemoteOff_req_and_feedback_resp(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭空调请求:ClimateControlService:RemoteOff,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_RemoteOff_req(timeout=timeout)
            self.response_to_RemoteOff_req()

    def check_SetTemperature_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程设置空调温度请求:ClimateControlService:SetTemperature"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetTemperature", {"zoneId": zoneid.value, "value": temp},
                            timeout=timeout)

    def check_SetTemperature_and_remote_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程设置空调温度请求:ClimateControlService:SetTemperature与RemoteOn"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req_v20("ClimateControlService_server", ["SetTemperature", "RemoteOn"],
                                [{"zoneId": zoneid.value, "value": temp}, None], timeout=timeout)

    def check_SetTemperatureAndOn_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程设置空调温度并关联空调启动请求:ClimateControlService:SetTemperatureAndOn"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetTemperatureAndOn",
                            {"zoneId": zoneid.value, "value": temp}, timeout=timeout)

    def check_Off_req(self, zoneid: ClimateZoneId, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭本地空调请求:ClimateControlService:Off"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "Off", {"zoneId": zoneid.value}, timeout=timeout)

    def notify_RemotePowerStatus(self, sts: RemoteClimateStatus = RemoteClimateStatus.On):
        prompt_info = f"----------> 通过SOA Partner发送远程上高压状态事件:ClimateControlService:RemotePowerStatus status {sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ClimateControlService_server", "RemotePowerStatus",
                                               {"status": sts.value})

    def check_GetClimateSystemStatus_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭本地空调请求:ClimateControlService:GetClimateSystemStatus"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "GetClimateSystemStatus", timeout=timeout)

    def response_to_GetClimateSystemStatus(self, ac_status: bool = False, temp_dri: float = 0, temp_pass: float = 0,
                                           temp_sec: float = 0, temp_sec_left: float = 0,
                                           temp_sec_right: float = 0, wind_speed_firrow: WindSpeed = WindSpeed.kOff,
                                           wind_speed_secrow: WindSpeed = WindSpeed.kOff,
                                           airmodedri_windmode: WindMode = WindMode.WindAuto,
                                           airmodedri_auto: bool = True,
                                           airmodepass_windmode: WindMode = WindMode.WindAuto,
                                           airmodepass_auto: bool = True,
                                           airmodesecrow_windmode: WindMode = WindMode.WindAuto,
                                           airmodesecrow_auto: bool = True, ison: bool = True,
                                           first_row_power_status: bool = True, second_row_power_status: bool = True,
                                           cooling_heating_status: CoolingHeatingStatus = CoolingHeatingStatus.kNone):
        prompt_info = f"----------> 通过SOA Partner模拟BGM返回响应:ClimateControlService:GetClimateSystemStatus"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("ClimateControlService_server", "GetClimateSystemStatus", {"acStatus": ac_status,
                                                                                                 "tempDriver": temp_dri,
                                                                                                 "tempPassenger": temp_pass,
                                                                                                 "tempSecRow": temp_sec,
                                                                                                 "tempSecLeft": temp_sec_left,
                                                                                                 "tempSecRight": temp_sec_right,
                                                                                                 "windSpeedFirRow": wind_speed_firrow.value,
                                                                                                 "windSpeedSecRow": wind_speed_secrow.value,
                                                                                                 "airModeDriver": {
                                                                                                     "mode": airmodedri_windmode.value,
                                                                                                     "isWindModeAuto": airmodedri_auto
                                                                                                 },
                                                                                                 "airModeDriver": {
                                                                                                     "mode": airmodepass_windmode.value,
                                                                                                     "isWindModeAuto": airmodepass_auto
                                                                                                 },
                                                                                                 "airModeDriver": {
                                                                                                     "mode": airmodesecrow_windmode.value,
                                                                                                     "isWindModeAuto": airmodesecrow_auto
                                                                                                 },
                                                                                                 "isOn": ison,
                                                                                                 "firstRowPowerStatus": first_row_power_status,
                                                                                                 "secondRowPowerStatus": second_row_power_status,
                                                                                                 "status": cooling_heating_status.value
                                                                                                 })

    def notify_ClimateSystemStatus(self, ac_status: bool = False, temp_dri: float = 0, temp_pass: float = 0,
                                   temp_sec: float = 0, temp_sec_left: float = 0,
                                   temp_sec_right: float = 0, wind_speed_firrow: WindSpeed = WindSpeed.kOff,
                                   wind_speed_secrow: WindSpeed = WindSpeed.kOff,
                                   airmodedri_windmode: WindMode = WindMode.WindAuto, airmodedri_auto: bool = True,
                                   airmodepass_windmode: WindMode = WindMode.WindAuto,
                                   airmodepass_auto: bool = True, airmodesecrow_windmode: WindMode = WindMode.WindAuto,
                                   airmodesecrow_auto: bool = True, ison: bool = True,
                                   first_row_power_status: bool = True, second_row_power_status: bool = True,
                                   cooling_heating_status: CoolingHeatingStatus = CoolingHeatingStatus.kNone):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送:ClimateControlService:ClimateSystemStatus"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("ClimateControlService_server", "ClimateSystemStatus",
                                   {"status": {"acStatus": ac_status,
                                               "tempDriver": temp_dri,
                                               "tempPassenger": temp_pass,
                                               "tempSecRow": temp_sec,
                                               "tempSecLeft": temp_sec_left,
                                               "tempSecRight": temp_sec_right,
                                               "windSpeedFirRow": wind_speed_firrow.value,
                                               "windSpeedSecRow": wind_speed_secrow.value,
                                               "airModeDriver": {
                                                   "mode": airmodedri_windmode.value,
                                                   "isWindModeAuto": airmodedri_auto
                                               },
                                               "airModeDriver": {
                                                   "mode": airmodepass_windmode.value,
                                                   "isWindModeAuto": airmodepass_auto
                                               },
                                               "airModeDriver": {
                                                   "mode": airmodesecrow_windmode.value,
                                                   "isWindModeAuto": airmodesecrow_auto
                                               },
                                               "isOn": ison,
                                               "firstRowPowerStatus": first_row_power_status,
                                               "secondRowPowerStatus": second_row_power_status,
                                               "status": cooling_heating_status.value
                                               }})

    def notify_ClimateFault(self, fault_id: FaultId = FaultId.OK, fault_msg: str = "OK"):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送事件信息:ClimateControlService:ClimateFault.faults {fault_id.name}, {fault_msg}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("ClimateControlService_server", "ClimateFault",
                                   {"faults": [{"faultId": fault_id.value, "faultMsg": fault_msg}]})

    def notify_SetClimateTempMaintainSts(self, id: str = "SetClimateTempMaintainSts", data: str = "0"):
        prompt_info = f"----------> 通过SOA Partner模拟CDC发送温度维持事件通知:InteractiveService:SetClimateTempMaintainSts"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("InteractiveService_server", "SetClimateTempMaintainSts",
                                   {"values": [{"id": id, "data": data}]})

    def notify_LockActTriggerSource(self, trigger_source_id: TriggerSourceId.RemoteKey):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:LockActTriggerSource.TriggerSourceId {trigger_source_id.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("CentralLockService_server", "LockActTriggerSource",
                                   {"sourceId": trigger_source_id.value})

    def notify_NotifyCentralLockSysInfo(self, sts: LockStatus = LockStatus.Undef,
                                     trigger_id: TriggerSourceId = TriggerSourceId.RemoteKey, update_eve: bool = False):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:CentralLockStatusInfo sts: {sts.value}, triggerId: {trigger_id}\
                       updateEve: {update_eve}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo", {"info": {"sts": sts.value,
                                                                                                  "triggerId": trigger_id.value,
                                                                                                  "updateEve": update_eve}})

    def notify_NotifyACDefrostSts(self, defrost_max: bool = False, climate_defrost: bool = False):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送除霜状态事件通知:ClimateControlService:NotifyACDefrostSts defrostMax: {defrost_max}, \
            climateDefrost: {climate_defrost}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("ClimateControlService_server", "NotifyACDefrostSts",
                                   {"sts": {"defrostMax": defrost_max,
                                            "climateDefrost": climate_defrost}})

    def check_ShieldWindowService_GetHeat_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ShieldWindowService:GetHeat请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ShieldWindowService:GetHeat请求")
            self.ck_s2s_req("ShieldWindowService_server", "GetHeat", timeout=timeout)

    def response_to_ShieldWindowService_GetHeat_req(self, id: ShieldWindowId = ShieldWindowId.ShieldWindowFront,
                                                    status: HeatStatus = HeatStatus.HeatStatusAutoOn):
        prompt_info = f"----------> 通过SOA Partner发送ShieldWindowService:GetHeat请求的响应, id:{id.value}, status: {status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("ShieldWindowService_server", "GetHeat",
                                                  args = [{"id": id.value, "status": status.value}])

    def check_ShieldWindowService_GetHeat_req_and_feedback_resp(self,
                                                                id: ShieldWindowId = ShieldWindowId.ShieldWindowFront,
                                                                status: HeatStatus = HeatStatus.HeatStatusAutoOn,
                                                                timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取ShieldWindowService:GetHeat请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_ShieldWindowService_GetHeat_req(timeout)
            self.response_to_ShieldWindowService_GetHeat_req(id=id, status=status)

    def check_OuterRearViewService_GetHeat_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出OuterRearViewService:GetHeat请求"):
            logger.info("通过SOA Partner监听TCAM是否发出OuterRearViewService:GetHeat请求")
            self.ck_s2s_req("OuterRearViewService_server", "GetHeat", timeout=timeout)

    def response_to_OuterRearViewService_GetHeat_req(self, id: ViewId = ViewId.RearViewAll, ison: bool = True):
        prompt_info = f"----------> 通过SOA Partner发送OuterRearViewService:GetHeat请求的响应, id:{id.value}, ison: {ison}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("OuterRearViewService_server", "GetHeat",
                                                  args = [{"id": id.value, "isOn": ison}])

    def check_OuterRearViewService_GetHeat_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll,
                                                                 ison: bool = True, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取OuterRearViewService:GetHeat请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_OuterRearViewService_GetHeat_req(timeout)
            self.response_to_OuterRearViewService_GetHeat_req(id=id, ison=ison)

    def notify_ShieldWindowService_HeatStatus(self, heat_status: HeatStatus = HeatStatus.HeatStatusAutoOn,
                                              id: ShieldWindowId = ShieldWindowId.ShieldWindowAll):
        prompt_info = f"----------> 通过SOA Partner发送后窗加热状态事件:ShieldWindowService:HeatStatus id {id.value}, HeatStatus {heat_status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ShieldWindowService_server", "HeatStatus",
                                               {"sts": {"id": id.value,
                                                        "status": heat_status.value}})

    def notify_OuterRearViewService_HeatStatus(self, id: ViewId = ViewId.RearViewAll, status: bool = False):
        prompt_info = f"----------> 通过SOA Partner发送外后视镜加热状态事件:OuterRearViewService:HeatStatus id {id.value}, status {status}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("OuterRearViewService_server", "HeatStatus",
                                               {"id": id.value, "status": status})

    def notify_hvActiveSts(self, sts: HVActiveSts = HVActiveSts.Close):
        prompt_info = f"----------> 通过SOA Partner发送高压继电器闭合状态事件:HighVoltageService:hvActiveSts sts {sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("HighVoltageService_server", "hvActiveSts", {"sts": sts.value})

    def check_SetFastDefrostMode_req(self, on: bool = True, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:SetFastDefrostMode请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ClimateControlService:SetFastDefrostMode请求")
            self.ck_s2s_req("ClimateControlService_server", "SetFastDefrostMode", {"on": on}, timeout=timeout)

    def check_ShieldWindowService_SetHeat_req(self, id: ShieldWindowId = ShieldWindowId.ShieldWindowAll,
                                              heat_status: HeatStatus = HeatStatus.HeatStatusAutoOn,
                                              timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ShieldWindowService:SetHeat请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ShieldWindowService:SetHeat请求")
            self.ck_s2s_req("ShieldWindowService_server", "SetHeat",
                            {"heat": {"id": id.value, "status": heat_status.value}}, timeout=timeout)

    def check_SeatService_SetHeatingLevel_req(self, id: SeatId = SeatId.All, info: HeatLevel = HeatLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求")
            self.ck_s2s_req("SeatService_server", "SetHeatingLevel",
                            {"params": [{"id": id.value, "uint8Info": info.value}], "source": source.value}, timeout=timeout)

    def response_to_SeatService_SetHeatingLevel_req(self):
        with allure.step("通过SOA Partner发送SeatService:SetHeatingLevel请求的响应"):
            logger.info("通过SOA Partner发送SeatService:SetHeatingLevel请求的响应")
            self.send_method_response("SeatService_server", "SetHeatingLevel", args=None)

    def check_SeatService_SetHeatingLevel_req_and_feedback_resp(self, id: SeatId = SeatId.All, info: HeatLevel = HeatLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求并返回响应")
            self.check_SeatService_SetHeatingLevel_req(id=id, info=info, source=source, timeout=timeout)
            self.response_to_SeatService_SetHeatingLevel_req()

    def notify_SeatHeatVentStatus(self, id: SeatId = SeatId.FrontLeft, 
                                  heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                  heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                  vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                  vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送座椅加热通风状态事件:SeatService:SeatHeatVentStatus: id {id.value}, heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "SeatHeatVentStatus", {"id": id.value,
                                                                                            "status": {
                                                                                                "heatLevel": heat_level.value,
                                                                                                "heatTime": heat_time,
                                                                                                "heatWorkStatus": heat_work_sts.value,
                                                                                                "ventLevel": vent_level.value,
                                                                                                "ventTime": vent_time,
                                                                                                "ventWorkStatus": vent_work_sts.value
                                                                                            }})

    def notify_FrntLeftSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "FrntLeftSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})

    def notify_FrntRightSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "FrntRightSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})

    def notify_RearLeftSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送左后座椅加热通风状态事件:SeatService:RearLeftSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "RearLeftSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})

    def notify_RearRightSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送左后座椅加热通风状态事件:SeatService:RearLeftSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "RearRightSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})

    def check_SteerWheelService_SetHeat_req(self, heat_level: HeatLevel = HeatLevel.Off,
                                            source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求")
            self.ck_s2s_req("SteerWheelService_server", "SetHeat", {"status": heat_level.value, "source": source.value},
                            timeout=timeout)

    def reponse_to_SteerWheelService_SetHeat_req(self, heat_level: HeatLevel = HeatLevel.Off,
                                            timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner发送SteerWheelService:SetHeat请求的响应"):
            logger.info("通过SOA Partner发送SteerWheelService:SetHeat请求的响应")
            self.send_method_response("SteerWheelService_server", "SetHeat", args=None)

    def check_SteerWheelService_SetHeat_req_and_feedback_resp(self, heat_level: HeatLevel = HeatLevel.Off,
                                            source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求并返回响应")
            self.check_SteerWheelService_SetHeat_req(heat_level=heat_level, source=source, timeout=timeout)
            self.reponse_to_SteerWheelService_SetHeat_req()

    def notify_SteerWheelService_Heat(self, heat_level: HeatLevel = HeatLevel.Off, source: SourceId = SourceId.Remote):
        prompt_info = f"----------> 通过SOA Partner发送方向盘加热状态事件:SteerWheelService:Heat heatlevel {heat_level.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SteerWheelService_server", "Heat", {"sts": {"level": heat_level.value, "source": source.value}})

    def notify_SteerHeatAvailiable(self, availiable: SteerHeatAvailiable = SteerHeatAvailiable.On):
        prompt_info = f"----------> 通过SOA Partner发送方向盘加热可用状态事件:SteerWheelService:SteerHeatAvailiable SteerHeatAvailiable {availiable.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SteerWheelService_server", "SteerHeatAvailiable", {"status": availiable.value})

    def check_GetSteerHeatAvailiable_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SteerWheelService:GetSteerHeatAvailiable请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SteerWheelService:GetSteerHeatAvailiable请求")
            self.ck_s2s_req("SteerWheelService_server", "GetSteerHeatAvailiable", timeout=timeout)

    def response_to_GetSteerHeatAvailiable_req(self, availiable: SteerHeatAvailiable = SteerHeatAvailiable.On):
        prompt_info = f"----------> 通过SOA Partner发送SteerWheelService:GetSteerHeatAvailiable请求的响应, SteerHeatAvailiable:{availiable.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("SteerWheelService_server", "GetSteerHeatAvailiable",
                                                  args = availiable.value)

    def check_GetSteerHeatAvailiable_req_and_feedback_resp(self,
                                                           availiable: SteerHeatAvailiable = SteerHeatAvailiable.On,
                                                           timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取SteerWheelService:GetSteerHeatAvailiable请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSteerHeatAvailiable_req(timeout)
            self.response_to_GetSteerHeatAvailiable_req(availiable=availiable)

    def check_PedalService_GetStatus_req(self, pedalid: PedalId = PedalId.PedalBraker, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出PedalService:GetStatus请求"):
            logger.info("通过SOA Partner监听TCAM是否发出PedalService:GetStatus请求")
            self.ck_s2s_req("PedalService_server", "GetStatus", {"pedals": [pedalid.value]}, timeout=timeout)

    def response_to_PedalService_GetStatus_req(self, pedalid: PedalId = PedalId.PedalBraker,
                                               sts: PressedStatus = PressedStatus.PedalNA):
        prompt_info = f"----------> 通过SOA Partner发送PedalService:GetStatus请求的响应, PedalId:{pedalid.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("PedalService_server", "GetStatus", args = [pedalid.value])

    def check_PedalService_GetStatus_req_and_feedback_resp(self, pedalid: PedalId = PedalId.PedalBraker,
                                                           sts: PressedStatus = PressedStatus.PedalNA,
                                                           timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取PedalService:GetStatus请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_PedalService_GetStatus_req(pedalid=pedalid, timeout=timeout)
            self.response_to_PedalService_GetStatus_req(pedalid=pedalid, sts=sts)

    def check_NotifyRemoteAuthStartSts_event(self, is_valid: bool = True, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRemoteAuthStartSts事件"):
            logger.info("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRemoteAuthStartSts事件")
            self.chk_notify("RemoteCtrlService_client", "NotifyRemoteAuthStartSts", {"isValid": is_valid},
                            timeout=timeout)

    def hmi_set_reset_config_sts(self):
        prompt_info = f"----------> ResetSOAConfigService_client: ResetAllVehicleSOAConfig 设置随车项恢复出厂设置"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request('ResetSOAConfigService_client', 'ResetAllVehicleSOAConfig', args={})

    def get_climate_sys_sts(self, ac_sts: Union[bool, None] = None,
                            temp_dri: Union[float, int, None] = None, temp_pass: Union[float, int, None] = None,
                            temp_sec_row: Union[float, int, None] = None,
                            wind_spd_first_row: Union[WindSpeed, None] = None,
                            wind_spd_sec_row: Union[WindSpeed, None] = None,
                            air_mode_dri: Union[AirWindMode, None] = None, is_wind_mode_auto_dri: [bool, None] = None,
                            air_mode_pass: Union[AirWindMode, None] = None, is_wind_mode_auto_pass: [bool, None] = None,
                            air_mode_sec_row: Union[AirWindMode, None] = None,
                            is_wind_mode_auto_sec_row: [bool, None] = None,
                            power_sts_first_row: [bool, None] = None, power_sts_sec_row: [bool, None] = None,
                            time_wait: Union[float, int, None] = 0, timeout: Union[float, int, None] = 1):

        prompt_info = f"----------> ClimateControlService_client: GetClimateSystemStatus获取空调系统状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            param_dic = {}
            temp_dic_dri = {}
            temp_dic_pass = {}
            temp_dic_sec_row = {}
            if ac_sts is not None:
                logger.info(f"--------------->check A/C状态是否为{ac_sts}")
                param_dic["acStatus"] = ac_sts
            if temp_dri is not None:
                logger.info(f"--------------->check驾驶位温度是否为{temp_dri}")
                param_dic["tempDriver"] = temp_dri
            if temp_pass is not None:
                logger.info(f"--------------->check 副驾驶位温度是否为{temp_pass}")
                param_dic["tempPassenger"] = temp_pass
            if temp_sec_row is not None:
                logger.info(f"--------------->check 后排温度是否为{temp_sec_row}")
                param_dic["tempSecRow"] = temp_sec_row
            if wind_spd_first_row is not None:
                logger.info(f"--------------->check 第一排风速是否为{wind_spd_first_row.name}")
                param_dic["windSpeedFirRow"] = wind_spd_first_row.value
            if wind_spd_sec_row is not None:
                logger.info(f"--------------->check 第二排风速是否为{wind_spd_sec_row.name}")
                param_dic["windSpeedSecRow"] = wind_spd_sec_row.value
            if air_mode_dri is not None:
                logger.info(f"--------------->check 驾驶位吹风模式是否为{air_mode_dri.name}")
                temp_dic_dri["mode"] = air_mode_dri.value
            if is_wind_mode_auto_dri is not None:
                logger.info(f"--------------->check 驾驶位是否位自动吹风模式，期望结果是{is_wind_mode_auto_dri}")
                temp_dic_dri["isWindModeAuto"] = is_wind_mode_auto_dri
            if air_mode_pass is not None:
                logger.info(f"--------------->check 副驶位吹风模式是否为{air_mode_pass.name}")
                temp_dic_pass["mode"] = air_mode_pass.value
            if is_wind_mode_auto_pass is not None:
                logger.info(f"--------------->check 副驾驶位是否位自动吹风模式，期望结果是{is_wind_mode_auto_pass}")
                temp_dic_pass["isWindModeAuto"] = is_wind_mode_auto_pass
            if air_mode_sec_row is not None:
                logger.info(f"--------------->check 第二排吹风模式是否为{air_mode_sec_row.name}")
                temp_dic_sec_row["mode"] = air_mode_sec_row.value
            if is_wind_mode_auto_sec_row is not None:
                logger.info(f"--------------->check 第二排是否位自动吹风模式，期望结果是{is_wind_mode_auto_sec_row}")
                temp_dic_sec_row["isWindModeAuto"] = is_wind_mode_auto_sec_row

            if temp_dic_dri != {}:
                param_dic["airModeDriver"] = temp_dic_dri

            if temp_dic_dri != {}:
                param_dic["airModePassenger"] = temp_dic_dri

            if temp_dic_sec_row != {}:
                param_dic["airModeSecRow"] = temp_dic_sec_row

            if power_sts_first_row is not None:
                logger.info(f"--------------->check 第一排空调开启状态是否位{power_sts_first_row}")
                param_dic["firstRowPowerStatus"] = power_sts_first_row
            if power_sts_sec_row is not None:
                logger.info(f"--------------->check 第二排空调开启状态是否位{power_sts_sec_row}")
                param_dic["secondRowPowerStatus"] = power_sts_sec_row

            logger.info(f"-------------------->GetClimateSystemStatus 入参为:{param_dic}")

            self.send_request_and_ck_resp('ClimateControlService_client', "GetClimateSystemStatus", {},
                                          {"out": param_dic}, timeout=timeout)
            sleep(time_wait)

    def hmi_set_climate_vent_sts(self, zone: ClimateZone, on: isOn):
        prompt_info = f"----------> ClimateControlService_client: SetAirVent 设置{zone.name}电动出风口开启关闭状态为{on.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", 'SetAirVent',
                                     {"zoneId": zone.value, "on": on.value})

    def hmi_set_climate_windmode_sts(self, zone: ClimateZone, mode: AirWindMode):
        prompt_info = f"----------> ClimateControlService_client: SetWindMode 设置{zone.name}空调吹风模式{mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "SetWindMode",
                                     {"zoneId": zone.value, "mode": mode.value})

    def get_windmode_sts(self, zone: ClimateZone, mode: AirWindMode):
        prompt_info = f"----------> ClimateControlService_client: GetWindMode 获取{zone.name}空调吹风模式{mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "GetWindMode",
                                     {"zoneId": zone.value, "mode": mode.value})
            
    def hmi_set_climate_temperature_sts(self, zone: ClimateZone, value: Union[float, int]):
        prompt_info = f"----------> ClimateControlService_client: SetTemperatureAndOn 设置{zone.name}设置空调温度（主/副/后排且联动空调开启{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "SetTemperatureAndOn",
                                     {"zoneId": zone.value, "value": value})

    def hmi_set_climate_temperature(self, zone: ClimateZone, value: Union[float, int]):
        prompt_info = f"----------> ClimateControlService_client: SetTemperature 设置{zone.name}空调温度{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", 'SetTemperature',
                                     {"zoneId": zone.value, "value": value})

    def hmi_set_auto_close_door_by_drive_gear(self, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> DoorService_client: SetAutoCloseTrigger 设置D档自动关门"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("DoorService_client", "SetAutoCloseTrigger", {"trigger": 0})
            sleep(time_wait)

    def hmi_set_key_config_info(self, key_type: KeyConfigType, value: int, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> KeyService_client: SetConfigInfo 设置钥匙配置信息为{key_type.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("KeyService_client", "SetConfigInfo",
                                     {"infos": [{"key": key_type.value, "value": value}]})
            sleep(time_wait)

    def hmi_set_diag_connect_sts(self, con_sts: int, con_act: int):
        prompt_info = f"----------> InterCommService_client_BGM_InterCommService: SetDiagnosticConnectStatus 设置诊断连接状态为{con_sts},激活状态为{con_act}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("InterCommService_client_BGM_InterCommService", 'SetDiagnosticConnectStatus',
                                     {"connectActive": con_act, 'connectStatus': con_sts})

    def check_no_wti_event(self, s2s_interface_name: str):
        prompt_info = f"---------->Check WTIService_client 中没有接口：{s2s_interface_name}相关事件上报"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_no_event("WTIService_client", s2s_interface_name)

    def get_horn_active_sts(self, sts: HornStatus):
        prompt_info = f"---------->通过 HornService:GetStatus 获取喇叭的状态，期望状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp('HornService_client', 'GetStatus', args={}, ck_info={'out': sts.value})

    def event_check_horn_sts(self, sts: HornStatus):
        prompt_info = f"---------->通过 HornService:Status 获取喇叭的状态改变通知，期望状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("HornService_client", "Status", {"sts": sts.value})

    def hmi_set_horn_sts(self, on_time: Union[float, int], off_time: Union[float, int], times: int):
        prompt_info = f"---------->通过 HornService:CyclicActivation 置喇叭周期性鸣笛{on_time}S开{off_time}S关共{times}次"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request(
                "HornService_client",
                "CyclicActivation",
                {"onTime": on_time * 1000, "offTime": off_time * 1000, "actNum": times},
            )

    def hmi_set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl, sourceId:SourceId):         #o_fan.liu 整改ok
        prompt_info = f"---------->通过 SeatService_client:SetHeatingLevel 通过{sourceId.name}，设置{pos.name}座椅加热等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "SetHeatingLevel",
                                     {"params": [{"id": pos.value, "uint8Info": level.value}], "source":sourceId.value})
            
#o_fan.liu
    def hmi_set_seat_vent_level(self, pos: SeatId, level: HeatVentiLvl, sourceId:SourceId):
        prompt_info = f"---------->通过 SeatService_client:SetVentingLevel 通过{sourceId.name}，设置{pos.name}座椅通风等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "SetVentingLevel",
                                     {"params": [{"id": pos.value, "uint8Info": level.value}], "source":sourceId.value})
            

    def hmi_set_seat_massg_level(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        prompt_info = f"---------->通过 SeatService_client:SetVentingLevel 设置{pos.name}座椅按摩开关为{is_on},类型为{type.name}，力度为{intensity.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "SetMassageConf",
                                     {"params": [{"id": pos.value, "conf": {"isOn": is_on, "type": type.value,
                                                                            "intensity": intensity.value}}]})

    def hmi_set_seat_adjust_direction(self, pos: SeatId, part: SeatPart, direction: AdjustDirection):
        prompt_info = f"---------->通过 SeatService_client:StartMoveDirection 调节{pos.name}座椅{part.name} 方向为{direction.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", 'StartMoveDirection',
                                     {"id": pos.value, "part": part.value, "direction": direction.value})

    def get_seat_massg_sts(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        prompt_info = f"---------->通过 SeatService_client:GetMassageConf 获取{pos.name}座椅按摩开关是否为{is_on},类型是否为{type.name}，力度是否为{intensity.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "GetMassageConf", {"seats": pos.value}, {
                "out": {"id": pos.value, "conf": {"isOn": is_on, "type": type.value, "intensity": intensity.value}}})

    def event_check_seat_massg_sts(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        prompt_info = f"---------->通过 SeatService_client:GetMassageConf 获取{pos.name}座椅按摩开关状态改变通知,是否为{is_on},类型是否为{type.name}，力度是否为{intensity.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("SeatService_client", "MassageConf", {"id": pos.value,
                                                                    "conf": {"isOn": is_on, "type": type.value,
                                                                             "intensity": intensity.value}})

    def get_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl):
        prompt_info = f"---------->通过 SeatService_client:GetHeatingLevel 获取{pos.name}座椅加热等级是否为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "GetHeatingLevel", {"seats": pos.value},
                                     {"out": [{"id": pos.value, "uint8Info": level.value}]})

    def get_seat_venti_level(self, pos: SeatId, level: HeatVentiLvl):
        prompt_info = f"---------->通过 SeatService_client:GetVentingLevel 获取{pos.name}座椅通风等级是否为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "GetVentingLevel", {"seats": pos.value},
                                     {"out": [{"id": pos.value, "uint8Info": level.value}]})

    def get_seat_position_info(self, pos: SeatId, back_angle: Union[int, float], long_pos: Union[int, float],
                               vertical_pos: Union[int, float], legrest_vertical_pos: Union[int, float]):
        prompt_info = f"---------->通过 SeatService_client:GetSeatPositionInfo 获取{pos.name}座椅靠背角度是否为{back_angle}，座椅前后位置是否为{long_pos}， 座椅高度位置是否为{vertical_pos}， 座椅腿托/坐垫高度位置是否为{legrest_vertical_pos}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("SeatService_client", "GetSeatPositionInfo", {"seats": [pos.value]},
                                          {"out": [{"id": pos.value, "position": {"backAngle": back_angle,
                                                                                  "longitudinalPosition": long_pos,
                                                                                  "verticalPosition": vertical_pos,
                                                                                  "LegrestVerticalPosition": legrest_vertical_pos}}]})

    def event_check_seat_position_info(self, pos: SeatId, back_angle: Union[int, float], long_pos: Union[int, float],
                                       vertical_pos: Union[int, float], legrest_vertical_pos: Union[int, float]):
        prompt_info = f"---------->通过 SeatService_client:SeatPosition 获取{pos.name}座椅靠背角度是否为{back_angle}，座椅前后位置是否为{long_pos}， 座椅高度位置是否为{vertical_pos}， 座椅腿托/坐垫高度位置是否为{legrest_vertical_pos}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("SeatService_client", "SeatPosition",
                              {"id": pos.value, "position": {"backAngle": back_angle, "longitudinalPosition": long_pos,
                                                             "verticalPosition": vertical_pos,
                                                             "LegrestVerticalPosition": legrest_vertical_pos}})

    def get_TailGate_GetStatus_sts(self, tailgate_sts: TailGateSts):
        prompt_info = f"----------> TailGateService_server GetStatus 请求{tailgate_sts.name}状态{tailgate_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_request("TailGateService_server", 'GetStatus',
                                                 {"tailgate_sts": tailgate_sts.value})

    def notify_DoorService_OpenCloseStatus(self, id: DoorId = DoorId.kDoorFrontLeft, isopen: bool = False):
        prompt_info = f"---------->通过 DoorService_server:OpenCloseStatus 发送门开关状态 id {id.value}, isOpen {isopen}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'OpenCloseStatus',
                                               {"sts": {"id": id.value, "isOpen": isopen}})

    def notify_FrntLeftDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        prompt_info = f"---------->通过 DoorService_server:FrntLeftDoorSts 发送主驾门开关状态 isOpenValidity {validity.value}, \
             isOpen {isopen}, sts {sts.value}, isAntiPinch {is_anti_pinchs}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'FrntLeftDoorSts',
                                               {"sts": {"openCloseSts":{"isOpen": isopen,
                                                                        "isOpenValidity": validity.value}, 
                                                        "sts": sts.value,
                                                        "isAntiPinch": is_anti_pinchs}})

    def notify_FrntRightDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        prompt_info = f"---------->通过 DoorService_server:FrntRightDoorSts 发送副驾门开关状态 isOpenValidity {validity.value}, \
             isOpen {isopen}, sts {sts.value}, isAntiPinch {is_anti_pinchs}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'FrntRightDoorSts',
                                               {"sts": {"openCloseSts":{"isOpen": isopen,
                                                                        "isOpenValidity": validity.value}, 
                                                        "sts": sts.value,
                                                        "isAntiPinch": is_anti_pinchs}})

    def notify_RearLeftDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        prompt_info = f"---------->通过 DoorService_server:RearLeftDoorSts 发送左后门开关状态 isOpenValidity {validity.value}, \
             isOpen {isopen}, sts {sts.value}, isAntiPinch {is_anti_pinchs}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'RearLeftDoorSts',
                                               {"sts": {"openCloseSts":{"isOpen": isopen,
                                                                        "isOpenValidity": validity.value}, 
                                                        "sts": sts.value,
                                                        "isAntiPinch": is_anti_pinchs}})

    def notify_RearRightDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        prompt_info = f"---------->通过 DoorService_server:RearRightDoorSts 发送右后门开关状态 isOpenValidity {validity.value}, \
             isOpen {isopen}, sts {sts.value}, isAntiPinch {is_anti_pinchs}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'RearRightDoorSts',
                                               {"sts": {"openCloseSts":{"isOpen": isopen,
                                                                        "isOpenValidity": validity.value}, 
                                                        "sts": sts.value,
                                                        "isAntiPinch": is_anti_pinchs}})


    def send_Alldoor_OpenCloseStatus_close(self):
        prompt_info = f"---------->通过 DoorService_server:OpenCloseStatus 发送门开关状态为所有门关闭"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.notify_DoorService_OpenCloseStatus(id=DoorId.kDoorFrontLeft)
            self.notify_DoorService_OpenCloseStatus(id=DoorId.kDoorRearRight)
            self.notify_DoorService_OpenCloseStatus(id=DoorId.kDoorRearLeft)
            self.notify_DoorService_OpenCloseStatus(id=DoorId.kDoorFrontRight)
            self.notify_DoorService_OpenCloseStatus(id=DoorId.kDoorAll)
            self.notify_TailGateService_OpenCloseStatus()

    def notify_DoorService_Status(self, id: DoorId = DoorId.kDoorFrontLeft, status: DoorStatus = DoorStatus.kClosed):
        prompt_info = f"---------->通过 DoorService_server:Status 发送门开关状态 id {id.value}, status {status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", 'Status',
                                               {"sts": {"id": id.value, "sts": status.value}})

    def send_Alldoor_Status_close(self):
        prompt_info = f"---------->通过 DoorService_server:Status 发送电动门运动状态为关闭"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.notify_DoorService_Status(id=DoorId.kDoorFrontLeft)
            self.notify_DoorService_Status(id=DoorId.kDoorFrontRight)
            self.notify_DoorService_Status(id=DoorId.kDoorRearLeft)
            self.notify_DoorService_Status(id=DoorId.kDoorRearRight)
            self.notify_DoorService_Status(id=DoorId.kDoorAll)
            self.notify_TailGateService_Status()

    def notify_LockStatus(self, lock_sts: LockSts):
        with allure.step(f"通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus为{lock_sts.value}"):
            logger.info(f"通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus为{lock_sts.value}")
            self.soa_partner.send_event_notify("CentralLockService_server", "LockStatus",
                                               {"sts": lock_sts.value})

    def notify_TailGateService_OpenCloseStatus(self, isopen: bool = False):
        with allure.step(f"通过SOA Partner发出尾门的状态TailGateService:OpenCloseStatus为{isopen}"):
            logger.info(f"通过SOA Partner发出尾门的状态TailGateService:OpenCloseStatus为{isopen}")
            self.soa_partner.send_event_notify("TailGateService_server", "OpenCloseStatus",
                                               {"sts": isopen})

    def notify_TailGateService_Status(self, tailgate_sts: TailGateSts = TailGateSts.kClosed):
        with allure.step(f"通过SOA Partner发出尾门的状态TailGateService::Status为{tailgate_sts.name}"):
            logger.info(f"通过SOA Partner发出尾门的状态TailGateService::Status为{tailgate_sts.name}")
            self.soa_partner.send_event_notify("TailGateService_server", "Status",
                                               {"sts": tailgate_sts.value})

    def check_SetDoorCloseLock_req(self, cmd: LockCmd = LockCmd.Lock,
                                   lock_req_source: LockReqSource = LockReqSource.Talematics,
                                   find_key_type: FindKeyType = FindKeyType.NoReq, timeout: Union[float, int] = 0.5):
        with allure.step("通过SOA Partner监听TCAM是否发出CentralLockService::SetDoorCloseLock请求"):
            logger.info("通过SOA Partner监听TCAM是否发出CentralLockService::SetDoorCloseLock请求")
            self.ck_s2s_req("CentralLockService_server", "SetDoorCloseLock", {"cmd": cmd.value,
                                                                              "source": lock_req_source.value,
                                                                              "findKeyType": find_key_type.value},
                            timeout=timeout)

    def response_to_SetDoorCloseLock_req(self):
        prompt_info = f"---------->使用SOA Partner模拟CentralLockService::SetDoorCloseLock请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("CentralLockService_server", "SetDoorCloseLock", args=None)

    def check_SetDoorCloseLock_req_and_feedback_resp(self, lock_cmd: LockCmd,
                                                     source: LockReqSource = LockReqSource.Talematics,
                                                     find_key_type: FindKeyType = FindKeyType.NoReq,
                                                     timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取CentralLockService::SetDoorCloseLock请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetDoorCloseLock_req(cmd=lock_cmd, lock_req_source=source, find_key_type=find_key_type,
                                            timeout=timeout)  # 监听TCAM发送接解闭锁请求
            self.response_to_SetDoorCloseLock_req()

    def check_SetTailGate_req(self, cmd: TailGateCmd = TailGateCmd.Open, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出尾门TailGateService::SetTailGate.Cmd请求"):
            logger.info("通过SOA Partner监听TCAM是否发出尾门TailGateService::SetTailGate.Cmd请求")
            self.ck_s2s_req("TailGateService_server", "SetTailGate", {"cmd": cmd.value}, timeout=timeout)

    def response_to_SetTailGate_req(self):
        prompt_info = f"----------> 通过SOA Partner发送尾门TailGateService::SetTailGate.Cmd请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("TailGateService_server", "SetTailGate", args=None)

    def check_SetTailGate_req_and_feedback_resp(self, cmd: TailGateCmd = TailGateCmd.Open,
                                                timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取尾门TailGateService::SetTailGate.Cmd请求, 并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetTailGate_req(cmd=cmd, timeout=timeout)  # 监听TCAM发送尾门请求
            self.response_to_SetTailGate_req()

    def check_TailGateService_SetPosition_req(self, pos: int, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出尾门翘起TailGateService::SetPosition请求"):
            logger.info("通过SOA Partner监听TCAM是否发出尾门翘起TailGateService::SetPosition请求")
            self.ck_s2s_req("TailGateService_server", "SetPosition", {"pos": pos}, timeout=timeout)

    def response_to_TailGateService_SetPosition_req(self):
        prompt_info = f"----------> 通过SOA Partner发送尾门翘起TailGateService::SetPosition请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("TailGateService_server", "SetPosition", args=None)

    def check_TailGateService_SetPosition_req_and_feedback_resp(self, pos: int, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取尾门翘起TailGateService::SetPosition请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetTailGate_req(pos=pos, timeout=timeout)  # 监听TCAM发送尾门翘起请求
            self.response_to_SetTailGate_req()

    def check_SetCarLocalTraceRequest_req(self, carloctr_req: CarLocalTraceReq = CarLocalTraceReq.kHornLiReq,
                                          timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出远程寻车KeyService::SetCarLocalTraceRequest请求"):
            logger.info("通过SOA Partner监听TCAM是否发出远程寻车KeyService::SetCarLocalTraceRequest请求")
            self.ck_s2s_req("KeyService_server", "SetCarLocalTraceRequest", {"carLoctrReq": carloctr_req.value},
                            timeout=timeout)

    def response_to_SetCarLocalTraceRequest_req(self):
        prompt_info = f"----------> 通过SOA Partner发送寻车KeyService::SetCarLocalTraceRequest请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("KeyService_server", "SetCarLocalTraceRequest", args=None)

    def check_SetCarLocalTraceRequest_req_and_feedback_resp(self,
                                                            carloctr_req: CarLocalTraceReq = CarLocalTraceReq.kHornLiReq,
                                                            timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取寻车KeyService::SetCarLoctrReq.carLoctrReq请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetCarLocalTraceRequest_req(carloctr_req=carloctr_req, timeout=timeout)  # 监听TCAM发送寻车请求
            self.response_to_SetCarLocalTraceRequest_req()

    def notify_NotifyTurnLampStatus(self, priority: int, turnlamp_mode: TurnLampMode = TurnLampMode.kHazard):
        with allure.step(
                f"通过SOA Partner发出转向灯的状态LightService::NotifyTurnLampStatus mode {turnlamp_mode.name}, priority {priority}"):
            logger.info(
                f"通过SOA Partner发出转向灯的的状态LightService::NotifyTurnLampStatus mode {turnlamp_mode.name}, priority {priority}")
            self.soa_partner.send_event_notify("LightService_server", "NotifyTurnLampStatus",
                                               {"sts": {"mode": turnlamp_mode.value, "priority": priority}})

    def notify_NotifyCarLoctrActvnSts(self,
                                      cartrace_sts: CarLocalTraceActiveStatus = CarLocalTraceActiveStatus.kSuccess):
        with allure.step(
                f"通过SOA Partner发出寻车执行功能的状态KeyService::NotifyCarLocalTraceActiveStatus {cartrace_sts.name}"):
            logger.info(
                f"通过SOA Partner发出寻车执行功能的状态KeyService::NotifyCarLocalTraceActiveStatus {cartrace_sts.name}")
            self.soa_partner.send_event_notify("KeyService_server", "NotifyCarLocalTraceActiveStatus",
                                               {"sts": cartrace_sts.value})

    def check_SetSpecificWindowPosition_req(self, *position_info: dict, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出车窗WindowAppService::SetSpecificWindowPosition请求"):
            logger.info("通过SOA Partner监听TCAM是否发出车窗WindowAppService::SetSpecificWindowPosition请求")
            win_pos_info = []
            for info in position_info:
                win_pos_info.append(info)
            self.ck_s2s_req("WindowAppService_server", "SetSpecificWindowPosition", {"windows": win_pos_info},
                            timeout=timeout)

    def response_to_SetSpecificWindowPosition_req(self, windowid: WindowId, windowidpos: WindowPos):
        prompt_info = f"----------> 通过SOA Partner发送车窗WindowAppService::SetSpecificWindowPosition请求的响应,响应的参数为:{windowid.name, windowidpos.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("WindowAppService_server", "SetSpecificWindowPosition",
                                                  {"windowid": windowid.value, "windowidpos": windowidpos.value})

    def check_SetSpecificWindowPosition_req_and_feedback_resp(self, windowid: WindowId, windowidpos: WindowPos,
                                                              timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取车窗WindowAppService::SetSpecificWindowPosition请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetSpecificWindowPosition_req(timeout)  # 监听TCAM发送车窗请求
            self.response_to_SetSpecificWindowPosition_req(windowid, windowidpos)

    def notify_WindowService_NotifyPosition_sts(self, win_id: list = [0, 1, 2, 3], position: int=0):
        with allure.step(
                f"通过SOA Partner发出车窗的状态WindowService::NotifyPosition为id {win_id} position {position}"):
            logger.info(
                f"通过SOA Partner发出车窗的状态WindowService::NotifyPosition为id {win_id} position {position}")
            for id in win_id:
                self.soa_partner.send_event_notify("WindowService_server", "NotifyPosition",
                                               {"position":{"id": id, "position": position}})

    def check_ChargeLidService_Close_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出充电口盖关ChargeLidService:Close()请求"):
            logger.info("通过SOA Partner监听TCAM是否发出充电口盖关ChargeLidService::Close()请求")
            self.ck_s2s_req("ChargeLidService_server", "Close", timeout=timeout)

    def response_to_ChargeLidService_Close_req(self):
        prompt_info = f"----------> 通过SOA Partner发送充电口盖关ChargeLidService:Close请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("ChargeLidService_server", "Close", args=None)

    def check_ChargeLidService_Close_req_and_feedback_resp(self, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取充电口盖关ChargeLidService:Close()请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_ChargeLidService_Close_req(timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_ChargeLidService_Close_req()

    def check_ChargeLidService_Open_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出充电口盖开ChargeLidService:Open()请求"):
            logger.info("通过SOA Partner监听TCAM是否发出充电口盖开ChargeLidService:Open()请求")
            self.ck_s2s_req("ChargeLidService_server", "Open", timeout=timeout)

    def response_to_ChargeLidService_Open_req(self):
        prompt_info = f"----------> 通过SOA Partner发送充电口盖开ChargeLidService:Open()请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("ChargeLidService_server", "Open", args=None)

    def check_ChargeLidService_Open_req_and_feedback_resp(self, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取充电口盖关ChargeLidService::void Open()请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_ChargeLidService_Open_req(timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_ChargeLidService_Open_req()

    def notify_ChargeLidService_status(self, chargelid_sts: ChargeLidSts = ChargeLidSts.kClosed):
        with allure.step(f"通过SOA Partner发出充电口盖状态ChargeLidService::Status为 {chargelid_sts.name}"):
            logger.info(f"通过SOA Partner发出充电口盖状态ChargeLidService::Status为 {chargelid_sts.name}")
            self.soa_partner.send_event_notify("ChargeLidService_server", "Status",
                                               {"sts": chargelid_sts.value})

    def hmi_set_rear_view_unfold(self, view_pos: ViewId, is_auto: bool):
        prompt_info = f"---------->通过 OuterRearViewService_client::Unfold 展开{view_pos.name}后视镜状态，并且自动展开模式设为{is_auto}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("OuterRearViewService_client", 'Unfold',
                                     {"views": [view_pos.value], "isAutoUnFold": is_auto})

    def hmi_set_rear_view_fold(self, view_pos: ViewId, is_auto: bool):
        prompt_info = f"---------->通过 OuterRearViewServicee_client::Fold 折叠{view_pos.name}后视镜状态，并且自动折叠模式设为{is_auto}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("OuterRearViewService_client", 'Fold',
                                     {"views": [view_pos.value], "isAutoUnFold": is_auto})
            
    def get_fota_NotifyAppointTime(self, master_notifyappointtime_event_field: MASTER_NotifyAppointTime_EVENT):
        time.sleep(3)
        fota_master_appointTime = self.return_latest_event("FotaMasterService_client", "NotifyAppointTime")[
            'appointment']
        if master_notifyappointtime_event_field.value == 0:
            value = fota_master_appointTime['taskId']
        elif master_notifyappointtime_event_field.value == 1:
            value = fota_master_appointTime['type']
        elif master_notifyappointtime_event_field.value == 2:
            value = fota_master_appointTime['appointmentTime']
        else:
            logger.error("Wrong FOTA Master NotifyAppointTime event field name !!!")
        logger.info(f"Current FOTA Master {master_notifyappointtime_event_field.name} = {value}")
        return value

    def notify_ChargingInfo(self, charg_sts: ChargingSts = ChargingSts.Default,
                            plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                            charg_complete_sts: bool = True, acdc_type: ACDCType = ACDCType.kDefault,
                            book_charg_sts: BookChargeSts = BookChargeSts.Default,
                            is_charging_pre: bool = True, is_charging: bool = True,isConnect: bool = True):
        """
        通过SOA Partner发送HighVoltageService:ChargingInfo事件通知
        
        Args:
            charg_sts (ChargingSts, optional): 充电状态. 默认为ChargingSts.Default.
            plug_sts (PluggerSts, optional): 插头状态. 默认为PluggerSts.Disconnected.
            tar_soc (float, optional): 目标SOC值. 默认为0.0.
            charg_complete_sts (bool, optional): 充电完成状态. 默认为True.
            acdc_type (ACDCType, optional): 充电桩类型. 默认为ACDCType.kDefault.
            book_charg_sts (BookChargeSts, optional): 预约充电状态. 默认为BookChargeSts.Default.
            is_charging_pre (bool, optional): 是否处于充电准备状态. 默认为True.
            is_charging (bool, optional): 是否正在充电. 默认为True.
            isConnect (bool, optional): 充电桩是否连接. 默认为True.
        
        Returns:
            None
        
        """
        with allure.step("通过SOA Partner发送HighVoltageService:ChargingInfo事件通知"):
            self.soa_partner.send_event_notify("HighVoltageService_server", "ChargingInfo",
                                               {"info": {
                                                   "chargingState": charg_sts.value,
                                                   "chargingSpeed": 0,
                                                   "remainChargingTime": 0,
                                                   "isConnect": isConnect,
                                                   "isTempHigh": True,
                                                   "bookChargeResp": 0,
                                                   "bookStateFeedBack": 0,
                                                   "chargeTargetSoc": tar_soc,
                                                   "pluggerStatus": plug_sts.value,
                                                   "chargePower": 0,
                                                   "totalChargeEnergy": 0,
                                                   "chargeEnergyThisTime": 0,
                                                   "chargeSpeedCalculate": 0,
                                                   "recentChargeStartTime": 0,
                                                   "recentChargeEndTime": 0,
                                                   "chargingCompleteStatus": charg_complete_sts,
                                                   "bookChargests": book_charg_sts.value,
                                                   "isChargingPreparing": is_charging_pre,
                                                   "isCharging": is_charging,
                                                   "acdcType": acdc_type.value,
                                                   "batteryReqCurrent": 0,
                                                   "isDischarging": False,
                                               }})

    def check_SetChargeSoc_req(self, soc: float = 80, timeout: Union[float, int] = 0.5):
        with allure.step("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetChargeSoc"):
            logger.info("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetChargeSoc")
            self.ck_s2s_req("HighVoltageService_server", "SetChargeSoc", timeout=timeout)

    def response_to_SetChargeSoc_req(self):
        prompt_info = f"----------> 通过SOA Partner发送设置充电SOC请求HighVoltageService:SetChargeSoc的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageService_server", "SetChargeSoc", args=None)

    def check_SetChargeSoc_req_and_feedback_resp(self, soc: float = 80, timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetChargeSoc, 并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetChargeSoc_req(soc=soc, timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_SetChargeSoc_req()

    def hmi_set_fragrance_sts(self, channel: FragChannel, ratio: int, level: FragLevel):
        prompt_info = f"---------->通过SOA ClimateControlService_client:SetFragranceType/SetFragranceLevel 设置香氛信息,设置香氛通道{channel.name}的香氛比例为{ratio}%,香氛等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", 'SetFragranceType',
                                     {"fragrance": [{"channel": channel.value, "ratio": ratio}]})
            self.send_method_request("ClimateControlService_client", 'SetFragranceLevel', {"level": level.value})

    def get_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        prompt_info = f"---------->通过SOA DoorService_client:GetDoorIceBreakActiveStatus 获取{door_pos.name}车门破冰功能激活状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("DoorService_client", "GetDoorIceBreakActiveStatus",
                                          {"doors": [door_pos.value]},
                                          {"out": {"id": door_pos.value, "sts": sts.value}})

    def event_check_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        prompt_info = f"---------->通过SOA DoorService_client:DoorIceBreakActiveStatus 获取{door_pos.name}车门破冰功能激活状态改变通知，check通知状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "DoorIceBreakActiveStatus",
                              {"sts": {"id": door_pos.value, "sts": sts.value}})

    def get_and_event_check_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        self.event_check_break_ice_active_sts(door_pos=door_pos, sts=sts)
        self.get_break_ice_active_sts(door_pos=door_pos, sts=sts)

    def cancel_auto_close_door_by_gear_driving(self, time_wait: Union[float, int] = 0):
        prompt_info = f"---------->通过SOA DoorService_client:CancelAutoCloseTrigger 取消D档自动关门"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("DoorService_client", "CancelAutoCloseTrigger", {"trigger": 0})

    def event_check_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        prompt_info = f"---------->通过SOA DoorService_client:AutoCloseTrigger 获取D档自动关门通知,期望的通知状态：激活状态为{act_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "AutoCloseTrigger", {"triggers": [act_sts.value]})

    def get_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        prompt_info = f"---------->通过SOA DoorService_client:GetAutoCloseTrigger 获取D档自动关门状态，期望的激活状态为{act_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("DoorService_client", "GetAutoCloseTrigger", {}, {"out": [act_sts.value]})

    def get_and_event_check_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        self.event_check_auto_close_door_by_gear_driving(act_sts=act_sts)
        self.get_auto_close_door_by_gear_driving(act_sts=act_sts)

    def get_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        prompt_info = f"---------->通过SOA DoorService_client:GetDoorAngle 获取{door_pos.name}门开启角度是否为：{angle}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("DoorService_client", "GetDoorAngle", {"doors": [door_pos.value]},
                                          {"out": [{"id": door_pos.value, "angle": angle}]})

    def event_check_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        prompt_info = f"---------->通过SOA DoorService_client:GetDoorAngle 获取{door_pos.name}门开启角度改变通知，期望的开角度为{angle}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "DoorAngle", {"angle": {"id": door_pos.value, "angle": angle}})

    def get_and_event_check_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        self.event_check_door_open_angle_sts(door_pos=door_pos, angle=angle)
        self.get_door_open_angle_sts(door_pos=door_pos, angle=angle)

    def get_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        prompt_info = f"---------->通过SOA DoorService_client:GetDoorSwitchSts 获取{door_pos.name}门{door_side.name}面的开关状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("DoorService_client", "GetDoorSwitchSts",
                                          {"doors": door_pos.value, "side": door_side.value},
                                          {"out": sts.value})

    def event_check_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        prompt_info = f"---------->通过SOA DoorService_client:GetDoorSwitchSts 获取{door_pos.name}门{door_side.name}面的开关状态改变事件通知，并且check 对应门的开关状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "NotifyDoorSwitchSts",
                              {"doors": door_pos.value, "side": door_side.value, "sts": sts.value})

    def get_and_event_check_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        self.event_check_door_switch_sts(door_pos=door_pos, door_side=door_side, sts=sts)
        self.get_door_switch_sts(door_pos=door_pos, door_side=door_side, sts=sts)

    def hmi_set_door_opener_sts(self, door_pos: DoorId, sts: DoorOpenSts, scene: VehicleInsideOutside= VehicleInsideOutside.VehicleInSide):
        prompt_info = f"---------->通过SOA DoorService_client:Open/Close/Stop 设置{door_pos.name}门车门动作请求为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts.name == "Open":
                self.send_method_request("DoorService_client", "Open", {"doors": [door_pos.value], "scene": scene.value})
            if sts.name == "Close":
                self.send_method_request("DoorService_client", "Close", {"doors": [door_pos.value]})
            if sts.name == "Stop":
                self.send_method_request("DoorService_client", "Stop", {"doors": [door_pos.value]})

    def check_GetOpenCloseStatus_req(self, door_id: list = [0, 1, 2, 3], timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出请求DoorService:GetOpenCloseStatus door_id: {door_id}"):
            logger.info("通过SOA Partner监听TCAM是否发出设请求DoorService:GetOpenCloseStatus")
            self.ck_s2s_req("DoorService_server", "GetOpenCloseStatus", {"doors": door_id}, timeout=timeout)

    def response_to_GetOpenCloseStatus_req(self,
                                           open_close_status: dict = {"0": False, "1": False, "2": False, "3": False}):
        prompt_info = f"----------> 通过SOA Partner发送DoorService:GetOpenCloseStatus请求的响应"
        status = []
        for k, v in open_close_status.items():
            status.append({"id": int(k), "isOpen": v})
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("DoorService_server", "GetOpenCloseStatus", status)

    def check_GetOpenCloseStatus_req_and_feedback_resp(self,
                                                       open_close_status: dict = {"0": False, "1": False, "2": False,
                                                                                  "3": False},
                                                       door_id: list = [0, 1, 2, 3], timeout: Union[float, int] = 1):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出请求DoorService:GetOpenCloseStatus，并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetOpenCloseStatus_req(door_id, timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_GetOpenCloseStatus_req(open_close_status)

    def check_TailGateService_GetStatus_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出请求TailGateService:GetStatus"):
            logger.info("通过SOA Partner监听TCAM是否发出设请求TailGateService:GetStatus")
            self.ck_s2s_req("TailGateService_server", "GetStatus", None, timeout)

    def response_to_TailGateService_GetStatus_req(self, status: TailGateSts = TailGateSts.kClosed):
        prompt_info = f"----------> 通过SOA Partner发送TailGateService:GetStatus请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("TailGateService_server", "GetStatus", status.value)

    def check_TailGateService_GetStatus_req_and_feedback_resp(self, status: TailGateSts = TailGateSts.kClosed,
                                                              timeout: Union[float, int] = 1):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出请求TailGateService:GetStatus，并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_TailGateService_GetStatus_req(timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_TailGateService_GetStatus_req(status=status)

    def check_GetLockStatus_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出请求CentralLockService:GetLockStatus"):
            logger.info("通过SOA Partner监听TCAM是否发出设请求CentralLockService:GetLockStatus")
            self.ck_s2s_req("CentralLockService_server", "GetLockStatus", None, timeout)

    def response_to_GetLockStatus_req(self, lock_status: LockStatus = LockStatus.AllLocked):
        prompt_info = f"----------> 通过SOA Partner发送CentralLockService:GetLockStatus请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("CentralLockService_server", "GetLockStatus", lock_status.value)

    def check_GetLockStatus_req_and_feedback_resp(self, lock_status: LockStatus = LockStatus.AllLocked,
                                                  timeout: Union[float, int] = 1):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出请求CentralLockService:GetLockStatus,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetLockStatus_req(timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_GetLockStatus_req(lock_status)

    def check_GetOccupied_req(self, seats: list = [12], timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出请求SeatService:GetOccupied"):
            logger.info("通过SOA Partner监听TCAM是否发出设请求SeatService:GetOccupied")
            self.ck_s2s_req("SeatService_server", "GetOccupied", {"seats": seats}, timeout)

    def response_to_GetOccupied_req(self, resp_seats: list = [0, 1, 4, 5, 6],
                                    resp_rawsensorstatus: list = [0, 0, 0, 0, 0],
                                    resp_status: list = [0, 0, 0, 0, 0]):
        prompt_info = f"----------> 通过SOA Partner发送SeatService:GetOccupied请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
        occupied_status = [
            {"seatId": 0, "rawSensorStatus": 0, "status": 0},
            {"seatId": 1, "rawSensorStatus": 0, "status": 0},
            {"seatId": 2, "rawSensorStatus": 0, "status": 0},
            {"seatId": 3, "rawSensorStatus": 0, "status": 0},
            {"seatId": 4, "rawSensorStatus": 0, "status": 0},
            {"seatId": 5, "rawSensorStatus": 0, "status": 0},
            {"seatId": 6, "rawSensorStatus": 0, "status": 0}]
        for id in range(0, len(resp_seats)):
            occupied_status[resp_seats[id]]["rawSensorStatus"] = resp_rawsensorstatus[id]
            occupied_status[resp_seats[id]]["status"] = resp_status[id]
            self.soa_partner.send_method_response("SeatService_server", "GetOccupied", occupied_status)

    def check_GetOccupied_req_and_feedback_resp(self, seats: list = [12], resp_seats: list = [0, 1, 4, 5, 6],
                                                resp_rawsensorstatus: list = [0, 0, 0, 0, 0],
                                                resp_occupiedstatus: list = [0, 0, 0, 0, 0],
                                                timeout: Union[float, int] = 1):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出请求SeatService:GetOccupied,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetOccupied_req(seats=seats, timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_GetOccupied_req(resp_seats, resp_rawsensorstatus, resp_occupiedstatus)

    def notify_ChargingInfo_v13(self, charg_sts: ChargingSts = ChargingSts.Default,
                                plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                                charg_complete_sts: bool = True,
                                book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                is_charging_pre: bool = True):
        prompt_info = f"---------->通过SOA Partner发送HighVolatgeService:ChargingInfo事件通知"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("HighVoltageService_server", "ChargingInfo",
                                               {"info": {
                                                   "chargingState": charg_sts.value,
                                                   "chargingSpeed": 0,
                                                   "remainChargingTime": 0,
                                                   "isConnect": True,
                                                   "isTempHigh": True,
                                                   "bookChargeResp": 0,
                                                   "bookStateFeedBack": 0,
                                                   "chargeTargetSoc": tar_soc,
                                                   "pluggerStatus": plug_sts.value,
                                                   "chargePower": 0,
                                                   "totalChargeEnergy": 0,
                                                   "chargeEnergyThisTime": 0,
                                                   "chargeSpeedCalculate": 0,
                                                   "recentChargeStartTime": 0,
                                                   "recentChargeEndTime": 0,
                                                   "chargingCompleteStatus": charg_complete_sts,
                                                   "bookChargests": book_charg_sts.value,
                                                   "isChargingPreparing": is_charging_pre
                                               }})

    def notify_BatteryTemperatureInfo(self, min_temp: float = -50, max_temp: float = 80,
                                      average_temp: float = 0):
        with allure.step(f"通过SOA Partner发送HighVoltageService:BatteryTemperatureInfo事件通知"):
            logger.info(f"通过SOA Partner发送HighVoltageService:BatteryTemperatureInfo事件通知")
            self.soa_partner.send_event_notify("HighVoltageService_server", "BatteryTemperatureInfo",
                                               {"info": {"maxTemperature": max_temp, "minTemperature": min_temp,
                                                "averageTemperature": average_temp}})

    def event_check_tailwing_mode(self, mode: TailWindMode):
        prompt_info = f"通过SOA Partner发送 TailWingService_client:Mode Check是否收到尾翼工作模式变为{mode.name}的事件通知"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event('TailWingService_client', 'Mode', {"mode": mode.value})

    def get_tailwing_mode(self, mode: TailWindMode):
        prompt_info = f"通过SOA Partner发送HighVoltageService:BatteryTemperatureInf 获取尾翼工作模式为{mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {}, {"out": mode.value})

    def get_and_event_check_tailwing_mode(self, mode: TailWindMode):
        self.event_check_tailwing_mode(mode=mode)
        self.get_tailwing_mode(mode=mode)

    def hmi_set_climate_angle_sts(self, pos: ClimateZone, side: OutletSide, hori_ang: int, ver_ang: int):
        prompt_info = f"通过SOA Partner发送 ClimateControlService_client:SetOutletAngle 设置空调{pos.name}区域电动出风口{side.name}出风水平角度{hori_ang},垂直角度为{ver_ang}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", 'SetOutletAngle',
                                     {"outlets": {"id": pos.value, "side": side.value, "horizontal": hori_ang,
                                                  "vertical": ver_ang}})

    def check_event_period(self, partner_key: str, event_name: str, target_period: Union[float, int],
                           epsilon: float) -> bool:
        self.soa_partner.empty_event_list(partner_key)
        time.sleep(60)
        time_list = [event.get("timestamp") for event in list(self.soa_partner.partner_infos[partner_key].event_queue.queue) if
                     event.get("function") == f'Update{event_name}Event']
        if not time_list:
            logger.error(f"Not receive event: Update{event_name}Event in 10s")
            return False
        for i in range(len(time_list) - 1):
            cur_period = time_list[i + 1] - time_list[i]
            if not abs(cur_period - target_period) <= epsilon:
                return False
        return True

    def check_ua_event_period(self, domain_name: DOMAIN, target_period: Union[float, int], epsilon: float):
        logger.info(f"start check {domain_name} Status event period")
        return self.check_event_period(partner_key=f'UpdateAgentService_client_{domain_name.name}_UA_Service',
                                       event_name='Status', target_period=target_period, epsilon=epsilon)

    def send_SetNetResidentSts_req(self, is_5G: bool):
        prompt_info = f"----------> 通过SOA Partner发送NetStatService:SetNetResidentSts 设置蜂窝网络5G状态为{is_5G}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("NetStatService_client", "SetNetResidentSts", {"is_5G": is_5G})

    def send_Get5GNetSts_req_and_ck_resp(self, sa_sts: SA_sts, timeout: int=10):
        prompt_info = f"----------> 通过SOA Partner发送NetStatService:GetSwitch5GNet 校验蜂窝网络5G状态为{sa_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            assert self.send_request_and_ck_resp('NetStatService_client', 'GetSwitch5GNet', {}, {"out": sa_sts.value}, timeout=timeout)

    def send_SetCellularNetSts_req(self, is_open: bool):
        prompt_info = f"----------> 通过SOA Partner发送NetStatService:SetCellularNetSts 设置蜂窝网络apn4状态为{is_open}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("NetStatService_client", "SetCellularNetSts", {"is_Open": is_open})

    def send_GetNetSts_req_and_ck_resp(self, apnsts: ApnSts, timeout: int=10):
        prompt_info = f"----------> 通过SOA Partner发送NetStatService:GetNetSts 校验蜂窝网络apn4状态为{apnsts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            assert self.send_request_and_ck_resp('NetStatService_client', 'GetNetSts', {}, {"out": [
                {"ApnName": 1, "ApnSts": 0}, {"ApnName": 4, "ApnSts": apnsts.value}]}, timeout=timeout)

    def remote_climate_open_susccess_when_inactive(self, temp: float = 22, timeout: int=5):
        prompt_info = f"通过SOA Partner模拟远程空调在inactive模式正常开启成功"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req(isOn=True, timeout=timeout)
            self.remote_climate_check_tcam_request(temp=temp, timeout=timeout)
            self.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.remote_climate_check_tcam_request(temp=temp, timeout=timeout)
            self.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            logger.info("空调开启成功！！")

    def remote_climate_check_tcam_request(self, temp: float = 22, timeout: int=5):
        prompt_info = f"通过SOA Partner检查TCAM是否发出远程开启空调请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_RemoteOn_req(timeout=timeout)
            self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=temp, timeout=timeout)

    def remote_lock_unlock_success_when_inactive(self, lock_status: LockStatus = LockStatus.Unlocked,
                                                 lock_cmd: LockCmd = LockCmd.Lock,
                                                 source: LockReqSource = LockReqSource.Talematics,
                                                 find_key_type: FindKeyType = FindKeyType.NoReq,
                                                 lock_result: LockStatus = LockStatus.AllLocked):
        self.check_TailGateService_GetStatus_req_and_feedback_resp(timeout=3)
        self.check_GetOpenCloseStatus_req_and_feedback_resp(timeout=3)
        self.check_GetLockStatus_req_and_feedback_resp(lock_status=lock_status, timeout=3)
        self.check_GetOpenCloseStatus_req_and_feedback_resp(door_id=[4], timeout=3)
        self.check_TailGateService_GetStatus_req_and_feedback_resp(timeout=3)
        self.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=lock_cmd, source=source,
                                                          find_key_type=find_key_type, timeout=3)
        self.notify_LockStatus(lock_sts=lock_result)

    def check_ClimateService_Off_req(self, zone_id: ClimateZoneId = ClimateZoneId.FirstRowLeft,
                                     timeout: Union[float, int] = 1):
        prompt_info = f"通过SOA Partner监听TCAM是否发出ClimateService:Off ClimateZoneId: {zone_id.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req('ClimateService_server', 'Off', {"zoneId": zone_id.value}, timeout=timeout)

    def response_to_ClimateService_Off_req(self):
        prompt_info = f"通过SOA Partner发送ClimateService:Off的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response('ClimateService_server', 'Off', args=None)

    def check_ClimateService_Off_req_and_feedback_resp(self, zone_id: ClimateZoneId = ClimateZoneId.FirstRowLeft,
                                                       timeout: Union[float, int] = 1):
        prompt_info = f"通过SOA Partner监听TCAM是否发出ClimateService:Off请求，并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_ClimateService_Off_req(zone_id=zone_id, timeout=timeout)
            self.response_to_ClimateService_Off_req()

    def hmi_set_chrglid_sts(self, sts: ChrgLidOperType, time_wait: Union[float, int] = 0):
        prompt_info = f"通过SOA ChargeLidService:Open/Close 设置充电口盖的状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts.name == "Open":
                self.send_method_request("ChargeLidService_client", "Open", {})
            elif sts.name == "Close":
                self.send_method_request("ChargeLidService_client", "Close", {})
            
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def get_chrglid_sts(self, sts: ChrgLidSts):
        prompt_info = f"通过SOA ChargeLidService:GetStatus 获取电口盖的状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("ChargeLidService_client", "GetStatus", {}, {"out": sts.value})

    def rvc_seat_heating_start_success(self, id: SeatId = SeatId.FrontLeft, heat_level: HeatLevel = HeatLevel.High, keep_time: int = 30,):
        prompt_info = f"通过SOA Partner模拟座椅加热启动加热成功场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True,keep_time=keep_time, timeout=20)
            self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=id, info=heat_level, timeout=20)
            sleep(2)
            self.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
            self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=id, info=heat_level, timeout=20)
            if id == SeatId.FrontLeft:
                self.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)
            elif id == SeatId.FrontRight:
                self.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)
            elif id == SeatId.RearLeft:
                self.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)
            else:
                self.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)

    def rvc_steer_wheel_heating_success(self, heat_level: HeatLevel = HeatLevel.High,keep_time: int = 30):
        prompt_info = f"通过SOA Partner模拟方向盘加热启动加热成功场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True,keep_time=keep_time, timeout=20)
            self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=heat_level, timeout=20)
            sleep(2)
            self.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
            self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=heat_level, timeout=20)
            self.notify_SteerWheelService_Heat(heat_level=heat_level)


    def remote_battery_heat_success_plan_a4(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟远程座舱预约电池预加热集度私桩插枪且充过电的场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_SetBatteryHeating_req(timeout=5)
            self.check_SetCharging_req(req=True, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=5)
            time.sleep(5)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            time.sleep(20)   

    def remote_battery_heat_success_plan_a5(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟远程座舱预约电池预加热集度私桩插枪且充过电的场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower,tar_soc=95,timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, tar_soc=95, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, tar_soc=95, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=8)
            self.check_SetBatteryHeating_req(timeout=5)
            self.check_SetCharging_req(req=True, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithPower, timeout=5)
            time.sleep(5)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            time.sleep(20)   

    def check_climate_heat_status_and_get_charginfo_and_get_equipmentinfo_get_mintemp(self, mintemp: float,
                                                                    plug_sts: PluggerSts = PluggerSts.ConnectedWithoutPower,
                                                                    charg_sts: ChargingSts = ChargingSts.NoCharging):
        prompt_info = f"----------> 通过SOA监听climate请求并返回响应, 监听获取充电信息请求并返回响应，监听获取充电桩信息并响应，监听获取电池最低温度并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=charg_sts,
                                                             plug_sts=plug_sts, timeout=10)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[1],timeout=10)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=8)

    def remote_battery_heat_success_plan_b1(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟远程座舱预约电池预加热未插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=5)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp = mintemp, timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=5)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=5)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(5)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            time.sleep(20)
            
    def remote_battery_heat_success_plan_b2(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟远程座舱预约电池预加热非集度桩插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[2],timeout=8)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[2],timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=25, actual_current=20, equipment_types=[2],timeout=8)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(5)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            time.sleep(20)
            
    def remote_battery_heat_success_plan_b3(self, mintemp: float):
        prompt_info = f"----------> 通过SOA模拟远程座舱预约电池预加热集度公桩插枪场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=10)
            self.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=10)
            self.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=10)
            self.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=10)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[1],timeout=8)
            self.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=mintemp, timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[1],timeout=8)
            self.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.ConnectedWithoutPower, timeout=5)
            self.check_getEquipmentInfo_req_and_feedback_resp(max_current=30.1, actual_current=30, equipment_types=[1],timeout=8)
            self.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
            self.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=5)
            self.check_SetBatteryHeating_req(timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(5)
            self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            time.sleep(20)   

    
    def trigger_call_sos_by_soa_partner(self, opercmd = eCallOperCmd.kSTART_ECALL, ReqSrc = eCallReqSource,
                                        funsts = eCallFunSts.kREADY, type = eCallType.kACTIVE, status = eCallSts.kWAIT_FOR_CONFIRM):
        logger.info(f"以{ReqSrc.name}的方式触发ecall")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"点击SOS失败, 原因:{str(e)}")
            assert False, str(e)
        try:
            self.chk_notify(
                "CallService_client",
                'NotifyECallStatus',
                {"Sts": {"FunctionSts": funsts.value,
                         "Type": type.value,
                         "Status": status.value}}, timeout=5
            )
        except AssertionError as e:
            logger.error(f"检查点击SOS服务状态失败, 原因:{str(e)}")
            assert False, str(e) 
        else:
            logger.info("partner点击SOS成功")

    def trigger_call_sos_notcheck_funsts_by_soa_partner(self, opercmd = eCallOperCmd.kSTART_ECALL, ReqSrc = eCallReqSource,
                                     type = eCallType.kACTIVE, status = eCallSts.kWAIT_FOR_CONFIRM):
        logger.info(f"以{ReqSrc.name}的方式触发ecall")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"点击SOS失败, 原因:{str(e)}")
            assert False, str(e)
        try:
            self.chk_notify(
                "CallService_client",
                'NotifyECallStatus',
                {"Sts": {"Type": type.value,
                         "Status": status.value}}, timeout=5
            )
        except AssertionError as e:
            logger.error(f"检查点击SOS服务状态失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("partner点击SOS成功")

    def confirm_call_sos(self, opercmd = eCallOperCmd.kCONFIRM_ECALL, ReqSrc = eCallReqSource.kCDC):
        logger.info("确认呼叫")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True},
            )
        except AssertionError as e:
            logger.error(f"点击确认呼叫SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("确认呼叫SOS成功")
    
    def chk_xcall_notify(self,funsts= eCallFunSts.kREADY, type = eCallType.kIDLE, status = eCallSts.kIDLE):
        try:
            self.chk_notify("CallService_client",
                'NotifyECallStatus',
                {"Sts": {
                    "FunctionSts": funsts.value,
                    "Type": type.value,
                    "Status": status.value}}
                    )
        except AssertionError as e:
            logger.error(f"检查SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("检查xcall状态成功")

    def cancel_call_sos(self, opercmd = eCallOperCmd.kCANCEL_ECALL, ReqSrc = eCallReqSource,
                            funsts= eCallFunSts.kREADY, type = eCallType.kACTIVE, status = eCallSts.kIDLE):
        logger.info(f"以{ReqSrc.name}的方式取消拨打SOS")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"取消拨打SOS失败, 原因:{str(e)}")
            assert False, str(e)
        # try:
        #     self.chk_notify(
        #         "CallService_client",
        #         'NotifyECallStatus',
        #         {"Sts": {
        #             "FunctionSts": funsts.value,
        #             "Type": type.value,
        #             "Status": status.value}}
        #     )
        # except AssertionError as e:
        #     logger.error(f"检查取消拨打SOS失败, 原因:{str(e)}")
        #     assert False, str(e)
        else:
            logger.info("检查取消拨打SOS成功")

    def hang_up_call_sos(self, opercmd = eCallOperCmd.kHANG_UP_ECALL, ReqSrc = eCallReqSource.kCDC,
                         funsts= eCallFunSts.kREADY, type = eCallType.kACTIVE, status = eCallSts.kHANG_UP):
        logger.info(f"{ReqSrc.name}的方式触发挂断ecall")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"挂断SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("挂断成功")
        try:
            self.chk_notify("CallService_client",
                'NotifyECallStatus',
                {"Sts": {
                    "FunctionSts": funsts.value,
                    "Type": type.value,
                    "Status": status.value}}
                    )
        except AssertionError as e:
            logger.error(f"检查挂断SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("检查挂断SOS成功")

    def hang_up_call_sos_not_check_funsts(self, opercmd = eCallOperCmd.kHANG_UP_ECALL, ReqSrc = eCallReqSource.kCDC,
                          type = eCallType.kACTIVE, status = eCallSts.kHANG_UP):
        logger.info(f"{ReqSrc.name}的方式触发挂断ecall")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SetECallMode',
                {"Cmd": opercmd.value, "Src": ReqSrc.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"挂断SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("挂断成功")
        try:
            self.chk_notify("CallService_client",
                'NotifyECallStatus',
                {"Sts": {
                    "Type": type.value,
                    "Status": status.value}},
                    timeout=10
                    )
        except AssertionError as e:
            logger.error(f"检查挂断SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("检查挂断SOS成功")        
    
    def trigger_bcall_sos(self,opercmd = bCallOperCmd):
        logger.info(f"bcall模式为{opercmd.name}_SOS")
        try:
            self.send_request_and_ck_resp(
                "CallService_client",
                'SendBCallCmd',
                {"Cmd": opercmd.value},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"触发{opercmd}_SOS失败, 原因:{str(e)}")
            assert False, str(e) 
    
    def chk_xcall_in_self_test_notify(self, funsts = eCallFunSts.kREADY):
        try:
            self.chk_notify(
                "CallService_client",
                'NotifyECallStatus',
                {"Sts": {"FunctionSts": funsts.value,
                         "Type": eCallType.kIDLE.value,
                         "Status": eCallSts.kIDLE.value}},
                         timeout=10
            )
        except AssertionError as e:
            logger.error(f"检查自检服务状态失败, 原因:{str(e)}")
            assert False, str(e)

    
    def hmi_set_tailgate_postion(self, pos: int, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner TailGateService::SetPosition 发送设置尾门翘起{pos}请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("TailGateService_client", "SetPosition", {"pos": pos})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    
    def hmi_set_door_postion(self, door_pos:DoorPos, pos:int,  scene: VehicleInsideOutside= VehicleInsideOutside.VehicleInSide, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner DoorService_client::SetPosition 设置{door_pos.name}门的开度为{pos}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("DoorService_client", "SetPosition", {"doors": [{"id": door_pos.value, "pos": pos}], "scene": scene.value})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
    

    def check_whether_ua_download(self, domain_name:DOMAIN):
        start_time = time.time() 
        end_time = start_time + 60 
        initial_downloadfilesize = self.get_ua_status(domain_name=domain_name, ua_event_field=UA_EVENT.DownloadFileSize)
        while time.time() < end_time:
            cur_downloadfilesize = self.get_ua_status(domain_name=domain_name, ua_event_field=UA_EVENT.DownloadFileSize)
            difference_value = cur_downloadfilesize - initial_downloadfilesize
            if difference_value > 0:
                logger.info(f"cur_downloadfilesize: {cur_downloadfilesize}, initial_downloadfilesize: {initial_downloadfilesize}, {domain_name} UA is download normaly")
                return True
            elif difference_value == 0:
                logger.info(f"{domain_name} UA's downloadspeed equals 0")
            else:
                logger.error(f"difference_value is illagel:{difference_value}")
        return False

    def get_fota_ConditionCheckResults(self, master_conditioncheckresult_field:MASTER_ConditionCheckResults_EVENT):
        time.sleep(12) #FOTA Master检查该event的周期是10s
        ConditionCheckResults = self.return_latest_event("FotaMasterService_client", "ConditionCheck")['result']
        if master_conditioncheckresult_field.value == 0:
            value = ConditionCheckResults['checkConditionType']
        elif master_conditioncheckresult_field.value == 1:
            value = ConditionCheckResults['results']
        else:
            logger.error("Wrong FOTA Master ConditionCheckResults event field name !!!")
        logger.info(f"Current FOTA Master {master_conditioncheckresult_field.name} = {value}")
        return value

    def get_fota_UpdateErrorInfo(self):
        time.sleep(12) #FOTA Master检查该event的周期是10s
        UpdateErrorInfo = self.return_latest_event("FotaMasterService_client", "UpdateErrorInfo")['info']
        logger.info(f"Current FOTA Master Info = {UpdateErrorInfo}")
        return UpdateErrorInfo

    def till_fota_event_to(self, master_event_field: MASTER_EVENT, target_status=None, timeout=60):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.get_fota_status(master_event_field=master_event_field)
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current FOTA Master {master_event_field} is {curr_status}")


    def event_check_hv_batt_thermy_sts(self,sts:HvBattThermReq,info:str = "HV Battery Thermal Status"):
        prompt_info = f"----------> 通过SOA Partner WTIService_client::WarningMsgList 获取高压电池告警事件提示是否为{info},状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("WTIService_client", "WarningMsgList", {"list":[{"name":info, "info":str(sts.value)}]})
        
        
    def get_hv_batt_thermy_sts(self,sts:HvBattThermReq,info:str = "HV Battery Thermal Status"):
        prompt_info = f"----------> 通过SOA Partner WTIService_client::GetWarningMsgList 获取高压电池告警提示是否为{info},状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},{"out":[{"name":info, "info":str(sts.value)}]})

    def event_check_and_get_hv_batt_thermy_sts(self,sts:HvBattThermReq,info:str = "HV Battery Thermal Status"):
        self.event_check_hv_batt_thermy_sts(sts= sts,info=info)
        self.get_hv_batt_thermy_sts(sts= sts,info=info)

    def hmi_set_turn_lamp_mode_and_priority(self,mode:TurnLampMode,priority:int):
        prompt_info = f"----------> 通过SOA Partner LightService_client::SetTurnLampMode 设置转向灯模式为{mode.name},优先级为{priority}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("LightService_client", "SetTurnLampMode", {"lamp": {"mode": mode.value, "priority": priority}})
    
    

    def response_to_SetRemoteClimateSwitchToHVDelay_req(self):
        prompt_info = f"----------> 通过SOA Partner发送远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("ClimateControlService_server", "SetRemoteClimateSwitchToHVDelay", args=None)
            
    def check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(self, extendtime: int = 30, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=extendtime, timeout=timeout)
            self.response_to_SetRemoteClimateSwitchToHVDelay_req()

    def get_fota_DownloadProcess(self, master_downloadprocess_event_field: MASTER_DownloadProcess_EVENT):
        time.sleep(3)
        fota_master_status = self.return_latest_event("FotaMasterService_client", "DownloadProcess")['downloadProgress']
        if master_downloadprocess_event_field.value == 0:
            value = fota_master_status['taskId']
        elif master_downloadprocess_event_field.value == 1:
            value = fota_master_status['state']
        elif master_downloadprocess_event_field.value == 2:
            value = fota_master_status['progress']
        elif master_downloadprocess_event_field.value == 3:
            value = fota_master_status['downloadSpeed']
        elif master_downloadprocess_event_field.value == 4:
            value = fota_master_status['leftTime']
        elif master_downloadprocess_event_field.value == 5:
            value = fota_master_status['errorCode']
        else:
            logger.error("Wrong FOTA Master event field name !!!")
        logger.info(f"Current FOTA Master {master_downloadprocess_event_field.name} = {value}")
        return value

    def get_light_inhibit_sts(self,type:LightType,sts:bool):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp('LightService_client','GetLightInhibitSts',args={"type":[type.value],"inhibitSts":sts}, ck_info={},timeout=0.1)

    def get_light_inhibit_sts_func(self,type:LightType,sts:bool):
        global start_get_light_inhibit_sts_flag
        while start_get_light_inhibit_sts_flag == 1:
            self.get_light_inhibit_sts(type = type,sts=sts)
            sleep(1)

    def start_get_light_inhibit_sts(self,type:LightType = LightType.LightBrake ,sts:bool = False):
        receiver_thread = Thread(target=self.get_light_inhibit_sts_func, args=(type,sts))
        receiver_thread.start()

    def stop_get_light_inhibit_sts(self):
        global start_get_light_inhibit_sts_flag
        start_get_light_inhibit_sts_flag = 0

    
    def hmi_set_extr_light_rear_fog_mode(self, mode: LightMode = LightMode.On):
        logger.info("设置后雾灯模式")
        self.hmi_light_control(type=LightType.LightFog, zone=LightZone.LightZoneRear, mode=mode)
    
    def get_fota_UpdateProcess(self, master_updateprocess_event_field: MASTER_UpdateProcess_EVENT):
        time.sleep(3)
        try:
            fota_master_status = self.return_latest_event("FotaMasterService_client", "UpdateProcess")['updateProgress']
        except Exception as err:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/soa.py")
            value = -1
            logger.error(err)
        else:
            if master_updateprocess_event_field.value == 0:
                value = fota_master_status['taskId']
            elif master_updateprocess_event_field.value == 1:
                value = fota_master_status['state']
            elif master_updateprocess_event_field.value == 2:
                value = fota_master_status['progress']
            elif master_updateprocess_event_field.value == 3:
                value = fota_master_status['leftTime']
            elif master_updateprocess_event_field.value == 4:
                value = fota_master_status['errorCode']
            else:
                logger.error("Wrong FOTA Master event field name !!!")
            logger.info(f"Current FOTA Master {master_updateprocess_event_field.name} = {value}")
        return value
    

    def set_rearview_autosts(self, view_pos: ViewId, sts: bool):
        prompt_info = f"---------->通过 OuterRearViewService_client::SetAutoFoldUnfold 设置{view_pos.name}后视镜自动展开折叠功能开启状态为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("OuterRearViewService_client", 'SetAutoFoldUnfold', {"params":[{"id":view_pos.value,"isOn":sts}]})

    def get_rearview_autosts(self, view_pos: ViewId, sts: bool):
        prompt_info = f"---------->通过 OuterRearViewService_client::GetAutoFoldUnfold 获取{view_pos.name}后视镜自动展开折叠功能开启状态为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("OuterRearViewService_client", 'GetAutoFoldUnfold', {"views": [view_pos.value]},{"out": [{"id": view_pos.value, "isOn": sts}]})
            
    def check_no_SetOutput_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetOutput请求"):
            self.ck_no_req("HighVoltageService_server", "SetOutput", timeout=timeout)

    def check_no_SetBatteryHeating_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求"):
            self.ck_no_req("HighVoltageService_server", "SetBatteryHeating", timeout=timeout)

    def empty_all(self, wait_time=0):
        """
        清空partner所有缓存数据

        :return:
        """
        self.soa_partner.empty_all(wait_time)

    def __generate_v2t_traceid(self):
        first_part = "00"
        second_part = str(uuid.uuid4())[:32]  # 生成一个32位的随机UUID
        third_part = str(uuid.uuid4())[:16]  # 生成另一个16位的随机UUID
        last_part = "01"
        full_string = f"{first_part}-{second_part}-{third_part}-{last_part}"
        encoded_string = base64.b64encode(full_string.encode()).decode()
        return encoded_string

    def call_vehicle_api(self, v2t_api: V2T_API, payload: dict):
        ascii_list = []
        for char in json.dumps(payload):
            ascii_list.append(ord(char))        
        # payload = [x for x in ascii_list if x != 32] # payload转成ASCILL码列表后需要去空格（32）
        traceId = self.__generate_v2t_traceid()
        args = {
            'api': v2t_api.value,
            'payload': ascii_list,
            'traceId': traceId
                }
        logger.info(f"=== api: {v2t_api.value} ===\n=== payload: {payload} ===\n=== traceId: {traceId} ===")
        if v2t_api.name == "OTA":
            self.send_method_request(partner_key=f'V2TRoutingForwarder_client_V2TOTAFotaForwarder',
                                     method_name='CallVehicleApi', 
                                     args=args)
        elif v2t_api.name == "FOD":
            self.send_method_request(partner_key=f'V2TRoutingForwarder_client_V2TCcpForwarder',
                                     method_name='CallVehicleApi', 
                                     args=args)
        elif v2t_api.name == "RemoteRescue":
            self.send_method_request(partner_key=f'V2TRoutingForwarder_client_V2TRemoteRescueForwarder',
                                     method_name='CallVehicleApi', 
                                     args=args)            
        else:
            logger.error(f"非法参数：{v2t_api.value}")
        
    def trigger_fota_type20(self, taskid: int):
        self.call_vehicle_api(V2T_API.OTA, payload={"data": {"taskId": taskid}, "type": 20})

    def trigger_fota_type70(self, taskid: int):
        self.call_vehicle_api(V2T_API.OTA, payload={"data": {"taskId": taskid, "taskStatus":1}, "type": 70})    
        
    def hmi_set_window_full_close(self, win_pos:WindowId):
        prompt_info = f"---------->通过 WindowService_client, Close 设置{win_pos.name}窗户全关"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("WindowService_client", "Close", {"windows": [win_pos.value]})
            
    def notify_LockSuccessTriggerSource(self, sourceid: TriggerSourceId = TriggerSourceId.RemoteKey):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:LockSuccessTriggerSource.TriggerSourceId {sourceid.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("CentralLockService_server", "LockSuccessTriggerSource",
                                   {"sourceId": sourceid.value})

    def check_GetPosition_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出请求WindowService::GetPosition"):
            logger.info("通过SOA Partner监听TCAM是否发出设请求WindowService::GetPosition")
            self.ck_s2s_req("WindowService_server", "GetPosition", None, timeout)

    def response_to_GetPosition_req(self, *position_info: dict):
        prompt_info = f"----------> 通过SOA Partner发送WindowService::GetPosition请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            win_pos_info = []
            for info in position_info:
                win_pos_info.append(info)
            self.soa_partner.send_method_response("WindowService_server", "GetPosition", {"windows": win_pos_info})
            
    def check_GetPosition_req_and_feedback_resp(self, *position_info: dict,
                                                  timeout: Union[float, int] = 1):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出请求WindowService::GetPosition,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetPosition_req(timeout)  # 监听TCAM发送获取窗户位置请求
            self.response_to_GetPosition_req(*position_info)

    
    def get_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = ""):
        prompt_info = f"---------->调用接口 GetFaultInfo 获取{pos.name}雨刮故障类型是否为{fault_type.name},提示信息是否为{fault_msg}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.send_method_request("WiperService_client", "GetFaultInfo", {}, {"out": [{"fault": fault_type.value, "faultMsg": fault_msg, "wiper": pos.value}]})


    def event_check_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = "OK"):
        prompt_info = f"---------->调用接口 WiperFault 查看是否有雨刮故障事件上报，check事件信息：{pos.name}雨刮故障类型是否为{fault_type.name},提示信息是否为{fault_msg}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "WiperFault", {"faults": [{"fault": fault_type.value, "faultMsg": fault_msg, "wiper": pos.value}]})
    
    def get_and_event_check_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = ""):
        self.event_check_wiper_fault_sts(pos = pos, fault_type = fault_type)
        self.get_wiper_fault_sts(pos = pos, fault_type = fault_type, fault_msg = fault_msg)
        
    def notify_BrakePedalStatus(self, status: PressedStatus = PressedStatus.PedalReleased, validity: ValidityLevel = ValidityLevel.kValid):
        prompt_info = f"---------->通过SOA Partner发送制动踏板位置状态PedalService_server::BrakePedalStatus{status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("PedalService_server", "BrakePedalStatus",
                                   {"status": {
                                       "value": status.value,
                                       "validity": validity.value,
                                       "sequenceTime": {
                                           "id": 456,
                                           "timestamp": int(time.time())
                                       }
                                   }})

    def trigger_fota_type90(self, taskid: int):
        logger.info("============== Send Type 90 ==============")
        self.call_vehicle_api(V2T_API.OTA, payload= {"type": 90, "data": {"taskId": taskid, "sessionId": "abc", "appointmentStatus": 1, "appointmentTime": "1670310827"}})
        time.sleep(3)

    def hmi_set_rain_auto_close_window_sts(self,sts:bool,time_wait: Union[float, int] = 0):
        prompt_info = f"---------->调用接口 SetRainAutoCloseWindow 设置雨天自动关窗状态为:{sts}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.send_method_request("WindowAppService_client", "SetRainAutoCloseWindow", {"isOn": sts})
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def get_rain_auto_close_window_sts(self,sts:bool):
        prompt_info = f"---------->调用接口 GetRainAutoCloseWindowStatus 获取雨天自动关窗状态为:{sts}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.send_request_and_ck_resp("WindowAppService_client", "GetRainAutoCloseWindowStatus",args={}, ck_info={"out":sts},timeout=1)

    def event_check_rain_auto_close_window_sts(self,sts:bool):
        prompt_info = f"---------->调用接口 RainAutoCloseWindowStatus 获取雨天自动关窗状态事件通知，期望通知状态为:{sts}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WindowAppService_client", "RainAutoCloseWindowStatus",ck_info={"sts": sts})
    
    def get_and_event_check_rain_auto_close_window_sts(self,sts:bool):
        self.event_check_rain_auto_close_window_sts(sts)
        self.get_rain_auto_close_window_sts(sts)

    def wait_for_service_reconnect(self, partner_key: str, timeout=30):
        self.soa_partner.wait_for_service_reconnect(partner_key = partner_key, timeout = timeout)
    
    def chek_hv_cli_seat_steer_driv_pseng_request(self):
        prompt_info = f"----------> 使用SOA Partner监听TCAM是否已发送上高压请求、空调开启请求、方向盘开启、主副驾开启请求，且请求参数正确；"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            # 监听TCAM是否已发送上高压请求
            self.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            # 监听TCAM是否已发送空调开启请求
            self.check_RemoteOn_req(timeout=5)
            self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)
            # 监听TCAM是否已发送方向盘开启请求
            self.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            # 监听TCAM是否已发送主副驾开启请求
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=10)
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            logger.info("tcam已发送上高压请求、空调开启请求、方向盘开启、主副驾开启请求，且请求参数正确")
            time.sleep(2)

    def re_chek_hv_cli_seat_steer_driv_pseng_request(self):
        prompt_info = f"----------> 使用SOA Partner监听TCAM是否已二次发送空调开启请求、方向盘开启、主副驾开启请求，且请求参数正确；"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            # 监听TCAM是否已发送空调开启请求
            self.check_RemoteOn_req(timeout=10)
            self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)
            # 监听TCAM是否已发送方向盘开启请求
            self.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            # 监听TCAM是否已发送主副驾开启请求
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=10)
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            logger.info("tcam已二次发送上高压请求、空调开启请求、方向盘开启、主副驾开启请求，且请求参数正确")
            time.sleep(2)

    def check_no_hv_cli_seat_steer_driv_pseng_req(self, timeout: Union[float, int] = 5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM未发出上高压请求、空调开启请求、方向盘开启、主副驾开启请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_no_req("HighVoltageService_server", "SetRemoteClimateSwitchToHV", timeout=timeout)
            self.ck_no_req("ClimateControlService_server","RemoteOn", timeout=timeout)
            self.ck_no_req("ClimateControlService_server", "SetTemperature", timeout=timeout)
            self.ck_no_req("SteerWheelService_server", "SetHeat", timeout=timeout)
            self.ck_no_req("SeatService_server", "SetHeatingLevel", timeout=timeout)
            logger.info("未检测到tcam发送上高压请求、空调开启请求、方向盘开启、主副驾开启请求")
    
    def cock_reserv_hv_cli_seat_steer_driv_pseng_start_success(self):
        prompt_info = f"通过SOA Partner模拟座舱预约座椅/方向盘/空调启动加热成功场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=10)
            sleep(2)
            self.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
            self.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(timeout=20)
            self.check_RemoteOn_req(timeout=20)
            self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
            self.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
            
    def chk_rvc_inacti_to_conve(self):
        prompt_info = f"通过SOA Partner检测TCAM是否调用本地空调开启、主副座椅加热、方向盘加热请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=20)
            self.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=10)
            self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            logger.info("TCAM已发送本地空调开启、主副座椅加热、方向盘加热请求，且参数正确")

    def chk_hv_delay_cli_seat_steer_driv_pseng_req(self, ac:bool=False, temp:int=23, seat:bool=False,seat_level=HeatLevel.Low, steer:bool=False, steer_level=HeatLevel.Low):
        prompt_info = f"使用SOA Partner监听TCAM是否已发送延长高压请求，空调开启或方向盘开启或主副驾开启请求，且请求参数正确"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            # 监听TCAM是否已发送延长上高压请求
            self.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            if ac:
                # 监听TCAM是否已发送空调开启请求
                self.check_RemoteOn_req(timeout=5)
                self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=temp, timeout=10)
            elif steer:
                # 监听TCAM是否已发送方向盘开启请求
                self.check_SteerWheelService_SetHeat_req(heat_level=steer_level, timeout=10)
            elif seat:
                # 监听TCAM是否已发送主副驾开启请求
                self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=seat_level, timeout=10)
                self.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=seat_level, timeout=10)
            logger.info("tcam已发送延长高压请求，空调开启或方向盘开启或主副驾开启请求，且请求参数正确")
            time.sleep(2)
    
    def set_ac_seat_steer_heating_start_success(self, heat_level: HeatLevel = HeatLevel.Low):
        prompt_info = f"通过SOA Partner模拟开启空调、座椅加热、方向盘加热启动成功场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
            sleep(2)
            self.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.check_RemoteOn_req(timeout=20)
            self.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
            self.notify_RemotePowerStatus(RemoteClimateStatus.On)
            self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=heat_level, timeout=20)
            self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=heat_level, timeout=20)
            self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=heat_level, timeout=20)
            self.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)
            self.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=heat_level)
            self.notify_SteerWheelService_Heat(heat_level=heat_level)
        logger.info(f"模拟开启空调、座椅加热、方向盘加热启动加热场景成功")

    def chk_ac_seat_steer_driv_pseng_off_req(self, ac_off:bool=False, steer_off:bool=False, seat_off:bool=False, timeout: int=20):
        prompt_info = f"使用SOA Partner监听TCAM是否已发送关闭空调、方向盘或主副驾请求，且请求参数正确"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if ac_off:
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=timeout)
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=timeout)
                self.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
                self.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
                self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=timeout)
                self.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
            elif steer_off:
                self.check_RemoteOff_req(timeout=timeout)
                self.notify_RemotePowerStatus(RemoteClimateStatus.Off)
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=timeout)
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=timeout)
                self.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
                self.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
            elif seat_off:
                self.check_RemoteOff_req(timeout=timeout)
                self.notify_RemotePowerStatus(RemoteClimateStatus.Off)
                self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=timeout)
                self.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
            else:
                self.check_RemoteOff_req(timeout=timeout)
                self.notify_RemotePowerStatus(RemoteClimateStatus.Off)
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=timeout)
                self.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=timeout)
                self.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
                self.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
                self.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=timeout)
                self.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        logger.info("tcam已发送关闭空调、方向盘或主副驾请求，且请求参数正确")

    def chk_no_ac_seat_steer_off_req(self, timeout:int= 20):
        services = [
                    ("ClimateControlService_server", "RemoteOff"),
                    ("SteerWheelService_server", "SetHeat"),
                    ("SeatService_server", "SetHeatingLevel")
                    ]
        prompt_info = f"----------> 通过SOA Partner监听TCAM未发出关闭空调、方向盘、主副驾请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            threads = []
            for service, action in services:
                t = Thread(target=self.ck_no_req, args=(service, action, timeout))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            logger.info("未检测到TCAM发出关闭空调、方向盘、主副驾请求")

    def set_convenience_duration(self, time):
        # time = 0 时退出舒享模式， time的单位是0.5h
        self.send_method_request(
            'VehicleModeService_client', "SetConvenienceModeDuration", {"duration": time}
        )
        logger.info(f"设置舒享模式，duration={time}")
    
    def check_keep_power_mode(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, do_assert=True,  **kwargs):
        '''
        keep_power 为 True 校验 当前模式，验当前是维持上电模式，
        keep_powe 为 False 校验 当前模式，验当前不是维持上电模式，
        exit_reason:0=kNormal  //正常状态，默认值 1=kUserReq  //用户请求关闭
        2=kHVSOC   //高压电池电量低于阈值 3=kGearNotP  //挡位非P挡
        4=kCarModeNotNormal //车辆模式不满足 5=kFOTAUpdate  //车辆开始FOTA升级
        6=kOther //其他原因退出
        '''
        if  keep_power:
            ck_info = {'out': {'modeSts': 1, 'reason': exit_reason.value}}
        else:
            ck_info = {'out': {'modeSts': 0, 'reason': exit_reason.value}}

        method_name = 'GetParkingComfortModeSts'
        ret = self.send_request_and_ck_resp(
            'VehicleSetStatusService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleSetStatusService ck_info={ck_info}       ret={ret}")
        if keep_power:
            logger.info(F"当前为  {'维持上电模式' if ret else '非维持上电模式'}")
        else:
            logger.info(F"当前为  {'维持上电模式或退出原因异常' if not ret else '非维持上电模式'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"

    
    def event_check_not_rain_auto_close_window_req(self):
        prompt_info = f"---------->调用接口 NotifyRainWinAutoCloseReqSts 获取下雨自动关窗事件上报通知，期望结果是没有对应事件上报"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_no_event("WindowService_client",  "NotifyRainWinAutoCloseReqSts")

            
    def notify_NotifyVIN(self, vin: str = "LSTEST6R9F2086644"):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送CarConfigService:NotifyVIN事件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            vin_code = []
            for ch in vin:
                vin_code.append(ord(ch))
            self.send_event_notify("CarConfigService_server", "NotifyVIN", {"vin": {"vin": vin_code}})

    def notify_NotifyHvBatteryCode(self, batt_code: str = "123456789012345678901234"):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送HighVoltageService:NotifyHvBatteryCode事件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            code_list = []
            for ch in batt_code:
                code_list.append(ord(ch))
            self.send_event_notify("HighVoltageService_server", "NotifyHvBatteryCode", {'info': {'length': 24, 'code': code_list}})

    def response_to_GetBatteryCodeInfo_req(self, batt_code: str = "123456789012345678901234"):
        prompt_info = f"----------> 通过SOA HighVoltageService_server:GetBatteryCodeInfo请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            code_list = []
            for ch in batt_code:
                code_list.append(ord(ch))
            self.soa_partner.send_method_response("HighVoltageService_server", "GetBatteryCodeInfo", {'length': 24, 'code': code_list})


    def get_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        prompt_info = f"---------->调用接口 GetRainWinAutoCloseReqSts 获取下雨自动关窗请求状态是否为:{sts.name}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.send_request_and_ck_resp("WindowService_client", "GetRainWinAutoCloseReqSts", {}, {"out": sts.value})

    
    def event_check_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        prompt_info = f"---------->调用接口 NotifyRainWinAutoCloseReqSts 获取下雨自动关窗事件上报通知，check通知状态是否为:{sts.name}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WindowService_client",  "NotifyRainWinAutoCloseReqSts", {"reqSts": sts.value})

    
    def get_and_event_check_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        self.event_check_rain_auto_close_window_req(sts)
        self.get_rain_auto_close_window_req(sts)

    
    def hmi_set_high_beam_ctrl_cmd(self,cmd_value:HighBeamCmd,hbid_value:int):
        prompt_info = f"---------->调用接口 SetHighBeamControl 进行远光灯控制,远光灯请求类型为:{cmd_value.name},客户端id为:{hbid_value}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.send_method_request("LightService_client","SetHighBeamControl",{"info": {"cmd": cmd_value.value, "clientId": hbid_value}})


    def event_check_high_beam_ctrl_sts(self,hbsts_prty:int):
        prompt_info = f"---------->调用接口 HighBeamStatus 远光灯状态事件上报,期望的客户端id为:{hbsts_prty}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("LightService_client","HighBeamStatus", {"sts": {"clientId": hbsts_prty}})

    def hmi_set_and_event_check_high_beam_ctrl_sts(self,cmd_value:HighBeamCmd,hbid_value:int,hbsts_prty:LowBeamClientId,sts:Union[HighBeamSts,None]=None):
        self.hmi_set_high_beam_ctrl_cmd(cmd_value,hbid_value)
        self.event_check_high_beam_sts(sts=sts,clientId = hbsts_prty)

    def get_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        prompt_info = f"---------->调用服务WindowService_client GetPosition 获取窗户的位置信息"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            if pos_drvr is not None:
                logger.info(f"--------->获取主驾窗户位置是否为{pos_drvr.name}")
                self.send_request_and_ck_resp("WindowService_client","GetPosition",{"windows": [0]},{"out": [{"id": 0, "position": 4*(pos_drvr.value-1)}]})
            if pos_pass is not None:
                logger.info(f"--------->获取副驾窗户位置是否为{pos_pass.name}")
                self.send_request_and_ck_resp("WindowService_client","GetPosition",{"windows": [1]},{"out": [{"id": 1, "position": 4*(pos_pass.value-1)}]})
            if pos_lere is not None:
                logger.info(f"--------->获取左后窗户位置是否为{pos_lere.name}")
                self.send_request_and_ck_resp("WindowService_client","GetPosition",{"windows": [2]},{"out": [{"id": 2, "position": 4*(pos_lere.value-1)}]})
            if pos_rire is not None:
                logger.info(f"--------->获取右后窗户位置是否为{pos_rire.name}")
                self.send_request_and_ck_resp("WindowService_client","GetPosition",{"windows": [3]},{"out": [{"id": 3, "position": 4*(pos_rire.value-1)}]})
    
    def get_four_windows_postion(self,pos:WinPos):
        prompt_info = f"---------->调用服务WindowService_client GetPosition 同时获取四个窗户的位置是否为{pos.name}"
        logger.info(prompt_info)
        pos_value = 4*(pos.value-1)
        with allure.step(prompt_info):
            self.send_request_and_ck_resp("WindowService_client", "GetPosition", {"windows":[4]},
                                                   {"out":[{"id":0,"position":pos_value},{"id":1,"position":pos_value},
                                                           {"id":2,"position":pos_value},{"id":3,"position":pos_value}]})
        
    def set_exhibition_mode(self, is_open: bool):
        self.send_method_request(
            'VehicleModeService_client', "SetExhibitionMode", {"isOpen": is_open}
        )

    
    def event_check_high_beam_switch_sts(self,sts:SteerWhlTouchSwtSts):
        prompt_info = f"---------->调用接口 NotifyHighBeamSwitchStatus 查看远光灯状态改变通知，期望的状态为:{sts.name}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("LightService_client","NotifyHighBeamSwitchStatus", {"swtsts": sts.value})

    def check_GetVIN_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取VIN请求:CarConfigService:GetVIN"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("CarConfigService_server", "GetVIN", timeout=timeout)

    def response_to_GetVIN_req(self, vin: str = "LSTEST6R9F2086644"):
        prompt_info = f"----------> 通过SOA Partner发送获取VIN请求的响应:CarConfigService:GetVIN"
        with allure.step(prompt_info):
            vin_code = []
            for ch in vin:
                vin_code.append(ord(ch))
            self.send_method_response("CarConfigService_server", "GetVIN", {"vin": vin_code})

    def check_GetVIN_req_and_feedback_resp(self, vin: str = "LSTEST6R9F2086644", timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取VIN请求:CarConfigService:GetVIN，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetVIN_req(timeout=timeout)
            self.response_to_GetVIN_req(vin=vin)

    def notify_OutputState(self, on: bool = True):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送HighVoltageService:OutputState事件通知"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("HighVoltageService_server", "OutputState", {"on": on})

    def check_GetOutput_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取上高压状态请求:HighVoltageService:GetOutput"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("HighVoltageService_server", "GetOutput", timeout=timeout)

    def response_to_GetOutput_req(self, on: bool = False):
        prompt_info = f"----------> 通过SOA Partner发送获取上高压状态请求的响应:HighVoltageService:GetOutput"
        with allure.step(prompt_info):
            self.send_method_response("HighVoltageService_server", "GetOutput", on)

    def check_GetOutput_req_and_feedback_resp(self, on: bool = False, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取上高压状态的请求:HighVoltageService:GetOutput，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetOutput_req(timeout=timeout)
            self.response_to_GetOutput_req(on=on)

    def notify_HVThermalOutOfControl(self, state: bool = False):
        prompt_info = f"----------> 通过SOA Partner模拟BGM发送HighVoltageService:HVThermalOutOfControl事件通知"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_event_notify("HighVoltageService_server", "HVThermalOutOfControl", {"state": state})

    def check_GetHVThermalOutOfControl_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取高压热失控状态请求:HighVoltageService:GetHVThermalOutOfControl"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("HighVoltageService_server", "GetHVThermalOutOfControl", timeout=timeout)

    def response_to_GetHVThermalOutOfControl_req(self, state: bool = False):
        prompt_info = f"----------> 通过SOA Partner发送获取高压热失控状态请求的响应:HighVoltageService:GetHVThermalOutOfControl"
        with allure.step(prompt_info):
            self.send_method_response("HighVoltageService_server", "GetHVThermalOutOfControl", state)

    def check_GetHVThermalOutOfControl_req_and_feedback_resp(self, state: bool = False, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取高压热失控状态的请求:HighVoltageService:GetHVThermalOutOfControl"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetHVThermalOutOfControl_req(timeout=timeout)
            self.response_to_GetHVThermalOutOfControl_req(state=state)
            
    def pack_ua_event_args_with_error(self, 
                                    ua_sts: UA_Sts,
                                    ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                    ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                    ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                    errorCode=0):
        ua_status = self.pack_ua_status_args_with_error(ua_sts = ua_sts, 
                                                        ua_download_sts = ua_download_sts,
                                                        ua_preupdate_sts = ua_preupdate_sts,
                                                        ua_update_sts = ua_update_sts,
                                                        errorCode = errorCode)
        ua_event_dict = {
            "status": ua_status
        }
        logger.info(f"Pack UA event args: 【{ua_event_dict}】")
        return ua_event_dict
            
    def pack_ua_status_args_with_error(self,
                                       ua_sts: UA_Sts,
                                       ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                       ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                       ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                       errorCode = 0):
        ua_dict = json.loads(json.dumps(UA_Status_Event))
        if ua_sts.name == 'IDLE':
            pass
        elif ua_sts.name == 'DOWNLOAD':
            ua_dict['status'] = 1
            ua_dict['downloadStatus']['downloadFileSize'] = 4000000000
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 10
            ua_dict['downloadStatus']['status'] = ua_download_sts
        elif ua_sts.name == 'READY_TO_INSTALL':
            ua_dict['status'] = 2
            ua_dict['downloadStatus']['downloadFileSize'] = 4000000000
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = ua_preupdate_sts
        elif ua_sts.name == 'INSTALLING':
            ua_dict['status'] = 3
            ua_dict['downloadStatus']['downloadFileSize'] = 4704677392
            ua_dict['downloadStatus']['totalFileSize'] = 4704677392
            ua_dict['downloadStatus']['downloadSpeed'] = 0
            ua_dict['downloadStatus']['status'] = 1
            ua_dict['preUpdateStatus']['status'] = 2
            ua_dict['updateStatus']['updateFileSize'] = 4000000000
            ua_dict['updateStatus']['totalFileSize'] = 4704677392
            ua_dict['updateStatus']['status'] = ua_update_sts
        else:
            logger.error(f"Illegal UA Status:{ua_sts}")
        ua_dict['errorCode'] = errorCode if errorCode != 0 else ua_dict['errorCode']
        logger.info(f"Pack UA status args: 【{ua_dict}】")
        return ua_dict
    
    def change_ua_event_and_getstatus_with_error(self,
                                                 domain_name: DOMAIN,
                                                 ua_sts: UA_Sts,
                                                 ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                                 ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                                 ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                                 errorCode=0):
        self.update_ua_event(domain_name=domain_name,
                             event_args=self.pack_ua_event_args_with_error(ua_sts=ua_sts,
                                                                           ua_download_sts=ua_download_sts,
                                                                           ua_preupdate_sts=ua_preupdate_sts,
                                                                           ua_update_sts=ua_update_sts,
                                                                           errorCode=errorCode))
        self.update_ua_response(domain_name=domain_name,
                                get_status_args=self.pack_ua_status_args_with_error(ua_sts=ua_sts, 
                                                                                    ua_download_sts=ua_download_sts,
                                                                                    ua_preupdate_sts=ua_preupdate_sts,
                                                                                    ua_update_sts=ua_update_sts,
                                                                                    errorCode=errorCode))

    def set_maintain_mode(self, status: bool):
        self.send_method_request(
            'VehicleSetStatusService_client', "SetMaintenanceMode", {"isOn": status}
        )

    def check_maintain_mode(self, status: bool):
        '''
        status 为 True 校验 当前模式是维修模式，
        status 为 False 校验 当前模式非维修模式，
        '''
        method_name = 'GetMaintenanceMode'
        if status:
            ck_info = {'out': True}
        else:
            ck_info = {'out': False}
        ret = self.send_request_and_ck_resp(
            'VehicleSetStatusService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleSetStatusService ck_info={ck_info}       ret={ret}")
        if status:
            logger.info(F"当前为  {'维修模式，与预期一致' if ret else '非维修模式，与预期不一致'}")
        else:
            logger.info(F"当前为  {'维修模式，预期不一致' if not ret else '非维修模式， 与预期一致'}")

    def notify_maintain_mode(self, status: bool):
        method_name = 'NotifyMaintenanceMode'
        if status:
            ck_info = {'mode': True}
        else:
            ck_info = {'mode': False}
        self.ck_s2s_event('VehicleSetStatusService_client', method_name, ck_info=ck_info)
        logger.info(f"维修模式的通知为预期的mode={status}")

    def set_and_check_maintain_mode(self, status: bool):
        self.set_maintain_mode(status=status)
        self.notify_maintain_mode(status=status)
        self.check_maintain_mode(status=status)

    
    def get_and_event_check_wiper_auto_mode(self, pos: WiperPos, mode: WipgAutFrntMod):
        prompt_info = f"S2S获取和EventCheck雨刮自动模式状态是否为：{mode.value}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "NotifyWiperAutoMode",
                                  {"mode": mode.value, "wiper": pos.value})
            self.send_request_and_ck_resp("WiperService_client", "GetWiperAutoMode", {"wipers": pos.value},
                                              {"out": mode.value}, timeout=1)
            
    
    def get_and_event_check_wiper_single_mode(self, pos: WiperPos, sts: isOn):
        prompt_info = f"S2S获取和EventCheck雨刮单挂模式状态是否为：{sts.value}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "WiperOneshotSts",
                                      {"info": {"id": pos.value, "sts": sts.value}})
            self.send_request_and_ck_resp("WiperService_client", "GetWiperOneshotSts", {"wipers": [0]},
                                                  {"out": [{"id": pos.value, "sts": sts.value}]})
            
        
    def get_and_event_check_wiper_return_pos(self, pos: WiperPos, sts: isOn):
        prompt_info = f"获取/通知雨刮回位位置是否为{sts.value}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "NotifyWiperPosition", {"positon": sts.value, "wiper": pos.value}, timeout=2)
            self.send_request_and_ck_resp("WiperService_client", "GetWiperPosition", {"wipers": 0},{"out": sts.value}, timeout=2)

    
    def get_and_event_check_rain_detected_pos(self, sts: bool):
        prompt_info = f"获取/通知下雨事件是否为{sts}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "RainStatusRestricted", {"status": sts})
            self.send_request_and_ck_resp("WiperService_client", "GetRainStatusRestricted", {},{"out": sts})

    def get_and_event_check_rain_level(self, level:int):
        prompt_info = f"获取/通知雨量值是否为{level}"
        logger.info(prompt_info)
        with allure.step(prompt_info):
            self.ck_s2s_event("WiperService_client", "Rainlevel", {"level": level})
            self.send_request_and_ck_resp("WiperService_client", "GetRainlevel", {}, {"out": level})

    def get_and_event_check_ambient_light_intensity(self,qf:int,value:int):
        promt_info = f"---------------->获取/通知环境光强度{value},QF={qf}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ck_s2s_event("WiperService_client", "LightLux", {"lux": value})
            self.send_request_and_ck_resp("WiperService_client", "GetRawLightLux", {},
                                                      {"out": {"value": value, "isValid": qf}})

    def get_and_event_check_day_and_night_sts(self,sts:bool):
        promt_info = f"---------------->获取/通知白天黑夜状态{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)    
            self.ck_s2s_event("WiperService_client", "DayNightStatus", {"status": sts})
            self.send_request_and_ck_resp("WiperService_client", "GetDayNightStatus", {}, {"out": sts})

        
    def get_and_event_check_solar_value(self,value:int):
        promt_info = f"---------------->获取/通知阳光强度{value}"
        with allure.step(promt_info):
            logger.info(promt_info)    
            self.ck_s2s_event("WiperService_client", "SolarValue",{"value": {"driverValue": value * 5, "passengerValue": value * 5}})
            self.send_request_and_ck_resp("WiperService_client", "GetSolarValue", {}, {"out": {"driverValue": value * 5,"passengerValue": value * 5}})

    
    def get_and_event_check_wiper_switch_sts(self,sts:SteerWhlTouchSwtSts):
        promt_info = f"---------------->获取/通知雨刮开关状态是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)    
            self.ck_s2s_event("WiperService_client", "SwitchStatus", {"status": sts.value, "wipers": 0})
            self.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0},{"out": sts.value})

    
    def get_turn_lamp_mode_sts(self,mode:TurnLampMode,priority:int):
        prompt_info = f"----------> 通过SOA Partner LightService_client::GetTurnLampStatus 获取转向灯模式，check模式是否为{mode.name},优先级是否为{priority}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("LightService_client", "GetTurnLampStatus", {},{"out": {"mode": mode.value, "priority": priority}})
    
    def set_usagemode_up_and_down(self, up_usagemode: UsageMode, down_usagemode: UsageMode):
        with allure.step(f"同时进行服务上切下切使用模式"):
            method_name1 = "SetUsageModeUp"
            method_name2 = "SetUsageModeDown"
            self.send_method_request( 'VehicleModeService_client', method_name1,{"mode": up_usagemode.value})
            self.send_method_request( 'VehicleModeService_client', method_name2,{"mode": down_usagemode.value})
    
    def set_carmode_by_serivice(self, carmod:CarMode):
        logger.info(f"----->设置car mode 为{carmod.name}")
        self.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": carmod.value})

    def notyfy_lock_warn_info(self, lock_warn: LockWarn, remind: DoorRemind, timeout=5):
        with allure.step(
                f"调用接口 NotifyLockWarning 通知期望的门锁告警信息,期望的'LockWarn': {lock_warn.name}, 'remind': {remind.name}"):
            logger.info(
                f"调用接口 NotifyLockWarning 通知期望的门锁告警信息,期望的'LockWarn': {lock_warn.name}, 'remind': {remind.name}")
            self.chk_notify("EntryService_client", "NotifyLockWarning", {"warnnings": {"lock": lock_warn.value, "reminder": remind.value}})

    def get_lock_warn_info(self, lock_warn: LockWarn, remind: DoorRemind, timeout=5):
        with allure.step(
                f"调用接口 GetLockWarning 获取期望的门锁告警信息,期望的'LockWarn': {lock_warn.name}, 'remind': {remind.name}"):
            logger.info(
                f"调用接口 GetLockWarning 获取期望的门锁告警信息,期望的'LockWarn': {lock_warn.name}, 'remind': {remind.name}")
            self.send_request_and_ck_resp("EntryService_client", "GetLockWarning", {}, {"out": {"lock": lock_warn.value, "reminder": remind.value}})

    def hmi_set_outview_heat_mode(self, sts: bool):
        prompt_info = f"----------> 调用接口SetHeat 设置后视镜加热除霜状态为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": sts}]})
            
    def set_auto_sts(self, sts: bool, cycle_mode: CycleMode, wind_zone: ClimateZone, wind_mode: AirWindMode, speed_zone: ClimateZone, speed: WindSpeed):
        prompt_info = f"---------->同时设置AC、循环模式、吹风模式、风速"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.hmi_set_climate_ac_sts(sts=sts)
            self.hmi_set_climate_cycle_mode(mode=cycle_mode)
            self.hmi_set_climate_windmode_sts(zone=wind_zone,mode=wind_mode)
            self.hmi_set_climate_windspeed(zone=speed_zone,speed=speed)


    def update_apa_sts(self, pa_sts, last_handle_type, uid='0000000000000001', apa_fail_reason=0):
        """更新apa状态，用于BGM GetApaSts的输入更新"""
        self.lastHandleUid = int(uid, 16)
        self.LastHandleType = last_handle_type
        self.APAFunctionStatus = pa_sts
        self.apaFunctionFailReason = apa_fail_reason


    def on_GetAPAStatus(self, partner_key, msg):
        if partner_key == "RPAAPAService_server" and msg["function"] == "GetAPAStatus":
            apa_sts_info = {
                            "paStatus": self.APAFunctionStatus,
                            "lastHandleType": self.LastHandleType,
                            "lastHandleUid": self.lastHandleUid,
                            "apaFunctionFailReason": 0
                        }
            self.send_method_response(partner_key, "GetAPAStatus", apa_sts_info)
    def hmi_get_door_anti_pinch_sts(self, id: DoorId, isantipinch: bool = False, time_wait: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner DoorService_client::AntiPinch 获取{id.value}门故障状态，check故障是否为{isantipinch}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "AntiPinch", {"info": {"door": id.value, "isAntiPinch": isantipinch}})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait) 
    
    def hmi_get_door_postion(self, doors:DoorPos, door_pos:DoorPos,pos:int, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner DoorService_client::GetPosition 获取{door_pos.value}门的开度为{pos}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("DoorService_client", "GetPosition", {"doors":[door_pos.value]},{"out": [{"id": door_pos.value, "pos":  pos}]}) 

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)


    def ck_key_service_unlock_event(self, keyid: list, key_type: DigitalKeyType, trigger: DigitalKeyIdTrigger):
        prompt_info = f"----------> 校验有解锁事件上报, keyid: {keyid}, type: {key_type.name}, trigger: {trigger.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("KeyService_client", "DigitalKeyId",
                                      {"info": {"keyId": DataTypeHanding.to_bytes(keyid), "trigger": trigger.value, "type": key_type.value}})


  #o_fan.liu          
    def hmi_set_steer_wheel_adjust_direction(self, direct: AdjustDirection, time_wait: Union[float, int] = 0):    #o_fan.liu
        with allure.step(f"设置方向盘调节方向为{direct.name}"):
            logger.info(f"设置方向盘调节方向为{direct.name}")
            self.send_method_request("SteerWheelService_client", "StartMoveDirection", {"direction": direct.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def hmi_event_check_tailgate_movests(self, status:MoveSts, time_wait: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner TailGateService_client::Status 获取尾门当前运动状态为{status.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("TailGateService_client", "Status", {"sts":status.value}) 

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
    
    def hmi_set_car_location_req(self,req:CarLocalTraceReq,time_wait: Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner KeyService_client::SetCarLocalTraceRequest 设置寻车请求为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("KeyService_client", 'SetCarLocalTraceRequest', {"carLoctrReq": req.value})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def get_ccp_status(self, CcpMaster_field: CCPMasterSts_Field):
        if self.soa_partner.partner_infos[f'CCPMasterService_client_CcpMasterService'].service_status != "START":
            # 发起请求之前做 服务在线 判断，避免 进/退boot 重启影响
            self.soa_partner.empty_all()
            self.soa_partner.wait_for_service_reconnect(f'CCPMasterService_client_CcpMasterService')
        ccp_master_status = self.send_request_and_return_resp(partner_key='CCPMasterService_client_CcpMasterService', method_name='GetCCPStatus', args={}).get("out")
        if CcpMaster_field.value == 0:
            value = ccp_master_status['taskInfo']
        elif CcpMaster_field.value == 1:
            value = ccp_master_status['state']
        elif CcpMaster_field.value == 2:
            value = ccp_master_status['errorCode']
        else:
            logger.error("Wrong CCP Master status field name !!!")
        logger.info(f"Current CCP Master {CcpMaster_field.name} = {value}")
        return value
    
    def get_ccp_ConditionCheckResult(self, CcpMasterConditionCheckResult_Field: CCPMasterConditionCheckResult_Field):
        if self.soa_partner.partner_infos[f'CCPMasterService_client_CcpMasterService'].service_status != "START":
            # 发起请求之前做 服务在线 判断，避免 进/退boot 重启影响
            self.soa_partner.empty_all()
            self.soa_partner.wait_for_service_reconnect(f'CCPMasterService_client_CcpMasterService')
        ccp_master_status = self.send_request_and_return_resp(partner_key='CCPMasterService_client_CcpMasterService', method_name='GetConditionCheckInfo', args={}).get("out")
        if CcpMasterConditionCheckResult_Field.value == 0:
            value = ccp_master_status['taskInfo']
        elif CcpMasterConditionCheckResult_Field.value == 1:
            value = ccp_master_status['conditionCheck']
        else:
            logger.error("Wrong CCP Master status field name !!!")
        logger.info(f"Current CCP Master ConditionCheckResult {CcpMasterConditionCheckResult_Field.name} = {value}")
        return value

    def set_hv_off_sts(self, is_off:bool):
        logger.info(f"----->设置下高压请求为{is_off}")
        self.send_method_request( 'VehicleModeService_client', "setHVOffSts", {"isOff":is_off})
    def till_ccp_event_to(self, CcpMasterSts_Field: CCPMasterSts_Field, target_status=None, timeout=60):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.get_ccp_status(CcpMaster_field = CcpMasterSts_Field)
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current CCP Master {CcpMasterSts_Field} is {curr_status}")

    def get_ccp_ActiveProgress(self):
        if self.soa_partner.partner_infos[f'CCPMasterService_client_CcpMasterService'].service_status != "START":
            # 发起请求之前做 服务在线 判断，避免 进/退boot 重启影响
            self.soa_partner.empty_all()
            self.soa_partner.wait_for_service_reconnect(f'CCPMasterService_client_CcpMasterService')
        ccp_active_progress = self.send_request_and_return_resp(partner_key='CCPMasterService_client_CcpMasterService', method_name='GetCCPActiveProgress', args={}).get("out")
        value = ccp_active_progress['progress']
        logger.info(f"Current CCP Master ActiveProgress = {value}")
        return value
    
    def till_ccp_ActiveProgress_to(self,target_status=None, timeout=60):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                ccp_active_progress = self.get_ccp_ActiveProgress()
                if ccp_active_progress == target_status:
                    return True
                else:
                    time.sleep(0.5)
                    logger.info(f"Current CCP Active Progress is {ccp_active_progress}")
                    
    def check_ccp_ActiveProgress_period(self, target_period: Union[float, int], epsilon: float):
        logger.info(f"start check CCP ActiveProgress period")
        return self.check_event_period(partner_key=f'CCPMasterService_client_CcpMasterService',
                                       event_name='CCPActiveProgress', target_period=target_period, epsilon=epsilon)


    def hmi_set_light_show_active(self, status: bool):
        prompt_info = f"----------> 通过SOA Partner LightService_client::SetLightShowActivateStatus 设置灯光秀激活状态为{status}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("LightService_client", "SetLightShowActivateStatus",{"status": status}) 
            
    def set_and_check_steer_wheel_sts(self,level1: HeatLevel,level2: HeatLevel):
        prompt_info = f"---------->设置并获取方向盘开启加热和关闭"
        with allure.step(prompt_info):
            self.send_method_request("SteerWheelService_client", "SetHeat", {"status": level1.value})
            self.send_request_and_ck_resp("SteerWheelService_client", "GetHeat", {}, {"out": {"level":level2.value}})#{"out": level2.value})
            logger.info(f"---------->设置并获取方向盘加热为{level1},获取结果为{level2}")
    
    def check_keep_power_mode_by_source(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, source:str="PetMode", do_assert=True,  **kwargs):
        '''
        keep_power 为 True 校验 当前模式，验当前是维持上电模式，
        keep_powe 为 False 校验 当前模式，验当前不是维持上电模式，
        exit_reason:0=kNormal  //正常状态，默认值 1=kUserReq  //用户请求关闭
        2=kHVSOC   //高压电池电量低于阈值 3=kGearNotP  //挡位非P挡
        4=kCarModeNotNormal //车辆模式不满足 5=kFOTAUpdate  //车辆开始FOTA升级
        6=kOther //其他原因退出
        '''
        if  keep_power:
            ck_info = {'out': {'modeSts': 1, 'reason': exit_reason.value, 'source':source}}
        else:
            ck_info = {'out': {'modeSts': 0, 'reason': exit_reason.value, 'source':source}}

        method_name = 'GetParkingComfortBaseFunctionSts'
        ret = self.send_request_and_ck_resp(
            'VehicleSetStatusService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleSetStatusService ck_info={ck_info}       ret={ret}")
        if keep_power:
            logger.info(F"当前为  {'维持上电模式' if ret else '非维持上电模式或source不匹配'}")
        else:
            logger.info(F"当前为  {'维持上电模式或退出原因异常或source不匹配' if not ret else '非维持上电模式'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"

    def set_keep_power_mode_by_source(self, modeSts: bool, source: str="PetMode"):
        self.send_method_request(
            'VehicleSetStatusService_client', "SetParkingComfortBaseFunctionByApp", {"cmd": {'modeSts': modeSts, 'source':source}}
        )

    def notify_and_get_door_movests(self, doorid: DoorId, doormovests: DoorMoveStatus, time_wait: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner DoorService_client::Status 通知当前{doorid.name}侧门运动状态为{doormovests.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("DoorService_client", "Status", {"sts": {"id": doorid.value, "sts": doormovests.value}})
            self.send_request_and_ck_resp("DoorService_client", "GetStatus", {"doors": [doorid.value]},
                                        {"out": [{"id": doorid.value, "sts": doormovests.value}]}) 
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def check_GetMaintenanceMode_req(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取维修模式请求:VehicleSetStatusService:GetMaintenanceMode"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("VehicleSetStatusService_server", "GetMaintenanceMode", timeout=timeout)

    def response_to_GetMaintenanceMode_req(self, result: bool = False):
        prompt_info = f"----------> 通过SOA Partner发送获取维修模式请求的响应:VehicleSetStatusService:GetMaintenanceMode"
        with allure.step(prompt_info):
            self.send_method_response("VehicleSetStatusService_server", "GetMaintenanceMode",result)

    def check_GetMaintenanceMode_req_and_feedback_resp(self, result: bool = False, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出获取维修模式请求:VehicleSetStatusService:GetMaintenanceMode，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetMaintenanceMode_req(timeout=timeout)
            self.response_to_GetMaintenanceMode_req(result=result)
    
    def check_SetParkingComfortModeOff_req(self, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出VehicleSetStatusService:SetParkingComfortMode请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("VehicleSetStatusService_server", "SetParkingComfortMode", {'modeSts': 0}, timeout=timeout)

    def response_to_SetParkingComfortModeOff_req(self):
        prompt_info = f"----------> 通过SOA Partner发送远程关闭维持上电请求:VehicleSetStatusService:SetParkingComfortMode的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("VehicleSetStatusService_server", "SetParkingComfortMode", {'modeSts': 0})


    def check_ParkingComfortModeOff_req_and_feedback_resp(self, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:VehicleSetStatusService:SetParkingComfortMode,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetParkingComfortModeOff_req(timeout=timeout)
            self.response_to_SetParkingComfortModeOff_req()

    def check_GetParkingComfortModeSts_req(self, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出VehicleSetStatusService:GetParkingComfortModeSts请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("VehicleSetStatusService_server", "GetParkingComfortModeSts", timeout=timeout)

    def response_to_GetParkingComfortModeSts_req(self, modeSts: int=0, reason: int=1):
        prompt_info = f"----------> 通过SOA Partner发送获取维持上电状态请求:VehicleSetStatusService:GetParkingComfortModeSts的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_response("VehicleSetStatusService_server", "GetParkingComfortModeSts", {'modeSts': modeSts, 'reason': reason})

    def check_GetParkingComfortModeSts_req_and_feedback_resp(self, modeSts:int=0, reason: int=1, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:VehicleSetStatusService:GetParkingComfortModeSts,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetParkingComfortModeSts_req(timeout=timeout)
            self.response_to_GetParkingComfortModeSts_req(modeSts=modeSts,reason=reason)

    def notify_ParkingComfortModeSts(self, ParkingComfortModeSts: int = 0, exit_reason: int = 1):
        prompt_info = f"----------> 通过SOA Partner发送维持上电模式状态的事件:VehicleSetStatusService::ParkingComfortModeSts: {ParkingComfortModeSts}, exit_reason: {exit_reason}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("VehicleSetStatusService_server", "ParkingComfortModeSts",
                                               {"sts":{"modeSts":ParkingComfortModeSts, "reason":exit_reason}})


    def hmi_get_automatic_door_closing(self, triggertype:TriggerType, time_wait = 2):
        prompt_info = f"---------->通过SOA DoorService_client:GetAutoCloseTrigger 获取D档自动关门设置状态{triggertype.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if triggertype.name == "disable":
                # self.ck_s2s_event("DoorService_client", "AutoCloseTrigger", {"triggers": []})
                self.send_request_and_ck_resp("DoorService_client", "GetAutoCloseTrigger", {}, {"out": []})
            elif triggertype.name == "enable":
                # self.ck_s2s_event("DoorService_client", "AutoCloseTrigger", {"triggers": [0]})
                self.send_request_and_ck_resp("DoorService_client", "GetAutoCloseTrigger", {}, {"out": [0]})
                
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def check_GetLockSuccessTriggerSource_req(self, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出CentralLockService:GetLockSuccessTriggerSource请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("CentralLockService_server", "GetLockSuccessTriggerSource", timeout=timeout)
    
    def check_GetLockActTriggerSource_req(self, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出CentralLockService:GetLockActTriggerSource请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("CentralLockService_server", "GetLockActTriggerSource", timeout=timeout)

    def check_GetLockSuccessTriggerSource_req_and_feedback_resp(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:CentralLockService:GetLockSuccessTriggerSource,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetLockSuccessTriggerSource_req(timeout=timeout)
            self.response_to_GetLockSuccessTriggerSource_req(trigger_source_id)

    def check_GetLockActTriggerSource_req_and_feedback_resp(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices, timeout: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:CentralLockService:GetLockSuccessTriggerSource,并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetLockActTriggerSource_req(timeout=timeout)
            self.response_to_GetLockActTriggerSource_req(trigger_source_id)

    def response_to_GetLockSuccessTriggerSource_req(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices):
        prompt_info = f"----------> 通过SOA Partner发送CentralLockService:GetLockSuccessTriggerSource请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("CentralLockService_server", "GetLockSuccessTriggerSource", trigger_source_id.value)

    def response_to_GetLockActTriggerSource_req(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices):
        prompt_info = f"----------> 通过SOA Partner发送CentralLockService:GetLockActTriggerSource"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("CentralLockService_server", "GetLockActTriggerSource", trigger_source_id.value)


    def check_NotifyRVCLockInfo_event(self, sts: UnlockSts=UnlockSts.kSuccess,uid: int = 0, seqId: str = '', timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRVCLockInfo事件"):
            logger.info("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRVCLockInfo事件")
            if uid == 0 and seqId == '':
                self.chk_notify("RemoteCtrlService_client", "NotifyRVCLockInfo", {"info": {'sts':sts.value}},
                                timeout=timeout)
            else:
                self.chk_notify("RemoteCtrlService_client", "NotifyRVCLockInfo", {"info": {'sts':sts.value,'uid':uid,'seqId':seqId}},
                                timeout=timeout)
                
    def send_Alldoor_close(self):
        prompt_info = f"---------->通过 DoorService_server:notify_DoorSts 发送门开关状态为所有门关闭"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.notify_FrntLeftDoorSts()
            self.notify_FrntRightDoorSts()
            self.notify_RearRightDoorSts()
            self.notify_RearLeftDoorSts()
            self.notify_TailGateService_OpenCloseStatus()
            self.notify_TailGateService_Status()
    
    def send_Alldoor_open(self):
        prompt_info = f"---------->通过 DoorService_server:notify_DoorSts 发送门开关状态为所有门打开"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
            self.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
            self.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
            self.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
            self.notify_TailGateService_OpenCloseStatus(isopen=True)
            self.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
    
    def set_alldoor_sts(self, sts: DoorStatus=DoorStatus.kClosing):
        prompt_info = f"---------->通过 DoorService_server:notify_DoorSts 发送门开关状态为所有门{sts}"
        with allure.step(prompt_info): 
            logger.info(prompt_info)
            self.notify_FrntLeftDoorSts(isopen=True,sts=sts)
            self.notify_FrntRightDoorSts(isopen=True,sts=sts)
            self.notify_RearRightDoorSts(isopen=True,sts=sts)
            self.notify_RearLeftDoorSts(isopen=True,sts=sts)
            if sts == DoorStatus.kClosed:
                self.notify_TailGateService_OpenCloseStatus(isopen=False)
            else:
                self.notify_TailGateService_OpenCloseStatus(isopen=True)
            self.notify_TailGateService_Status(tailgate_sts=sts)

    def notify_WindowPosition_sts(self, positions: list = [100, 100,100, 100],):
        position_list =  [{"id": id, "position": position} for id, position in enumerate(positions)]
        with allure.step(
                f"通过SOA Partner发出车窗的状态WindowService::WindowPosition为position_list"):
            logger.info(
                f"通过SOA Partner发出车窗的状态WindowService::WindowPosition为position_list")
            self.soa_partner.send_event_notify("WindowService_server", "WindowPosition",
                                            {"position":position_list})

    def check_GetOuterRearViewHeatStatus_req(self, id: ViewId = ViewId.RearViewAll, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出OuterRearViewService:GetOuterRearViewHeatStatus请求"):
            logger.info("通过SOA Partner监听TCAM是否发出OuterRearViewService:GetOuterRearViewHeatStatus请求")
            self.ck_s2s_req("OuterRearViewService_server", "GetOuterRearViewHeatStatus", {"views": [id.value]}, timeout=timeout)

    def response_to_GetOuterRearViewHeatStatus_req(self, id: ViewId = ViewId.RearViewAll, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, \
                                                   heat_sts: HeatSts = HeatSts.On):
        prompt_info = f"----------> 通过SOA Partner发送OuterRearViewService:GetOuterRearViewHeatStatus请求的响应, ViewId:{id.value}, \
            HeatWorkSts: {heat_work_sts.value}, HeatSts: {heat_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("OuterRearViewService_server", "GetOuterRearViewHeatStatus",
                                                  args = [{"id": id.value, "sts": {"workSts": heat_work_sts.value,"heatSts": heat_sts.value}}])

    def check_GetOuterRearViewHeatStatus_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, \
                                                                 heat_sts: HeatSts = HeatSts.On, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取OuterRearViewService:GetOuterRearViewHeatStatus请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetOuterRearViewHeatStatus_req(id, timeout)
            self.response_to_GetOuterRearViewHeatStatus_req(id, heat_work_sts, heat_sts)

            
    def notify_FrontCameraHeatStatus(self, heat_sts: HeatStatus = HeatStatus.HeatStatusOn):
        prompt_info = f"----------> 通过SOA Partner发送前摄像头加热状态事件:ShieldWindowService::FrontCameraHeatStatus: HeatStatus {heat_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ShieldWindowService_server", "FrontCameraHeatStatus ", {"sts": heat_sts.value})


    def notify_RearShieldWindowHeatStatus(self, heat_sts: HeatStatus = HeatStatus.HeatStatusOn):
        prompt_info = f"----------> 通过SOA Partner发送后挡风玻璃加热状态事件:ShieldWindowService::RearShieldWindowHeatStatus: HeatStatus {heat_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ShieldWindowService_server", "RearShieldWindowHeatStatus", {"sts": heat_sts.value})
			
    def notify_OuterRearViewHeatStatus(self, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, heat_sts: HeatSts = HeatSts.On):
        prompt_info = f"----------> 通过SOA Partner发送外后视镜加热状态事件:OuterRearViewService:OuterRearViewHeatStatus HeatWorkSts {heat_work_sts.value}, \
            HeatSts {heat_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("OuterRearViewService_server", "OuterRearViewHeatStatus", {"sts": {"workSts": heat_work_sts.value,"heatSts": heat_sts.value}})

    def check_envent_door_movement_and_antipinch_status(self, sidedoor: SideDoor, isopen: bool, doormovests: DoorMoveStatus, antipinch: bool, time_wait: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner DoorService_client 通知当前{sidedoor.name}门运动状态为{doormovests.name}, 防夹状态为{antipinch}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sidedoor.name == "All":
                self.ck_s2s_event("DoorService_client", "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})
                self.ck_s2s_event("DoorService_client", "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})
                self.ck_s2s_event("DoorService_client", "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})
                self.ck_s2s_event("DoorService_client", "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})

            elif sidedoor.name == "FrntLeftDoorSts":
                self.ck_s2s_event("DoorService_client", "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})
                
            elif sidedoor.name == "FrntRightDoorSts":
                self.ck_s2s_event("DoorService_client", "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})
            
            elif sidedoor.name == "RearLeftDoorSts":
                self.ck_s2s_event("DoorService_client", "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})

            elif sidedoor.name == "RearLeftDoorSts":
                self.ck_s2s_event("DoorService_client", "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": isopen}, "sts": doormovests.value, "isAntiPinch": antipinch}})


            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def check_envent_lock_reminder(self, lockreminder: LockReminder, time_wait = 1):
        prompt_info = f"---------->通过SOA CentralLockService::CentralLockReminder 校验当前解闭锁动作提醒通知状态为{lockreminder.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("CentralLockService_client", "CentralLockReminder", {"reminder": lockreminder.value})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def set_power_outlet_req(self, poweroutletreq: PowerOutLetReq, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner VehicleModeService_client::SetPowerOutletConnect 设置当前12v电源继电器为{poweroutletreq.name}状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("VehicleModeService_client", "SetPowerOutletConnect", {"req": poweroutletreq.value})
            
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def notify_OuterRearViewFoldStatus(self, view_id: ViewId = ViewId.RearViewAll, value_left: ViewFoldStatus = ViewFoldStatus.StatusFolded, \
                                       validity_left: ValidityLevel = ValidityLevel.kValid, value_right: ViewFoldStatus = ViewFoldStatus.StatusFolded, \
                                        validity_right: ValidityLevel = ValidityLevel.kValid):
        prompt_info = f"----------> 通过SOA Partner发送通知外后视镜折叠状态事件:OuterRearViewService:OuterRearViewFoldStatus"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            fold_status = [{"id": 0, "value": value_left.value, "validity": validity_left.value}, 
                            {"id": 1, "value": value_right.value, "validity": validity_right.value}]
            if view_id.value == 0: 
                fold_status.remove(fold_status[0])
            elif view_id.value == 1:
                fold_status.remove(fold_status[1])
            self.soa_partner.send_event_notify("OuterRearViewService_server", "OuterRearViewFoldStatus", {"status": fold_status})

    def notify_ViewFault(self, *view_fault):
        prompt_info = f"----------> 通过SOA Partner发送通知外后视镜故障状态事件:OuterRearViewService:ViewFault"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            faults = []
            for fault in view_fault:
                faults.append({"faultId": fault[0], "faultMsg": fault[1], "viewId": fault[2]})
            self.soa_partner.send_event_notify("OuterRearViewService_server", "ViewFault", {"faults": faults})                                            

    def check_Unfold_req(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出OuterRearViewService:Unfold请求"):
            logger.info("通过SOA Partner监听TCAM是否发出OuterRearViewService:Unfold请求")
            self.ck_s2s_req("OuterRearViewService_server", "Unfold", {"views": [id.value], "isAutoUnFold": is_auto_unfold}, timeout=timeout)

    def response_to_Unfold_req(self, result: int = 0):
        prompt_info = f"----------> 通过SOA Partner发送OuterRearViewService:Unfold请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("OuterRearViewService_server", "Unfold", args = result)

    def check_Unfold_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, \
        timeout: Union[float, int] = 1, result: int = 0):
        prompt_info = f"---------->获取OuterRearViewService:Unfold请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_Unfold_req(id=id, is_auto_unfold=is_auto_unfold, timeout=timeout)
            self.response_to_Unfold_req(result=result)

    def check_Fold_req(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出OuterRearViewService:Fold请求"):
            logger.info("通过SOA Partner监听TCAM是否发出OuterRearViewService:Fold请求")
            self.ck_s2s_req("OuterRearViewService_server", "Fold", {"views": [id.value], "isAutoUnFold": is_auto_unfold}, timeout=timeout)

    def response_to_Fold_req(self, result: int = 0):
        prompt_info = f"----------> 通过SOA Partner发送OuterRearViewService:Fold请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("OuterRearViewService_server", "Fold", args = result)

    def check_Fold_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, result: int = 0, \
                                         is_auto_unfold: bool = True, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取OuterRearViewService:Fold请求的响应,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_Fold_req(id=id,is_auto_unfold=is_auto_unfold,timeout=timeout)
            self.response_to_Fold_req(result)

    def notify_PetModeSts(self, sts: PetModeSts = PetModeSts.kOFF):
        prompt_info = f"----------> 通过SOA Partner发送通知宠物模式状态事件:PetModeSts={sts.value}状态"
        with allure.step(prompt_info):
            self.soa_partner.send_event_notify("InteractiveService_server", "PetModeSts", {"sts": sts.value})  

    def check_SeatService_SetVentingLevel_req(self, id: SeatId = SeatId.All, info: HeatLevel = HeatLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求"):
            logger.info("通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求")
            self.ck_s2s_req("SeatService_server", "SetVentingLevel",
                            {"params": [{"id": id.value, "uint8Info": info.value}], "source": source.value}, timeout=timeout)

    def response_to_SeatService_SetVentingLevel_req(self):
        with allure.step("通过SOA Partner发送SeatService:SetVentingLevel请求的响应"):
            logger.info("通过SOA Partner发送SeatService:SetVentingLevel请求的响应")
            self.send_method_response("SeatService_server", "SetVentingLevel", args=None)

    def check_SeatService_SetVentingLevel_req_and_feedback_resp(self, id: SeatId = SeatId.All, info: VentLevel = VentLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求并返回响应")
            self.check_SeatService_SetVentingLevel_req(id=id, info=info, source=source, timeout=timeout)
            self.response_to_SeatService_SetVentingLevel_req()

    def rvc_seat_venting_start_success(self, id: SeatId = SeatId.FrontLeft, vent_level: VentLevel = VentLevel.High, keep_time: int = 30,):
        prompt_info = f"通过SOA Partner模拟座椅通风启动通风成功场景"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True,keep_time=keep_time, timeout=20)
            self.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=id, info=vent_level, timeout=20)
            sleep(2)
            self.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
            self.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=id, info=vent_level, timeout=20)
            if id == SeatId.FrontLeft:
                self.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=vent_level)
            elif id == SeatId.FrontRight:
                self.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=vent_level)
            elif id == SeatId.RearLeft:
                self.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=vent_level)
            else:
                self.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=vent_level)

    def set_viewmirror_angle(self, viewPos: ViewPos, hori_angle: Union[int, float], vert_angle: Union[int, float], time_wait: Union[float, int] = 0):
        with allure.step(f"调用接口SetMirrorAngleTarget 调节{viewPos}水平方向角度{hori_angle}垂直方向角度{vert_angle}"):
            logger.info(f"调用接口SetMirrorAngleTarget 调节{viewPos}水平方向角度{hori_angle}垂直方向角度{vert_angle}")
            self.send_method_request("OuterRearViewService_client", "SetMirrorAngleTarget", {"params": [{"viewId":viewPos.value, "horizontalAngle":hori_angle, "verticalAngle":vert_angle}]})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def get_viewmirror_angle(self, views:ViewPos,viewPos: ViewPos, hori_angle: Union[int, float], vert_angle: Union[int, float], time_wait: Union[float, int] = 3):
        with allure.step(f"调用接口GetMirrorAngle 获取{viewPos}水平方向角度{hori_angle}垂直方向角度{vert_angle}"):
            logger.info(f"调用接口GetMirrorAngle 获取{viewPos}水平方向角度{hori_angle}垂直方向角度{vert_angle}")
            self.send_request_and_ck_resp("OuterRearViewService_client", 'GetMirrorAngle', {"views":[views.value]}, 
                                              {"out":[{"viewId": viewPos.value, "horizontalAngle": hori_angle,"verticalAngle":vert_angle}]})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def set_carloctr_req(self,req:CarLocalTraceReq):
        prompt_info = f"----------> 通过SOA Partner KeyService_client:SetCarLocalTraceRequest,请求设置设置寻车模式为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("KeyService_client", "SetCarLocalTraceRequest", {"req": req.value})
    
    def check_keep_power_mode_and_time(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, displaytime:DisplayLeftTime=DisplayLeftTime.kUnknown, do_assert=True,  **kwargs):
        '''
        keep_power 为 True 校验 当前模式，验当前是维持上电模式，
        keep_powe 为 False 校验 当前模式，验当前不是维持上电模式，
        exit_reason:0=kNormal  //正常状态，默认值 1=kUserReq  //用户请求关闭
        2=kHVSOC   //高压电池电量低于阈值 3=kGearNotP  //挡位非P挡
        4=kCarModeNotNormal //车辆模式不满足 5=kFOTAUpdate  //车辆开始FOTA升级
        6=kOther //其他原因退出
        '''
        if  keep_power:
            ck_info = {'out': {'modeSts': 1, 'reason': exit_reason.value, 'displayLeftTime': displaytime.value}}
        else:
            ck_info = {'out': {'modeSts': 0, 'reason': exit_reason.value, 'displayLeftTime': displaytime.value}}

        method_name = 'GetParkingComfortModeSts'
        ret = self.send_request_and_ck_resp(
            'VehicleSetStatusService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleSetStatusService ck_info={ck_info}       ret={ret}")
        if keep_power:
            logger.info(F"当前为  {'维持上电模式' if ret else '非维持上电模式'}")
        else:
            logger.info(F"当前为  {'维持上电模式或退出原因异常' if not ret else '非维持上电模式'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"
            
    def get_and_check_envent_door_fault_sts(self, checkinterfacetype: CheckInterfaceType, doorid: DoorId, doorfaultsts: DoorfFultSts, time_wait = 1):
        prompt_info = f"---------->通过SOA DoorService_client:DoorFault 校验{doorid.name}侧门故障状态为{doorfaultsts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if checkinterfacetype.name == "Get":
                self.request_and_ck_resp("DoorService_client", "GetFaultInfo", {},{"out": [{"fault": doorfaultsts.value, "faultMsg": "", "door": doorid.value}]})
            elif checkinterfacetype.name == "CheckNotify":
                self.ck_s2s_event("DoorService_client", "DoorFault", {"faults": [{"fault": doorfaultsts.value, "faultMsg": "", "door": doorid.value}]})
            elif checkinterfacetype.name == "All":
                self.ck_s2s_event("DoorService_client", "DoorFault", {"faults": [{"fault": doorfaultsts.value, "faultMsg": "", "door": doorid.value}]})
                self.send_request_and_ck_resp("DoorService_client", "GetFaultInfo", {},{"out": [{"fault": doorfaultsts.value, "faultMsg": "", "door": doorid.value}]})
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def check_no_GetHeat_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SteerWheelService:GetHeat请求"):
            self.ck_no_req("SteerWheelService_server", "GetHeat", timeout=timeout)

    def check_no_GetRemotePowerStatus_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetRemotePowerStatus请求"):
            self.ck_no_req("ClimateControlService_server", "GetRemotePowerStatus", timeout=timeout)
            
    def check_no_GetDefrostSts_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetDefrostSts请求"):
            self.ck_no_req("ClimateControlService_server", "GetDefrostSts", timeout=timeout)
            
    def check_no_GetChargingInfo_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:GetChargingInfo请求"):
            self.ck_no_req("HighVoltageService_server", "GetChargingInfo", timeout=timeout)
            
    def check_no_GetBatteryTemperatureInfo_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:GetBatteryTemperatureInfo请求"):
            self.ck_no_req("HighVoltageService_server", "GetBatteryTemperatureInfo", timeout=timeout)

    def notify_NotifyConfigList(self, ccp_dict_list:list=None):
        ccp_list = [{"name": 566, "value": 0x10},{"name": 962, "value": 0x0}]
        if ccp_dict_list != None:
            for ccp_dict in ccp_dict_list:
                if ccp_list[0]["name"] == ccp_dict["name"]:
                    ccp_list[0]["value"] = ccp_dict["value"]
                if ccp_list[1]["name"] == ccp_dict["name"]:
                    ccp_list[1]["value"] = ccp_dict["value"]
        with allure.step(
                f"模拟BGM发送车辆配置字值改变通知，通知的参数{ccp_list}"):
            logger.info(
                f"模拟BGM发送车辆配置字值改变通知，通知的参数{ccp_list}")
            # ccp_list = [
            #         {"name": 180, "value": 0x02},
            #         {"name": 181, "value": 0x02},
            #         {"name": 182, "value": 0x01},
            #         {"name": 186, "value": 0x02},
            #         {"name": 189, "value": 0x02},
            #         {"name": 566, "value": 0x10},
            #         {"name": 950, "value": 0x02}
            #         ]
            # for ccp in ccp_list:
            #     if ccp["name"] == ccp_name:
            #         ccp["value"] = ccp_value
            self.soa_partner.send_event_notify("CarConfigService_server", "NotifyConfigList", {'list':ccp_list})

    
    def notify_ConfigDataNotify(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        config_info = {
                            "ecuName":"TCAM",
                            "info":{
                                    "ecuName":"TCAM",
                                    "fileInfoList":[
                                                        {
                                                            "appName": app_name,
                                                            "configFileName": file_name,
                                                            "publishID": publish_id+1782596115442114560,
                                                            "action": action,
                                                            "fileType": file_type,
                                                            "pushType": push_type,
                                                            "data": config_data,
                                                            "strategy": strategy,
                                                            "domainVersion": domain_version,
                                                            "md5": hashlib.md5(config_data.encode("utf-8")).hexdigest().upper()
                                                            }
                                                    ]
                                    }
                        }
        with allure.step(f"模拟BGM发送远程配置数据"):
            logger.info(f"模拟BGM发送远程配置数据: {0}".format(json.dumps(config_info)))
            self.soa_partner.send_event_notify("ConfigMasterService_server", "ConfigDataNotify", config_info)

    def check_GetEcuAppsVersion_req(self, ecu: str = "TCAM", timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求")
            self.ck_s2s_req("ConfigMasterService_server", "GetEcuAppsVersion", {"ecuName":ecu}, timeout=timeout)

    def response_to_GetEcuAppsVersion_req(self, app_name: str = "gb32960", publish_id: int = 0, \
                                        is_empty: bool = False, report_type: int = 4, status_type: int = 1025, \
                                        time_stamp: int = 0):
        with allure.step("通过SOA Partner发送ConfigMasterService:GetEcuAppsVersion请求的响应"):
            logger.info("通过SOA Partner发送ConfigMasterService:GetEcuAppsVersion请求的响应")
            app_versions_info = {
                        "isEmpty": is_empty,
                        "ecuName": "TCAM",
                        "appVersionList":[
                                            {
                                                "appName": app_name,
                                                "configFileName": "key_value_tab_config",
                                                "publishID": publish_id+1782596115442114560,
                                                "reportData":[
                                                                {
                                                                    "reportType":4,
                                                                    "statusType":1025,
                                                                    "statusMessage":"kAppApply",
                                                                    "appIndex":0,
                                                                    "timestamp": time.time()*1000}]},
                                            ],
                        "reportData":[]}
            for app_version in app_versions_info["appVersionList"]:
                if app_version["appName"] == app_name:
                    app_version["publishID"] = publish_id+1782596115442114560
                    app_version["reportData"][0]["reportType"] = report_type
                    app_version["reportData"][0]["statusType"] = status_type
                    if time_stamp != 0:
                        app_version["reportData"][0]["timestamp"] = time_stamp
            self.send_method_response("ConfigMasterService_server", "GetEcuAppsVersion", args=app_versions_info)

    def check_GetEcuAppsVersion_req_and_feedback_resp(self, app_name: str = "gb32960", publish_id: int = 0, \
                                        is_empty: bool = False, report_type: int = 4, status_type: int = 1025, \
                                        time_stamp: int = 0, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求并返回响应")
            self.check_GetEcuAppsVersion_req(timeout=timeout)
            self.response_to_GetEcuAppsVersion_req(app_name=app_name, publish_id=publish_id, is_empty=is_empty, \
                                                   report_type=report_type, status_type=status_type, time_stamp=time_stamp)

    def check_GetConfigMasterVersion_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求")
            self.ck_s2s_req("ConfigMasterService_server", "GetConfigMasterVersion", timeout=timeout)

    def response_to_GetConfigMasterVersion_req(self, config_version: str = "Config2.0.12.1"):
        with allure.step("通过SOA Partner发送ConfigMasterService:GetConfigMasterVersion请求的响应"):
            logger.info("通过SOA Partner发送ConfigMasterService:GetConfigMasterVersion请求的响应")
            self.send_method_response("ConfigMasterService_server", "GetConfigMasterVersion", args=config_version)

    def check_GetConfigMasterVersion_req_and_feedback_resp(self, config_version: str = "Config2.0.12.1", timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求并返回响应")
            self.check_GetConfigMasterVersion_req(timeout=timeout)
            self.response_to_GetConfigMasterVersion_req(config_version=config_version)

    def check_GetAppConfig_req(self, app_name: str = "gb32960", timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetAppConfig请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetAppConfig请求")
            self.ck_s2s_req("ConfigMasterService_server", "GetAppConfig", {"ecuName": "TCAM","appName": app_name}, timeout=timeout)

    def response_to_GetAppConfig_req(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                    publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        with allure.step("通过SOA Partner发送ConfigMasterService:GetAppConfig请求的响应"):
            logger.info("通过SOA Partner发送ConfigMasterService:GetAppConfig请求的响应: {0}".format(config_data))
            config_info = {
                            "ecuName":"TCAM",
                            "fileInfoList":[
                                                {
                                                    "appName": app_name,
                                                    "configFileName": file_name,
                                                    "publishID": publish_id+1782596115442114560,
                                                    "action": action,
                                                    "fileType": file_type,
                                                    "pushType": push_type,
                                                    "data": config_data,
                                                    "strategy": strategy,
                                                    "domainVersion": domain_version,
                                                    "md5": hashlib.md5(config_data.encode("utf-8")).hexdigest().upper()
                                                }
                                            ]
                           }
            self.send_method_response("ConfigMasterService_server", "GetAppConfig", args=config_info)

    def check_GetAppConfig_req_and_feedback_resp(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                                strategy: int = 3, domain_version: str = "2.0.0", timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetAppConfig请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:GetAppConfig请求并返回响应")
            self.check_GetAppConfig_req(app_name=app_name, timeout=timeout)
            self.response_to_GetAppConfig_req(config_data=config_data, app_name=app_name, file_name=file_name, publish_id=publish_id, \
                                              action=action, file_type=file_type, push_type=push_type, strategy=strategy, \
                                              domain_version=domain_version)

    def check_SendConfigStatusToTsp_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求")
            self.ck_s2s_req("ConfigMasterService_server", "SendConfigStatusToTsp", timeout=timeout)

    def response_to_SendConfigStatusToTsp_req(self, config_result: bool = True):
        with allure.step("通过SOA Partner发送ConfigMasterService:SendConfigStatusToTsp请求的响应"):
            logger.info("通过SOA Partner发送ConfigMasterService:SendConfigStatusToTsp请求的响应")
            self.send_method_response("ConfigMasterService_server", "SendConfigStatusToTsp", args=config_result)

    def check_SendConfigStatusToTsp_req_and_feedback_resp(self, config_result: bool = True, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求并返回响应")
            self.check_SendConfigStatusToTsp_req(timeout=timeout)
            self.response_to_SendConfigStatusToTsp_req(config_result=config_result)

    def send_config_data_and_feedback_result(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        self.notify_ConfigDataNotify(app_name=app_name, config_data=config_data, file_name=file_name, publish_id=publish_id, \
                                    action=action, file_type=file_type, push_type=push_type, strategy=strategy, \
                                    domain_version=domain_version)
        self.check_SendConfigStatusToTsp_req_and_feedback_resp(timeout=5)
        self.check_SendConfigStatusToTsp_req_and_feedback_resp(timeout=5)
        self.check_SendConfigStatusToTsp_req_and_feedback_resp(timeout=5)
        # self.check_SendConfigStatusToTsp_req_and_feedback_resp(timeout=5)

    def check_NotifyRemoteAuthStartModeSts_event(self, sts: RemoteAuthSts = RemoteAuthSts.kDefault, send_time:int=0xffffffff, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:RemoteAuthStartModeSts事件"):
            if sts == RemoteAuthSts.kReadyEntry:
                if send_time == 0xffffffff:
                    send_time = 0
                else:
                    send_time = 120 - send_time
                for i in range(120,send_time,-1):
                        logger.info(f"通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:RemoteAuthStartModeSts事件 sts的值{sts.name} ： {sts.value}, time:{i}")
                        self.ck_s2s_event("RemoteCtrlService_client", "RemoteAuthStartModeSts", {'info':{"sts": sts.value, 'time': i}}, timeout=timeout)
            else:
                logger.info(f"通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:RemoteAuthStartModeSts事件 sts的值{sts.name} ： {sts.value}, time:{0xffffffff}")
                self.ck_s2s_event("RemoteCtrlService_client", "RemoteAuthStartModeSts", {'info':{"sts": sts.value, 'time': 0xffffffff}}, timeout=timeout)

    def notify_VehicleInsidePersonSts(self, userInVehicleStatus: bool = False, userInVehicleStatusWithCam: bool = False):
        prompt_info = f"----------> 通过SOA Partner发送车内有人状态事件:SeatService:VehicleInsidePersonSts userInVehicleStatus：{userInVehicleStatus}, \
            userInVehicleStatusWithCam：{userInVehicleStatusWithCam}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_server", "VehicleInsidePersonSts", {"personSts": {"userInVehicleStatus": userInVehicleStatus,"userInVehicleStatusWithCam": userInVehicleStatusWithCam}})

    def check_Play2_req(self, app: str = None,
                                   txt: str = None,
                                   param: str = None, timeout: Union[float, int] = 0.5):
        with allure.step("通过SOA Partner监听TCAM是否发出CdcTtsService::Play2请求"):
            logger.info("通过SOA Partner监听TCAM是否发出CdcTtsService::Play2请求")
            if app or txt or param:
                self.ck_s2s_req("CdcTtsService_server_cdc_a_ttsservice", "Play2", {"app": app, "txt": txt, "param": param}, timeout=timeout)
            else:
                self.ck_s2s_req("CdcTtsService_server_cdc_a_ttsservice", "Play2", timeout=timeout)
    
    def event_check_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        prompt_info = f"---------->调用服务WindowService_client WindowPosition Check窗户的位置改变的通知"
        logger.info(prompt_info)
        check_list = []
        with allure.step(prompt_info):
            if pos_drvr is not None:
                logger.info(f"--------->获取主驾窗户位置是否为{pos_drvr.name}")
                check_cont = {"id": 0, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_pass is not None:
                logger.info(f"--------->获取副驾窗户位置是否为{pos_pass.name}")
                check_cont = {"id": 1, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_lere is not None:
                logger.info(f"--------->获取左后窗户位置是否为{pos_lere.name}")
                check_cont = {"id": 2, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_rire is not None:
                logger.info(f"--------->获取右后窗户位置是否为{pos_rire.name}")
                check_cont = {"id": 0, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            self.ck_s2s_event("WindowService_client","WindowPosition",{"position": check_list})


    def set_and_cancel_auto_lock_settings(self, settings: Settings, time_wait = 2):
        prompt_info = f"---------->通过SOA DoorService_client::CancelAutoUnlockTrigger||SetAutoUnlockTrigger 设置 or 取消P档自动解锁设置项为{settings.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if settings.name == "Set":
                self.send_method_request("DoorService_client", "SetAutoUnlockTrigger", {"trigger": 0})
                
            elif settings.name == "CancelSet":
                self.send_method_request("DoorService_client", "CancelAutoUnlockTrigger", {"trigger": 0}) 
            else:
                logger.info(f"parameters not supported")
      
            self.send_method_request
            logger.info(f"--------->等待{time_wait}")            
            sleep(time_wait)
            
    def notify_GB32960Data(self, gb_data: dict = {}):
        with allure.step("通过SOA Partner发送GB32960Service:GB32960Data事件"):
            logger.info(f"通过SOA Partner发送GB32960Service:GB32960Data事件")
            self.soa_partner.send_event_notify("GB32960Service_server", "GB32960Data", {"info": gb_data})
    
    def event_check_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        prompt_info = f"---------->调用服务WindowService_client WindowPosition Check窗户的位置改变的通知"
        logger.info(prompt_info)
        check_list = []
        with allure.step(prompt_info):
            if pos_drvr is not None:
                logger.info(f"--------->获取主驾窗户位置是否为{pos_drvr.name}")
                check_cont = {"id": 0, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_pass is not None:
                logger.info(f"--------->获取副驾窗户位置是否为{pos_pass.name}")
                check_cont = {"id": 1, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_lere is not None:
                logger.info(f"--------->获取左后窗户位置是否为{pos_lere.name}")
                check_cont = {"id": 2, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            if pos_rire is not None:
                logger.info(f"--------->获取右后窗户位置是否为{pos_rire.name}")
                check_cont = {"id": 0, "position": 4*(pos_drvr.value-1),"validity": 0}
                check_list.append(check_cont)

            self.ck_s2s_event("WindowService_client","WindowPosition",{"position": check_list})

    def event_check_NotifyCarLocalTraceActiveStatus(self,cartrace_sts: CarLocalTraceActiveStatus = CarLocalTraceActiveStatus.kSuccess):
        prompt_info = f"通过SOA Partner检查寻车执行功能的状态KeyService::NotifyCarLocalTraceActiveStatus {cartrace_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("KeyService_client", "NotifyCarLocalTraceActiveStatus",{"sts": cartrace_sts.value})

    def set_maintenanceMode(self, maintenanceMode: bool):
        self.send_method_request(
            "VehicleSetStatusService_client", "SetMaintenanceMode", {"isOn": maintenanceMode}
        )

    def update_InteractiveService_response(self, pet_mode_sts: str):
        get_return_args = {"OutputValueList": {"id":"PetModeSts","data":"0", "code":0}}
        get_return_args["OutputValueList"].update({"data": pet_mode_sts})

        self.stop_send_InteractiveService_response()
        self.soa_partner.partner_infos[
            f'InteractiveService_server'].args = get_return_args
        self.start_send_InteractiveService_response()       

    def stop_send_InteractiveService_response(self):
        try:
            self.send_response_to_req_stop(partner_key=f'InteractiveService_server',
                                           func=self.on_setPetModeSts)
        except KeyError:
            logger.error("当前服务未注册,无法调用stop")

    def start_send_InteractiveService_response(self):
        self.send_response_to_req_start(partner_key=f'InteractiveService_server',
                                        func=self.on_setPetModeSts)

    def on_setPetModeSts(self, partner_key, msg):
        if 'InteractiveService_server' in partner_key and msg["function"] == 'Get':
            if not hasattr(self.soa_partner.partner_infos[partner_key], "args"):
                setattr(self.soa_partner.partner_infos[partner_key], "args", {"OutputValueList": {"id":"PetModeSts","data":"0", "code":0}})
            self.send_method_response(partner_key=partner_key, method_name='Get',
                                      args=self.soa_partner.partner_infos[partner_key].args)

    def till_UpdateProcess_event_to(self, master_updateprocess_event_field: MASTER_UpdateProcess_EVENT, target_status=None, timeout=60):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.get_fota_UpdateProcess(master_updateprocess_event_field=master_updateprocess_event_field)
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current FOTA Master {master_updateprocess_event_field} is {curr_status}")

    def hmi_set_and_get_braking_close_the_door(self, isOn: bool, time_wait: Union[float, int] = 1):
        prompt_info = f"----------> 通过SOA Partner EntryService_client 设置和获取踩刹车关门设置项为{isOn}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("EntryService_client", "SetBrakeCloseDoorInhibit", {"isOn": isOn})
            self.send_request_and_ck_resp("EntryService_client","GetBrakeCloseDoorInhibitStatus",{},{"out": isOn})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def start_single_partner(self, service: str, role: str, instance: str = None, heartbeat: int = 600):
        return self.soa_partner.start_single_partner(service, role, instance, heartbeat)

    def stop_single_partner(self, partner_key):
        return self.soa_partner.stop_single_partner(partner_key)

    def check_GetConfigList_req(self, name: int = 566, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出请求:CarConfigService:GetConfigList"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("CarConfigService_server", "GetConfigList", {"names": [name]}, timeout=timeout)

    def response_to_GetConfigList_req(self, ccp_value: int = 0x10):
        prompt_info = f"----------> 通过SOA Partner发送CarConfigService:GetConfigList请求的响应"
        with allure.step(prompt_info):
            self.send_method_response("CarConfigService_server", "GetConfigList", [{"name": 566, "value": ccp_value}])

    def check_GetConfigList_req_and_feedback_resp(self, name: int = 566, ccp_value: int = 0x10, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出CarConfigService:GetConfigList请求，并发送响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetConfigList_req(name=name, timeout=timeout)
            self.response_to_GetConfigList_req(ccp_value=ccp_value)

    def notify_NotifyAmbientTempRawData(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True):
        prompt_info = f"----------> 通过SOA Partner发送环境温度:ClimateControlService:NotifyAmbientTempRawData {temp}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ClimateControlService_server", "NotifyAmbientTempRawData",
                                               {"data": {"temp": temp, "tempUnit": tempunit, "isValid": is_valid}})

    def notify_Temperature(self, climatezoneId: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 10.0, is_valid: bool = True):
        prompt_info = f"----------> 通过SOA Partner发送舱内温度:ClimateControlService:Temperature {temp}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ClimateControlService_server", "Temperature",
                                               {"info": {"ClimateZoneId": climatezoneId.value, "value": temp, "isValid": is_valid}})
            
    def check_getAmbientTempRawData_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求")
            self.ck_s2s_req("ClimateControlService_server", "getAmbientTempRawData", timeout=timeout)

    def response_to_getAmbientTempRawData_req(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True):
        with allure.step("通过SOA Partner发送ClimateControlService:getAmbientTempRawData请求的响应"):
            logger.info("通过SOA Partner发送ClimateControlService:getAmbientTempRawData请求的响应")
            self.send_method_response("ClimateControlService_server", "getAmbientTempRawData", {"temp": temp, "tempUnit": tempunit, "isValid": is_valid})

    def check_getAmbientTempRawData_req_and_feedback_resp(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求并返回响应")
            self.check_getAmbientTempRawData_req(timeout=timeout)
            self.response_to_getAmbientTempRawData_req(temp=temp, tempunit=tempunit, is_valid=is_valid)

    def check_GetCurrentTemperature_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperaturea请求"):
            logger.info("通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperature请求")
            self.ck_s2s_req("ClimateControlService_server", "GetCurrentTemperature", timeout=timeout)

    def response_to_GetCurrentTemperature_req(self, zone_id: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 9.0, is_valid: bool = True):
        with allure.step("通过SOA Partner发送ClimateControlService:GetCurrentTemperature请求的响应"):
            logger.info("通过SOA Partner发送ClimateControlService:GetCurrentTemperature请求的响应")
            self.send_method_response("ClimateControlService_server", "GetCurrentTemperature", {"zoneId": zone_id.value, "value": temp, "isValid": is_valid})

    def check_GetCurrentTemperature_req_and_feedback_resp(self, zone_id: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 9.0, is_valid: bool = True, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperature请求并返回响应"):
            logger.info("通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperature请求并返回响应")
            self.check_GetCurrentTemperature_req(timeout=timeout)
            self.response_to_GetCurrentTemperature_req(zone_id=zone_id, temp=temp, is_valid=is_valid)

    def check_Temperature_req_and_feedback_resp(self, s: int= 1, ambienttemp: float = 9.1, temp: float = 10.0, is_valid: bool = True):
        for i in range(0, s):
            self.check_getAmbientTempRawData_req_and_feedback_resp(temp=ambienttemp,is_valid=is_valid, timeout=20)
            self.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=temp,is_valid=is_valid, timeout=20)

    def hmi_set_glove_box_active_req(self, settype: SetType, time_wait: Union[float, int] = 2):
        prompt_info = f"----------> 通过SOA Partner GloveBoxService_client设置手套箱为{settype.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if settype.name == "Open":
                self.send_method_request("GloveBoxService_client", "Open", {})
                
            elif settype.name == "Unlock":
                self.send_method_request("GloveBoxService_client", "Unlock", {})

            elif settype.name == "Lock":
                self.send_method_request("GloveBoxService_client", "Lock", {})

            else:
                logger.info(f"The request type is not supported")
                assert False
                
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def hmi_check_notify_key_connect_sts(self, keytype: KeyType, isconnect: bool, time_wait: Union[float, int] = 2):
        prompt_info = f"----------> 通过SOA Partner KeyService_client::DigitalKeyConnectedStatus校验当前钥匙类型为{keytype.name}, 连接状态为{isconnect}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("KeyService_client", "DigitalKeyConnectedStatus", {"status":  
                [{"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  "type": keytype.value, "isConnected": isconnect}]})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
    def set_findkey_req(self, findzone: FindZone, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> KeyService_client: SetFindKeyZone 设置寻钥匙区域为{findzone.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("KeyService_client", "SetFindKeyZone",{"zone": findzone.value})
            sleep(time_wait)

    def reset_soa_config(self, timeout: Union[float, int] = 0):
        promt_info = f"----------------> 通过SOA Partner发出 ResetSOAConfigService:ResetAllVehicleSOAConfig 恢复初始化设置"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ResetSOAConfigService_client", "ResetAllVehicleSOAConfig", {})
        sleep(timeout)


    def event_check_reset_vehicle_sts(self, state: MainState, notify: Notification, telestate:TeleState, autoState:AutoState, cockpitState:CdcState, digitalKeyState:BncmState, timeout: Union[float, int] = 4.5):
        logger.info(f"通过SOA Partner发出 ObtDiagService:RestartStatus check整车域控重启通知域控重启状态机状态信息为{state}，域控重启提示信息为{notify},TCAM复位状态{telestate}，ACU复位状态{autoState},CDC复位状态{cockpitState}，BNCM复位状态{digitalKeyState}")
        with allure.step(f"通过SOA Partner发出 ObtDiagService:RestartStatus check整车域控重启通知"):
            self.ck_s2s_event("ObtDiagService_client", "RestartStatus", {"status": {"mainState": state.value, "notification": notify.value,
                                                                                    "telematicsState":telestate.value,"autoDrivingState":autoState.value,"cockpitState":cockpitState.value,"digitalKeyState":digitalKeyState.value}})
        sleep(timeout)            

    def set_and_frntleft_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_client", "FrntLeftSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})

    def set_and_frntringht_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):

        prompt_info = f"----------> 通过SOA Partner发送副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("SeatService_client", "FrntRightSeatHeatVentStatus", {"status": {
                                                                                                        "heatLevel": heat_level.value,
                                                                                                        "heatTime": heat_time,
                                                                                                        "heatWorkStatus": heat_work_sts.value,
                                                                                                        "ventLevel": vent_level.value,
                                                                                                        "ventTime": vent_time,
                                                                                                        "ventWorkStatus": vent_work_sts.value
                                                                                                    }})
            
    def event_check_frntleft_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 59,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 59,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone):
        
        prompt_info = f"----------> check 主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value},ventLevel: {vent_level.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            self.ck_s2s_event("SeatService_client", "FrntLeftSeatHeatVentStatus", {"status":{
                                                                                    "heatLevel": heat_level.value,
                                                                                    "heatTime": heat_time,
                                                                                    "heatWorkStatus": heat_work_sts.value,
                                                                                    "ventLevel": vent_level.value,
                                                                                    "ventTime": vent_time,
                                                                                    "ventWorkStatus": vent_work_sts.value
                                                                                    }})

    def event_check_frntringht_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 59,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 59,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone):
        
        prompt_info = f"----------> check 副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus: heatLevel {heat_level.value}, heatTime: {heat_time}, \
            heatWorkStatus {heat_work_sts.value},ventLevel: {vent_level.value}, ventTime: {vent_time}, ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            self.ck_s2s_event("SeatService_client", "FrntRightSeatHeatVentStatus", {"status":{
                                                                                    "heatLevel": heat_level.value,
                                                                                    "heatTime": heat_time,
                                                                                    "heatWorkStatus": heat_work_sts.value,
                                                                                    "ventLevel": vent_level.value,
                                                                                    "ventTime": vent_time,
                                                                                    "ventWorkStatus": vent_work_sts.value
                                                                                    }})
            
    def rvc_set_seat_vent_level(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        prompt_info = f"---------->通过 SeatService_client:SetVentingLevel 设置{pos.name}座椅通风等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "SetVentingLevel",
                                     {"params": [{"id": pos.value, "uint8Info": level.value}],"source":source.value})
            
    def rvc_set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        prompt_info = f"---------->通过 SeatService_client:SetHeatingLevel 设置{pos.name}座椅加热等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("SeatService_client", "SetHeatingLevel",
                                     {"params": [{"id": pos.value, "uint8Info": level.value}],"source":source.value})

    def send_check_reset_vehicle_sts(self, state: MainState, notify: Notification, telestate:TeleState, autoState:AutoState, cockpitState:CdcState, digitalKeyState:BncmState, timeout: Union[float, int] = 4.5):
        logger.info(f"通过SOA Partner发出 ObtDiagService:RestartStatus check整车域控重启通知域控重启状态机状态信息为{state}，域控重启提示信息为{notify},TCAM复位状态{telestate}，ACU复位状态{autoState},CDC复位状态{cockpitState}，BNCM复位状态{digitalKeyState}")
        with allure.step(f"通过SOA Partner发出 ObtDiagService:RestartStatus check整车域控重启通知"):
            self.send_request_and_return_resp("ObtDiagService_client", "GetRestartStatus", {"out": {"mainState": state.value, "notification": notify.value,
                                                                                    "telematicsState":telestate.value,"autoDrivingState":autoState.value,"cockpitState":cockpitState.value,"digitalKeyState":digitalKeyState.value}})
        sleep(timeout)       

    def check_envent_unlocking_action_sts(self, sourceid: LockTrigerSource, time_wait: Union[float, int] = 0):
        prompt_info = f"---------->通过SOA CentralLockService::LockActTriggerSource 接口校验当前解闭锁动作触发源通知状态为{sourceid.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("CentralLockService_client", "LockActTriggerSource", {"sourceId": sourceid.value})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
    
    def set_auto_calibration(self, req: calibration_req=calibration_req.KOn, functionID:CalibrationFunctionID = CalibrationFunctionID.ChrgLid, source:SourceType=SourceType.kScreen, isAlloweSkip:bool=False):
        prompt_info = f"---------->通过 ObtDiagService_client:SetIntelligentCalibrationFunctionCmd 设置智能标定"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ObtDiagService_client", "SetIntelligentCalibrationFunctionCmd",
                                     {"cmd": {'req': req.value, 'intelligentFunctionID': functionID.value, 'sourceType':source.value, 'isAllowedSkip': isAlloweSkip}})

    def set_Calibration_Authorization(self, req: Authorization_req=Authorization_req.kAuthorize):
        prompt_info = f"---------->通过 ObtDiagService_client:SetIntelligentCalibrationAuthorizationCmd 设置智能标定授权"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ObtDiagService_client", "SetIntelligentCalibrationAuthorizationCmd",
                                     {"cmd": {'req': req.value}})

    def set_Calibration_Retry(self, req: retry_req=retry_req.kRetry):
        prompt_info = f"---------->通过 ObtDiagService_client:SetIntelligentCalibrationFunctionRetryCmd 触发重试智能标定"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ObtDiagService_client", "SetIntelligentCalibrationFunctionRetryCmd",
                                     {"cmd": {'retryReq': req.value}})

    def event_check_Calibration_Status_Info(self,text_id: int=255, functionID:CalibrationFunctionID = CalibrationFunctionID.ChrgLid, status: calibration_status=calibration_status.kIdle):
        with allure.step(f"获取标定状态事件上报,Check上报的ID是{functionID.name}, 上报的标定状态是{status.name}"):
            logger.info(f"获取标定状态事件上报,Check上报的ID是{functionID.name}, 上报的标定状态是{status.name}")
            self.ck_s2s_event("ObtDiagService_client", "IntelligentCalibrationStatusInfo", {"info":{'status': status.value, 'intelligentFunctionID': functionID.value, 'textID': text_id}})

    def get_Calibration_Status_Info(self,text_id: int=255, functionID:CalibrationFunctionID = CalibrationFunctionID.ChrgLid, status: calibration_status=calibration_status.kIdle):
        with allure.step(f"请求标定状态,Check上报的ID是{functionID.name}, 上报的标定状态是{status.name}"):
            logger.info(f"请求标定状态,Check上报的ID是{functionID.name}, 上报的标定状态是{status.name}")
            self.send_request_and_ck_resp("ObtDiagService_client", "GetIntelligentCalibrationStatusInfo", {},{"out": {'status': status.value, 'intelligentFunctionID': functionID.value, 'textID': text_id}})

    def event_check_Calibration_Result_Info(self, functionID:CalibrationFunctionID = CalibrationFunctionID.ChrgLid, errorCode: calibration_error_code=calibration_error_code.kSuccess):
        with allure.step(f"获取标定结果事件上报,Check上报的ID是{functionID.name}, 上报的标定结果是{errorCode.name}"):
            logger.info(f"获取标定结果事件上报,Check上报的ID是{functionID.name}, 上报的标定结果是{errorCode.name}")
        self.ck_s2s_event("ObtDiagService_client", "IntelligentCalibrationResultInfo", {"info":{'errorCode': errorCode.value, 'intelligentFunctionID': functionID.value}})


    def get_fota_notifybookinfolist(self, master_NotifyBookInfoListEVENT_field: NotifyBookInfoListEVENT):
        time.sleep(3)
        rtc_bookinfolist = self.return_latest_event("RtcAlarmService_client", "NotifyBookInfoList")['bookInfoList'][0]
        if master_NotifyBookInfoListEVENT_field.value == 0:
            value = rtc_bookinfolist['bookType']
        elif master_NotifyBookInfoListEVENT_field.value == 1:
            value = rtc_bookinfolist['repeatType']
        elif master_NotifyBookInfoListEVENT_field.value == 3:
            value = rtc_bookinfolist['startTime']
        else:
            logger.error("Wrong FOTA Master NotifyBookInfoList event field name !!!")
        logger.info(f"Current FOTA Master {master_NotifyBookInfoListEVENT_field.name} = {value}")
        return value

    def send_cancel_service_book_event(self, service_name: str):
        self.send_method_request(
            "RtcAlarmService_client", "CancelServiceBookEvent", {"serviceName": service_name})


    def check_notify_key_connect_sts(self, keytype: KeyType, isconnect: bool, keyid: list, zone: BLEKeyPrsntZone, battwarbsts:bool = False, time_wait: Union[float, int] = 2):
        prompt_info = f"----------> 通过SOA Partner KeyService_client::DigitalKeyConnectedStatus校验当前钥匙类型为{keytype.name}, 连接状态为{isconnect}, 该钥匙槽定位的区域{zone.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("KeyService_client", "DigitalKeyConnectedStatus", {"status":  
                [{"keyId": keyid, "type": keytype.value, "isConnected": isconnect, "zone":zone.value, "battWarnSts":battwarbsts}]})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def check_central_lock_sts_info(self, lock_sts:LockStatus, trigger_srcid:TriggerSourceId, timeout=1):
        prompt_info = f"----------> 通过SOA Partner CentralLockService_client::NotifyCentralLockSysInfo校验中控锁为{lock_sts.name}, 中控锁触发原因为{trigger_srcid.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            info1 = {"sts": lock_sts.value, "triggerId": trigger_srcid.value, "updateEve": True}
            self.ck_s2s_event("CentralLockService_client", "NotifyCentralLockSysInfo", {"info": info1}, timeout)
            
    def check_no_GetSeatHeatVentStatus_req(self, timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出SeatService:GetSeatHeatVentStatus请求"):
            self.ck_no_req("SeatService_server", "GetSeatHeatVentStatus", timeout=timeout)

    def check_Remote_Climate_Status(self, status: RemClimateSts):
        prompt_info = f"----------> 通过SOA ClimateControlService_client:RemotePowerStatus请求的响应,响应的关键参数远程空调状态为:{status.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("ClimateControlService_client", "RemotePowerStatus", {"status": status.value})

    def check_lock_status(self, lock_sts: LockSts):
        with allure.step(f"通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus为{lock_sts.value}"):
            logger.info(f"通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus为{lock_sts.value}")
            self.ck_s2s_event("CentralLockService_client", "LockStatus",
                                               {"sts": lock_sts.value})

    def check_SetMaxCoolingCtrl_req(self, onOffCmd: bool = True, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出极速制冷开启请求:ClimateControlService:SetMaxCoolingCtrl"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":onOffCmd}}, timeout=timeout)

    def check_SetMaxHeatingCtrl_req(self, onOffCmd: bool = True, timeout: Union[float, int] = 0.5):
        prompt_info = f"----------> 通过SOA Partner监听TCAM是否发出极速制热开启请求:ClimateControlService:SetMaxHeatingCtrl"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_req("ClimateControlService_server", "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":onOffCmd}}, timeout=timeout)

    def notify_MaxCoolingHeatingInfo(self, maxCoolingSts: bool = True, maxHeatingSts: bool = True):
        prompt_info = f"---------->通过SOA Partner发送ClimateControlService:MaxCoolingHeatingInfo 制冷状态为{maxCoolingSts}制热状态为{maxHeatingSts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",
                                     {"info": {"maxCoolingSts":maxCoolingSts, "maxHeatingSts":maxHeatingSts}})

    def get_internal_light_mode(self, mode: LightMode):
        prompt_info = f"===============>获取内灯模式为: {mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp(
                partner_key="LightService_client",
                method_name="GetInternalLightMode",
                args={"out": mode.value},
                ck_info={"out": mode.value}
            )

    def set_Max_Cooling_Ctrl(self, onOffCmd: bool = True):
        prompt_info = f"----------> 调用接口 ClimateControlService_client  设置急速制冷为{onOffCmd}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":onOffCmd}})

    def set_Max_Heating_Ctrl(self, onOffCmd: bool = True):
        prompt_info = f"----------> 调用接口 ClimateControlService_client  设置急速制热为{onOffCmd}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("ClimateControlService_client", "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":onOffCmd}})

    def check_max_cooling_heating_info(self, maxCoolingSts: bool = True, maxHeatingSts: bool = True):
        prompt_info = f"---------->通过SOA Partner Check ClimateControlService:MaxCoolingHeatingInfo 制冷状态为{maxCoolingSts}制热状态为{maxHeatingSts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.chk_notify("ClimateControlService_client", "MaxCoolingHeatingInfo",
                                     {"info": {"maxCoolingSts":maxCoolingSts, "maxHeatingSts":maxHeatingSts}})

    def set_child_lock_unlock_req(self, doorid: DoorId, childlockreq: ChildLockReq, time_wait: Union[float, int] = 0):
        if childlockreq.name == "Lock":
            with allure.step(f'通过SoaPartner设置当前{doorid.name}侧门请求儿童锁：{childlockreq.name}'):
                logger.info(f'通过SoaPartner设置当前{doorid.name}侧门请求儿童锁：{childlockreq.name}') 
                self.send_method_request("DoorService_client", "LockChildLock", {"doors": [doorid.value]})
                
        elif childlockreq.name == "UnLock":
            with allure.step(f'通过SoaPartner设置当前{doorid.name}侧门请求儿童锁：{childlockreq.name}'):
                logger.info(f'通过SoaPartner设置当前{doorid.name}侧门请求儿童锁：{childlockreq.name}')
                self.send_method_request("DoorService_client", "UnLockChildLock", {"doors": [doorid.value]})
            
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def event_check_side_door_open_protection_sts(self, frontleft: Union[bool, int] = None,
                                                  frontrigiht: Union[bool, int] = None,
                                                  rearleft: Union[bool, int] = None,
                                                  rearright: Union[bool, int] = None,
                                                  time_wait: Union[float, int] = 0):
        prompt_info = f"----------> DoorService_client: SideDoorOpenProtectionSts 校验侧方开门保护状态是否激活"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("DoorService_client", "SideDoorOpenProtectionSts", {"openProtectionSts":
                                                   {"isActiveFL ":frontleft, "isActiveFR" :frontrigiht, "isActiveRL" :rearleft, "isActiveRR" :rearright}})   
            
            
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def set_light_show_file(self, sequence_id,act:SequenceAction):
        self.send_method_request("LightService_client", "SequenceControl", {"seqId": sequence_id, "act": act.value})
        
    def check_Light_ShowActivate_Status(self, status: bool ):
        prompt_info = f"---------->BGM重启检测BGM发送灯光秀激活/禁用事件 "
        with allure.step("通过SOA Partner发送HighVoltageService_client:GetDisplayBookChargingInfo请求"):
            logger.info(prompt_info) 
            self.ck_s2s_event("LightService_client", "LightShowActivateStatus",{"status":status})

    def check_GetSpeed_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出ChassisService:GetSpeed请求。
        
        Args:
            timeout (int, optional): 监听超时时间，默认为1秒。
        
        Returns:
            None
        
        """
        with allure.step(f"通过SOA Partner监听TCAM是否发出ChassisService:GetSpeed"):
            logger.info(f"通过SOA Partner监听TCAM是否发出ChassisService:GetSpeed")
            self.ck_s2s_req("ChassisService_server", "GetSpeed", timeout=timeout)

    def response_to_GetSpeed_req(self, speed: float = 0, is_valid: bool = True):
        """
        通过SOA Partner响应ChassisService:GetSpeed请求
        
        Args:
            speed (float, optional): 速度值. 默认为0.
            is_valid (bool, optional): 是否有效. 默认为True.
        
        Returns:
            None
        """
        with allure.step(f"通过SOA Partner响应ChassisService:GetSpeed请求"):
            logger.info(f"通过SOA Partner响应ChassisService:GetSpeed请求")
            self.soa_partner.send_method_response("ChassisService_server", "GetSpeed",
                                                  {"speed": speed, "isvalid": is_valid})

    def check_GetSpeed_req_and_feedback_resp(self, speed: float = 0, is_valid: bool = True, timeout: Union[float, int] = 0.5):
        """
        Args:
            speed (float, optional): 返回的速度值. Defaults to 0.
            is_valid (bool, optional): 是否为有效速度值. Defaults to True.
            timeout (Union[float, int], optional): 超时时间. Defaults to 0.5.
        
        Returns:
            None
        
        Raises:
            无
        
        功能：
            发送ChassisService:GetSpeed请求并回复对应的响应
        
        调用方式：
            self.check_GetSpeed_req_and_feedback_resp(speed, is_valid, timeout)
        
        详细描述：
            该方法主要用于发送获取速度值的请求并返回相应的响应，参数包括速度值、是否为有效速度值以及超时时间。
            方法首先通过logger输出日志信息，然后调用check_GetSpeed_req方法发送请求，
            接着调用response_to_GetSpeed_req方法返回对应的响应。
        
        """
        prompt_info = f"---------->获取ChassisService:GetSpeed请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_GetSpeed_req(timeout)
            self.response_to_GetSpeed_req(speed=speed, is_valid=is_valid)

    def notify_NotifyChargingEquipmentInformation(self, max_current: float = 3.8, actual_current: float = 4.0,
                                                  equipment_types: list = [3], charge_power: float = 300.0):
        """
        通过SOA Partner发送HighVoltageService:NotifyChargingEquipmentInformation事件通知
        
        Args:
            max_current (float, optional): 最大电流值，默认为3.8A。
            actual_current (float, optional): 实际电流值，默认为4.0A。
            equipment_types (list, optional): 充电设备类型列表，默认为[3]。
            charge_power (float, optional): 充电功率，默认为300.0W。
        
        Returns:
            None
        
        """
        with allure.step(f"通过SOA Partner发送HighVoltageService:NotifyChargingEquipmentInformation事件通知"):
            logger.info(f"通过SOA Partner发送HighVoltageService:NotifyChargingEquipmentInformation事件通知")
            self.soa_partner.send_event_notify("HighVoltageService_server", "NotifyChargingEquipmentInformation",
                                               {"info": {"maxCurrent": max_current, "actualCurrent": actual_current,
                                                "equipmentTypes": equipment_types, "chargePowerInput": charge_power}})

    def check_RemoteBatteryHeatingInfo(self, modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                              heatsts: RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOff,
                                              source: HeatingEnergySource = HeatingEnergySource.kNone, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知
        
        Args:
            modests (RemoteBatteryHeatingModeSts, optional): 电池加热模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat
            heatsts (RemoteBatteryHeatingSts, optional): 电池加热状态，默认为RemoteBatteryHeatingSts.kOff
            source (HeatingEnergySource, optional): 加热能量来源，默认为HeatingEnergySource.kNone
            timeout (Union[float, int], optional): 超时时间，默认为0.5
        
        Returns:
            None
        
        """
        with allure.step(f"通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知"):
            logger.info(f"通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知")
            self.chk_notify("RemoteCtrlService_client", "RemoteBatteryHeatingInfo",
                                               {"heatInfo": {"modeSts": modests.value, "heatSts": heatsts.value, "source": source.value}}, timeout=timeout)

    def battery_protect_exect_planb(self, value: float = -28.0, source: HeatingEnergySource = HeatingEnergySource.kHVBattery,
                                          modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                          heatsts: RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOn):
        """
        执行电池保护计划B
        
        Args:
            value (float, optional): 电池温度值，默认为-28.0.
            source (HeatingEnergySource, optional): 加热能量来源，默认为HeatingEnergySource.kHVBattery.
            modests (RemoteBatteryHeatingModeSts, optional): 电池加热模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat.
            heatsts (RemoteBatteryHeatingSts, optional): 电池加热状态，默认为RemoteBatteryHeatingSts.kOn.
        
        Returns:
            None
        
        """
        self.soa_partner.empty_all()
        self.check_SetOutput_req(timeout=2)
        time.sleep(0.5)
        self.notify_hvActiveSts()
        self.soa_partner.empty_all()
        self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=value, timeout=3)
        time.sleep(4.9)
        self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa_partner.empty_all()
        self.check_RemoteBatteryHeatingInfo(modests=modests, heatsts=heatsts, source=HeatingEnergySource.kHVBattery, timeout=3)
        self.check_high_voltage_setoutput_request(check_time=10)

    def check_no_SetCharging_req(self, timeout: Union[float, int]):
        """
        监听TCAM不会发出HighVoltageService_server:SetCharging请求
        
        Args:
            timeout (Union[float, int]): 监听超时时间
        
        Returns:
            None
        
        """
        with allure.step("通过SOA Partner监听TCAM不会发出HighVoltageService_server:SetCharging请求"):
            logger.info("通过SOA Partner监听TCAM不会发出HighVoltageService_server:SetCharging请求")
            self.ck_no_req("HighVoltageService_server", "SetCharging", timeout=timeout)

    def check_no_RemoteBatteryHeatingInfo(self, timeout: Union[float, int] = 0.5):
        """
        检查TCAM是否未发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知。
        
        Args:
            timeout (Union[float, int], optional): 超时时间，默认为0.5秒。
        
        Returns:
            None
        
        """
        with allure.step(f"通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知"):
            logger.info(f"通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知")
            self.ck_no_event("RemoteCtrlService_client", "RemoteBatteryHeatingInfo", timeout=timeout)

    def battery_protect_exect_plana(self, min_temp: float = -31.0, acdc_type: ACDCType = ACDCType.kDC,
                                          plug_sts1: PluggerSts = PluggerSts.Disconnected,
                                          plug_sts2: PluggerSts = PluggerSts.ConnectedWithPower,
                                          value: float = -28.0, thermal_sts: ThermalReqSts = ThermalReqSts.Heating,
                                          modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat):
        """
        电池保护执行Plan A方案
        
        Args:
            min_temp (float, optional): 电池最低温度，默认为-31.0.
            acdc_type (ACDCType, optional): ACDC类型，默认为ACDCType.kDC.
            plug_sts1 (PluggerSts, optional): 插头状态1，默认为PluggerSts.Disconnected.
            plug_sts2 (PluggerSts, optional): 插头状态2，默认为PluggerSts.ConnectedWithPower.
            value (float, optional): 目标加热温度值，默认为-28.0.
            thermal_sts (ThermalReqSts, optional): 热请求状态，默认为ThermalReqSts.Heating.
            modests (RemoteBatteryHeatingModeSts, optional): 远程加热请求模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat.
        Returns:
            None
        
        """
        self.notify_BatteryTemperatureInfo(min_temp=min_temp)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=acdc_type, plug_sts=plug_sts1)
        self.notify_NotifyChargingEquipmentInformation()
        self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value= value, timeout=3)
        if acdc_type==ACDCType.kDC:
            self.check_SetCharging_req(req=True, timeout=3)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=acdc_type, plug_sts=plug_sts2)
        if plug_sts2==PluggerSts.ConnectedWithPower:
            self.notify_BatteryHeatingInfo(req_sts=thermal_sts)
            if thermal_sts == ThermalReqSts.Heating:
                self.check_RemoteBatteryHeatingInfo(modests=modests,
                                                    heatsts=RemoteBatteryHeatingSts.kOn,
                                                    source=HeatingEnergySource.kCharger, timeout=3)
                logger.info("开始Plan A加热方案，采取充电桩取电，7) case 2")
            else:
                time.sleep(39.9)
                self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
                time.sleep(2)
                logger.info("开始Plan B加热方案，采取动力电池取电，7 case 1")

        else:
            time.sleep(9.9)
            self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
            time.sleep(2)
            logger.info("开始Plan B加热方案，采取动力电池取电，6 case 1")

            
            
    def notify_ThermalSystemDeviceFaultInfo(self, device: DeviceType=DeviceType.kAll, faultSts:ThermalFaultSts=ThermalFaultSts.kNormal):
        with allure.step(f"通过SOA Partner发出HighVoltageService:ThermalSystemDeviceFaultInfo事件通知"):
            logger.info(f"通过SOA Partner监听TCAM是否发出HighVoltageService:ThermalSystemDeviceFaultInfo事件通知")
            self.soa_partner.send_event_notify("HighVoltageService_server", "ThermalSystemDeviceFaultInfo",
                                               {"infos": {"device": device.value, "faultSts": faultSts.value}})
            
            
    def check_NotifyRemoteBatteryHeatingInfo_event(self,modeSts:RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kIdle ,heatSts:RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOff ,
                                                   source:HeatingEnergySource = HeatingEnergySource.kNone ,timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:RemoteBatteryHeatingInfo事件"):
            logger.info("通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:RemoteBatteryHeatingInfo事件")
            self.chk_notify("RemoteCtrlService_client", "RemoteBatteryHeatingInfo", {'heatInfo':{"modeSts": modeSts.value,"heatSts":heatSts.value,"source":source.value}},
                            timeout=timeout)
            
    def check_NotifyACDefrostSts(self, defrost_max: bool = False, climate_defrost: bool = False):
        prompt_info = f"----------> check除霜状态事件通知:ClimateControlService:NotifyACDefrostSts defrostMax: {defrost_max}, \
            climateDefrost: {climate_defrost}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("ClimateControlService_client", "NotifyACDefrostSts",
                                   {"sts": {"defrostMax": defrost_max,
                                            "climateDefrost": climate_defrost}})


    def battery_protect_exect_planB_by_stage_wait_HVActiveSts(self, min_temp: float = -31.0):
        """
        根据阶段等待HVActiveSts执行低温自保护PlanB方案
        
        Args:
            min_temp (float, optional): 最低温度阈值. 默认为-31.0.
        
        Returns:
            None
        
        """
        wait_time=self.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.check_NotifyTimeUpEventInfo_event(service_name="low_temp_protect", timeout=wait_time+3)
        time.sleep(9.9)
        self.notify_BatteryTemperatureInfo(min_temp=min_temp)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa_partner.empty_all()
        self.check_SetOutput_req(timeout=2)

    def battery_protect_exect_planB_by_stage_wait_ThermalReqSts(self, min_temp: float = -31.0, value: float = -28.0):
        """
        按照阶段等待ThermalReqSts执行低温保护方案B
        
        Args:
            min_temp (float, optional): 最低温度阈值，默认为-31.0摄氏度.
            value (float, optional): 加热请求值，默认为-28.0摄氏度.
        
        Returns:
            None
        
        """
        wait_time=self.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.check_NotifyTimeUpEventInfo_event(service_name="low_temp_protect", timeout=wait_time+3)
        time.sleep(9.9)
        self.notify_BatteryTemperatureInfo(min_temp=min_temp)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa_partner.empty_all()
        self.check_SetOutput_req(timeout=2)
        time.sleep(0.5)
        self.notify_hvActiveSts()
        self.soa_partner.empty_all()
        self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=value, timeout=3)

    def check_battery_protect_planB_stoped_with_HVActiveSts_closed(self):
        """
        检查电池保护方案B是否已停止且高压系统已关闭。
        
        Args:
            无。
        
        Returns:
            无返回值，若执行过程中出现问题则会抛出异常。
        
        Raises:
            异常类型未定义，可能会根据实际执行情况抛出不同的异常。
        
        """
        self.notify_hvActiveSts()
        self.soa_partner.empty_all()
        self.check_no_SetBatteryHeating_req(timeout=5)
        self.check_no_SetOutput_req(timeout=6)

    def check_battery_protect_planB_stoped_with_ThermalReqSts_heating(self):
        """
        检查电池保护方案B是否因ThermalReqSts.Heating停止
        
        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        
        该函数会执行以下操作：
        1. 调用 notify_BatteryHeatingInfo 函数，发送 ThermalReqSts.Heating 的请求状态。
        2. 调用 soa_partner 的 empty_all 函数，清空 soa_partner 中的数据。
        3. 调用 check_no_RemoteBatteryHeatingInfo 函数，检查在指定超时时间内是否没有收到 RemoteBatteryHeatingInfo 消息。
        4. 调用 check_no_SetOutput_req 函数，检查在指定超时时间内是否没有收到 SetOutput_req 消息。
        """
        self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa_partner.empty_all()
        self.check_no_RemoteBatteryHeatingInfo(timeout=3)
        self.soa_partner.empty_all()
        self.check_no_SetOutput_req(timeout=6)

    def battery_protect_exect_planA_DC_by_stage_SetCharging(self, min_temp: float = -31.0, value: float = -28.0):
        """
        执行PlanA DC充电阶段下的电池保护策略，设置充电信息
        
        Args:
            min_temp (float, optional): 最小温度值，默认为-31.0。
            value (float, optional): 加热请求值，默认为-28.0。
        
        Returns:
            None
        
        """
        wait_time=self.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.check_NotifyTimeUpEventInfo_event(service_name="low_temp_protect", timeout=wait_time+3)
        time.sleep(9.9)
        self.notify_BatteryTemperatureInfo(min_temp=min_temp)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.notify_NotifyChargingEquipmentInformation()
        self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=value, timeout=3)

    def battery_protect_exect_planA_by_stage_wait_pluggerStatus(self, min_temp: float = -31.0, value: float = -28.0 , 
                                                                      acdc_type: ACDCType = ACDCType.kDC):
        """
        执行低温保护方案A根据阶段等待充电枪状态
        
        Args:
            min_temp (float, optional): 最低温度阈值，默认为-31.0.
            value (float, optional): 加热请求值，默认为-28.0.
            acdc_type (ACDCType, optional): 电源类型，默认为ACDCType.kDC.
        
        Returns:
            None
        
        """
        wait_time=self.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.check_NotifyTimeUpEventInfo_event(service_name="low_temp_protect", timeout=wait_time+3)
        time.sleep(9.9)
        self.notify_BatteryTemperatureInfo(min_temp=min_temp)
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                 acdc_type=acdc_type, plug_sts=PluggerSts.Disconnected)
        self.notify_NotifyChargingEquipmentInformation()
        self.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=value, timeout=3)
        if acdc_type==ACDCType.kDC:
            self.check_SetCharging_req(req=True, timeout=3)

    def check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating(self, acdc_type: ACDCType = ACDCType.kDC):
        """
        检查执行方案A时加热停止
        
        Args:
            acdc_type (ACDCType, optional): 电源类型，默认为ACDCType.kDC，表示直流电源。
        
        Returns:
            None
        
        """
        self.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                 acdc_type=acdc_type, plug_sts=PluggerSts.ConnectedWithPower)
        self.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa_partner.empty_all()
        self.check_no_RemoteBatteryHeatingInfo(timeout=3)

    def check_NotifyPrepareTimeUpEventInfo_event(self, service_name: str = "rvcsubscribe", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出RtcAlarmService_client:NotifyPrepareTimeUpEventInfo事件
        
        Args:
            service_name (str, optional): 服务名称，默认为"rvcsubscribe"。
            timeout (Union[float, int], optional): 超时时间，默认为1秒。
        
        Returns:
            None
        
        """
        with allure.step("通过SOA Partner监听TCAM是否发出 RtcAlarmService_client:NotifyPrepareTimeUpEventInfo事件"):
            logger.info("通过SOA Partner监听TCAM是否发出 RtcAlarmService_client:NotifyPrepareTimeUpEventInfo事件")
            self.chk_notify("RtcAlarmService_client", "NotifyPrepareTimeUpEventInfo", {'bookEvent':{"serviceName": service_name}}, timeout=timeout)

    def check_NotifyTimeUpEventInfo_event(self, service_name: str = "rvcsubscribe", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出RtcAlarmService_client:NotifyTimeUpEventInfo事件
        
        Args:
            service_name (str, optional): 服务名称，默认为"rvcsubscribe"。
            timeout (Union[float, int], optional): 超时时间，单位为秒，支持浮点数和整数，默认为1。
        
        Returns:
            None
        
        """
        with allure.step("通过SOA Partner监听TCAM是否发出 RtcAlarmService_client:NotifyTimeUpEventInfo事件"):
            logger.info("通过SOA Partner监听TCAM是否发出 RtcAlarmService_client:NotifyTimeUpEventInfo事件")
            self.chk_notify("RtcAlarmService_client", "NotifyTimeUpEventInfo", {'bookEvent':{"serviceName": service_name}}, timeout=timeout)

    def get_and_check_door_action_req(self, checktype: CheckInterfaceType, doorid: DoorId, dooraction:DoorAction, triggerId:DoorActionTriggerId, time_wait: Union[float, int] = 0):
        with allure.step(f"通过SoaPartner校验{doorid.name}车门动作请求为{dooraction.name}, 车门动作请求源为{triggerId.name}"):
            logger.info(f"通过SoaPartner校验{doorid.name}车门动作请求为{dooraction.name}, 车门动作请求源为{triggerId.name}")
            if checktype.name == "Get":
                with allure.step(f'通过SOAPartner获取当前{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}'):
                    logger.info(f'通过SOAPartner获取当前{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}')
                self.send_request_and_return_respt("DoorService_client", "GetDoorActionRequest", {"doors": [doorid.value]}, 
                                                   {"out": [{"id": doorid.value, "action": dooraction.value, "triggerId": triggerId.value}]}, timeout= time_wait)
            elif checktype.name == "CheckNotify":
                with allure.step(f'通过SOAPartner校验当前通知{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}'):
                    logger.info(f'通过SOAPartner校验当前通知{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}')
                self.ck_s2s_event("DoorService_client", "DoorActionRequest",{"pos": [{"id": doorid.value, "action":  dooraction.value, "triggerId": triggerId.value}]}, timeout= time_wait)
                
            elif checktype.name == "All":
                with allure.step(f'通过SOAPartner校验通知和获取当前{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}'):
                    logger.info(f'通过SOAPartner校验通知和获取当前{doorid.name}车门动作请求为:{dooraction.name}, 车门动作触发源为:{triggerId.name}')
                self.ck_s2s_event("DoorService_client", "DoorActionRequest",{"pos": [{"id": doorid.value, "action":  dooraction.value, "triggerId": triggerId.value}]}, timeout= time_wait)
                self.send_request_and_return_respt("DoorService_client", "GetDoorActionRequest", {"doors": [doorid.value]}, 
                                                   {"out": [{"id": doorid.value, "action": dooraction.value, "triggerId": triggerId.value}]}, timeout= time_wait)

            else:
                logger.info(f"The request type is not supported")
                assert False                
                
            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)

    def ctrl_mul_alm_illuminate(self, bright, r, g, b, zoneid_lst: List[ALMZoneId]):
        for zoneid in zoneid_lst:
            with allure.step(f"控制{zoneid.name}亮度{bright}_r:{r}_g:{g}_b:{b}"):
                self.send_method_request(
                    partner_key="LightService_client",
                    method_name="LightShowControlWithLightDevice",
                    args={
                        "lights": [
                            {
                                "light": {"type": 35, "zoneId": zoneid.value},
                                "PixelData": [0],
                                "type": 0,
                                "color": [
                                    {"brightness": bright,
                                     "color":
                                         {"cRed": r, "cGreen": g, "cBlue": b}
                                     }
                                ]
                            }
                        ]
                    }
                )
                sleep(0.5)
    
    def get_and_check_Pressure(self,tyres: tyres=tyres.kTyreFrintLeft, pressure: float=200):
        with allure.step(f"请求位置{tyres.name}的胎压, 上报的胎压值为{pressure}"):
            logger.info(f"请求位置{tyres.name}的胎压, 上报的胎压值为{pressure}")
            self.send_request_and_ck_resp("TyreService_client", "GetPressure", {"tyres": tyres.value},{"out": [{"id": tyres.value, "pressure": pressure}]})

    def get_and_check_Temperature(self,tyres: tyres=tyres.kTyreFrintLeft, temperature: int=64):
        with allure.step(f"请求位置{tyres.name}的胎压, 上报的胎温值为{temperature}"):
            logger.info(f"请求位置{tyres.name}的胎压, 上报的胎温值为{temperature}")
            self.send_request_and_ck_resp("TyreService_client", "GetTemperature", {"tyres": tyres.value},{"out": [{"id": tyres.value, "temperature": temperature}]})

    def get_and_set_outerdoorswlight_mode(self,target_doorid:DoorId,target_mode:OutDoorSwitchLightMode,target_sts:isOn):
        promt_info = f"----------------> 通过SOA Partner发出 DoorService_client:GetOutDoorSwitchLightSts,获取当前的门板指示灯模式是否{target_doorid.name}门为{target_mode.name},如果不一致会自动重设"
        with allure.step(promt_info):
            logger.info(promt_info)
            current_lists = self.send_request_and_return_resp("DoorService_client", "GetOutDoorSwitchLightSts", {"doors": [4]})[
                    "out"]  # 获取当前的门板指示灯模式
            print("当前模式：",current_lists)
            if any(current_list["sts"] != target_mode.value for current_list in current_lists):
                logger.info("\033[0;35;40m当前门板指示灯模式不等设置值,开始切换模式\033[0m")
                self.send_method_request("DoorService_client", "SetOutDoorSwitchLightMode", {"doors":target_doorid.value, "mode": target_mode.value})
                sleep(0.5)
                logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
                self.send_request_and_ck_resp("DoorService_client", "GetOutDoorSwitchLightSts", {"doors": [4]},
                                                          {"out":[{"id":0, "sts": target_sts.value}, 
                                                                  {"id": 1, "sts": target_sts.value}, 
                                                                  {"id": 2, "sts": target_sts.value}, 
                                                                  {"id": 3, "sts": target_sts.value}]})  
                logger.info("\033[0;35;40m主动获取到预期门板指示灯模式\033[0m")
            else:
                logger.info("\033[0;35;40m当前门板指示灯模式等于设置值,重新设置当前模式\033[0m")
                self.send_method_request("DoorService_client", "SetOutDoorSwitchLightMode",
                                            {"doors":target_doorid.value, "mode": target_mode.value})  # 设置门板指示灯mode0-OFF/mode1-OnStatic/mode2-OnDynamic
                logger.info("\033[0;35;40m门板指示灯模式设置成功无通知等待300ms获取当前模式\033[0m")
                sleep(0.5)
                self.send_request_and_ck_resp("DoorService_client", "GetOutDoorSwitchLightSts", {"doors": [4]},
                                                          {"out":[{"id":0, "sts": target_sts.value}, 
                                                                  {"id": 1, "sts": target_sts.value}, 
                                                                  {"id": 2, "sts": target_sts.value}, 
                                                                  {"id": 3, "sts": target_sts.value}]})    # 获取门板指示灯状态sts0-OFF/sts1-On/sts2-Error/sts3-Reserved
                logger.info("\033[0;35;40m主动获取到预期门板指示灯模式\033[0m")

    def check_SetDischargeLimitSoc_req(self, soc: float = 20.0, timeout: Union[float, int] = 0.5):
        with allure.step("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetDischargeLimitSoc"):
            logger.info("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetDischargeLimitSoc")
            self.ck_s2s_req("HighVoltageService_server", "SetDischargeLimitSoc", ck_info= {"soc":soc}, timeout=timeout)

    def response_to_SetDischargeLimitSoc_req(self):
        prompt_info = f"----------> 通过SOA Partner发送设置充电SOC请求HighVoltageService:SetDischargeLimitSoc"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageService_server", "SetDischargeLimitSoc", args=None)

    def check_SetDischargeLimitSoc_req_and_feedback_resp(self, soc: float = 20.0, timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetDischargeLimitSoc, 并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetDischargeLimitSoc_req(soc=soc, timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_SetDischargeLimitSoc_req()

    def notify_DischargingInfo(self, dischargingState: DisChargingState = DisChargingState.Default,
                            isConnect: bool = False,
                            isTempHigh: bool = False,
                            dischargeLimitSoc:float = 255,
                            dischargePower: int = -1,
                            dischargeEnergyThisTime: int = -1,
                            recentDischargeStartTime:int = 0,
                            recentDischargeEndTime : int = 0,
                            isDischargingPreparin:bool = False,
                            isDischarging:bool = False):
        """
        通过SOA Partner发送HighVoltageService:DischargingInfo事件通知
        
        Args:
            dischargingState (DisChargingState, optional): 	放电状态. 默认为DisChargingState.Default
            isConnect (bool, optional): 是否连接放电枪. 默认为False.
            isTempHigh (bool, optional): 放电口温度过高提示. 默认为False
            dischargeLimitSoc (float, optional): 放电限值SOC. 范围SOC：20~100，精度0.1，默认255，表示百分比
            dischargePower (float, optional): 放电输出功率. 默认为-1.
            dischargeEnergyThisTime (BookChargeSts, optional):  本次放电电量*/. 默认为BookChargeSts.Default.
            recentDischargeStartTime (int, optional): 放电开始时间. 默认为0.
            recentDischargeEndTime (int, optional): 放电结束时间. 默认为0.
            isDischargingPreparin (bool, optional):  放电准备中. 默认为false.
            isDischarging (bool, optional): 放电中. 默认为false

        Returns:
            None
        
        """
        with allure.step("通过SOA Partner发送HighVoltageService:DischargingInfo事件通知"):
            self.soa_partner.send_event_notify("HighVoltageService_server", "DischargingInfo",
                                               {"info": {
                                                   'dischargingState':dischargingState.value,
                                                   'isConnect':isConnect,
                                                   'isTempHigh':isTempHigh,
                                                   'dischargeLimitSoc':dischargeLimitSoc,
                                                   'dischargePower':dischargePower,
                                                   'dischargeEnergyThisTime':dischargeEnergyThisTime,
                                                   'recentDischargeStartTime':recentDischargeStartTime,
                                                   'recentDischargeEndTime':recentDischargeEndTime,
                                                   'isDischargingPreparin':isDischargingPreparin,
                                                   'isDischarging':isDischarging
                                               }})
            

    def check_SetDischargingControl_req(self, cmdtype: CommandType = CommandType.kDefault ,sid:DischargeSourceId = DischargeSourceId.kRemoteControl, timeout: Union[float, int] = 0.5):
        with allure.step("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageAppService:SetDischargingControl"):
            logger.info("通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageAppService:SetDischargingControl")
            self.ck_s2s_req("HighVoltageAppService_server", "SetDischargingControl", ck_info={'cmd':{'type': cmdtype.value, 'source':sid.value}},timeout=timeout)

    def response_to_SetDischargingControl_req(self):
        prompt_info = f"----------> 通过SOA Partner发送设置充电SOC请求HighVoltageAppService:SetDischargingControl"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageAppService_server", "SetDischargingControl", args=None)

    def check_SetDischargingControl_req_and_feedback_resp(self,cmdtype: CommandType = CommandType.kDefault ,sid:DischargeSourceId = DischargeSourceId.kRemoteControl, timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageAppService:SetDischargingControl, 并返回响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetDischargingControl_req(cmdtype=cmdtype, sid=sid,timeout=timeout)  # 监听TCAM发送充电口盖请求
            self.response_to_SetDischargingControl_req()


    def response_to_GetBookChargingInfo_req(self,source: HV_SourceId,reqSts: ACBookChargingReqSts,workSts: ACBookChargingWorkSts,
                                            startTime: int,endTime: int,repeatType: CoolgReq,isToTargetSOCStop: bool):
        prompt_info = f"----------> 通过SOA Partner发送HighVoltageAppService_client:GetBookChargingInfo请求"
        logger.info(prompt_info) 
        with allure.step("通过SOA Partner发送HighVoltageService_client:GetBookChargingInfo请求"):   
            self.send_request_and_ck_resp("HighVoltageAppService_client", "GetBookChargingInfo", {},
                                                  {"out":{"acInfo":{"source":source.value,"reqSts":reqSts.value,"workSts":workSts.value,
                                                                    "info":{"startTime":startTime,"endTime":endTime,"repeatType":repeatType.value},
                                                                    "isToTargetSOCStop":isToTargetSOCStop}}}) 

    def event_to_BookChargingInfo(self,source: HV_SourceId,reqSts: ACBookChargingReqSts,workSts: ACBookChargingWorkSts,
                                            startTime: int,endTime: int,repeatType: CoolgReq,isToTargetSOCStop: bool):
        prompt_info = f"----------> 检测SOA Partner发送HighVoltageAppService_client:BookChargingInfo请求"
        logger.info(prompt_info) 
        with allure.step("检测SOA Partner发送HighVoltageService_client:BookChargingInfo请求"):   
            self.ck_s2s_event("HighVoltageAppService_client", "BookChargingInfo", 
                                                  {"info":{"acInfo":{"source":source.value,"reqSts":reqSts.value,"workSts":workSts.value,
                                                                    "info":{"startTime":startTime,"endTime":endTime,"repeatType":repeatType.value},
                                                                    "isToTargetSOCStop":isToTargetSOCStop}}})
    def response_to_GetDisplayBookChargingInfo_req(self,type: DisplayBookChargingType,startTime ,endTime ):
        prompt_info = f"----------> 通过SOA Partner发送HighVoltageAppService_client:GetDisplayBookChargingInfo请求"
        logger.info(prompt_info) 
        logger.info(f"type is:{type},startTime is:{startTime}, endTime is:{endTime}") 

        with allure.step("通过SOA Partner发送HighVoltageService_client:GetDisplayBookChargingInfo请求"):    
            self.send_request_and_ck_resp("HighVoltageAppService_client", "GetDisplayBookChargingInfo", {},
                                                  {"out":{"type":type.value,
                                                          "startTime":{"kYear":startTime[0],"kMonth":startTime[1],"kDay":startTime[2],"kHour":startTime[3],"kMinute":startTime[4],"kSecond":startTime[5]},
                                                          "endTime":{"kYear":endTime[0],"kMonth":endTime[1],"kDay":endTime[2],"kHour":endTime[3],"kMinute":endTime[4],"kSecond":endTime[5]}}})

    def check_Light_ShowActivate_Status(self, status: bool ):
        prompt_info = f"---------->BGM重启检测BGM发送灯光秀激活/禁用事件 "
        logger.info(prompt_info) 
        with allure.step("检测BGM发送LightService_client:LightShowActivateStatus请求"):
            self.ck_s2s_event("LightService_client", "LightShowActivateStatus",{"status":status})

    def set_SetACBookCharging_req(self, type: CommandType,source: HV_SourceId,startTime,endTime,repeatType: CoolgReq,isToTargetSOCStop: bool):
        with allure.step("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求"):
            logger.info("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求")
            self.send_method_request("HighVoltageAppService_client", "SetACBookCharging", {"cmd":{"type":type.value,"source":source.value,
                                                                                                  "timeInfo":{"startTime":startTime,"endTime":endTime,"repeatType":repeatType.value},
                                                                                                  "isToTargetSOCStop":isToTargetSOCStop}})

    def response_to_GetBookChargingTime_req(self, type: DisplayBookChargingType,type1: HV_SourceId,startTime,endTime):
        with allure.step("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求"):         
            self.send_request_and_ck_resp("HighVoltageService_client", "GetBookChargingTime", {"type": type.value},
                                                 {"out":{'type': type1.value,"startTime":{"kYear":startTime[0],"kMonth":startTime[1],"kDay":startTime[2],"kHour":startTime[3],"kMinute":startTime[4],"kSecond":startTime[5]},
                                                          "endTime":{"kYear":endTime[0],"kMonth":endTime[1],"kDay":endTime[2],"kHour":endTime[3],"kMinute":endTime[4],"kSecond":endTime[5]}}})

    def check_BookChargingTime(self, type: DisplayBookChargingType,startTime,endTime):
        with allure.step("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求"):         
            self.ck_s2s_event("HighVoltageService_client", "BookChargingTime", {"info":{"type":type.value,
                                                          "startTime":{"kYear":startTime[0],"kMonth":startTime[1],"kDay":startTime[2],"kHour":startTime[3],"kMinute":startTime[4],"kSecond":startTime[5]},
                                                          "endTime":{"kYear":endTime[0],"kMonth":endTime[1],"kDay":endTime[2],"kHour":endTime[3],"kMinute":endTime[4],"kSecond":endTime[5]}}})

    def set_usagemode_withoutkey(self, mode:TargetUsageMode, time_wait: Union[float, int] = 0):
        prompt_info = f"----------> SOAPartner 通过VehicleModeService_client: SideDoorOpenProtectionSts接口设置无钥匙进入激活状态为{mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("VehicleModeService_client", "SetUsageModeWithoutKey", {"mode": mode.value})

            logger.info(f"--------->等待{time_wait}")
            sleep(time_wait)
            
    def set_light_show_file(self, sequence_id,act:SequenceAction):
        with allure.step("通过SOA Partner发送LightService_client:SequenceControl请求"):
            logger.info("通过SOA Partner发送LightService_client:SequenceControl请求")
            self.send_method_request("LightService_client", "SequenceControl", {"seqId": sequence_id, "act": act.value})

    def set_SetCharging_req(self, req: bool):
        with allure.step("通过SOA Partner发送HighVoltageService_client:SetCharging请求"):
            logger.info("通过SOA Partner发送HighVoltageService_client:SetCharging请求")
            self.send_method_request("HighVoltageService_client", "SetCharging", {"on": req})

    def set_SetChargingControl_req(self, type: CommandType,source: HV_SourceId):
        with allure.step("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求"):
            logger.info("通过SOA Partner发送HighVoltageService_client:SetChargingControl请求")
            self.send_method_request("HighVoltageAppService_client", "SetChargingControl", {"cmd":{"type":type.value,"source":source.value}})
            
#shulin:20241014
    def set_SetChargeSoc_req(self,soc:Union[float, int] = 0):
        prompt_info = f"----------> 通过SOA Partner设置充电SOC请求HighVoltageService:SetChargeSoc的目标值"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageService_client", "SetChargeSoc",  {"soc": soc})

    def ctrl_wireless_charge(self, zone: WPCZoneId, sts: isOn):
        with allure.step(f"控制无线充电区域{zone.name}为{sts.name}"):
            self.send_method_request(
                partner_key="WirelessPhoneChargingService_client",
                method_name="SetWirelessCharging",
                args={
                    "req": [
                        {"zone": zone.value},
                        {"isOn": sts.value}
                    ]
                }
            )

    def check_wireless_inform(
            self,
            isforgotten: WPCIsForgotten = WPCIsForgotten.NotForgotten,
            ctrlsts: WPCCtrlSts = WPCCtrlSts.Enable,
            chargingsts: WPCChargingSts = WPCChargingSts.Standby,
            faultid: WPCFaultsId = WPCFaultsId.Ok,
    ):
        with allure.step(f"WPC_遗留状态{isforgotten.name}: {isforgotten.value}, 功能反馈{ctrlsts.name}: {ctrlsts.value},"
                         f"充电状态{chargingsts.name}: {chargingsts.value}, 故障状态{faultid.name}: {faultid.value}"):
            self.ck_s2s_event(
                "WirelessPhoneChargingService_client",
                "WirelessChargingInfo",
                {
                    "info":
                        [
                            {
                                "zone": 0,
                                "isForgotten": isforgotten.value,
                                "ctrlSts": ctrlsts.value,
                                "chargingSts": chargingsts.value,
                                "faults": [{"faultId": faultid.value, "faultMsg": ""}]
                            }
                        ]
                }
            )

    def check_two_wireless_inform(
            self,
            isforgotten: WPCIsForgotten = WPCIsForgotten.NotForgotten,
            ctrlsts: WPCCtrlSts = WPCCtrlSts.Enable,
            chargingsts: WPCChargingSts = WPCChargingSts.Standby,
            faultid: WPCFaultsId = WPCFaultsId.Ok,
            isforgotten_pass: WPCIsForgotten = WPCIsForgotten.NotForgotten,
            ctrlsts_pass: WPCCtrlSts = WPCCtrlSts.Enable,
            chargingsts_pass: WPCChargingSts = WPCChargingSts.Standby,
            faultid_pass: WPCFaultsId = WPCFaultsId.Ok,
    ):
        with allure.step(f"WPC_主驾遗留{isforgotten.name}: {isforgotten.value}, 主驾功能反馈{ctrlsts.name}: {ctrlsts.value},"
                         f"主驾充电状态{chargingsts.name}: {chargingsts.value}, 主驾故障状态{faultid.name}: {faultid.value}, "
                         f"副驾遗留{isforgotten_pass.name}: {isforgotten_pass.value}, 副驾功能反馈{ctrlsts_pass.name}: {ctrlsts_pass.value},"
                         f"副驾充电状态{chargingsts_pass.name}: {chargingsts_pass.value}, 副驾故障状态{faultid_pass.name}: {faultid_pass.value},"):
            self.ck_s2s_event(
                "WirelessPhoneChargingService_client",
                "WirelessChargingInfo",
                {
                    "info":
                        [
                            {
                                "zone": 0,
                                "isForgotten": isforgotten.value,
                                "ctrlSts": ctrlsts.value,
                                "chargingSts": chargingsts.value,
                                "faults": [{"faultId": faultid.value, "faultMsg": ""}]
                            },
                            {
                                "zone": 1,
                                "isForgotten": isforgotten_pass.value,
                                "ctrlSts": ctrlsts_pass.value,
                                "chargingSts": chargingsts_pass.value,
                                "faults": [{"faultId": faultid_pass.value, "faultMsg": ""}]
                            }
                        ]
                }
            )

    def check_no_NotifyTimeUpEventInfo(self, timeout: Union[float, int]):
        """
        监听TCAM不会发出RtcAlarmService_server:NotifyTimeUpEventInfo事件
        
        Args:
            timeout (Union[float, int]): 监听超时时间
        
        Returns:
            None
        
        """
        with allure.step("通过SOA Partner监听TCAM不会发出RtcAlarmService_server:NotifyTimeUpEventInfo事件"):
            logger.info("通过SOA Partner监听TCAM不会发出RtcAlarmService_server:NotifyTimeUpEventInfo事件")
            self.ck_no_req("RtcAlarmService_client", "NotifyTimeUpEventInfo", timeout=timeout)

    def set_SetCloudBmsStrategyConfig_req(self,value:Union[float, int] = 0):
        """设置SOC统一请求"""
        prompt_info = f"----------> 通过SOA Partner设置SOC统一请求HighVoltageService:SetCloudBmsStrategyConfig的目标值"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("HighVoltageService_client", "SetCloudBmsStrategyConfig", {"configCmd":{"type":0,"value":value}}) 

    def set_SetDischargingControl_req(self,type:Union[float, int] = 0,source:Union[float, int] = 0):
        """设置放电请求"""
        prompt_info = f"----------> 通过SOA Partner设置放电请求HighVoltageService:SetDischargingControl的目标值"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("HighVoltageAppService_client", "SetDischargingControl", {"cmd":{"type":type,"source":source}})

    def set_GetVehicleTimeInfo_req(self,value:Union[float, int] = 0):
        """设置授时状态"""
        prompt_info = f"----------> 仿真TCAM的授时请求GetVehicleTimeInfo:GetVehicleTimeInfo的状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("VehicleTimeService_client", "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": value}})

    def check_DoorService_SetPosition_req(self, doors_pos_dict:dict = {DoorId.kDoorFrontLeft: 5},scene:VehicleInsideOutside = VehicleInsideOutside.VehicleInSide,timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出车门开度DoorService::SetPosition请求"):
            logger.info("通过SOA Partner监听TCAM是否发出车门开度DoorService::SetPosition请求")
            doors = []
            for i,v in doors_pos_dict.items():
                doors.append({"id": i.value,"pos": v})
            logger.info(f"监听TCAM是否发出车门开度DoorService::SetPosition请求:{doors},{scene.value}")
            self.ck_s2s_req("DoorService_server", "SetPosition", {"doors": doors,
                                                                  'scene':scene.value}, timeout=timeout)

    def response_to_DoorService_SetPosition_req(self):
        prompt_info = f"----------> 通过SOA Partner发送车门开度DoorService::SetPosition请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("DoorService_server", "SetPosition", args=None)

    def check_DoorService_SetPosition_req_and_feedback_resp(self,  doors_pos_dict:dict = {DoorId.kDoorFrontLeft: 5},scene:VehicleInsideOutside = VehicleInsideOutside.VehicleInSide, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取车门开度DoorService::SetPosition请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_DoorService_SetPosition_req(doors_pos_dict, scene, timeout=timeout)  # 监听TCAM发送车门翘起请求
            self.response_to_DoorService_SetPosition_req()

    def notify_DoorFault(self,door_fault_dict :dict = {DoorId.kDoorFrontLeft:DoorfFultSts.FaultPlayProtectionActive}):
        prompt_info = f"----------> 通过SOA Partner发送车门DoorService::DoorFault通知 {door_fault_dict}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("DoorService_server", "DoorFault",
                                                {"faults": [{'door':doorid.value,'faultMsg':"",'fault':fault.value} for doorid,fault in door_fault_dict.items()]})

    def notify_NotifyLockWarning(self,lock_warn: LockWarn=LockWarn.CloseDoorFail, remind: DoorRemind = DoorRemind.NoRequest):
        prompt_info = f"----------> 通过SOA Partner发送门锁告警信息,期望的'LockWarn': {lock_warn.name}, 'remind': {remind.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_event_notify("EntryService_server", "NotifyLockWarning",
                                                {"warnnings": {"lock": lock_warn.value, "reminder": remind.value}})

    def check_DoorService_Close_req(self, doors:list=[DoorId.kDoorFrontLeft], timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出车门关闭DoorService::Close请求"):
            logger.info("通过SOA Partner监听TCAM是否发出车门关闭DoorService::Close请求")
            Doors = [door.value for door in doors]
            self.ck_s2s_req("DoorService_server", "Close", {"doors": Doors,
                                                                  }, timeout=timeout)

    def response_to_DoorService_Close_req(self):
        prompt_info = f"----------> 通过SOA Partner发送车门关闭 DoorService::Close请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("DoorService_server", "Close", args=None)

    def check_DoorService_Close_req_and_feedback_resp(self, doors:list=[DoorId.kDoorFrontLeft] , timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取车门关闭DoorService::Close请求,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_DoorService_Close_req(doors, timeout=timeout)  
            self.response_to_DoorService_Close_req()

    def get_Remote_Rescue_DriveSts(self):
        time.sleep(4) #周期3S发送
        Remote_Rescue_DriveSts = self.return_latest_event("RemoteRescueService_client_BGM_RemoteRescueService", "FOTARescueInfo")['info']['driveSts']
        return Remote_Rescue_DriveSts            
    
    def check_DriveSts_event_period(self, target_period: Union[float, int], epsilon: float):
        logger.info(f"start check Remote Rescue DriveSts Status event period")
        return self.check_event_period(partner_key=f'RemoteRescueService_client_BGM_RemoteRescueService',
                                       event_name='FOTARescueInfo', target_period=target_period, epsilon=epsilon)
        
    def set_SetGunPullOutCharge_req(self,value:Union[float, int] = 0,out:Union[float, int] = 0):
        """设置拔枪充电口盖自动关闭充电口盖时间"""
        prompt_info = f"----------> 设置拔枪充电口盖自动关闭充电口盖时间GetVehicleTimeInfo:SetClsChargeLidTiSts的状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("ChargeLidService_client", 'SetGunPullOutChargeLidCloseTimeConfig', {"configCmd":{"closeTimeCmd": value}},  {"out": out})
            
    def set_eco_sts(self, sts: bool, timeout: Union[float, int] = 0.5):
        promt_info = f"----------------> 通过SOA Partner发出 ClimateControlService:SetEcoMode 设置ECO开关状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.send_method_request("ClimateControlService_client", "SetEcoMode", {"on": sts})
        sleep(timeout)

    def trigger_remote_rescue_inhibitControl(self):
        current_time_stamp = int(time.time() * 1000)
        openinhibit = {"cmd":1,"cmdDetail":{"inhibitControl":2,"resetControl":0},"sign":"-","timeStamp":current_time_stamp,"timeout":10800000}
        self.call_vehicle_api(V2T_API.RemoteRescue, payload = openinhibit)

    def notify_BookChargingInfo(self,source: DischargeSourceId=DischargeSourceId.kRemoteControl, reqSts: ACBookChargingReqSts = ACBookChargingReqSts.kDefault,workSts:ACBookChargingWorkSts=ACBookChargingWorkSts.kBookStsDefault,startTime:int=0,endTime:int=0,repeatType:bool=False,isToTargetSOCStop:bool=False):
        prompt_info = """----------> 通过SOA Partner发送HighVoltageAppService_server:BookChargingInfo的通知"""
        with allure.step(prompt_info):
            logger.info("""----------> 通过SOA Partner发送HighVoltageAppService_server:BookChargingInfo的通知 {}""".format({"info": {"acInfo": {'source':source.value,
                                                                     'reqSts':reqSts.value,
                                                                     'workSts':workSts.value,
                                                                     'info':{'startTime':startTime,
                                                                             'endTime':endTime,
                                                                             'repeatType':repeatType},
                                                                     'isToTargetSOCStop':isToTargetSOCStop}}}))
            self.soa_partner.send_event_notify("HighVoltageAppService_server", "BookChargingInfo",
                                                {"info": {"acInfo": {'source':source.value,
                                                                     'reqSts':reqSts.value,
                                                                     'workSts':workSts.value,
                                                                     'info':{'startTime':startTime,
                                                                             'endTime':endTime,
                                                                             'repeatType':repeatType},
                                                                     'isToTargetSOCStop':isToTargetSOCStop}}})

    def check_SetACBookCharging_req(self, com_type: BookChargingCommandType=BookChargingCommandType.kCancel,source: DischargeSourceId=DischargeSourceId.kDefault,startTime:int=0,endTime:int=0,repeatType: RepeatType=RepeatType.kDefault,isToTargetSOCStop: bool=False,timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageAppService_server::SetACBookCharging请求"):
            logger.info("通过SOA Partner监听TCAM是否发出HighVoltageAppService_server::SetACBookCharging请求{}".format({"cmd":{"type":com_type.value,"source":source.value,
                                                                                                  "timeInfo":{"startTime":startTime,"endTime":endTime,"repeatType":repeatType.value},
                                                                                                  "isToTargetSOCStop":isToTargetSOCStop}}))

            self.ck_s2s_req("HighVoltageAppService_server", "SetACBookCharging", {"cmd":{"type":com_type.value,"source":source.value,
                                                                                                  "timeInfo":{"startTime":startTime,"endTime":endTime,"repeatType":repeatType.value},
                                                                                                  "isToTargetSOCStop":isToTargetSOCStop}}, timeout=timeout)

    def response_to_SetACBookCharging_req(self):
        prompt_info = f"----------> 通过SOA Partner发送HighVoltageAppService_server::SetACBookCharging请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageAppService_server", "SetACBookCharging", args=None)

    def check_SetACBookCharging_req_and_feedback_resp(self,com_type: BookChargingCommandType=BookChargingCommandType.kCancel,source: DischargeSourceId=DischargeSourceId.kDefault,startTime:int=0,endTime:int=0,repeatType: RepeatType=RepeatType.kDefault,isToTargetSOCStop: bool=False, timeout: Union[float, int] = 1):
        prompt_info = f"---------->获取HighVoltageAppService_server::SetACBookCharging,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetACBookCharging_req(com_type, source, startTime,endTime,repeatType,isToTargetSOCStop,timeout=timeout)  
            self.response_to_SetACBookCharging_req()

    def check_SetChargingControl_req(self, com_type:ControlCommandType=ControlCommandType.kDefault, source:DischargeSourceId=DischargeSourceId.kRemoteControl,timeout: Union[float, int] = 1):
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageAppService_server::SetChargingControl请求"):
            logger.info("通过SOA Partner监听TCAM是否发出HighVoltageAppService_server::SetChargingControl请求")

            self.ck_s2s_req("HighVoltageAppService_server", "SetChargingControl", {"cmd":{"type":com_type.value,"source":source.value}}, timeout=timeout)

    def response_to_SetChargingControl_req(self):
        prompt_info = f"----------> 通过SOA Partner发送HighVoltageAppService_server::SetChargingControl请求的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.soa_partner.send_method_response("HighVoltageAppService_server", "SetChargingControl", args=None)

    def check_SetChargingControl_req_and_feedback_resp(self,com_type:ControlCommandType=ControlCommandType.kDefault, source:DischargeSourceId=DischargeSourceId.kRemoteControl,timeout:Union[float, int] = 1):
        prompt_info = f"---------->获取HighVoltageAppService_server::SetChargingControl,并且回复对应的响应"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_SetChargingControl_req(com_type, source,timeout=timeout)  
            self.response_to_SetChargingControl_req()

    def notify_DisplayBookChargingInfo(self,displaybookchargingtype: DisplayBookChargingType=DisplayBookChargingType.kAC, startTime:list =[2236,13,32,24,60,60],endTime:list=[2236,13,32,24,60,60]):
        prompt_info = """----------> 通过SOA Partner发送HighVoltageAppService_server:DisplayBookChargingInfo的通知"""
        with allure.step(prompt_info):
            logger.info("""----------> 通过SOA Partner发送HighVoltageAppService_server:DisplayBookChargingInfo的通知 {}""".format({"info": {'type':displaybookchargingtype.value,"startTime":startTime,"endTime":endTime}}))
            
            self.soa_partner.send_event_notify("HighVoltageAppService_server", "DisplayBookChargingInfo",
                                                {"info": {'type':displaybookchargingtype.value,"startTime":{"kYear":startTime[0],"kMonth":startTime[1],"kDay":startTime[2],"kHour":startTime[3],"kMinute":startTime[4],"kSecond":startTime[5]},
                                                          "endTime":{"kYear":endTime[0],"kMonth":endTime[1],"kDay":endTime[2],"kHour":endTime[3],"kMinute":endTime[4],"kSecond":endTime[5]}}})
            
    def hmi_set_window_full_open(self, win_pos:WindowId):
        prompt_info = f"---------->通过 WindowService_client, Open 设置{win_pos.name}窗户全开"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("WindowService_client", "Open", {"windows": [win_pos.value]})

    def hmi_set_window_position(self, win_pos:WindowId, position: Union[WinPos, None] = None):
        prompt_info = f"---------->通过 WindowService_client, SetPosition 设置{win_pos.name}窗户位置为{position.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("WindowService_client", "SetPosition", {"windows": [{"id": win_pos.value, "position": (position.value-1)*4}]})

    def check_window_status(self,zone:WindowId,switch_status:WindowSwitchStatus):
        prompt_info = f"---------->通过 WindowService_client, GetWindowSwitchStatus 获取开关状态窗户位置为{switch_status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp("WindowService_client", "GetWindowSwitchStatus",{"zone":zone.value},{'out':[{'zone':zone.value,'sts':switch_status.value}]})

    def check_window_event(self,zone:WindowId,event_status:WindowSwitchStatus):
        prompt_info = f"---------->通过 WindowService_client, NotifyWindowSwitchStatus 获取状态上报为{event_status.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("WindowService_client", "NotifyWindowSwitchStatus",{"info":{"zone": zone.value, "sts":event_status.value}})
   
   
            
#o_fan.liu edit 
    def get_gear_level(self, gear: Gear):
        with allure.step(f"获取设置的档位等级为{gear.name}"):
            logger.info(f"获取设置的档位等级为{gear.name}")
            self.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": gear.value})

    def notify_wifiStsChanged(self, type: str, hasAccessibility: str):
        data = {"type": type, "hasAccessibility": hasAccessibility}
        self.send_event_notify("InteractiveService_server", "WifiStsChanged",{"values": [{"id": "NetWorkAccess", "data": str(data)}]})
        
    def set_tweeter_updown(self, zone_id:TweeterZoneId,tweeter_command:TweeterCommand):
        prompt_info = f"---------->通过 TweeterService_client, SetTweeterStatus设置{zone_id.name}扬声器升降状态为{tweeter_command.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("TweeterService_client", "SetTweeterStatus",{"zondId": zone_id.value, "command": tweeter_command.value})

    def get_left_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
        prompt_info = f"===============>获取左照脚灯模式为: {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp(
                partner_key="LightService_client",
                method_name="GetStatus",
                args={"lights": [{"type": 24, "zoneId": 1}]},
                ck_info={
                    "out":
                        [
                            {"light": {"type": 24, "zoneId": 1}, "sts": sts.value, "brightness": 0,
                             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
                        ]
                },
                timeout=timeout
            )

    def get_right_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
        prompt_info = f"===============>获取右照脚灯模式为: {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp(
                partner_key="LightService_client",
                method_name="GetStatus",
                args={"lights": [{"type": 24, "zoneId": 2}]},
                ck_info={
                    "out":
                        [
                            {"light": {"type": 24, "zoneId": 2}, "sts": sts.value, "brightness": 0,
                             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
                        ]
                },
                timeout=timeout
            )

    def get_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
        prompt_info = f"===============>获取照脚灯模式为: {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_request_and_ck_resp(
                partner_key="LightService_client",
                method_name="GetStatus",
                args={"lights": [{"type": 24, "zoneId": 0}]},
                ck_info={
                    "out":
                        [
                            {"light": {"type": 24, "zoneId": 1}, "sts": sts.value, "brightness": 0,
                             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                            {"light": {"type": 24, "zoneId": 2}, "sts": sts.value, "brightness": 0,
                             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
                        ]
                },
                timeout=timeout
            )

    def check_left_footlight_inform(self, sts: FootLightSts, timeout: int = 5):
        prompt_info = f"===============>通知左照脚灯模式为: {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event(
                partner_key="LightService_client",
                interface_name="Status",
                ck_info={"sts": {"light": {"type": 24, "zoneId": 1}, "sts": sts.value}},
                timeout=timeout
            )

    def check_right_footlight_inform(self, sts: FootLightSts, timeout: int = 5):
        prompt_info = f"===============>通知右照脚灯模式为: {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event(
                partner_key="LightService_client",
                interface_name="Status",
                ck_info={"sts": {"light": {"type": 24, "zoneId": 2}, "sts": sts.value}},
                timeout=timeout
            )

    def set_footlight_sts(self, sts: OnOff):
        logger.info(f"============>设置照脚灯模式为: {sts.name}")
        if sts.value:
            self.hmi_light_control(type=LightType.LightFoot, zone=LightZone.LightZoneAllOrSingle,
                                       mode=LightMode.On, brightness=100)
        else:
            self.hmi_light_control(type=LightType.LightFoot, zone=LightZone.LightZoneAllOrSingle,
                                       mode=LightMode.On, brightness=0)

    def check_vehicle_inside_person_sts(self, userInVehicleStatus: bool = False, userInVehicleStatusWithCam: bool = False):
        prompt_info = f"----------> check车内有人状态事件:SeatService:VehicleInsidePersonSts userInVehicleStatus：{userInVehicleStatus}, \
            userInVehicleStatusWithCam：{userInVehicleStatusWithCam}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ck_s2s_event("SeatService_client", "VehicleInsidePersonSts", {"personSts": {"userInVehicleStatus": userInVehicleStatus,"userInVehicleStatusWithCam": userInVehicleStatusWithCam}})



    def check_SetHvPulseHeating_req(self, on: bool = True,timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:SetHvPulseHeating请求
        
        Args:
            on (bool, optional): 是否开启电池脉冲加热，默认为True.
            timeout (Union[float, int], optional): 超时时间，单位为秒，默认为1.
        
        Returns:
            None
        
        """
        logger.info(f"通过SOA Partner监听TCAM是否发出HighVoltageService:SetHvPulseHeating请求")
        with allure.step("通过SOA Partner监听TCAM是否发出HighVoltageService:SetHvPulseHeating请求"):
            self.ck_s2s_req("HighVoltageService_server", "SetHvPulseHeating", 
                            { "on": on}, timeout=timeout)



    def notify_pulseHeatingInfo(self, pulseHeating_sts: PulseHeatingSts = PulseHeatingSts.kDefault,
                                  target_temperature: float=-41,):
        with allure.step(f"通过SOA Partner发出HighVoltageService:pulseHeatingInfo事件通知"):
            logger.info(f"通过SOA Partner发送HighVoltageService:pulseHeatingInfo事件通知")
            self.soa_partner.send_event_notify("HighVoltageService_server", "PulseHeatingInfo",
                                               {"sts": {"pulseHeatingSts": pulseHeating_sts.value, "pulseHeatingTargetTemperature": target_temperature,
                                                       }})

    def start_send_InteractiveService_response_wifi(self):
        self.send_response_to_req_start(partner_key=f'InteractiveService_server',
                                        func=self.on_getWifiSts)
        
    def on_getWifiSts(self, partner_key, msg):
        if 'InteractiveService_server' in partner_key and msg["function"] == 'Get':
            if not hasattr(self.soa_partner.partner_infos[partner_key], "args"):
                setattr(self.soa_partner.partner_infos[partner_key], "args", {"OutputValueList": {"id":"isWifiAPAvailable","data":"1", "code":0}})
            self.send_method_response(partner_key=partner_key, method_name='Get',
                                      args=self.soa_partner.partner_infos[partner_key].args)
    def stop_send_InteractiveService_response_wifi(self):
        try:
            self.send_response_to_req_stop(partner_key=f'InteractiveService_server',
                                           func=self.on_getWifiSts)
        except KeyError:
            logger.error("当前服务未注册,无法调用stop")

    def set_batter_saver_connect(self, battersaver: bool):
        prompt_info = f"----------> 通过SOA Partner VehicleModeService_client::SetBatterySaverConnect 设置节电继电器闭合状态为{battersaver}状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.send_method_request("VehicleModeService_client", "SetBatterySaverConnect", {"isConnect": battersaver})


            
#o_fan.liu       
    def event_check_frntleft_heat_sts2(self, heat_level: HeatLevel = HeatLevel.Off,                                                         ################o_fan.liu
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, 
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone, source:SourceId=SourceId.Idle):
        
        prompt_info = f"----------> check 主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus: heatLevel {heat_level.value},  \
            heatWorkStatus {heat_work_sts.value},ventLevel: {vent_level.value}, , ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            self.ck_s2s_event("SeatService_client", "FrntLeftSeatHeatVentStatus", {"status":{
                                                                                    "heatLevel": heat_level.value,
                                                                                    "heatWorkStatus": heat_work_sts.value,
                                                                                    "ventLevel": vent_level.value,
                                                                                    "ventWorkStatus": vent_work_sts.value,
                                                                                    "source":source.value
                                                                                    }})
           
                   

    def event_check_frntright_heat_sts2(self, heat_level: HeatLevel = HeatLevel.Off,                                                         ################o_fan.liu
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, 
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone, source:SourceId=SourceId.Idle):
        
        prompt_info = f"----------> check 副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus: heatLevel {heat_level.value},  \
            heatWorkStatus {heat_work_sts.value},ventLevel: {vent_level.value}, , ventWorkStatus: {vent_work_sts.value}"
        with allure.step(prompt_info):
            self.ck_s2s_event("SeatService_client", "FrntRightSeatHeatVentStatus", {"status":{
                                                                                    "heatLevel": heat_level.value,
                                                                                    "heatWorkStatus": heat_work_sts.value,
                                                                                    "ventLevel": vent_level.value,
                                                                                    "ventWorkStatus": vent_work_sts.value,
                                                                                    "source":source.value
                                                                                    }})

                       
 #o_fan.liu edit 
    def get_tailgate_AntiPinch_sts(self, sts: bool):
        with allure.step(f"获取尾门防夹状态为{sts}"):
            logger.info(f"获取尾门防夹状态为{sts}")
            self.send_request_and_ck_resp("TailGateService_client", "GetLiftgateSysSts", {}, {"out": {"isAntiPinchOn":sts}})
            
 #o_fan.liu edit
    def event_check_tailgate_AntiPinch_sts(self, sts: bool):
        with allure.step(f"尾门防夹事件上报，Check上报的防夹状态是否为{sts}"):
            logger.info(f"尾门防夹事件上报，Check上报的防夹状态是否为{sts}")
            self.ck_s2s_event("TailGateService_client", "NotifyLiftgateSysSts", {"sts": {"isAntiPinchOn":sts}})

    def stop_send_InteractiveService_response_gso(self):
        try:
            self.send_response_to_req_stop(partner_key=f'InteractiveService_server',
                                           func=self.on_isWifiConnectHotSpot)
        except KeyError:
            logger.error("当前服务未注册,无法调用stop")

    def start_send_InteractiveService_response_gso(self, isWifiConnectHotSpot: int):
        self.isWifiConnectHotSpot = isWifiConnectHotSpot
        self.send_response_to_req_start(partner_key=f'InteractiveService_server',
                                        func=self.on_isWifiConnectHotSpot)

    def update_InteractiveService_get_response(self, isWifiConnectHotSpot: int):
        self.stop_send_InteractiveService_response_gso()
        self.start_send_InteractiveService_response_gso(isWifiConnectHotSpot = isWifiConnectHotSpot)
            
    def on_isWifiConnectHotSpot(self, partner_key, msg):
        if 'InteractiveService_server' in partner_key and msg["function"] == 'Get':
            if not hasattr(self.soa_partner.partner_infos[partner_key], "args"):
                setattr(self.soa_partner.partner_infos[partner_key], "args", {"OutputValueList": {"id": "isWifiConnectHotSpot", "data": f'{self.isWifiConnectHotSpot}'}})
            self.send_method_response(partner_key=partner_key, method_name='Get',
                                      args=self.soa_partner.partner_infos[partner_key].args)
            
    def notify_wifiStsChanged_NetWorkAccess(self, type: str, hasAccessibility: str):
        data = {"type": type, "hasAccessibility": hasAccessibility}
        self.send_event_notify("InteractiveService_server", "WifiStsChanged",{"values": [{"id": "NetWorkAccess", "data": json.dumps(data)}]})
