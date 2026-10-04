#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : DoipGateway.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/10 14:51
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import copy
import time
from functools import reduce
from collections import defaultdict, OrderedDict
from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.socket_client.SocketData import SocketData
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.socket_client.UdpClient import UdpClient
from xat_ecu.legacy.socket_client.SocketClient import SocketClient
from xat_ecu.legacy.protocol.ProtocolConfigData import *


class DoipClientGateway(object):

    def __init__(self, uds_host="169.254.19.1", uds_port=13400):
        self.uds_host = uds_host
        self.uds_port = uds_port
        self.udp_client_sock = None
        self.udp_broadcast_client_sock = None
        self.tcp_client_sock = None
        self.return_data_obj = []
        self.sp_0x78_time_dict = defaultdict(OrderedDict)
        self.counter_with_0x78 = 0
        self.check_replay_finished = False
        self.replay_message_id_list = [0x8003, 0x0000, 0x0004, 0x4002, 0x4004, 0x0008, 0x0006]

    def new_tcp_connect_start(self, after_connect):
        if not self.tcp_client_sock:
            self.tcp_client_sock = SocketClient(self.uds_host, self.uds_port)
            if not after_connect:
                self.tcp_client_sock.start()
        else:
            if self.tcp_client_sock.is_stop:
                self.tcp_client_sock.start()

    def new_udp_connect_start(self):
        self.udp_client_sock = UdpClient(self.uds_host, self.uds_port)
        self.udp_client_sock.start()

    def new_udp_broadcast_connect_start(self):
        self.udp_broadcast_client_sock = UdpClient(self.uds_host, self.uds_port)
        self.udp_broadcast_client_sock.start_recv_udp_broadcast()

    def get_current_broadcast_host(self):
        if not self.udp_broadcast_client_sock:
            raise AssertionError(f"not init udp broadcast object.")
        return self.udp_broadcast_client_sock.accept_broadcast_host

    def get_udp_broadcast_data(self, in_time, need_new_data=True):
        if need_new_data:
            SocketData.UDP_BROADCAST_CLIENT_DATA[self.udp_broadcast_client_sock].clear()
        time.sleep(in_time)
        time_list = []
        for message_info in SocketData.UDP_BROADCAST_CLIENT_DATA[self.udp_broadcast_client_sock]:
            for t, message in message_info.items():
                time_list.append(t)
        return time_list

    def get_current_udp_broadcast_data(self):
        return SocketData.UDP_BROADCAST_CLIENT_DATA[self.udp_broadcast_client_sock].pop()

    def split_package_data(self, protocol_data):
        full_protocol_data = []

        while protocol_data:
            if int(protocol_data[4: 8].hex(), 16) != len(protocol_data[8:]):
                if int(protocol_data[4: 8].hex(), 16) < len(protocol_data[8:]):
                    logger.debug(f"all package len less actual data len.")
                    split_data = protocol_data[:int(protocol_data[4: 8].hex(), 16) + 8]
                    full_protocol_data.append(split_data)
                    protocol_data = protocol_data[int(protocol_data[4: 8].hex(), 16) + 8:]
                else:
                    logger.info(f"all package len large ran actual data len")
                    return
            else:
                full_protocol_data.append(protocol_data)
                return full_protocol_data
            time.sleep(0.001)

    def send_and_get_callback_data(self, data, doip_type=None, socket_type="tcp", need_expect_type=None):
        if not doip_type:
            raise AssertionError(f"request doip type error,got:{doip_type}")
        if not isinstance(doip_type, list):
            raise AssertionError(f"doip type error,expect list,but got:{type(doip_type)}")
        if socket_type == "udp":
            SocketData.UDP_CLIENT_DATA[self.udp_client_sock].clear()
            self.sp_0x78_time_dict.clear()
            self.return_data_obj.clear()
            self.check_replay_finished = False
            self.udp_client_sock.udp_send(data)
            return self._get_socket_client_data(doip_type, socket_type, need_expect_type)
        else:
            SocketData.TCP_CLIENT_DATA[self.tcp_client_sock].clear()
            self.return_data_obj.clear()
            self.check_replay_finished = False
            self.tcp_client_sock.async_send_message(data)
            if need_expect_type:
                sub_id = data[12] if 0x8001 in need_expect_type else None
                if self.sp_0x78_time_dict.get(sub_id):
                    del self.sp_0x78_time_dict[sub_id]
            else:
                sub_id = None
            return self._get_socket_client_data(doip_type, socket_type, need_expect_type, sub_id=sub_id)

    @wait_until_function_return_result(timeout=ProtocolResponseConfigData.uds_ne_code_time_out,
                                       interval=ProtocolResponseConfigData.uds_get_call_message_interval_time
                                       )
    def _get_socket_client_data(self, filter_type, socket_type, need_expect_type, sub_id=None):
        self.return_data_obj.clear()
        iter_data = SocketData.TCP_CLIENT_DATA[self.tcp_client_sock] if socket_type == "tcp" else SocketData.UDP_CLIENT_DATA[self.udp_client_sock]
        if not iter_data:
            return
        need_expect_dict = {}
        if need_expect_type:
            # need_expect_type += self.replay_message_id_list
            for i in need_expect_type:
                need_expect_dict[i] = []

        result = self.split_package_data(reduce(lambda x, y: x + y, iter_data))
        if result is None:
            return
        logger.debug(f"current package data is:{[i.hex() for i in result]}")
        for data in result:
            data_obj = doip_parse(data)
            if need_expect_dict:
                if data_obj.DataType in need_expect_dict:
                    need_expect_dict[data_obj.DataType].append(data_obj)
            else:
                if data_obj.DataType in filter_type:
                    return data_obj

        if not need_expect_type:
            return
        self.check_replay_finished = False
        for doip_type, doip_obj_list in need_expect_dict.items():
            if not doip_obj_list:
                return
            if sub_id and doip_type == 0x8001:
                for value in doip_obj_list:
                    if value.DataInfo.DiagData[0] == sub_id + 0x40:
                        self.check_replay_finished = True
                    if list(value.DataInfo.DiagData[0: 3]) != [0x7f, sub_id, 0x78]:
                        self.check_replay_finished = True
                    else:
                        self.counter_with_0x78 += 1
                        if self.sp_0x78_time_dict.get(sub_id):
                            all_counter = [counter for counter in self.sp_0x78_time_dict[sub_id]]
                            if self.counter_with_0x78 not in all_counter:
                                self.sp_0x78_time_dict[sub_id][self.counter_with_0x78] = time.time()
                        else:
                            self.sp_0x78_time_dict[sub_id][self.counter_with_0x78] = time.time()

            if doip_type in self.replay_message_id_list:
                self.check_replay_finished = True
            self.return_data_obj.extend(doip_obj_list)

        self.counter_with_0x78 = 0
        return self.return_data_obj if self.check_replay_finished else None
