#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : ProtocolServerKeywords.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/10 10:56
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import copy
import time
import socket
import netifaces
from copy import deepcopy
from threading import Thread
from collections import defaultdict

from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.socket_client.SocketData import SocketData
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.protocol.ProtocolConfigData import *
from xat_ecu.legacy.protocol.DoipServerGateway import DoipServerGateway
from xat_ecu.legacy.EMQTT.MQTTClient import MQTTClient


def json_pretty(json_data, **kwargs):
    if not json_data:
        return ''
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            pass
    if isinstance(json_data, object):
        return json.dumps(
            json_data,
            indent=2,
            sort_keys=False,
            ensure_ascii=False,
            **kwargs)
    return json_data


def _get_local_network_ip():
    host_name = socket.gethostname()
    ip_info = socket.gethostbyname_ex(host_name)
    ip_addresses = ip_info[2]
    network_ip_list = [ip for ip in ip_addresses]
    logger.info(f"all ip is:\n {'|'.join(network_ip_list)}")
    return network_ip_list


def get_local_network_ip():
    interfaces = netifaces.interfaces()
    network_info = []

    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs.get(netifaces.AF_INET)

        if ip_info is not None:
            ip = ip_info[0]['addr']
            netmask = ip_info[0]['netmask']
            network_info.append({'interface': interface, 'ip': ip, 'netmask': netmask})

    return [i.get('ip') for i in network_info]


def struct_json_pretty(struct_data):
    return json_pretty(struct_data, cls=StructJSONEncoder)


class StructJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return bytes.hex(obj)
        return json.JSONEncoder.default(self, obj)


