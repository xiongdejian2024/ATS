# -*- coding: utf-8 -*-

"""
@File        : bgm_eth_internal.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/10/31 14:51 PM
@Description : BGM内部以太网信号操作-dp20
@Examples    : example of how to use it
"""
import re
import importlib
import signal
import time
from datetime import datetime
from xat_ecu.legacy.soa_partner.src.base_partner_dp20 import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.eth_internal_router import *
from xat_ecu.legacy.utils.utils import exec_shell_command


forward_client = "CD_McuForwarderService_client"


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
    """根据起始bit和长度，将信号值相关的bit以Intel格式输出, """
    res = []
    end = start_position + signal_length - 1
    start_bytes = start_position // 8
    end_bytes = end // 8
    for i in range(start_bytes, end_bytes + 1):
        tmp_list = list(reversed([8 * i + x for x in range(8)]))
        if i == start_bytes:
            for x in tmp_list:
                if start_position <= x <= end:
                    res.append(x)
        elif i == end_bytes:
            res.extend(tmp_list[len(res) - signal_length:])
        else:
            res.extend(tmp_list)
    return res


def kill_process_by_port(port):
    cmd = os.popen(f'lsof -i :{port}')
    data = cmd.read()
    try:
        for i in data.split('\n'):
            process = re.findall(r".*\s+(\d+)\s+root.*", i)
            if process:
                logger.info(f"发现：{process[0]}|{i}")
                exec_shell_command(f"kill -9 {process[0]}")
                logger.info(f"=========================")
    finally:
        cmd.close()


def start_mcu_router(server_ip, server_port):
    """ 启动mcu router进程"""
    router_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eth_internal_router.py')
    start_cmd = f'python3 {router_path} {server_ip} {server_port}'
    logger.info(f"start_mcu_router: command:{start_cmd}")
    process = subprocess.Popen(start_cmd, shell=True, close_fds=True, preexec_fn=os.setsid)
    return process


class partner_client(tcp_socket_client):

    def __init__(self, threadID, name, server_ip, server_port, callback_func, receive_timeout=900):
        super().__init__(threadID, name)
        self.server_ip = server_ip
        self.server_port = server_port
        self.callback_func = callback_func
        self.connect(self.server_ip, self.server_port)
        self.cb = []
        self.set_receive_timeout(receive_timeout)
        self.cb.append(self.get_message_from_router)
        self.start()

    def send_method_request(self, role, method_name, args_dict):
        request_data = {"function": method_name, "args": json.dumps(args_dict)}
        socket_request_data = pickle.dumps(request_data)
        self.send(socket_request_data)

    def get_message_from_router(self, payload_data):
        payload_data = pickle.loads(bytes(payload_data))
        self.callback_func("eth_internal_router", payload_data)

    def stop_operators(self):
        self.close()


class SignalItemInfo:
    """pcap中的信号对象"""

    def __init__(self):
        self.sequence = 0
        self.timestamp = 0
        self.signal_value = 0

    def __repr__(self):
        return f"sequence: {self.sequence}, timestamp:{self.timestamp}, signal_value:{self.signal_value}"


class TcpPacket:
    """解析以太网数据包的属性信息"""

    def __init__(self, index, timestamp, payload,
                 payload_start, payload_length):
        self.index = index
        self.timestamp = timestamp
        self.payload = payload
        self.payload_start = payload_start  # 在总数据包中的起始字节
        self.payload_length = payload_length  # 该以太网帧的data的字节长度

    def __repr__(self):
        detail = f"报文序号：{self.index}, 时间戳：{self.timestamp}, 起始位置:{self.payload_start}, " \
                 f"报文长度：{self.payload_length}, 报文内容：{self.payload}"
        return detail


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
        self.signals_value_list = []
        self.name = ""
        self.layout_format = ""
        self.sig_ub = None
        self.ub_flag = True

    def __repr__(self):
        return f"PDU ID: {self.hex_str_pdu_header}, header_length:{self.hex_str_pdu_header_length}, " \
               f"start_position:{self.start_position}, signal_length:{self.signal_length}, factor:{self.factor}, " \
               f"offset:{self.offset}, sender: {self.sender}, initial_value: {self.initial_value}"


