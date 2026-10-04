# -*- coding: utf-8 -*-
"""
@File        : AutosarCP_pdu_common.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2024/10/20 10:17 PM
@Description : AutosarCP格式的PDU相关的通用内容
@Examples    : example of how to use it
"""

import importlib
import time
import math
import threading
from socket import *
from typing import Dict, List, Union
from scapy.all import sniff, wrpcap
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import SOCKET_IP_PORT, SERVER_SENDER_MAP


def channel_name_to_quadruple(channel: str):
    """
    根据以太网的channel name返回默认的DP2.0的ip和端口四元组
    :param channel: 以太网通道名，例如TcpChannel.CdMcuTCPServer_CdNadTCPClient1：‘CdMcuTCPServer_CdNadTCPClient1’
    :return: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
    """
    server_name, client_name = channel.split('_')
    return SOCKET_IP_PORT[server_name], SOCKET_IP_PORT[client_name]


def get_signal_value(payload, start_index, length, layout_format="Motorola MSB"):
    """
    从字符串格式payload中根据信号的起始位和长度计算信号值
    :param payload:  字符串的payload
    :param start_index:  起始bit位
    :param length:  信号占用bit长度
    :param layout_format:  字节排布顺序
    :return:
    """
    layout_format = layout_format.lower().replace(" ", '').strip()
    result = 0
    if layout_format == "motorolamsb":
        n = 1
        while (n * 8 - 1) < start_index:
            n = n + 1
        result = payload[(n - 1) * 8 - 1 + (8 - start_index % 8): ((n - 1) * 8 - 1 + (8 - start_index % 8) + length)]
    elif layout_format == "opaque":
        dbc_bit_layout = index_change_to_intel(start_index, length)
        result = "".join([payload[dbc_bit_to_bin_index(x)] for x in dbc_bit_layout])
    else:
        assert False, f"layout_format:{layout_format}异常"

    return int(result, 2)


def dbc_bit_to_bin_index(bit):
    """dbc中的bit位转成2进制数据中的index"""
    byte_index, bytes_mod = divmod(bit, 8)
    return byte_index * 8 + 7 - bytes_mod


def bin_index_to_dbc_bit(index):  # 暂未使用
    """2进制数据中的index在dbc中对应的bit位"""
    byte_index, bytes_mod = divmod(index, 8)
    return 8 * byte_index + 7 - bytes_mod


def index_change_to_intel(start_position, signal_length):
    """根据起始bit和长度，将信号值相关的bit以Intel格式输出
    @:param start_position: 起始bit位
    @:param signal_length: 信号长度
    举例start_position=12， signal_len=10
    15 14 13 12
          21 20 19 18 17 16
    :return [21, 20, 19, 18, 17, 16, 15, 14, 13, 12]
    """
    res = []
    end = start_position + signal_length - 1  # 12+10-1 = 21
    start_bytes_index = start_position // 8  # 1
    end_bytes_index = end // 8  # 2
    for i in range(start_bytes_index, end_bytes_index + 1):  # 1, 2
        tmp_list = list(reversed([8 * i + x for x in range(8)]))  # 15,14,13,12,11,10,9,8 | 23,22,21,20,19,18,17,16
        if i == start_bytes_index:  # 起始字节
            for x in tmp_list:
                if start_position <= x <= end:  # 15,14,13,12
                    res.append(x)
        elif i == end_bytes_index:  # 结束字节
            res = tmp_list[len(res) - signal_length:] + res  # 21,20,19,18,17,16
        else:  # 中间字节
            res = tmp_list + res
    return res