class ProtocolServerKeywords(object):

    def __init__(self, protocol_type="doip", uds_host="172.16.9.21", uds_port=13400, remote_mock_server=False):
        self.uds_host = uds_host
        self.uds_port = uds_port
        self.remote_mock_server = remote_mock_server
        self.max_cache_number = 20
        self.protocol_type = protocol_type
        self.nack_mock_data_0x8001 = dict()
        self.ack_mock_data_0x8001 = dict()
        self.mock_data_0x8001 = dict()
        self.server_tcp_replay_data_queue = defaultdict(deque)
        self.server_udp_replay_data_queue = deque(maxlen=5000)
        self.domain_accept_data_queue = defaultdict(deque)
        self.mock_server_data = deepcopy(update_doip_service_data)
        self.emq_obj = None
        self.doip_sock_obj = None
        self.function_route_ip_map = dict()
        self.local_ip_list = get_local_network_ip()
        self.mock_service_start_send_flag = {}
        if remote_mock_server:
            self.update_mock_data_topic = "mock_uds_data"
            self.emq_obj = MQTTClient()
        else:
            self.doip_sock_obj = DoipServerGateway(uds_host, uds_port)

    def start_udp_connect(self):
        if self.remote_mock_server:
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)
            self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "start_udp_connect"}))
        else:
            self.doip_sock_obj.new_udp_connect_start()

    def start_tcp_connect(self):
        if self.remote_mock_server:
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)
            self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "start_tcp_connect"}))
        else:
            self.doip_sock_obj.new_tcp_connect_start()

    def stop_udp_connect(self):
        if self.remote_mock_server:
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)
            self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "stop_udp_connect"}))
        else:
            self.doip_sock_obj.udp_server_sock.stop()

    def stop_tcp_connect(self):
        if self.remote_mock_server:
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)
            self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "stop_tcp_connect"}))
        else:
            self.doip_sock_obj.tcp_server_sock.stop()

    def stop_mqtt_server(self):
        if self.emq_obj:
            self.emq_obj.disconnect()

    def init_middleware(self):
        p_type = str(self.protocol_type).lower()
        if p_type == "doip":
            if self.remote_mock_server:
                if not self.emq_obj.is_connected():
                    self.emq_obj.connect(self.uds_host)
                self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "init_middleware"}))
            else:
                self.init_mock_data()
                self.start_tcp_connect()
                time.sleep(2)
                self.mock_server_handler()
        elif p_type == "can":
            pass
        elif p_type == "fr":
            pass

    def convert_str_keys_to_int(self, dictionary, new_dict):
        for key in dictionary.keys():
            if isinstance(key, str):
                new_dict[int(key)] = dictionary.get(key)
        for k, value in dictionary.items():
            if isinstance(value, dict):
                new_dict[int(k)] = dictionary[k]
                self.convert_str_keys_to_int(value, new_dict[int(k)])
        return new_dict

    def init_middleware(self):
        p_type = str(self.protocol_type).lower()
        if p_type == "doip":
            if self.remote_mock_server:
                if not self.emq_obj.is_connected():
                    self.emq_obj.connect(self.uds_host)
                self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty({'op_type': "init_middleware"}))
            else:
                self.init_mock_data()
                self.start_tcp_connect()
                time.sleep(2)
                self.mock_server_handler()
        elif p_type == "can":
            pass
        elif p_type == "fr":
            pass

    def convert_str_keys_to_int(self, dictionary, new_dict):
        for key in dictionary.keys():
            if isinstance(key, str):
                new_dict[int(key)] = dictionary.get(key)
        for k, value in dictionary.items():
            if isinstance(value, dict) and "replay_data" not in value:
                new_dict[int(k)] = dictionary[k]
                self.convert_str_keys_to_int(value, new_dict[int(k)])
        return new_dict

    def handle_replay_data(self, data_list, sa, ta, _sock):
        for i in data_list:
            if sa != 0x1fff:
                data = self.doip_generate_service_0x8001(sa, ta,
                                                         bytes.fromhex(i))
                self.server_tcp_replay_data_queue[_sock].append(data)
                logger.info(f"Send: [{hex(sa)} -> {hex(ta)}] | {i}")
            else:
                for ip, domain_list in self.function_route_ip_map.items():
                    if ip in self.local_ip_list:
                        for _sa in domain_list:
                            data = self.doip_generate_service_0x8001(
                                _sa,
                                ta,
                                bytes.fromhex(i)
                            )
                            self.server_tcp_replay_data_queue[_sock].append(
                                data)
                            logger.info(
                                f"Send: [{hex(sa)} -> {hex(ta)}] | {i}")

    def __routing_map_handler(self):
        """
        模拟回复mock_data数据
        :return:
        """
        while self.doip_sock_obj.tcp_server_sock.listen_flag or self.doip_sock_obj.udp_server_sock.listen_flag:
            try:
                for _sock in self.doip_sock_obj.tcp_server_sock.register_sock_set:
                    if SocketData.TCP_SERVER_DATA.get(_sock):
                        if _sock not in self.server_tcp_replay_data_queue:
                            self.server_tcp_replay_data_queue[_sock] = deque([], maxlen=1000)
                        doip_data_obj = doip_parse(SocketData.TCP_SERVER_DATA[_sock].popleft())
                        if doip_data_obj.DataType == 0x8001:
                            sa = doip_data_obj.DataInfo.TargetAddress
                            ta = doip_data_obj.DataInfo.SourceAddress
                            if self.nack_mock_data_0x8001.get(sa) is not None and self.nack_mock_data_0x8001.get(
                                    str(sa)):
                                code = self.nack_mock_data_0x8001.get(doip_data_obj.DataInfo.TargetAddress)
                                data = self.doip_update_service_data_0x8003(sa, ta, code)
                                self.server_tcp_replay_data_queue[_sock].append(data)
                            else:
                                code = self.ack_mock_data_0x8001.get(sa, 0)
                                if not code:
                                    code = self.ack_mock_data_0x8001.get(str(sa), 0)

                                if sa == 0x1fff:
                                    if not self.function_route_ip_map:
                                        data = self.doip_update_service_data_0x8002(target_address=ta, return_code=code)
                                        self.server_tcp_replay_data_queue[_sock].append(data)
                                    else:
                                        for ip, domain_list in self.function_route_ip_map.items():
                                            if ip in self.local_ip_list:
                                                for _sa in domain_list:
                                                    data = self.doip_update_service_data_0x8002(
                                                        source_address=_sa,
                                                        target_address=ta,
                                                        return_code=code
                                                    )
                                                    self.server_tcp_replay_data_queue[_sock].append(data)
                                else:
                                    data = self.doip_update_service_data_0x8002(sa, ta, code)
                                    self.server_tcp_replay_data_queue[_sock].append(data)

                                body_data = doip_data_obj.DataInfo.DiagData
                                domain_data = self.mock_data_0x8001.get(sa)
                                if f"{ta}->{sa}" not in self.domain_accept_data_queue:
                                    self.domain_accept_data_queue[f"{ta}->{sa}"] = deque([body_data.hex()],
                                                                                         maxlen=self.max_cache_number)
                                else:
                                    self.domain_accept_data_queue[f"{ta}->{sa}"].append(body_data.hex())

                                logger.info(f"Accept: [{hex(ta)} -> {hex(sa)}] | {body_data.hex()}")
                                if domain_data:
                                    if body_data[0] == 0x36:
                                        replay_data = f"76" + format(body_data[1], '02X')
                                        data = self.doip_generate_service_0x8001(sa, ta, bytes.fromhex(replay_data))
                                        self.server_tcp_replay_data_queue[_sock].append(data)
                                        logger.info(f"Send: [{hex(sa)} -> {hex(ta)}] | {replay_data}")
                                        continue

                                    if body_data[0] == 0x37:
                                        replay_data = f"77"
                                        data = self.doip_generate_service_0x8001(sa, ta, bytes.fromhex(replay_data))
                                        self.server_tcp_replay_data_queue[_sock].append(data)
                                        logger.info(f"Send: [{hex(sa)} -> {hex(ta)}] | {replay_data}")
                                        continue

                                    if domain_data.get(body_data[0]):
                                        try:
                                            try:
                                                mock_pre_data3 = domain_data[body_data[0]].get(body_data[1] * 2 ** 16 + body_data[2] * 2 ** 8 + body_data[3])
                                                if isinstance(mock_pre_data3, list):
                                                    self.handle_replay_data(mock_pre_data3, sa, ta, _sock)
                                                elif isinstance(mock_pre_data3, dict):
                                                    key = f"{body_data[0]}_{body_data[1] * 2 ** 16 + body_data[2] * 2 ** 8 + body_data[3]}"
                                                    if not self.mock_service_start_send_flag.get(key):
                                                        self.mock_service_start_send_flag[key] = True
                                                        Thread(target=self.__daemon_data_send, args=(mock_pre_data3, sa, ta, _sock, key), daemon=True).start()
                                                    logger.info(
                                                        f"当前mock_service_start_send_flag3是：{self.mock_service_start_send_flag}")
                                            except Exception as e:
                                                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                                                pass

                                            try:
                                                mock_pre_data2 = domain_data[body_data[0]].get(body_data[1] * 2 ** 8 + body_data[2])
                                                if isinstance(mock_pre_data2, list):
                                                    self.handle_replay_data(mock_pre_data2, sa, ta, _sock)
                                                elif isinstance(mock_pre_data2, dict):
                                                    key = f"{body_data[0]}_{body_data[1] * 2 ** 8 + body_data[2]}"
                                                    if not self.mock_service_start_send_flag.get(key):
                                                        self.mock_service_start_send_flag[key] = True
                                                        Thread(target=self.__daemon_data_send,
                                                               args=(mock_pre_data2, sa, ta, _sock, key),
                                                               daemon=True).start()
                                                    logger.info(
                                                        f"当前mock_service_start_send_flag2是：{self.mock_service_start_send_flag}")
                                            except Exception as e:
                                                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                                                    pass
                                            try:
                                                mock_pre_data1 = domain_data[body_data[0]].get(body_data[1])
                                                if isinstance(mock_pre_data1, list):
                                                    self.handle_replay_data(mock_pre_data1, sa, ta, _sock)
                                                elif isinstance(mock_pre_data1, dict):
                                                    key = f"{body_data[0]}_{body_data[1]}"
                                                    if not self.mock_service_start_send_flag.get(key):
                                                        self.mock_service_start_send_flag[key] = True
                                                        Thread(target=self.__daemon_data_send,
                                                               args=(mock_pre_data1, sa, ta, _sock, key),
                                                               daemon=True).start()
                                                    logger.info(f"当前mock_service_start_send_flag1是：{self.mock_service_start_send_flag}")
                                            except Exception as e:
                                                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                                                pass

                                        except Exception as e:
                                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                                            logger.warning(f'handle body data error,got:{e}')

                        else:
                            if doip_data_obj.DataType == 0x0005:
                                data = copy.deepcopy(doip_frame_raw_data_0x0006)
                                data['DataInfo']['TargetAddress'] = doip_data_obj.DataInfo.SourceAddress
                                self.server_tcp_replay_data_queue[_sock].append(doip_build(data))
                            else:
                                if self.mock_server_data.get(doip_data_obj.DataType):
                                    for i in self.mock_server_data[doip_data_obj.DataType]:
                                        self.server_tcp_replay_data_queue[_sock].append(i)

                if SocketData.UDP_SERVER_DATA[self.doip_sock_obj.udp_server_sock]:
                    doip_data_obj = doip_parse(SocketData.UDP_SERVER_DATA[self.doip_sock_obj.udp_server_sock].popleft())
                    if self.mock_server_data.get(doip_data_obj.DataType):
                        for i in self.mock_server_data[doip_data_obj.DataType]:
                            self.server_udp_replay_data_queue.append(i)

                time.sleep(0.01)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                logger.warning(f"服务端处理数据映射错误：{e}")

    def __server_send_replay_handler(self):
        while self.doip_sock_obj.tcp_server_sock.listen_flag or self.doip_sock_obj.udp_server_sock.listen_flag:
            try:
                for _sock, data in self.server_tcp_replay_data_queue.items():
                    while data:
                        self.doip_sock_obj.tcp_server_sock.async_send_message(_sock, data.popleft())
                if self.server_udp_replay_data_queue:
                    self.doip_sock_obj.udp_server_sock.udp_data(self.server_udp_replay_data_queue.popleft())
                time.sleep(0.01)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
                logger.warning(f"mock服务端发送数据错误：{e}")

    def __daemon_data_send(self, data_dict, sa, ta, _sock, key):
        """

        :param _sock:
        :param data_dict: {"replay_data": ['7F2278'], "replay_cycle": 0.5}
        :return:
        """
        try:
            if data_dict.get("replay_cycle"):
                cycle_time = float(data_dict["replay_cycle"])
            else:
                cycle_time = 0.5
            replay_data_list = []
            for i in data_dict["replay_data"]:
                if sa != 0x1fff:
                    data = self.doip_generate_service_0x8001(sa, ta, bytes.fromhex(i))
                    replay_data_list.append(data)
                    logger.info(f"Send: [{hex(sa)} -> {hex(ta)}] | {i}")
                else:
                    for ip, domain_list in self.function_route_ip_map.items():
                        if ip in self.local_ip_list:
                            for _sa in domain_list:
                                data = self.doip_generate_service_0x8001(
                                    _sa,
                                    ta,
                                    bytes.fromhex(i)
                                )
                                replay_data_list.append(data)
                                logger.info(
                                    f"Send: [{hex(sa)} -> {hex(ta)}] | {i}")
            while (self.doip_sock_obj.tcp_server_sock.listen_flag or self.doip_sock_obj.udp_server_sock.listen_flag) and self.mock_service_start_send_flag[key]:
                for data in replay_data_list:
                    self.server_tcp_replay_data_queue[_sock].append(data)
                time.sleep(cycle_time)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServerKeywords.py")
            logger.warning(f"模拟服务端发送周期信号失败：{e}")

    def mock_server_handler(self):
        Thread(target=self.__server_send_replay_handler, daemon=True).start()
        Thread(target=self.__routing_map_handler, daemon=True).start()

    def init_mock_data(self):
        self.doip_update_service_data_0x0004()
        self.doip_update_service_data_0x0006()
        self.doip_update_service_data_0x0008()
        self.doip_update_service_data_0x4002()
        self.doip_update_service_data_0x4004()

    def check_accept_message_count_by_domain(self,
                                             target_address,
                                             check_data,
                                             source_address=0x0e80,
                                             need_clear_accept_data=True):
        """
        检查BGM发送给模拟域控的数据，以及发送给域控的数据次数
        :param source_address: 发送诊断的源地址，如：0x0e80
        :param target_address: 发送诊断的目的地址，如：0x1401
        :param need_clear_accept_data: 检查后模拟端清楚接收到的消息
        :param check_data:  服务端接收到的数据，如下表示检测1101诊断数据接收到了3次，1103诊断数据接收到了2次:
                    {
                        "1101": 3,
                        "1103": 2
                    }
        """
        all_data = self.domain_accept_data_queue.get(f"{source_address}->{target_address}")
        logger.debug(f"accept all data is:{all_data}")
        for k, v in check_data.items():
            if all_data.count(k) != v:
                message = f"{hex(target_address)} accept {k} data count is:{all_data.count(k)},but expect count is:{v}"
                logger.warning(message)
                raise AssertionError(message)
        if need_clear_accept_data:
            self.clear_accept_message_by_domain(target_address=target_address, source_address=source_address)

    def clear_accept_message_by_domain(self,
                                       target_address,
                                       source_address=0x0e80):
        """
        清除BGM发送给模拟域控的数据
        :param source_address: 发送诊断的源地址，如：0x0e80
        :param target_address: 发送诊断的目的地址，如：0x1011
        """
        accept_data = self.domain_accept_data_queue.get(f"{source_address}->{target_address}")
        if accept_data:
            self.domain_accept_data_queue[f"{source_address}->{target_address}"].clear()

    def doip_generate_service_0x8001(self,
                                     source_address=None,
                                     target_address=None,
                                     diag_data=None
                                     ):
        """
        :param source_address: 发送诊断的源地址，如：0x0e80
        :param target_address: 发送诊断的目的地址，如：0x1002
        :param diag_data:  诊断数据，如: [0x10, 0x01]
        """
        data = deepcopy(doip_frame_raw_data_0x8001)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if diag_data:
            data["DataInfo"]["DiagData"] = bytes(diag_data)
        data["DataLen"] = 4 + len(diag_data)
        return doip_build(data)

    def update_function_diag_ip_route_map(self, data):
        """
        更新功能诊断功能路由与对应ip映射
        :param data:  诊断数据，如下：
        {
            "172.18.128.80": [0x1002, 0x1003],
            "172.18.128.184": [0x1011],
            "172.18.128.231": [0x1401],
        }
        """
        self.function_route_ip_map = data
        if self.remote_mock_server:
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)
            data = {"op_type": "update_mock_data", "function_ip_map": self.function_route_ip_map}
            self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty(data))

    def stop_mock_server_cycle_data(self, data):
        """
        停止模拟服务端周期性发送的数据
        :param data: {f"{0x1011}_{0x1001}": True}
        :return:
        """
        if not self.mock_service_start_send_flag.get(data):
            logger.warning(f"没有发现正在运行的：{data}")
        else:
            self.mock_service_start_send_flag[data] = False

    def doip_update_service_data_0x8001(self,
                                        diag_data=None,
                                        ack_code=None,
                                        nrc_code=None,
                                        ):
        """
        :param diag_data:  诊断数据，如下：
                {
                0x1fff: {
                    0x10: {
                        0x01: ['7F78', '5001'],
                        0X02: ['7F11'],
                        0X03: ['500300000000'],
                        0X04: []
                    }
                },
                0x1011: {
                    0x10: {
                        0x01: ['7F78', '5001'],
                        0X02: ['7F11'],
                        0X03: ['500300000000'],
                        0X04: []
                    },
                    0x11: {
                        0X01: ['5101'],
                        0X81: ['5181'],
                        0x21: []
                    },
                    0x19: {
                        0x01: ['5901010101']
                    },
                    0x14: {
                        0x01: ['5401']
                    },
                    0x22: {
                        0xf190: ['62010101010101010010101010101010102']
                    },
                    0x2E: {
                        0xf186: ['0000000000000']
                    }
                }
            }
        :param ack_code: {0x1011: 0, 0x1201: 0}
        :param nrc_code: {0x1401: 3, 0x1001: 1}
        """
        if self.remote_mock_server:
            self.clear_mock_data_0x8001()
            if not self.emq_obj.is_connected():
                self.emq_obj.connect(self.uds_host)

        if ack_code:
            self.ack_mock_data_0x8001.update(ack_code)
            if self.remote_mock_server:
                data = {"op_type": "update_mock_data", "ack_code": ack_code}
                self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty(data))
        if nrc_code:
            self.nack_mock_data_0x8001.update(nrc_code)
            if self.remote_mock_server:
                data = {"op_type": "update_mock_data", "nrc_code": self.nack_mock_data_0x8001}
                self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty(data))
        if diag_data:
            for domain, service_info in diag_data.items():
                if domain not in self.mock_data_0x8001:
                    self.mock_data_0x8001.update({domain: service_info})
                else:
                    for sub_id, data_info in service_info.items():
                        if sub_id not in self.mock_data_0x8001[domain]:
                            self.mock_data_0x8001[domain].update({sub_id: data_info})
                        else:
                            for k, v in data_info.items():
                                if k not in self.mock_data_0x8001[domain][sub_id]:
                                    self.mock_data_0x8001[domain][sub_id].update({k: v})
                                else:
                                    self.mock_data_0x8001[domain][sub_id][k] = v
            if self.remote_mock_server:
                data = {"op_type": "update_mock_data", "diag_data": self.mock_data_0x8001}
                self.emq_obj.publish(self.update_mock_data_topic, struct_json_pretty(data))

            self.mock_data_0x8001 = self.convert_str_keys_to_int(self.mock_data_0x8001, {})
            logger.info(f"更新服务端回复数据，当前数据是：{self.mock_data_0x8001}")

    def clear_mock_data_0x8001(self):
        self.mock_data_0x8001.clear()

    def doip_update_service_data_0x0000(self, nrc_code=None):
        data = deepcopy(doip_frame_raw_data_0x0000)
        if nrc_code:
            data["DataInfo"] = nrc_code
        return doip_build(data)

    def doip_update_service_data_0x0004(self,
                                        vin=None,
                                        logical_address=None,
                                        eid=None,
                                        gid=None,
                                        further_action_required=None):
        data = deepcopy(doip_frame_raw_data_0x0004)
        if vin:
            data["DataInfo"]["Vin"] = vin
        if logical_address:
            data["DataInfo"]["LogicalAddress"] = logical_address
        if eid:
            data["DataInfo"]["EID"] = bytes.fromhex(eid)
        if gid:
            data["DataInfo"]["GID"] = bytes.fromhex(gid)
        if further_action_required:
            data["DataInfo"]["FurtherActionRequired"] = further_action_required
        self.mock_server_data[0x0001].append(doip_build(data))
        self.mock_server_data[0x0002].append(doip_build(data))
        self.mock_server_data[0x0003].append(doip_build(data))

    def doip_update_service_data_0x0006(self,
                                        target_address=None,
                                        source_address=None,
                                        res_code=None,
                                        ):
        """
        构造0006的响应数据
        """
        data = deepcopy(doip_frame_raw_data_0x0006)
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if res_code:
            data["DataInfo"]["ResCode"] = res_code
        self.mock_server_data[0x0005].append(doip_build(data))

    def doip_update_service_data_0x0008(self, source_address=None):
        """
        响应那个逻辑地址是否在线
        :param source_address: 如0e80逻辑地址在线：0x0e80
        """
        data = deepcopy(doip_frame_raw_data_0x0008)
        if source_address:
            data["DataInfo"] = source_address
        self.mock_server_data[0x0007].append(doip_build(data))

    def doip_update_service_data_0x4002(self, node_type=None,
                                        tcp_data_max_numer=None,
                                        now_tcp_data_open_number=None):
        """
        :param node_type: 节点类型，0: doip网关；1: doip节点
        :param tcp_data_max_numer: tcp连接最大数
        :param now_tcp_data_open_number: 当前打开的数
        """
        data = deepcopy(doip_frame_raw_data_0x4002)
        if node_type:
            data["DataInfo"]["NodeType"] = node_type
        if tcp_data_max_numer:
            data["DataInfo"]["TCP_DATA_MAX_NUMBER"] = tcp_data_max_numer
        if now_tcp_data_open_number:
            data["DataInfo"]["NOW_TCP_DATA_OPEN_NUMBER"] = now_tcp_data_open_number
        self.mock_server_data[0x4001].append(doip_build(data))

    def doip_update_service_data_0x4004(self, mode=1):
        """
        :param mode: 诊断电源模式请求: 0：not ready 1:ready 2:not supported
        """
        data = deepcopy(doip_frame_raw_data_0x4004)
        data["DataInfo"] = mode
        self.mock_server_data[0x4003].append(doip_build(data))

    def doip_update_service_data_0x8002(self,
                                        source_address=None,
                                        target_address=None,
                                        return_code=None):
        data = deepcopy(doip_frame_raw_data_0x8002)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if return_code:
            data["DataInfo"]["ReturnCode"] = bytes(return_code)
        raw_data = doip_build(data)
        return raw_data

    def doip_update_service_data_0x8003(self,
                                        source_address=None,
                                        target_address=None,
                                        nrc_code=None):
        data = deepcopy(doip_frame_raw_data_0x8003)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if nrc_code:
            data["DataInfo"]["NRCCode"] = bytes(nrc_code)
        raw_data = doip_build(data)
        return raw_data