class ChannelConfig:
    """
    单个通道配置信息，包含本地IP、本地port、远程IP、远程端口、传输协议，提供通道内接收到的payload的解析、该通道下信号的发送
    对于UDP通道，优先创建单播通道，如果组播找不到对于的单播的话，再创建
    """

    def __init__(self, channel_name, localIpAddress, localPort, remoteIpAddress, remotePort,
                 transport_protocol, partner, mock_ecu, multicast_ip):
        """
        @param channel_name: 通道的名字
        @param transport_protocol: 通道的类型：发送通道、接收通道
        """
        self.channel_name = channel_name
        self.localIpAddress = localIpAddress
        self.localPort = localPort
        self.remoteIpAddress = remoteIpAddress
        self.remotePort = remotePort
        self.transport_protocol = transport_protocol
        self.mock_ecu = mock_ecu
        self.is_multicast_channel = False  # 默认单播通道
        self.multicast_ip = multicast_ip

        self.receive_data = ""  # 从该通道获取到的数据
        self.tcp_packet_list = []  # 元素类型：TcpPacket 存放当前通道下收到的payload 包含 index、时间戳、payload

        self.signal_info_dict = {}  # 信号的名称与信号对象的映射
        self.pduid_obj_mapping = {}  # 根据pdu id找到对应的pdu对象
        self.active_cycle_message_list = []  # 保存周期性报文中已经开始发送的报文
        self.partner = partner
        self.event_data_index = 0

    def add_tcp_packet(self, hex_str, time_stamp=0):
        """当前通道收到payload后，进行追加保存"""
        i = self.event_data_index + 1
        self.event_data_index = i
        curr_tcp_info = TcpPacket(i, time_stamp, hex_str, len(self.receive_data), int(len(hex_str)))
        self.receive_data += hex_str
        self.tcp_packet_list.append(curr_tcp_info)

    def empty(self):
        """重置当前通道的接收缓存"""
        self.event_data_index = 0
        self.receive_data = ""
        self.tcp_packet_list = []

    def parse_signal_info(self, signal_obj: SignalObj):
        """将pcap解出来的上下行payload解析出指定的以太网信号数据"""
        curr_index = 0
        signal_value_list = []
        payload = self.receive_data
        for i in range(payload.count(signal_obj.hex_str_pdu_header_length)):
            index = payload.index(signal_obj.hex_str_pdu_header_length, curr_index)
            if index % 2 == 1:
                curr_index = index + 1
                continue
            hex_str = payload[index:index + (8 + signal_obj.pdu_length) * 2]  # 输入要转换的十六进制字符串
            binary_str = bin(int(hex_str, 16))[2:]  # 先将十六进制字符串转换为整数，再通过bin()函数得到对应的二进制字符串

            result = binary_str.replace(bin(int(signal_obj.hex_str_pdu_header_length, 16))[2:], "")
            curr_index = index + 1
            signal_item = SignalItemInfo()
            signal_item.timestamp, signal_item.sequence = self.get_timestamp(index)
            if len(result) >= signal_obj.start_position:
                signal_item.signal_value = get_signal_value(result, signal_obj.start_position, signal_obj.signal_length,
                                                            signal_obj.layout_format)
            else:
                continue
            signal_value_list.append(signal_item)
            self.signal_info_dict[signal_obj.name].signals_value_list.append(signal_item)

    def get_signal_values(self, signal_name):
        """
        获取给到信号的信号值列表
        @param signal_name: 指定的信号名
        return: 信号值列表[value1, value2, value3...]
        """
        signal_obj = self.signal_info_dict[signal_name]
        self.parse_signal_info(signal_obj)  # 生成信号值信息
        signal_value_tuple_list = []
        signal_items = []
        for signal_value in self.signal_info_dict[signal_name].signals_value_list:
            signal_value_tuple_list.append(signal_value.signal_value)
            signal_items.append((signal_value.sequence, signal_value.timestamp, signal_value.signal_value))
        logger.info(f"{signal_name}信号值>>>> {signal_value_tuple_list}")
        return signal_value_tuple_list

    def all_cycle_frame_calculation_pdu_data(self):
        """
            放在线程中，设置发送方是Soc的需要自动周期发送的帧
            1、判断是否正在发送：维护正在发送列表；
            2、计算、更新pdu_data、send_type；
        """
        for pdu_id in self.pduid_obj_mapping:
            ethernet_pdu = self.pduid_obj_mapping[pdu_id]
            if "Cyclic" in ethernet_pdu.send_type:
                time.sleep(0.005)  # 控制首次周期报文发送，使其发送时间分散
                ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)
                ethernet_pdu_cycle = int(ethernet_pdu.send_type.replace("Cyclic-", "").replace("ms", ""))
                setattr(ethernet_pdu, "cycle_time", ethernet_pdu_cycle)  # 计算pdu_data 的同时设置周期毫秒数
        else:
            time.sleep(0.02)

    def __calculation_pdu_data(self, ethernet_pdu):
        """重新计算并返回帧报文的pdu_data，发送周期"""
        ub_set = []
        pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
        pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
        pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
        pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
        bytes_list = DataTypeHanding.to_intlist(0, pdu_length)
        binary_string = ''.join(bin(b)[2:].zfill(8) for b in bytes_list)
        pdu_value_list = list(binary_string)
        for pdu_attr_name in dir(ethernet_pdu):
            if "__" not in pdu_attr_name and pdu_attr_name not in ["send_flag", "change_flag", "pdu_data",
                                                                   "last_send_time", "receiver"]:
                pdu_sub_obj = getattr(ethernet_pdu, pdu_attr_name)
                if not isinstance(pdu_sub_obj, int):
                    if not isinstance(pdu_sub_obj, str):
                        if not isinstance(pdu_sub_obj, dict):
                            initial_value = self.signal_info_dict[pdu_attr_name].initial_value
                            start_position = getattr(pdu_sub_obj, 'start_position')
                            signal_length = getattr(pdu_sub_obj, 'signal_length')
                            signal_bytes_position = 0
                            for n in range(pdu_length):
                                if (n + 1) * 8 > start_position:
                                    signal_bytes_position = n
                                    break
                            signal_value_list = list(bin(initial_value)[2:].zfill(signal_length))
                            index = 0
                            for signal_value_bit in signal_value_list:
                                seq = signal_bytes_position * 8 - 1 + (8 - start_position % 8) + index
                                if seq < len(pdu_value_list):
                                    pdu_value_list[seq] = signal_value_bit
                                    index = index + 1
                                else:
                                    break
                            else:
                                sig_ub = self.signal_info_dict[pdu_attr_name].sig_ub
                                ub_flag = self.signal_info_dict[pdu_attr_name].ub_flag
                                if sig_ub is not None:
                                    if ub_flag is True:
                                        if sig_ub not in ub_set:
                                            ub_idx = dbc_bit_to_bin_index(sig_ub)
                                            pdu_value_list[ub_idx] = "1"  # 信号如果有UB位，则保持1
                                    else:
                                        ub_idx = dbc_bit_to_bin_index(sig_ub)
                                        pdu_value_list[ub_idx] = "0"
                                        if sig_ub not in ub_set:
                                            ub_set.append(sig_ub)
        else:
            pdu_value_str = "".join(pdu_value_list)
            new_list = []
            for i in range(int(len(pdu_value_str) / 8)):
                curr_bin_str = pdu_value_str[8 * i:(8 * i + 8)]
                new_list.append(int(curr_bin_str, 2))
            else:
                pdu_header_id_list.extend(pdu_length_list)
                pdu_header_id_list.extend(new_list)
                return pdu_header_id_list

    def start_all_cycle_message_send(self):
        """
        发送该通道下的所有的周期报文
        """
        counter = 0
        for pdu_id in self.pduid_obj_mapping:
            ethernet_pdu = self.pduid_obj_mapping[pdu_id]
            if "Cyclic-" in ethernet_pdu.send_type and ethernet_pdu.sender == self.mock_ecu:  # 周期报文且发送方是模拟的ECU
                if ethernet_pdu.multicast_flag:
                    msgName = f"cycle-multicast-{pdu_id}"
                else:
                    msgName = f"cycle-signal-{pdu_id}"
                self.partner.send_method_request(forward_client, "startSendMessage",
                                                 {"channelName": self.channel_name,
                                                  "payload": ethernet_pdu.pdu_data,
                                                  "msgAttr": {"msgName": msgName,
                                                              "isCycle": True,
                                                              "ivl": ethernet_pdu.cycle_time,  # 周期发送间隔
                                                              "cnt": 0}})
                counter += 1
                time.sleep(0.1)
        else:
            logger.info(f"start_all_cycle_message_send: {self.channel_name} 下的周期报文数为：{counter} 。")

    def stop_all_cycle_message_send(self):
        """
        发送该通道下的所有的周期报文
        """
        counter = 0
        for pdu_id in self.pduid_obj_mapping:
            ethernet_pdu = self.pduid_obj_mapping[pdu_id]
            if "Cyclic-" in ethernet_pdu.send_type and ethernet_pdu.sender == self.mock_ecu:  # 周期报文且发送方是模拟的ECU
                if ethernet_pdu.multicast_flag:
                    msgName = f"cycle-multicast-{pdu_id}"
                else:
                    msgName = f"cycle-signal-{pdu_id}"
                self.partner.send_method_request(forward_client, "stopSendMessage",
                                                 {"channelName": self.channel_name,
                                                  "msgName": msgName})
                logger.info(f"停发周期数据: {self.channel_name}, {ethernet_pdu.pdu_data}")
                counter += 1
                time.sleep(0.1)
        else:
            logger.info(f"stop_all_cycle_message_send: {self.channel_name} 下的周期报文数为：{counter} 。")

    def send_pdu(self, pdu_id: int, send_num=1, send_cyclic=10):
        """
        发送PDU报文

        :param pdu_id: 报文ID, 数据类型：int，为excel的PDU Header ID列
        :param send_num: 发送次数，默认为1
        :param send_cyclic: 发送周期，仅对Trigger类型的报文有效，默认10毫秒
        """
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"send_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        if ethernet_pdu.sender != self.mock_ecu:  # 周期报文且发送方是模拟的ECU
            logger.info(f"send_pdu: {self.channel_name} 不支持的报文ID：{pdu_id}")
            return
        if "Cyclic-" in ethernet_pdu.send_type:
            time.sleep(0.005)  # 控制首次周期报文发送，使其发送时间分散
            ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)
            logger.info(
                f"send_pdu: channel:{self.channel_name}, cycle_pdu_id:{pdu_id}, payload:{ethernet_pdu.pdu_data}")
            ethernet_pdu_cycle = int(ethernet_pdu.send_type.replace("Cyclic-", "").replace("ms", ""))
            setattr(ethernet_pdu, "cycle_time", ethernet_pdu_cycle)  # 计算pdu_data 的同时设置周期毫秒数
            if ethernet_pdu.multicast_flag:
                msgName = f"cycle-multicast-{pdu_id}"
            else:
                msgName = f"cycle-signal-{pdu_id}"
            self.partner.send_method_request(forward_client, "startSendMessage",
                                             {"channelName": self.channel_name,
                                              "payload": ethernet_pdu.pdu_data,
                                              "msgAttr": {"msgName": msgName,
                                                          "isCycle": True,
                                                          "ivl": ethernet_pdu.cycle_time,  # 周期发送间隔
                                                          "cnt": 0}})
        else:
            ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)
            logger.info(
                f"send_pdu: channel:{self.channel_name}, trigger_pdu_id:{pdu_id}, payload:{ethernet_pdu.pdu_data}")
            self.partner.send_method_request(forward_client, "startSendMessage",
                                             {"channelName": self.channel_name,
                                              "payload": ethernet_pdu.pdu_data,
                                              "msgAttr": {"msgName": f"trigger-{pdu_id}",
                                                          "isCycle": True,
                                                          "ivl": send_cyclic,  # 发送间隔
                                                          "cnt": send_num}})

    def stop_send_single_pdu(self, pdu_id: int):
        """
        停止发送单个PDU报文
        :param pdu_id: 报文ID
        """
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"stop_send_single_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        if ethernet_pdu.sender != self.mock_ecu:  # 周期报文且发送方是模拟的ECU
            logger.info(f"stop_send_single_pdu: {self.channel_name} 不支持的报文ID：{pdu_id}")
            return

        self.partner.send_method_request(forward_client, "stopSendMessage",
                                         {"channelName": self.channel_name,
                                          "msgName": f"cycle-{pdu_id}"})
        logger.info(
            f"stop_send_single_pdu: channel:{self.channel_name}, cycle_pdu_id:{pdu_id},payload:{ethernet_pdu.pdu_data}")

    def set_signal_value(self, pdu_id, signal_name, signal_value, ub_flag: bool, set_num=1, send_cycle=100):
        """
        设定周期类型帧中的指定信号的数值
        @param pdu_id:
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param ub_flag : UB位设置，True为1，False为0
        @param set_num : 设置发送次数
        @param send_cycle : 发送周期
        """
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        if ethernet_pdu.sender != self.mock_ecu:  # 周期报文且发送方是模拟的ECU
            logger.info(f"set_signal_value: {self.channel_name} 不支持的报文ID：{pdu_id}")
            return
        if signal_name in dir(ethernet_pdu):
            pdu_sub_obj = getattr(ethernet_pdu, signal_name)
            signal = self.signal_info_dict[signal_name]
            if isinstance(signal_value, float):
                new_signal_value = (signal_value - signal.offset) / signal.factor
                #  四舍五入
                if new_signal_value >= 0:
                    new_signal_value = int(new_signal_value + 0.5)
                else:
                    new_signal_value = int(new_signal_value - 0.5)
                signal.initial_value = new_signal_value
                setattr(pdu_sub_obj, 'initial_value', new_signal_value)
            else:
                signal.initial_value = signal_value
                setattr(pdu_sub_obj, 'initial_value', signal_value)
            setattr(pdu_sub_obj, 'ub_flag', ub_flag)
            ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)  # 更新其值
            time.sleep(0.01)
            if "Cyclic-" in ethernet_pdu.send_type:  # 对于周期报文，即刻通知mcu Forward进行对应报文的payload修改
                self.send_pdu(pdu_id)
            else:
                self.send_pdu(pdu_id, send_num=set_num, send_cyclic=send_cycle)

    def set_multiple_signal_value(self, pdu_id, sig_dict, ub_flag: bool, set_num=1, send_cycle=100):
        """
        设定周期类型帧中的指定信号的数值
        @param pdu_id:
        @param sig_dict:  {"signal1": value, "signal2": value1}
        @param ub_flag : UB位设置，True为1，False为0
        @param set_num : 设置发送次数
        @param send_cycle : 发送周期
        """
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        if ethernet_pdu.sender != self.mock_ecu:  # 周期报文且发送方是模拟的ECU
            logger.info(f"set_signal_value: {self.channel_name} 不支持的报文ID：{pdu_id}")
            return
        for signal_name, signal_value in sig_dict.items():
            if signal_name in dir(ethernet_pdu):
                pdu_sub_obj = getattr(ethernet_pdu, signal_name)
                signal = self.signal_info_dict[signal_name]
                if isinstance(signal_value, float):
                    new_signal_value = (signal_value - signal.offset) / signal.factor
                    #  四舍五入
                    if new_signal_value >= 0:
                        new_signal_value = int(new_signal_value + 0.5)
                    else:
                        new_signal_value = int(new_signal_value - 0.5)
                    signal.initial_value = new_signal_value
                    setattr(pdu_sub_obj, 'initial_value', new_signal_value)
                else:
                    signal.initial_value = signal_value
                    setattr(pdu_sub_obj, 'initial_value', signal_value)
                setattr(pdu_sub_obj, 'ub_flag', ub_flag)
                ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)  # 更新其值
            time.sleep(0.01)
            if "Cyclic-" in ethernet_pdu.send_type:  # 对于周期报文，即刻通知mcu Forward进行对应报文的payload修改
                self.send_pdu(pdu_id)
            else:
                self.send_pdu(pdu_id, send_num=set_num, send_cyclic=send_cycle)

    def get_timestamp(self, index):
        """
        获取时间戳和pcap的以太网数据包index
        :param index: signal对象在上下行payload中的index
        :return:
        """
        timestamp = 0
        sequence = 0
        for curr_tcp_info in self.tcp_packet_list:
            if curr_tcp_info.payload_start <= index < curr_tcp_info.payload_start + curr_tcp_info.payload_length:
                timestamp = curr_tcp_info.timestamp
                sequence = curr_tcp_info.index
                break
        return timestamp, sequence

    def to_string(self):
        return f"通道名：{self.channel_name}, 本地IP:{self.localIpAddress}, 本地端口：{self.localPort}, " \
               f"远端IP:{self.remoteIpAddress}, 远端端口:{self.remotePort}, 传输协议：{self.transport_protocol}"