def index_change_to_motorola_msb(start_position, signal_length):
    """根据起始bit和长度，将信号值相关的bit以Motorola_msb格式输出
    @:param start_position: 起始bit位
    @:param signal_length: 信号长度
    举例start_position=12， signal_len=10
             12 11 10  9  8
    23 22 21 20 19
    :return  MSB： [12,11,10,9,8,23,22,21,20,19]
    """
    res = []
    start_bytes_index = start_position // 8  # 1
    start_byte_valid_bit = start_position - (8 * start_bytes_index - 1)  # 12-7 = 5
    if signal_length <= start_byte_valid_bit:
        end_bytes_index = start_bytes_index
    else:
        end_bytes_index = start_bytes_index + math.ceil((signal_length - start_byte_valid_bit) / 8)  # 1+(10-5)//8 = 2
    # end = start_position + signal_length - 1  # 12+10-1 = 21
    for i in range(start_bytes_index, end_bytes_index + 1):  # 1, 2
        tmp_list = list(reversed([8 * i + x for x in range(8)]))  # 15,14,13,12,11,10,9,8 | 23,22,21,20,19,18,17,16
        if i == start_bytes_index:  # 起始字节
            for x in tmp_list:
                if start_position >= x and len(res) < signal_length:  # 12,11,10,9,8
                    res.append(x)
            if signal_length == len(res):  # 信号bit在一个字节内
                return res
        elif i == end_bytes_index:  # 结束字节
            res.extend(tmp_list[0:signal_length - len(res)])  # 0:(10-5), 23,22,21,20,19
        else:  # 中间字节
            res.extend(tmp_list)
    return res


def index_change_to_motorola_lsb(start_position, signal_length):
    """根据起始bit和长度，将信号值相关的bit以Motorola_lsb格式输出
    @:param start_position: 起始bit位
    @:param signal_length: 信号长度
    举例start_position=12， signal_len=10
           5  4  3  2  1  0
    15 14 13 12
    :return  LSB： [5,4,3,2,1,0,15,14,13,12]
    """
    return []


class SignalObj:
    def __init__(self):
        self.pdu_length = 0
        self.hex_str_pdu_header = ""
        self.hex_str_pdu_header_length = ""
        self.start_position = 0
        self.signal_length = 0
        self.factor = 0
        self.offset = 0
        self.sender = ""
        self.initial_value = 0
        self.signals_value_list: List[SignalItemInfo] = []  # 信号值对象列表，每一个值的数据结构为：SignalItemInfo
        self.downstream = False  # 是否是下行信号
        self.name = ""
        self.layout_format = ""
        self.sig_ub = None

    def __repr__(self):
        return f"name: {self.name}, header_length:{self.hex_str_pdu_header_length}, " \
               f"start_position:{self.start_position}, signal_length:{self.signal_length}, factor:{self.factor}, " \
               f"offset:{self.offset}, sender: {self.sender}, initial_value: {self.initial_value}, " \
               f"sig_ub: {self.sig_ub}"


class SignalItemInfo:
    """pcap中的信号对象"""

    def __init__(self):
        self.timestamp = 0
        self.signal_value = 0

    def __repr__(self):
        return f"({round(self.timestamp, 3)}, {self.signal_value})"


