#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :soa.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :soa通信能力模拟 实现接口
"""
from typing import Union, List, Dict

from xat_ecu.api.interfaces.dp2.interface import CommonSoa
from xat_ecu.api.constants.common import FailType
from xat_ecu.api.interfaces.dp2.base_common.constants.common_data import *


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
    
    def ck_field(self, partner_key: str, field_name: str, field_info: dict, timeout=1, deviation=0, fuzz_match=True):
        self.soa_partner.ck_field(partner_key, field_name, field_info, timeout, deviation, fuzz_match)

    def ck_req(self, partner_key: str, interface_name: str, ck_info: Union[dict, None] = None, timeout=1):
        self.soa_partner.ck_s2s_req(partner_key, interface_name, ck_info, timeout)
    
    def ck_event(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        return self.soa_partner.ck_s2s_event(partner_key, interface_name, ck_info, timeout, fuzz_match)

    def request_and_ck_errorcode(self, partner_key: str, method_name: str, args: dict, errorcode: ErrorCode,
                                 timeout=2, is_async=False):
        """发送请求，并检查返回错误码"""
        return self.soa_partner.send_request_and_ck_resp(partner_key, method_name, args, {"out": errorcode.value}, timeout, is_async)

    def empty_all(self, wait_time=0):
        return self.soa_partner.empty_all(wait_time)

    def empty_event_list(self, partner_key=None):
        return self.soa_partner.empty_event_list(partner_key)

    def empty_req_list(self, partner_key=None):
        return self.soa_partner.empty_req_list(partner_key)

    def empty_resp_list(self, partner_key=None):
        return self.soa_partner.empty_resp_list(partner_key)
    