socket_multicast = None   # 上位机 组播报文接收对象


class socket_multicast_listen(threading.Thread):
    def __init__(self, multicast_ip='239.255.5.1', multicast_port=30501, payload_src_ip="172.20.5.12"):
        threading.Thread.__init__(self)
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port
        self.payload_src_ip = payload_src_ip
        self.cb = []
        self.exit_flag = False

    def run(self):
        logger.info("socket multicast listen Starting ...... ")
        time.sleep(2)
        self.receive_multicast()
        logger.info("socket multicast listen Exiting !!!")

    def receive_multicast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.multicast_ip, self.multicast_port))
        mreq = socket.inet_aton(self.multicast_ip) + socket.inet_aton('0.0.0.0')
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while not self.exit_flag:
            data, addr = sock.recvfrom(1024)
            if self.payload_src_ip:
                if addr[0] == self.payload_src_ip:
                    for cb_obj in self.cb:
                        cb_obj(list(data))

    def setup_data_callback(self, callBack):
        self.cb.append(callBack)
        return True

    def close(self):
        self.exit_flag = True


class CCUCDEthInternalDp20:
    """
    socket通道管理，负责通道的创建、删除
    """

    def __init__(self, mock_ecu,
                 test_ecu,
                 mcu_forward_port=None,
                 sdb_version="v_0_4_0",
                 veh_type="jupiter",
                 multicast_ip='239.255.5.1',
                 multicast_port=30501,
                 multicast_filter_src_ip="172.20.5.12",
                 forward_service="CD_McuForwarderService",
                 receive_timeout=900):
        """
        默认自动创建所有通道，但是否发送所有通道下的周期报文由使用人决定
        @param mock_ecu: 模拟的ECU
        @param test_ecu: 被测对象
        @param mcu_forward_port: mock ecu连接的eth internal router的端口号
        @param sdb_version: 内部以太网信号的SDB版本
        @param veh_type： 车型, 对DP20而言，当前为默认jupiter
        @param receive_timeout: partner client 连接forward后，超过指定的秒数，断开连接
        """

        self.mock_ecu = mock_ecu
        self.test_ecu = test_ecu
        self.veh_type = veh_type
        self.sdb_version = sdb_version
        self.router_process = None
        self.partner = None
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port
        self.multicast_filter_src_ip = multicast_filter_src_ip
        self.forward_service = forward_service
        self.channel_config = socketConfig(self.sdb_version, self.veh_type)
        self.active_channel_name = []
        self.channel_name_dict = {}  # 发送通道名称与通道对象映射
        self.signal_pduid_mapping = {}  # 信号名称与对应的message的pdu id 的映射
        self.pduid_channel_dict = {}  # 根据 pduid 找到对应的 channel_name
        self.pduid_signalobj_mapping = {}  # 根据pdu id找到属于该报文的的信号对象

        global socket_multicast
        if mock_ecu == "CCUSOCCD":
            res = os.system("ps -ef |grep 'partner' |grep -v grep |awk '{print $2}'|xargs kill -9")
            if res == 0:
                logger.info("partner clear success")
            else:
                logger.error(f"partner clear failed, ret: {res}")
            # try:
            #     kill_process_by_port(9999)
            #     kill_process_by_port(9998)
            # except Exception as e:
            #     logger.warning(f"kill process error:{e}")
            self.partner = S2sBaseClass([(self.forward_service, "client")])
            self.partner.method_default_timeout = 5
            self.partner.register_callback(forward_client, self.call_back_func)
        elif mock_ecu == "LCUL":
            self.router_process = start_mcu_router("172.20.5.1", mcu_forward_port)
            time.sleep(5)
            self.partner = partner_client(2, "LCU-L connect eth_internal_router thread ...",
                                          "172.20.5.1", mcu_forward_port, self.call_back_func, receive_timeout)
            if socket_multicast is None:
                socket_multicast = socket_multicast_listen(multicast_ip=self.multicast_ip,
                                                           multicast_port=self.multicast_port,
                                                           payload_src_ip=self.multicast_filter_src_ip)
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
                socket_multicast.start()
            else:
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
        elif mock_ecu == "LCUR":
            self.router_process = start_mcu_router("172.20.5.2", mcu_forward_port)
            time.sleep(5)
            self.partner = partner_client(3, "LCU-R connect eth_internal_router thread ...",
                                          "172.20.5.2", mcu_forward_port, self.call_back_func, receive_timeout)
            if socket_multicast is None:
                socket_multicast = socket_multicast_listen(multicast_ip=self.multicast_ip,
                                                           multicast_port=self.multicast_port,
                                                           payload_src_ip=self.multicast_filter_src_ip)
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
                socket_multicast.start()
            else:
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
        elif mock_ecu == "CCUSOCAD":
            self.router_process = start_mcu_router("172.20.5.21", mcu_forward_port)
            time.sleep(5)
            self.partner = partner_client(4, "CCUSOCAD connect eth_internal_router thread ...",
                                          "172.20.5.21", mcu_forward_port, self.call_back_func, receive_timeout)
            if socket_multicast is None:
                socket_multicast = socket_multicast_listen(multicast_ip=self.multicast_ip,
                                                           multicast_port=self.multicast_port,
                                                           payload_src_ip=self.multicast_filter_src_ip)
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
                socket_multicast.start()
            else:
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
        elif mock_ecu == "CCUMCUAD":
            self.router_process = start_mcu_router("172.20.5.22", mcu_forward_port)
            time.sleep(5)
            self.partner = partner_client(5, "CCUMCUAD connect eth_internal_router thread ...",
                                          "172.20.5.22", mcu_forward_port, self.call_back_func, receive_timeout)
            if socket_multicast is None:
                socket_multicast = socket_multicast_listen(multicast_ip=self.multicast_ip,
                                                           multicast_port=self.multicast_port,
                                                           payload_src_ip=self.multicast_filter_src_ip)
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
                socket_multicast.start()
            else:
                socket_multicast.setup_data_callback(self.handle_nuc_multicast_message)
        else:
            logger.error(f"不支持{mock_ecu}的模拟，当前支持列表：CCUSOCCD、LCUL、LCUR、CCUSOCAD、CCUMCUAD")

        self.__get_signal_dict()  # 生成通道名称信息, 装载各个通道的信号数据

        self.__refresh_pdu_data_cycle_ms()  # 计算各个通道周期报文的pdu_data
        self.__create_all_channel()  # 默认创建所有的通道，与MCU Forward交互
        self.start_all_cycle_message_send()  # 默认启动每个通道下的周期报文的周期发送，与MCU Forward交互

    def environment_teardown(self):
        """停止soa partner、mcu router进程的执行"""

        self.stop_all_cycle_message_send()
        self.__delete_all_channel()
        try:
            if self.mock_ecu == "CCUSOCCD":
                self.partner.stop_operators()
                time.sleep(2)
            else:
                self.router_process.terminate()
                self.router_process.wait()
                os.killpg(self.router_process.pid, signal.SIGINT)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/eth_internal_dp20.py")
            pass

        if socket_multicast is not None:
            socket_multicast.close()

    def handle_nuc_multicast_message(self, data):
        time_stamp = int(datetime.now().timestamp() * 1000)
        for channel_name in self.channel_name_dict:
            channel_info = self.channel_name_dict.get(channel_name)
            if channel_info.is_multicast_channel:
                hex_str = ''.join(hex(b)[2:].zfill(2) for b in data)
                channel_info.add_tcp_packet(hex_str, time_stamp)

    def call_back_func(self, service_name, payload):
        """
        {'action':'event','function':'messageFromMCU','args':'{"msg":{"channelName":3,"timeStamp":26,"payload":[]}}'}
        """
        try:
            if payload['function'] == "UpdatemessageFromMCUEvent":
                channel_name = json.loads(payload['args'])["msg"]['channelName']
                time_stamp = int(datetime.now().timestamp() * 1000)
                if channel_name in self.channel_name_dict:
                    data_list = json.loads(payload['args'])["msg"]['payload']
                    hex_str = ''.join(hex(b)[2:].zfill(2) for b in data_list)
                    self.channel_name_dict.get(channel_name).add_tcp_packet(hex_str, time_stamp)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/eth_internal_dp20.py")
            pass

    def empty(self):
        """
        重置所有通道的接收缓存
        """
        for channel_name in self.channel_name_dict:
            self.channel_name_dict.get(channel_name).empty()
            logger.info(f"通道 {channel_name} 接收缓存重置成功！！")

    def get_signal_values(self, signal_name):
        """
        获取给到信号的信号值列表
        @param signal_name: 指定的信号名
        return: 信号值列表[value1, value2, value3...]
        """
        pdu_id = self.signal_pduid_mapping.get(signal_name)
        if pdu_id in self.pduid_channel_dict:
            channel_name = self.pduid_channel_dict.get(pdu_id)
            signal_value_tuple_list = []
            signal_items = []
            channel_obj = self.channel_name_dict.get(channel_name)
            channel_obj.get_signal_values(signal_name)
            for signal_value in channel_obj.signal_info_dict[signal_name].signals_value_list:
                signal_value_tuple_list.append(signal_value.signal_value)
                signal_items.append((signal_value.sequence, signal_value.timestamp, signal_value.signal_value))
            return signal_value_tuple_list

    def check_signal_values(self, signal_name, expect_value, timeout=5):
        """
        获取给到信号的信号值列表
        @param signal_name: 指定的信号名
        @param expect_value: 期望的值
        @param timeout: 超时时间
        return: 信号值列表[value1, value2, value3...]
        """
        pdu_id = self.signal_pduid_mapping.get(signal_name)
        if pdu_id in self.pduid_channel_dict:
            channel_name = self.pduid_channel_dict.get(pdu_id)
            channel_obj = self.channel_name_dict.get(channel_name)
            channel_obj.get_signal_values(signal_name)
            while timeout:
                for signal_value in channel_obj.signal_info_dict[signal_name].signals_value_list:
                    if signal_value.signal_value == expect_value:
                        return True
                timeout -= 0.1
                time.sleep(0.1)
            logger.warning(f"没有发现期望值：{expect_value}")
            assert False

    def __create_all_channel(self):
        """
        创建已知的所有通道
        """
        logger.info("--------------------------------------------------")
        for channel_name in self.channel_name_dict:
            logger.info(f"开始创建通道：{channel_name}， 配置信息: {self.channel_name_dict.get(channel_name).to_string()}")
            if self.channel_name_dict.get(channel_name).transport_protocol == "TCP":
                channel_type = 1
            elif self.channel_name_dict.get(channel_name).transport_protocol == "UDP":
                channel_type = 2
            else:
                channel_type = 2
            localIpAddress = self.channel_name_dict.get(channel_name).localIpAddress
            localPort = self.channel_name_dict.get(channel_name).localPort
            remoteIpAddress = self.channel_name_dict.get(channel_name).remoteIpAddress
            remotePort = self.channel_name_dict.get(channel_name).remotePort
            multicastIpAddress = self.channel_name_dict.get(channel_name).multicast_ip
            self.partner.send_method_request(forward_client, "createChannel",
                                             {"channelName": channel_name,
                                              "channelConfig": {"channelType": channel_type,
                                                                "localIpAddress": localIpAddress,
                                                                "localPort": localPort,
                                                                "remoteIpAddress": remoteIpAddress,
                                                                "remotePort": remotePort,
                                                                "multicastIpAddress": multicastIpAddress}})
            logger.info(f"通道 {channel_name} 创建成功！！")
            time.sleep(1)
            self.active_channel_name.append(channel_name)

        logger.info("--------------------------------------------------")

    def __refresh_pdu_data_cycle_ms(self):
        for channel_name in self.channel_name_dict:
            self.channel_name_dict.get(channel_name).all_cycle_frame_calculation_pdu_data()
            logger.info(f"初始化 {channel_name} 下 报文的 pdu_data 成功！！！")

    def __delete_all_channel(self):
        """
        删除所有的通道
        """
        logger.info("--------------------------------------------------")
        for channel_name in self.channel_name_dict:
            self.partner.send_method_request(forward_client,
                                             "deleteChannel",
                                             {"channelName": channel_name})
            logger.info(f"通道 {channel_name} 删除请求成功！！")
            time.sleep(1)
        logger.info("--------------------------------------------------")

    def start_all_cycle_message_send(self):
        """
        发送所有通道下所有的周期报文
        """
        for channel_name in self.channel_name_dict:
            self.channel_name_dict.get(channel_name).start_all_cycle_message_send()
            logger.info(f"初始化 {channel_name} 下 报文的 pdu_data 成功")
            time.sleep(1)

    def stop_all_cycle_message_send(self):
        """
        停止发送所有通道下所有的周期报文
        """
        for channel_name in self.channel_name_dict:
            self.channel_name_dict.get(channel_name).stop_all_cycle_message_send()
            logger.info(f"停止 {channel_name} 下 周期报文的 发送 成功")
            time.sleep(1)

    def send_pdu(self, pdu_id: int, send_num=1, send_cyclic=10):
        """
        发送该通道下单个周期报文，首先根据pdu_id 找到对应的channel, 并判断报文是否是周期报文
        广播报文关联sender为mock ecu，且端口为30501的通道
        """
        if pdu_id in self.pduid_channel_dict:
            channel_name = self.pduid_channel_dict.get(pdu_id)
            if channel_name in self.channel_name_dict:
                self.channel_name_dict.get(channel_name).send_pdu(pdu_id, send_num, send_cyclic)
            else:
                logger.info(f" 通道: {channel_name} 不存在， 调用send_pdu失败")
        else:
            logger.info(f" pdu_id: {pdu_id} 不存在， 调用send_pdu失败")

    def stop_send_single_pdu(self, pdu_id: int):
        """
        停止该通道下单个报文的发送
        """
        if pdu_id in self.pduid_channel_dict:
            channel_name = self.pduid_channel_dict.get(pdu_id)
            if channel_name in self.channel_name_dict:
                self.channel_name_dict.get(channel_name).stop_send_single_pdu(pdu_id)
            else:
                logger.info(f" 通道: {channel_name} 不存在， 调用stop_send_single_pdu失败")
        else:
            logger.info(f" pdu_id: {pdu_id} 不存在， 调用stop_send_single_pdu失败")

    def set_signal_multiple_value(self, sig_dict: dict, ub_flag=True):
        """
        对于周期型信号，即可发送，对于事件型信号，需自行发送
        @:param sig_dict: {"signal1": value1, "signal2": value2},同一个Pdu
        """
        for signal_name, signal_value in sig_dict.items():
            if signal_name in self.signal_pduid_mapping:
                pdu_id = self.signal_pduid_mapping.get(signal_name)
                if pdu_id in self.pduid_channel_dict:
                    channel_name = self.pduid_channel_dict.get(pdu_id)
                    if channel_name in self.channel_name_dict:
                        self.channel_name_dict.get(channel_name).set_multiple_signal_value(pdu_id,
                                                                                           sig_dict,
                                                                                           ub_flag)

    def set_signal_value(self, signal_name, signal_value, ub_flag=True):
        """
        对于周期型信号，即可发送，对于事件型信号，需自行发送
        """
        if signal_name in self.signal_pduid_mapping:
            pdu_id = self.signal_pduid_mapping.get(signal_name)
            if pdu_id in self.pduid_channel_dict:
                channel_name = self.pduid_channel_dict.get(pdu_id)
                if channel_name in self.channel_name_dict:
                    self.channel_name_dict.get(channel_name).set_signal_value(pdu_id,
                                                                              signal_name,
                                                                              signal_value,
                                                                              ub_flag)

    def __get_signal_dict(self):
        """
        从内部以太网数据库中根据以太网报文名称获取报文的初始值，
        先处理非广播报文，再处理组播报文
        """
        cls_full_module_name = f"xat_ecu.legacy.sdk.data.{self.veh_type}.eth.{self.sdb_version}"
        cls_module = importlib.import_module(cls_full_module_name)
        logger.info("dynamic cls_module_name is {}".format(cls_module.__name__))
        # 第一步：处理非组播通道的帧
        for module_name in cls_module.__all__:
            module_obj = getattr(cls_module, module_name)
            setattr(self, module_name, module_obj)
            for ethernet_pdu_name in dir(module_obj):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
                if ethernet_pdu_name.startswith("CCU") or ethernet_pdu_name.startswith("LCU"):  # 报文
                    ethernet_pdu = getattr(module_obj, ethernet_pdu_name)  # pdu对象，如BGMIntEthPDU0001
                    # 获取pdu对象的属性
                    client_socket = getattr(ethernet_pdu, "client_socket")
                    if client_socket == "SocketMulticast":
                        continue
                    else:
                        setattr(ethernet_pdu, "multicast_flag", False)

                    sender = getattr(ethernet_pdu, "sender")
                    server_socket = getattr(ethernet_pdu, "server_socket")
                    receiver = getattr(ethernet_pdu, "receiver")

                    if self.mock_ecu == sender and self.test_ecu in receiver:  # Client Socket可能是 SocketMulticast
                        setattr(ethernet_pdu, "sender_or_receiver", "sender")
                        sender_socket = self.channel_config.get_socketDescription(self.mock_ecu, server_socket)
                        receiver_socket = self.channel_config.get_socketDescription(self.test_ecu, client_socket)
                        channel_name = f"{sender}-{server_socket}-{self.test_ecu}-{client_socket}"
                        channel_name_new = f"{self.test_ecu}-{client_socket}-{sender}-{server_socket}"
                        if channel_name not in self.channel_name_dict and channel_name_new not in self.channel_name_dict:
                            channel_info = ChannelConfig(channel_name,
                                                         sender_socket.ip_address,
                                                         sender_socket.port_number,
                                                         receiver_socket.ip_address,
                                                         receiver_socket.port_number,
                                                         sender_socket.transport_protocol,
                                                         self.partner,
                                                         self.mock_ecu,
                                                         "")
                            self.channel_name_dict[channel_info.channel_name] = channel_info
                        elif channel_name in self.channel_name_dict:
                            channel_info = self.channel_name_dict[channel_name]
                        else:
                            channel_info = self.channel_name_dict[channel_name_new]
                    elif self.mock_ecu in receiver and self.test_ecu == sender:  # mock ecu 接收以太网数据(单播、广播)
                        setattr(ethernet_pdu, "sender_or_receiver", "receiver")
                        sender_socket = self.channel_config.get_socketDescription(self.test_ecu, server_socket)
                        receiver_socket = self.channel_config.get_socketDescription(self.mock_ecu, client_socket)
                        channel_name = f"{sender}-{server_socket}-{self.mock_ecu}-{client_socket}"
                        channel_name_new = f"{self.mock_ecu}-{client_socket}-{sender}-{server_socket}"
                        if channel_name not in self.channel_name_dict and channel_name_new not in self.channel_name_dict:
                            channel_info = ChannelConfig(channel_name,
                                                         receiver_socket.ip_address,
                                                         receiver_socket.port_number,
                                                         sender_socket.ip_address,
                                                         sender_socket.port_number,
                                                         sender_socket.transport_protocol,
                                                         self.partner,
                                                         self.mock_ecu,
                                                         "")
                            self.channel_name_dict[channel_info.channel_name] = channel_info
                        elif channel_name in self.channel_name_dict:
                            channel_info = self.channel_name_dict[channel_name]
                        else:
                            channel_info = self.channel_name_dict[channel_name_new]
                    else:
                        continue

                    pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
                    pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
                    pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
                    pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
                    bin_str_pdu_header_id = ''.join(hex(b)[2:].zfill(2) for b in pdu_header_id_list)
                    bin_pdu_length_list = ''.join(hex(b)[2:].zfill(2) for b in pdu_length_list)
                    self.pduid_signalobj_mapping[pdu_header_id] = []
                    # 解析eth信号对象
                    for pdu_signal_name in dir(ethernet_pdu):
                        if "__" not in pdu_signal_name:
                            pdu_sub_obj = getattr(ethernet_pdu, pdu_signal_name)
                            if not isinstance(pdu_sub_obj, int):
                                if not isinstance(pdu_sub_obj, str):
                                    if not isinstance(pdu_sub_obj, dict) and not isinstance(pdu_sub_obj, list):
                                        # 不是int，str，dict则是eth信号对象，此时的pdu_attr_name为eth信号名
                                        signal = SignalObj()
                                        signal.start_position = getattr(pdu_sub_obj, 'start_position')
                                        signal.signal_length = getattr(pdu_sub_obj, 'signal_length')
                                        if 'layout_format' in dir(pdu_sub_obj):
                                            signal.layout_format = getattr(pdu_sub_obj, 'layout_format')
                                        else:
                                            signal.layout_format = getattr(ethernet_pdu, 'layout_format')
                                        signal.offset = getattr(pdu_sub_obj, 'offset')
                                        signal.factor = getattr(pdu_sub_obj, 'factor')
                                        signal.sender = sender
                                        signal.initial_value = getattr(pdu_sub_obj, 'initial_value')
                                        signal.pdu_length = pdu_length
                                        signal.hex_str_pdu_header = bin_str_pdu_header_id
                                        signal.hex_str_pdu_header_length = bin_str_pdu_header_id + bin_pdu_length_list
                                        signal.sig_ub = getattr(pdu_sub_obj, 'sig_ub')
                                        signal.name = pdu_signal_name
                                        channel_info.signal_info_dict[pdu_signal_name] = signal
                                        self.signal_pduid_mapping[pdu_signal_name] = pdu_header_id
                                        self.pduid_channel_dict[pdu_header_id] = channel_info.channel_name
                                        channel_info.pduid_obj_mapping[pdu_header_id] = ethernet_pdu
                                        self.pduid_signalobj_mapping[pdu_header_id].append(signal)

        # 第二步：处理组播通道的帧
        for module_name in cls_module.__all__:
            module_obj = getattr(cls_module, module_name)
            setattr(self, module_name, module_obj)
            for ethernet_pdu_name in dir(module_obj):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
                if ethernet_pdu_name.startswith("CCU") or ethernet_pdu_name.startswith("LCU"):  # 报文
                    ethernet_pdu = getattr(module_obj, ethernet_pdu_name)  # pdu对象，如BGMIntEthPDU0001
                    # 获取pdu对象的属性
                    client_socket = getattr(ethernet_pdu, "client_socket")
                    if client_socket != "SocketMulticast":
                        continue
                    else:
                        setattr(ethernet_pdu, "multicast_flag", True)

                    sender = getattr(ethernet_pdu, "sender")
                    server_socket = getattr(ethernet_pdu, "server_socket")
                    receiver = getattr(ethernet_pdu, "receiver")

                    if self.mock_ecu == sender and self.test_ecu in receiver:
                        setattr(ethernet_pdu, "sender_or_receiver", "sender")  # 通过mock ecu 以组播的形式发送的信号
                        sender_socket = self.channel_config.get_socketDescription(self.mock_ecu, server_socket)
                        receiver_socket = self.channel_config.get_socketDescription(self.test_ecu, client_socket)
                        for channel_name in self.channel_name_dict:
                            channel_info = self.channel_name_dict[channel_name]
                            if channel_info.mock_ecu == self.mock_ecu and channel_info.transport_protocol == "UDP" \
                                    and channel_info.localPort == 30501:
                                channel_info.is_multicast_channel = True
                                break
                        else:  # 未找到可复用的通道，则创建，client_socket为 SocketMulticast
                            channel_name = f"{sender}-{server_socket}-{self.test_ecu}-{client_socket}"

                            channel_info = ChannelConfig(channel_name,
                                                         sender_socket.ip_address,
                                                         sender_socket.port_number,
                                                         receiver_socket.ip_address,
                                                         receiver_socket.port_number,
                                                         sender_socket.transport_protocol,
                                                         self.partner,
                                                         self.mock_ecu,
                                                         "")
                            channel_info.is_multicast_channel = True
                            logger.info(f"创建组播发送通道：{channel_name}，{channel_info.to_string()}")
                            self.channel_name_dict[channel_info.channel_name] = channel_info
                    elif self.mock_ecu in receiver and self.test_ecu == sender:  # mock ecu 接收以太网数据(单播、广播)
                        setattr(ethernet_pdu, "sender_or_receiver", "receiver")
                        sender_socket = self.channel_config.get_socketDescription(self.test_ecu, server_socket)
                        receiver_socket = self.channel_config.get_socketDescription(self.mock_ecu, client_socket)
                        if self.mock_ecu == "CCUSOCCD":
                            if "CCUSOCCD-SocketMulticast" not in self.channel_name_dict:
                                channel_name = "CCUSOCCD-SocketMulticast"
                                channel_info = ChannelConfig(channel_name,
                                                             "172.20.5.11",
                                                             30501,
                                                             "",
                                                             0,
                                                             "UDP",
                                                             self.partner,
                                                             self.mock_ecu,
                                                             "239.255.5.1")
                                logger.info(f"创建组播接收通道：{channel_name}，{channel_info.to_string()}")
                            else:
                                channel_info = self.channel_name_dict["CCUSOCCD-SocketMulticast"]
                        else:
                            for channel_name in self.channel_name_dict:
                                channel_info = self.channel_name_dict[channel_name]
                                if channel_info.mock_ecu == self.mock_ecu and channel_info.transport_protocol == "UDP" \
                                        and channel_info.localPort == 30501:
                                    channel_info.is_multicast_channel = True
                                    break
                            else:  # 未找到可复用的通道，则创建，client_socket为："SocketMulticast"
                                channel_name = f"{sender}-{server_socket}-{self.mock_ecu}-{client_socket}"
                                channel_info = ChannelConfig(channel_name,
                                                             receiver_socket.ip_address,
                                                             receiver_socket.port_number,
                                                             sender_socket.ip_address,
                                                             sender_socket.port_number,
                                                             sender_socket.transport_protocol,
                                                             self.partner,
                                                             self.mock_ecu,
                                                             "")
                                channel_info.is_multicast_channel = True
                                logger.info(f"创建组播接收通道：{channel_name}，{channel_info.to_string()}")
                        self.channel_name_dict[channel_info.channel_name] = channel_info
                    else:
                        continue

                    pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
                    pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
                    pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
                    pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
                    bin_str_pdu_header_id = ''.join(hex(b)[2:].zfill(2) for b in pdu_header_id_list)
                    bin_pdu_length_list = ''.join(hex(b)[2:].zfill(2) for b in pdu_length_list)
                    self.pduid_signalobj_mapping[pdu_header_id] = []
                    # 解析eth信号对象
                    for pdu_signal_name in dir(ethernet_pdu):
                        if "__" not in pdu_signal_name:
                            pdu_sub_obj = getattr(ethernet_pdu, pdu_signal_name)
                            if not isinstance(pdu_sub_obj, int):
                                if not isinstance(pdu_sub_obj, str):
                                    if not isinstance(pdu_sub_obj, dict) and not isinstance(pdu_sub_obj, list):
                                        # 不是int，str，dict则是eth信号对象，此时的pdu_attr_name为eth信号名
                                        signal = SignalObj()
                                        signal.start_position = getattr(pdu_sub_obj, 'start_position')
                                        signal.signal_length = getattr(pdu_sub_obj, 'signal_length')
                                        if 'layout_format' in dir(pdu_sub_obj):
                                            signal.layout_format = getattr(pdu_sub_obj, 'layout_format')
                                        else:
                                            signal.layout_format = getattr(ethernet_pdu, 'layout_format')
                                        signal.offset = getattr(pdu_sub_obj, 'offset')
                                        signal.factor = getattr(pdu_sub_obj, 'factor')
                                        signal.sender = sender
                                        signal.initial_value = getattr(pdu_sub_obj, 'initial_value')
                                        signal.pdu_length = pdu_length
                                        signal.hex_str_pdu_header = bin_str_pdu_header_id
                                        signal.hex_str_pdu_header_length = bin_str_pdu_header_id + bin_pdu_length_list
                                        signal.name = pdu_signal_name
                                        channel_info.signal_info_dict[pdu_signal_name] = signal
                                        signal.sig_ub = getattr(pdu_sub_obj, 'sig_ub')
                                        self.signal_pduid_mapping[pdu_signal_name] = pdu_header_id
                                        self.pduid_channel_dict[pdu_header_id] = channel_info.channel_name
                                        channel_info.pduid_obj_mapping[pdu_header_id] = ethernet_pdu
                                        self.pduid_signalobj_mapping[pdu_header_id].append(signal)