class EthChannelDb:
    """以太网数据库的操作集合，包括数据库加载，解析，设置信号，解析信号，pdu组包"""

    def __init__(self, veh_type="jupiter", bl_ver="v_0_4_0", channel=''):
        self.eth_channel_module = importlib.import_module(f"xat_ecu.legacy.sdk.data.{veh_type}.eth.{bl_ver}.{channel}")
        logger.info("动态模块名是：{}".format(self.eth_channel_module.__name__))
        self.periodic_pdus: List[int] = []  # [pduid1, pduid2], 用于控制周期pdu的发送
        self.sig_info_dict: Dict[str, SignalObj] = {}  # {signal_name: SignalObj}, 用于信号解析后存放数据，以及设置信号值的存储
        self.pduid_sigobjs_map: Dict[
            int, List[SignalObj]] = {}  # {pduid: [SignalObj1, SignalObj2, SignalObj3]}, 用于获取到一帧数据后快速解析所有信号
        self.pduid_pduobj_map = {}  # pdu_header_id与报文对象的映射字典，用于根据pduid发送pdu对象
        self.signal_pduid_map = {}  # signal和pduid的映射 {signal1: pduid1, signal2: pduid1, signal3: pduid2}，用于设置信号后发送pdu
        self.parse_eth_database(self.eth_channel_module)

        self.errors = []  # 存储异常,todo

    def parse_eth_database(self, eth_channel_module):
        """
        从内部以太网数据库中根据以太网报文名称获取报文的初始值
        :param eth_channel_module : 以太网通道加载后的模块
        :return:
        """
        for ethernet_pdu_name in dir(eth_channel_module):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
            if "EthSignalIPdu" not in ethernet_pdu_name:
                continue
            pdu_obj = getattr(eth_channel_module, ethernet_pdu_name)
            pdu_id = pdu_obj.pdu_header_id
            pdu_header_id_list = DataTypeHanding.to_intlist(pdu_id, 4)
            pdu_length_list = DataTypeHanding.to_intlist(pdu_obj.pdu_length_bytes, 4)

            self.pduid_sigobjs_map[pdu_id] = []
            # 解析pdu信号对象
            for signal_name in dir(pdu_obj):
                if "__" in signal_name:
                    continue
                signal_obj = getattr(pdu_obj, signal_name)
                if type(signal_obj) in [str, dict, int, list]:
                    continue
                # 不是int，str，dict则是eth信号对象，此时的pdu_attr_name为eth信号名

                signal = SignalObj()
                signal.start_position = signal_obj.start_position
                signal.signal_length = signal_obj.signal_length
                signal.layout_format = signal_obj.layout_format
                signal.offset = signal_obj.offset
                signal.factor = signal_obj.factor
                signal.sender = pdu_obj.sender
                signal.initial_value = signal_obj.initial_value
                signal.pdu_length = pdu_obj.pdu_length_bytes
                signal.name = signal_name
                signal.sig_ub = signal_obj.sig_ub

                self.signal_pduid_map[signal_name] = pdu_id
                self.sig_info_dict[signal_name] = signal
                self.pduid_sigobjs_map[pdu_id].append(signal)

            # 设置pdu数据
            setattr(pdu_obj, "send_flag", False)  # 设置周期报文是否持续发送
            setattr(pdu_obj, "pdu_data", [])  # pdu当前组包的数据，每次设置信号后触发
            setattr(pdu_obj, "pdu_id_length_list", pdu_header_id_list + pdu_length_list)
            setattr(pdu_obj, "cycle_time", None)
            if "Cyclic-" in getattr(pdu_obj, "send_type"):
                self.periodic_pdus.append(pdu_id)
                setattr(pdu_obj, "cycle_time", int(pdu_obj.send_type.replace("Cyclic-", "").replace("ms", "")))
            self.pduid_pduobj_map[pdu_id] = pdu_obj
            self.combine_pdu_data(pdu_id)

    def parse_signal(self, load: bytes, timestamp: float):
        """
        解析信号
        :param load: 一帧下行tcp数据，pdu_id(4 bytes) + pdu_len(4 bytes) + payload
        :param timestamp: tcp发送时间戳(代码运行所在系统的时间)
        :return:
        """
        pdu_id = DataTypeHanding.to_int(load[0: 4])
        payload_hex_string = DataTypeHanding.to_hexstr(load[8:])
        payload_bin_string = bin(int(payload_hex_string, 16))[2:].rjust(8 * DataTypeHanding.to_int(load[4: 8]), '0')
        if pdu_id not in self.pduid_sigobjs_map:
            msg = f'{time.time()}--pduid{pdu_id}异常，软件出现bug'
            logger.error(msg)
            self.errors.append(ValueError(msg))
            return
        for signal_obj in self.pduid_sigobjs_map[pdu_id]:
            signal_item = SignalItemInfo()
            signal_item.timestamp = timestamp
            signal_item.signal_value = get_signal_value(payload_bin_string,
                                                        signal_obj.start_position,
                                                        signal_obj.signal_length,
                                                        signal_obj.layout_format)
            self.sig_info_dict[signal_obj.name].signals_value_list.append(signal_item)

    def set_signal(self, signal_name: str, signal_value: Union[int, float]):
        """
        设置信号值
        :param signal_name: 信号名
        :param signal_value: 信号值，如果是float就是物理值，如果是int就是总线值
        :return:
        """
        signal = self.sig_info_dict[signal_name]
        if isinstance(signal_value, float):
            new_signal_value = (signal_value - signal.offset) / signal.factor
            #  四舍五入
            if new_signal_value >= 0:
                new_signal_value = int(new_signal_value + 0.5)
            else:
                new_signal_value = int(new_signal_value - 0.5)
            signal.initial_value = new_signal_value
        else:
            signal.initial_value = signal_value
        return self.combine_pdu_data(self.signal_pduid_map[signal_name])

    def combine_pdu_data(self, pduid):
        """
        重新计算并返回帧报文的pdu_data，发送周期
        :param pduid: 报文id
        :return: 组包后的pdu_data_list
        """
        if pduid not in self.pduid_pduobj_map:
            raise ValueError(f"输入的{pduid}不在数据库内")
        pdu_obj = self.pduid_pduobj_map[pduid]
        pdu_length = pdu_obj.pdu_length_bytes
        bytes_list = DataTypeHanding.to_intlist(0, pdu_length)
        binary_string = ''.join(bin(b)[2:].zfill(8) for b in bytes_list)  # 转成二进制数据
        binary_list = list(binary_string)
        for signal_obj in self.pduid_sigobjs_map[pdu_obj.pdu_header_id]:
            initial_value = signal_obj.initial_value
            start_position = signal_obj.start_position
            signal_length = signal_obj.signal_length
            if signal_length > pdu_length * 8:
                signal_length = pdu_length * 8
                logger.warning(f"{signal_obj.name}长度超出pdu长度，请检查sdb")

            signal_value_bin_list = list(bin(initial_value)[2:].zfill(signal_length))
            if signal_obj.layout_format == "Motorola MSB":
                signal_bit_in_dbc_index = index_change_to_motorola_msb(start_position, signal_length)
            elif signal_obj.layout_format == "Opaque":
                signal_bit_in_dbc_index = index_change_to_intel(start_position, signal_length)
            else:  # 暂未使用
                signal_bit_in_dbc_index = index_change_to_motorola_lsb(start_position, signal_length)

            for index, signal_value_bit in enumerate(signal_value_bin_list):
                binary_list[dbc_bit_to_bin_index(signal_bit_in_dbc_index[index])] = signal_value_bit
            if signal_obj.sig_ub is not None:
                ub_idx = dbc_bit_to_bin_index(signal_obj.sig_ub)
                binary_list[ub_idx] = 1  # 信号如果有UB位，则保持1

        pdu_value_str = "".join([str(x) for x in binary_list])
        new_list = []
        for i in range(int(len(pdu_value_str) / 8)):
            curr_bin_str = pdu_value_str[8 * i:(8 * i + 8)]
            new_list.append(int(curr_bin_str, 2))
        else:
            res = pdu_obj.pdu_id_length_list + new_list
            pdu_obj.pdu_data = res
            return res


class EthControlBase:
    """
    以太网总线控制的基类，包括周期报文的发送，停止
    tcp和udp可以继承该类进行开发
    """

    def __init__(self, channel: str, veh_type="jupiter", bl_ver="v_0_4_0"):
        self.channel = channel
        self.server, self.client = self.channel.split('_')
        self.db = EthChannelDb(veh_type, bl_ver, channel)
        self.running = True
        self.t_errors = []

    def stop_running(self):
        """释放所有资源, 当前是停止周期报文发送"""
        self.running = False

    def send_data(self, data: List[int]):
        """
        发送报文原子能力，父类无能力，需要派生类实现
        :param data: data
        :return:
        """

    def start_send_all_cycle_pdu(self, sender=None):
        """
        启动所有周期报文的发送, 但是发送依赖置位send_flag
        :param sender: 数据库中pdu的sender属性
        :return:
        """
        for pduid in self.db.periodic_pdus:
            if sender is None:
                sender = SERVER_SENDER_MAP[self.server]
            if self.db.pduid_pduobj_map[pduid].sender != SERVER_SENDER_MAP[self.server]:
                continue
            self._start_cycle_send(pduid)

    def stop_send_cycle_pdu(self, pduid: int):
        """
        停止周期发送报文
        :param pduid: 报文id
        :return:
        """
        setattr(self.db.pduid_pduobj_map[pduid], 'send_flag', False)

    def stop_send_all_cycle_pdu(self, sender=None):
        """
        停止所有周期发送报文
        :sender: 数据库中pdu的sender属性
        :return:
        """
        for pduid in self.db.periodic_pdus:
            if sender is None:
                sender = SERVER_SENDER_MAP[self.server]
            if self.db.pduid_pduobj_map[pduid].sender != SERVER_SENDER_MAP[self.server]:
                continue
            self.stop_send_cycle_pdu(pduid)

    def resume_send_cycle_pdu(self, pduid: int):
        """
        恢复周期发送报文
        :param pduid:报文id
        :return:
        """
        setattr(self.db.pduid_pduobj_map[pduid], 'send_flag', True)

    def resume_send_all_cycle_pdu(self, sender=None):
        """
        停止所有周期发送报文
        :sender: 数据库中pdu的sender属性
        :return:
        """
        for pduid in self.db.periodic_pdus:
            if sender is None:
                sender = SERVER_SENDER_MAP[self.server]
            if self.db.pduid_pduobj_map[pduid].sender != SERVER_SENDER_MAP[self.server]:
                continue
            self.resume_send_cycle_pdu(pduid)

    def _start_cycle_send(self, pduid):
        """
        设启动周期发送pduid的报文
        :param pduid: 报文id
        :return:
        """
        pdu_obj = self.db.pduid_pduobj_map[pduid]
        cycle_time = pdu_obj.cycle_time
        t_send = threading.Thread(target=self._send_cycle_pdu_thread,
                                  args=(pduid, cycle_time),
                                  name=f'周期发送{hex(pduid)}',
                                  daemon=True)
        t_send.start()

    def _send_cycle_pdu_thread(self, pduid, cycle_time):
        """
        周期发送报文的线程
        :param pduid: 报文id
        :param cycle_time: 发送周期，ms
        :return:
        """
        while self.running:
            if self.db.pduid_pduobj_map[pduid].send_flag:
                self.send_pdu(pduid)
                time.sleep(cycle_time / 1000)
            else:
                time.sleep(0.001)

    def _send_trigger_pdu_thread(self, pduid, send_num, cycle_time):
        """
        按指定周期发送事件帧一定次数
        :param pduid: 报文id
        :param cycle_time: 发送周期，ms
        :return:
        """
        while send_num != 0:
            self.send_pdu(pduid, send_num, cycle_time)
            time.sleep(cycle_time / 1000)
            send_num -= 1

    def set_signal_and_send(self, signal_name, signal_value, send_pdu_immediately=False, send_num=1, cycle_time=5):
        """
        设定Event Trigger类型帧中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否立即发送
        @param send_num: 如果立即发送，指定发送次数，默认1次
        @param cycle_time: 如果立即发送，指定发送周期，默认5ms
        """
        self.db.set_signal(signal_name, signal_value)
        if send_pdu_immediately:
            self.send_pdu(self.db.signal_pduid_map[signal_name], send_num, cycle_time)

    def send_pdu(self, pduid: int, send_num=1, cycle_time=5):
        """
        发送pdu数据
        @param pduid: 报文id
        @param send_num: 指定发送次数，默认1次
        @param cycle_time: 指定发送周期，默认5ms
        :return:
        """
        if send_num == 1:
            self.send_data(self.db.pduid_pduobj_map[pduid].pdu_data)
        else:
            t_send = threading.Thread(target=self._send_trigger_pdu_thread, args=(pduid, send_num, cycle_time))
            t_send.start()


if __name__ == '__main__':
    a = EthChannelDb(channel="LcuRSoAdUDP_CdSocSoAdUDP")
    print(a.set_signal('PwrContnsChRiCfgStsContnsRiCh1CfgSts', 1))