class socketConfig:
    """
    基于当前的车型以及sdb版本，加载对应的socket配置信息，并提供方法根据ecu名称、socket名称，获取对应的IP、port、传输协议
    """

    def __init__(self, sdb_version, veh_type):
        """
        基于当前的车型以及sdb版本，加载对应的socket配置信息
        @param sdb_version: 内部以太网信号的SDB版本
        @param veh_type： 车型, 对DP20而言，当前为默认jupiter
        """
        self.veh_type = veh_type
        self.sdb_version = sdb_version
        self.ip_port_protocol_dict = {}
        self.__get_ip_port_protocol_dict()

    def __get_ip_port_protocol_dict(self):
        """
        从内部以太网数据库中根据以太网报文名称获取报文的初始值
        """
        module_name = f"xat_ecu.legacy.sdk.data.{self.veh_type}.eth.{self.sdb_version}.participant_config"
        self.bgm_eth_internal_participant = importlib.import_module(module_name)
        for participant_name in dir(self.bgm_eth_internal_participant):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
            if participant_name.startswith("CCU") or participant_name.startswith("LCU"):
                ethernet_participant = getattr(self.bgm_eth_internal_participant, participant_name)
                # 获取pdu对象的属性
                ip_address = getattr(ethernet_participant, "ip_address")
                # 解析eth信号对象
                for socket_name in dir(ethernet_participant):
                    if "__" not in socket_name:
                        pdu_sub_obj = getattr(ethernet_participant, socket_name)
                        if not isinstance(pdu_sub_obj, int):
                            if not isinstance(pdu_sub_obj, str):
                                if not isinstance(pdu_sub_obj, dict):
                                    # 不是int，str，dict则是eth信号对象，此时的pdu_attr_name为eth信号名
                                    port_number = getattr(pdu_sub_obj, 'port_number')
                                    transport_protocol = getattr(pdu_sub_obj, 'transport_protocol')
                                    socket_desc = socketDescription(ip_address, port_number, transport_protocol)
                                    self.ip_port_protocol_dict[f"{participant_name}-{socket_name}"] = socket_desc
        else:
            socket_desc = socketDescription("239.255.5.1", 30501, "UDP")
            self.ip_port_protocol_dict["SocketMulticast"] = socket_desc

    def get_socketDescription(self, participant_name, socket_name):
        """
        根据ecu名称、socket名称，获取对应的IP、port、传输协议
        """

        return self.ip_port_protocol_dict[f"{participant_name}-{socket_name}"]


class socketDescription:
    def __init__(self, ip_address, port_number, transport_protocol):
        self.ip_address = ip_address
        self.port_number = port_number
        self.transport_protocol = transport_protocol

    def to_string(self):
        logger.info(f"{self.ip_address} {self.port_number} {self.transport_protocol}")


def get_ub_bit_value(hex_str, ub_idx):
    """
    @hex_str: 抓包数据，去掉前8个字节
    @ub_idx: SDB中定义的UB位索引
    """
    bin_string = ''.join(bin(int(b, 16))[2:].zfill(4) for b in hex_str)
    ub_idx_new = dbc_bit_to_bin_index(ub_idx)
    logger.info(f"对应UB位的值：{bin_string[ub_idx_new]}")


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    # data = [0, 63, 192, 0, 0, 117, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 144, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 191, 231, 252, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #         7, 208, 0, 0, 0, 0, 0, 63, 231, 252, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16]
    # hex_string = ''.join(hex(b)[2:].zfill(2) for b in data)
    # logger.info(hex_string)
    test = CCUCDEthInternalDp20(mock_ecu="LCUL", test_ecu="CCUMCUCD")

