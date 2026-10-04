# -*- coding: utf-8 -*-

"""
@File        : bgm_eth_internal.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/02/04 14:51 PM
@Description : BGM内部以太网信号操作
@Examples    : example of how to use it
"""
import json
import time

from scapy.all import *
from socket import *
import importlib
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import change_bgm_config, recover_bgm_config
from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu import S2sCombinationSendPdu
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_tcp_server import is_socket_connected
from xat_ecu.legacy.sdk.Internal_ETH.tools.utils import write_s2s_json, s2s_path, s2s_json


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


class BgmEthInternal:
    """
    bgm内部以太网控制，包括下行抓包解析，上行模拟udp或tcp数据发送
    """

    def __init__(self,
                 ipdu=None,
                 nucapp=None,
                 **kwargs):
        """
        初始化通信双方的ip、端口，以及总线信号控制和电源控制
        !!!! 如果不传递实参，则可以离线解析pcap数据
        @param ipdu: 总线信号控制模块, 默认None
        @param nucapp: 电源控制，默认None
        @param kwargs: 可选参数如下：
            @param tcp_up_mcu_ip: mcu上行tcp的发送ip：默认172.16.5.2
            @param tcp_up_mpu_ip: mpu上行tcp的接收ip：默认172.16.5.1
            @param tcp_down_mpu_ip: mpu下行tcp的发送ip：默认172.16.5.1
            @param tcp_down_mcu_ip: mcu下行tcp的接收ip：默认172.16.5.2
            @param udp_mpu_ip: mpu接收udp的ip：默认172.16.5.1
            @param udp_mcu_ip: mcu发送udp的ip：默认172.16.5.2
            @param tcp_down_mpu_port: 下行tcp的mpu发送端口，默认30500
            @param tcp_down_mcu_port: 下行tcp的mcu接收端口，默认30500
            @param tcp_up_mpu_port: 上行tcp的mpu接收端口，默认30501
            @param tcp_up_mcu_port: 上行tcp的mcu发送端口，默认30501
            @param udp_mpu_port: mpu接收udp的端口，默认30502
            @param udp_mcu_port: cu发送udp的端口，默认30502
            @param enable_inter_service: 是否使能BGM域内服务的跨域通信
            @param veh_type: 整车版本，一般传递ecu.tc_config['veh_type']，当前暂时不用传递，因为不分区车型
            @param bl_ver: 数据库大版本，一般传递ecu.tc_config['bl_ver']
        """
        self.ipdu = ipdu
        self.nucapp = nucapp
        self.tcp_down_mpu_ip = kwargs.get("tcp_down_mpu_ip", "172.16.5.1")
        self.tcp_down_mcu_ip = kwargs.get("tcp_down_mcu_ip", "172.16.5.2")
        self.tcp_up_mcu_ip = self.tcp_down_mcu_ip  # 当前S2S的tcp收到ip是相同的，故不用传参
        self.tcp_up_mpu_ip = self.tcp_down_mpu_ip
        self.udp_mpu_ip = kwargs.get("udp_mpu_ip", "172.16.5.1")
        self.udp_mcu_ip = kwargs.get("udp_mcu_ip", "172.16.5.2")
        self.tcp_down_mpu_port = kwargs.get("tcp_down_mpu_port", 30500)
        self.tcp_down_mcu_port = kwargs.get("tcp_down_mcu_port", 30500)
        self.tcp_up_mpu_port = kwargs.get("tcp_up_mpu_port", 30501)
        self.tcp_up_mcu_port = kwargs.get("tcp_up_mcu_port", 30501)
        self.udp_mpu_port = kwargs.get("udp_mpu_port", 30502)
        self.udp_mcu_port = kwargs.get("udp_mcu_port", 30502)
        self.enable_inter_service = kwargs.get("enable_inter_service", False)
        self.veh_type = kwargs.get("veh_type", "mars1")
        self.bl_ver = kwargs.get("bl_ver", "v_2_0_0")

        self.bgm_env_change = False  # 是否需要改bgm的s2s.json配置
        self.mock_mcu_tcp = False  # 是否要模拟mcu发送tcp数据给mpu
        self.mock_mcu_udp = False  # 是否要模拟mcu发送udp数据给mpu
        self.pcap_name = ""  # 抓包存储的名称
        self.bgm_ssh = BGM_SSH()

        if self.ipdu is not None and self.nucapp is not None:  # 均为None则为离线解析
            self.env_pre_process()

        self.signal_info_dict = {}  # 信号数据集合{signal1: SignalObj1, signal2: SignalObj2, ....}
        self.signal_pduid_mapping = {}  # signal和pduid的映射 {signal1: pduid1, signal2: pduid1, signal3: pduid2}
        self.pduid_obj_mapping = {}  # pduid与pdu对象的映射{5311：BGMIntEthPDU5311}
        self.pduid_signalobj_mapping = {}  # pduid和信号对象的映射{5311: [signal1, signal2]}
        self._get_signal_dict()
        self.up_payload = ""  # 上行tcp数据包
        self.down_payload = ""  # 下行tcp数据包
        self.tcp_packet_list = []  # tcp数据帧

    def env_pre_process(self):
        """环境前处理，推送tcpdump至bgm内，修改s2s.json配置，根据ip端口配置确认是否要模拟mcu的udp或tcp数据发送，如需则启动模拟"""
        # self.bgm_ssh.init_bgm_tcpdump()
        new_s2s_json = {"mcuIpTcp": self.tcp_down_mcu_ip,
                        "mpuIpTcp": self.tcp_down_mpu_ip,
                        "mcuIpUdp": self.udp_mcu_ip,
                        "mpuIpUdp": self.udp_mpu_ip,
                        "tcpReqClientPort": self.tcp_down_mpu_port,
                        "tcpReqServerPort": self.tcp_down_mcu_port,
                        "tcpResClientPort": self.tcp_up_mpu_port,
                        "tcpResServerPort": self.tcp_up_mcu_port,
                        "udpResClientPort": self.udp_mpu_port,
                        "udpResServerPort": self.udp_mcu_port}
        for key in new_s2s_json:
            if new_s2s_json[key] != s2s_json[key]:
                write_s2s_json(new_s2s_json)
                logger.info("s2s.json需要重新更新")
                change_bgm_config(nucapp=self.nucapp, bgm_inter_enable=self.enable_inter_service, s2s_path=s2s_path)
                self.bgm_env_change = True
                break

        if not self.bgm_env_change and self.enable_inter_service:  # 仅使能域内服务域外通信
            write_s2s_json({})
            change_bgm_config(nucapp=self.nucapp, bgm_inter_enable=True, s2s_path=s2s_path)
            self.bgm_env_change = True

        if self.tcp_up_mcu_ip != "172.16.5.2":
            self.mock_mcu_tcp = True
            logger.info("开始启动mcu tcp的模拟发送")
            self.mock_socket_server = MockSocketServer(self.tcp_up_mcu_ip, self.tcp_up_mcu_port,
                                                       self.tcp_down_mcu_ip, self.tcp_down_mcu_port,
                                                       self.tcp_down_mpu_ip, self.tcp_down_mpu_port,
                                                       self.tcp_up_mpu_ip, self.tcp_up_mpu_port)
            self.start_mock_mcu()

        if self.udp_mcu_ip != "172.16.5.2":
            self.mock_mcu_udp = True
            logger.info("开始启动mcu udp的模拟发送")
            self.cspdu = S2sCombinationSendPdu(self.ipdu, address=(self.udp_mcu_ip, self.udp_mcu_port))
            self.cspdu.continuous_combinationpdu_start()
            self.cspdu.s2ssendpdu_start(tar_address=(self.udp_mpu_ip, self.udp_mpu_port))

    def env_post_process(self):
        """环境后处理，包括停tcp收到socket，恢复bgm配置"""
        if self.mock_mcu_tcp:
            self.stop_mock_mcu()
        if self.mock_mcu_udp:
            self.cspdu.s2ssendpdu_stop()
            self.cspdu.continuous_combinationpdu_stop()
        if self.bgm_env_change:
            recover_bgm_config(nucapp=self.nucapp)

    def start_mock_mcu(self):
        """启动模拟mcu的tcp数据以及接收mpu下发的tcp数据"""
        self.mock_socket_server.start_listen()
        self.mock_socket_server.get_client_socket()

    def stop_mock_mcu(self):
        """停止模拟mcu的收发tcp数据"""
        self.mock_socket_server.stop_client_socket()
        self.mock_socket_server.stop_listen()

    def _get_signal_dict(self):
        """
        从内部以太网数据库中根据以太网报文名称获取报文的初始值
        """
        module_name = f"xat_ecu.legacy.sdk.data.{self.veh_type}.Internal_ETH.{self.bl_ver}.bgm_eth_internal"
        self.bgm_eth_internal = importlib.import_module(module_name)
        for ethernet_pdu_name in dir(self.bgm_eth_internal):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
            if "BGMIntEthPDU" in ethernet_pdu_name:  # 报文
                ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)  # pdu对象，如BGMIntEthPDU0001
                # 获取pdu对象的属性
                pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
                pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
                sender = getattr(ethernet_pdu, "sender")
                pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
                pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
                binary_string_pdu_header_id = ''.join(hex(b)[2:].zfill(2) for b in pdu_header_id_list)
                bin_pdu_length_list = ''.join(hex(b)[2:].zfill(2) for b in pdu_length_list)
                self.pduid_signalobj_mapping[pdu_header_id] = []

                # 解析eth信号对象
                for pdu_attr_name in dir(ethernet_pdu):
                    if "__" not in pdu_attr_name:
                        pdu_sub_obj = getattr(ethernet_pdu, pdu_attr_name)
                        if not isinstance(pdu_sub_obj, int):
                            if not isinstance(pdu_sub_obj, str):
                                if not isinstance(pdu_sub_obj, dict):
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
                                    signal.hex_str_pdu_header = binary_string_pdu_header_id
                                    signal.hex_str_pdu_header_length = binary_string_pdu_header_id + bin_pdu_length_list
                                    signal.downstream = True if "Down" in ethernet_pdu.client_socket else False
                                    signal.name = pdu_attr_name
                                    self.signal_info_dict[pdu_attr_name] = signal
                                    self.signal_pduid_mapping[pdu_attr_name] = pdu_header_id
                                    self.pduid_obj_mapping[pdu_header_id] = ethernet_pdu
                                    self.pduid_signalobj_mapping[pdu_header_id].append(signal)

    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", host="172.16.5.1", port=30500, **kwargs):
        """
        开启 bgm 内部抓包
        @param name:  抓包存储 文件名 ，最后会加上时间
        @param iface: 抓包的网卡
        @param host: 抓包指定的ip，可以填None，代表不指定ip
        @param port: 抓包指定的port，可以填None，代表不指定port
        @param kwargs:
        @return:
        """
        # 保存路径，默认保存在bgm 里面的 /log 下
        path = kwargs.get("path", "/update")
        # 抓包长度
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        self.pcap_name = f"{name}{otherStyleTime}.pcap"
        file_path = os.path.join(path, self.pcap_name)
        # 抓包 指令
        if host is not None and port is not None:
            host_and_port = f"host {host} and port {port}"
        elif host is not None and port is None:
            host_and_port = f"host {host}"
        elif host is None and port is not None:
            host_and_port = f"port {port}"
        else:
            host_and_port = ""

        cmd = f'cd /data/;chmod +x tcpdump;/data/tcpdump -i {iface} {host_and_port} -vvv -w {file_path}'
        self.bgm_ssh.start_bgm_tcpdump(cmd=cmd)

    def stop_tcpdump_and_parse_signal(self, sleep_time=0):
        """
        停止抓包,，复制到本地，并解析信号，同时删除bgm内部的pcap包
        @param sleep_time: 等待多久停止抓包
        """
        time.sleep(sleep_time)
        self.bgm_ssh.stop_bgm_tcpdump()
        pcap_path = self.bgm_ssh.scp_bgm_log_to_local(bgm_log_name=self.pcap_name, del_flag=True)
        self.update(pcap_path)

    def update(self, pcap_file_path=None, duration=5):
        """
        装载PCAP文件的信号值信息，分为离线解析和在线实时解析，给pcap则认为离线解析
        调用会先清除之前抓取的数据
        :param pcap_file_path: pcap 文件的路径信息
        :param duration: 如果解析类型为在线，则超时时间为监听的最大时长，单位秒
        """
        self.empty()

        if pcap_file_path is not None:
            pcap_parse_tcp = PcapParseTcpInfo(self.signal_info_dict, self.tcp_up_mcu_ip, self.tcp_up_mcu_port,
                                              self.tcp_down_mcu_ip, self.tcp_down_mcu_port, self.tcp_down_mpu_ip,
                                              self.tcp_down_mpu_port, self.tcp_up_mpu_ip, self.tcp_up_mpu_port)
            pcap_parse_tcp.parse_pcap_file(pcap_file_path)
            self.up_payload = pcap_parse_tcp.up_payload
            self.down_payload = pcap_parse_tcp.down_payload
            self.tcp_packet_list = pcap_parse_tcp.tcp_packet_list

            # 逐个信号解析
            for signal_name in self.signal_info_dict:
                signal_obj = self.signal_info_dict.get(signal_name)  # SignalObj
                pcap_parse_tcp.parse_signal_info(signal_obj)
            self.signal_info_dict = pcap_parse_tcp.signal_info_dict
            # logger.info(f"MobDevRPAReqResp的值列表：{self.get_signal_items('MobDevRPAReqResp')}")
            # logger.info(f"MMobDevRPAReqResp最后的值为：{self.get_last_signal('MobDevRPAReqResp')}")
        else:
            self.mock_socket_server.mock_mcu_listen_pdu(duration)  # 起一个线程抓指定时间的tcp数据
            # todo： 不对啊，直接走下面代码，还没有抓到最后的数据呢，好像没用
            self.down_payload = self.mock_socket_server.down_payload
            self.tcp_packet_list = self.mock_socket_server.tcp_packet_list
            # logger.info(f"SwtCDCLiLoBeamSw的值列表：{self.get_signal_items('SwtCDCLiLoBeamSw')}")
            # logger.info(f"SwtCDCLiLoBeamSw最后的值为：{self.get_last_signal('SwtCDCLiLoBeamSw')}")

    def empty(self):
        """
        清空已经装载的信号值信息
        """
        for signal_name in self.signal_info_dict:
            self.signal_info_dict[signal_name].signals_value_list = []
        if self.mock_mcu_tcp:
            self.mock_socket_server.empty_listen_result()  # 清空实时监听的结果

    def _refresh_signal_value_list(self):
        # 重新装载信号值列表
        pcap_parse_tcp = PcapParseTcpInfo(self.signal_info_dict, self.tcp_up_mcu_ip, self.tcp_up_mcu_port,
                                          self.tcp_down_mcu_ip, self.tcp_down_mcu_port, self.tcp_down_mpu_ip,
                                          self.tcp_down_mpu_port, self.tcp_up_mpu_ip, self.tcp_up_mpu_port)
        pcap_parse_tcp.down_payload = self.down_payload
        pcap_parse_tcp.tcp_packet_list = self.tcp_packet_list

        # 逐个信号解析
        for signal_name in self.signal_info_dict:
            signal_obj = self.signal_info_dict.get(signal_name)  # SignalObj
            pcap_parse_tcp.parse_signal_info(signal_obj)
        self.signal_info_dict = pcap_parse_tcp.signal_info_dict

    def get_signal_items(self, signal_name):
        """
        获取给到信号的数据列表
        @param signal_name: 指定的信号名
        return: 信号数据列表[(pcap_index, timestamp, signal_value), (), ()...]
        """
        if self.mock_mcu_tcp:
            self._refresh_signal_value_list()
        signal_value_tuple_list = []
        for signal_value in self.signal_info_dict[signal_name].signals_value_list:
            signal_value_tuple_list.append((signal_value.sequence, signal_value.timestamp, signal_value.signal_value))
        logger.info(f"{signal_name}以太网数据>>>> {signal_value_tuple_list}")
        return signal_value_tuple_list

    def get_signal_values(self, signal_name):
        """
        获取给到信号的信号值列表
        @param signal_name: 指定的信号名
        return: 信号值列表[value1, value2, value3...]
        """
        if self.mock_mcu_tcp:
            self._refresh_signal_value_list()
        signal_value_tuple_list = []
        signal_items = []
        for signal_value in self.signal_info_dict[signal_name].signals_value_list:
            signal_value_tuple_list.append(signal_value.signal_value)
            signal_items.append((signal_value.sequence, signal_value.timestamp, signal_value.signal_value))
        logger.info(f"{signal_name}信号数据>>>> {signal_items}")
        logger.info(f"{signal_name}信号值>>>> {signal_value_tuple_list}")
        return signal_value_tuple_list

    def get_last_signal(self, signal_name):
        """
        获取对应信号的最后一个值
        """
        if self.mock_mcu_tcp:
            self._refresh_signal_value_list()
        if len(self.signal_info_dict[signal_name].signals_value_list) > 1:
            signal_value = self.signal_info_dict[signal_name].signals_value_list[-1]
            return signal_value.sequence, signal_value.timestamp, signal_value.signal_value
        else:
            return None, None, None

    def set_signal(self, signal_name, signal_value, send_pdu_immediately=False):
        """
        设定pdu中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否立即发送一帧
        """
        signal = self.signal_info_dict[signal_name]
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
        if send_pdu_immediately:
            self.send_pdu(self.signal_pduid_mapping[signal_name])

    def send_pdu(self, pdu_id: int, send_num=1):
        """
        发送PDU报文

        :param pdu_id: 报文ID, 数据类型：int，为excel的PDU Header ID列
        :param send_num: 发送次数，默认为1
        """
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"send_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        if "Cyclic-" in ethernet_pdu.send_type:
            send_cyclic = int(ethernet_pdu.send_type.replace("Cyclic-", "").replace("ms", ""))
        else:
            send_cyclic = 0

        pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
        pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
        pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
        pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
        bytes_list = DataTypeHanding.to_intlist(0, pdu_length)
        binary_string = ''.join(bin(b)[2:].zfill(8) for b in bytes_list)
        pdu_value_list = list(binary_string)
        for pdu_attr_name in dir(ethernet_pdu):
            if "__" not in pdu_attr_name:
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
                            # 假设数据为20，即0b10100， start_pos=6, length=5

                            if pdu_sub_obj.layout_format == "Motorola MSB":  # 格式为6,5,4,3,2
                                index = 0
                                for signal_value_bit in signal_value_list:
                                    seq = signal_bytes_position * 8 - 1 + (8 - start_position % 8) + index
                                    pdu_value_list[seq] = signal_value_bit
                                    index = index + 1
                            else:
                                res = index_change_to_intel(start_position, signal_length)  # 假设为7，6,10,9,8
                                for i, signal_value_bit in enumerate(signal_value_list):
                                    bit_index = res[i]
                                    seq = dbc_bit_to_bin_index(bit_index)
                                    pdu_value_list[seq] = signal_value_bit
        else:
            pdu_value_str = "".join(pdu_value_list)
            new_list = []
            for i in range(int(len(pdu_value_str) / 8)):
                curr_bin_str = pdu_value_str[8 * i:(8 * i + 8)]
                new_list.append(int(curr_bin_str, 2))
            else:
                # new_list.reverse()
                pdu_header_id_list.extend(pdu_length_list)
                pdu_header_id_list.extend(new_list)
                self.mock_socket_server.mock_mcu_send_pdu(pdu_header_id_list, send_cyclic, send_num)

    def ck_signal_values(self, signal_name: str, ck_values: list):
        """
        针对明确知道pcap数据包中信号值的场景，校验信号值的数量和值是否符合预期，一般用于事件型信号
        @param signal_name: 信号名
        @param ck_values：信号值列表
        """
        assert self.get_signal_values(signal_name) == ck_values

    def ck_period_time(self, signal_name: str, period, deviation=0.2, permit_fail_times=0):
        """
        用于周期性信号校验，但是考虑插帧场景，允许一定次数失败，返回失败次数
        @param signal_name: 信号名
        @param period: 期望周期, 单位s
        @param deviation: 默认±20%为可接受偏差
        @param permit_fail_times: 允许失败的次数，默认0次
        return: 失败次数
        """
        items = self.get_signal_items(signal_name)
        fail_timestamps = []
        last_time = None
        for item in items:
            if last_time is None:
                last_time = item[1]
            else:
                if abs(float(item[1]) - float(last_time) - period) / period > deviation:
                    fail_timestamps.append(item[1])
                    assert len(fail_timestamps) <= permit_fail_times, f"周期偏差次数过多, 失败时间戳{fail_timestamps}"
                last_time = item[1]
        return len(fail_timestamps)

    def ck_ordered_array(self, signal_name: str, ck_array: list):
        """
        校验周期下行pdu中信号为有序数组，无异常跳变，用于触发信号跳变后以新值继续周期发送的case
        从获取到ck_array第一个信号开始校验，因为抓tcpdump开始的数据可能还没有下发服务请求，不是期望值
        一直校验到pcap中最后的一个信号值
        @param signal_name: 信号名
        @param ck_array:  信号数组
        """
        tmp = copy.deepcopy(ck_array)
        curr_ck_value = ck_array.pop(0)
        start_ck = False
        values = self.get_signal_values(signal_name)

        if not values:  # 没有数据
            assert False, "未获取到数据"

        for value in values:
            if not start_ck and value == curr_ck_value:
                start_ck = True  # 拿到第一个期望数据，开始校验有序数组
                last_ck_value = curr_ck_value
                if ck_array:
                    curr_ck_value = ck_array.pop(0)
                continue

            if start_ck:
                if value == last_ck_value:
                    continue
                elif value == curr_ck_value:
                    last_ck_value = curr_ck_value
                    if ck_array:
                        curr_ck_value = ck_array.pop(0)
                else:
                    assert False, f"{value}不该出现在该时刻"
        if not start_ck:
            assert False, f"给的第一个数据不存在"
        if ck_array:
            assert False, f"未校验完成，剩余{ck_array}"
        logger.info(f"校验有序数组{tmp} -- True")

    def ck_period_signal_trigger(self, signal_name: str, idle_value: int, trigger_values: list):
        """
        校验周期下发的报文中有顺序的信号跳变, 用于下行几帧信号后回到idle的case
        @param signal_name: 信号名
        @param idle_value: 周期下发的报文中触发指定value后回到的idle值，如0
        @param trigger_values: 触发的非idle值列表，如发送3帧3，再发一帧1回到idle，[3, 3, 3, 1]
        """
        values = self.get_signal_values(signal_name)
        valid_values = [x for x in values if x != idle_value]
        assert trigger_values == valid_values, f"校验值{trigger_values} != 抓取信号{valid_values}"
        logger.info(f"校验跳变信号{trigger_values} -- True")


class MockSocketServer:

    def __init__(self, tcp_up_mcu_ip, tcp_up_mcu_port, tcp_down_mcu_ip, tcp_down_mcu_port,
                 tcp_down_mpu_ip, tcp_down_mpu_port, tcp_up_mpu_ip, tcp_up_mpu_port):
        self.tcp_up_mcu_ip = tcp_up_mcu_ip
        self.tcp_up_mcu_port = tcp_up_mcu_port
        self.tcp_down_mcu_ip = tcp_down_mcu_ip
        self.tcp_down_mcu_port = tcp_down_mcu_port
        self.tcp_down_mpu_ip = tcp_down_mpu_ip
        self.tcp_down_mpu_port = tcp_down_mpu_port
        self.tcp_up_mpu_ip = tcp_up_mpu_ip
        self.tcp_up_mpu_port = tcp_up_mpu_port

        UP_ADDRESS = (tcp_up_mcu_ip, tcp_up_mcu_port)
        DOWN_ADDRESS = (tcp_down_mcu_ip, tcp_down_mcu_port)
        # 创建监听socket
        self.upTcpServerSocket = socket(AF_INET, SOCK_STREAM)
        self.downTcpServerSocket = socket(AF_INET, SOCK_STREAM)
        # 绑定IP地址和固定端口
        self.upTcpServerSocket.bind(UP_ADDRESS)
        self.downTcpServerSocket.bind(DOWN_ADDRESS)
        self.upTcpServerSocket.settimeout(3)  # 设置超时时间，3s监听不到就抛异常，避免一直阻塞
        self.downTcpServerSocket.settimeout(3)
        self.up_client_socket = None
        self.down_client_socket = None
        self.down_payload = ""
        self.tcp_packet_list = []
        self.start_listen_flag = False
        self.get_client_socket_flag = False  # 是否在进行监听socket连接请求
        self.connection_established = False  # 上行socket的状态
        self.down_connection_established = False  # 下行socket的状态，暂未使用

    def start_listen(self):
        if self.start_listen_flag is False:
            self.upTcpServerSocket.listen(50)
            self.downTcpServerSocket.listen(50)
            self.start_listen_flag = True

    def get_client_socket(self):
        if self.get_client_socket_flag is False:
            thread1 = threading.Thread(target=self.__get_client_socket_thread, name="get client socket thread",
                                       daemon=True)
            self.get_client_socket_flag = True
            thread1.start()
            self._start_listen_pdu_data()

            thread2 = threading.Thread(target=self.__monitor_socket_status, name="monitor_socket_status", daemon=True)
            thread2.start()

    def __get_client_socket_thread(self):
        # 上下行socket状态字典，用于判断socket是否连接成功
        while self.get_client_socket_flag:
            try:
                logger.debug("等待socket连接")
                up_result = self.upTcpServerSocket.accept()
                self.up_client_socket = up_result[0]
                self.connection_established = True
                logger.info(f"监听到的socket port:{up_result[1]}")

                down_result = self.downTcpServerSocket.accept()
                self.down_client_socket = down_result[0]
                logger.info(self.down_client_socket.getsockopt(SOL_SOCKET, SO_RCVBUF))
                logger.info(f"监听到的socket port:{down_result[1]}")
            except OSError as e:
                logger.debug(f"socket OSError: {e}")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/bgm_eth_internal.py")
                logger.debug(f"socket Exception: {e}")
        else:
            logger.info("get client socket thread exit by test end")

    def __monitor_socket_status(self):
        """监听socket状态"""
        while self.get_client_socket_flag:
            time.sleep(1)
            try:
                if not is_socket_connected(self.up_client_socket):
                    self.connection_established = False
                # if not is_socket_connected(self.down_client_socket):
                #     self.down_connection_established = False
            except OSError as e:
                logger.error(f"{self.up_client_socket} --OSError {e}")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/bgm_eth_internal.py")
                logger.error(f"{self.up_client_socket} --Exception {e}")
        else:
            logger.info("monitor socket status thread exit by test end")

    def _start_listen_pdu_data(self):
        """开始监听下行TCP pdu报文"""
        t_listen_tcp = threading.Thread(target=self._listen_data_thread,
                                        daemon=True)
        t_listen_tcp.start()

    def _listen_data_thread(self):
        """
        Mock MCU监听MPU发送过来的TCP报文的线程
        """
        while self.get_client_socket_flag:
            if not self.connection_established:
                continue
            try:
                data = self.down_client_socket.recv(1024 * 101)
                # todo: 当前没有解析的需求，但是不recv则发送缓冲区会满，导致对端数据无法发送
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/bgm_eth_internal.py")
                time.sleep(1)

    def reset_client_socket(self):
        self.get_client_socket_flag = False
        self.connection_established = False

    def stop_client_socket(self):
        self.up_client_socket.close()
        self.down_client_socket.close()

    def stop_listen(self):
        self.reset_client_socket()
        self.upTcpServerSocket.close()
        self.downTcpServerSocket.close()

    def __send_pdu(self, data, send_cyclic, send_num):
        for i in range(send_num):
            self.up_client_socket.send(bytes(data))
            time.sleep(send_cyclic / 1000)

    def mock_mcu_send_pdu(self, pdu_data: list, send_cyclic=0, send_num=1, conn_timeout=5):
        """模拟mcu发送tcp上行数据"""
        # self.start_listen()
        # self.get_client_socket()

        wait_time = 0
        while wait_time < conn_timeout:
            if self.connection_established:
                break
            time.sleep(1)
            wait_time = wait_time + 1
        else:
            logger.info("TCP 连接建立失败，无法发送PDU报文")
            return
        try:
            logger.info(f"开始发送的pdu数据为：{pdu_data}, 发送周期为{send_cyclic}ms, 发送次数为{send_num}")
            thread = threading.Thread(
                target=self.__send_pdu,
                name="mock mcu send pdu",
                args=(pdu_data, send_cyclic, send_num),
                daemon=True
            )
            thread.start()
            # thread.join()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/bgm_eth_internal.py")
            logger.error(e.__repr__())
            self.up_client_socket.close()

    def mock_mcu_listen_result(self, timeout_second):
        """
        Mock MCU监听MPU发送过来的TCP报文
        @param timeout_second: 超时时间，单位秒
        @return:
        """
        # self.start_listen()
        # self.get_client_socket()
        time_start = time.time()
        listen_flag = True
        i = 1
        while listen_flag:
            data = self.down_client_socket.recv(1024 * 101)
            hex_string = ''.join(hex(b)[2:].zfill(2) for b in data)
            self.down_payload += hex_string
            curr_tcp_info = TcpPacket(i, time.time(), self.tcp_down_mpu_ip, self.tcp_down_mcu_ip,
                                      self.tcp_down_mpu_port,
                                      self.tcp_down_mcu_port, hex_string, len(self.down_payload), int(len(hex_string)))
            self.tcp_packet_list.append(curr_tcp_info)
            i = i + 1

            time_now = time.time()
            listen_flag = (time_now - time_start) < timeout_second
        else:
            logger.info("------------------TCP下行监听到的字节长度---------------------")
            logger.info(self.down_payload)
            logger.info(self.tcp_packet_list)

    def mock_mcu_listen_pdu(self, timeout_second=10):
        before_thread = threading.Thread(target=self.mock_mcu_listen_result, args=(timeout_second,))
        before_thread.setDaemon(True)
        before_thread.start()

    def empty_listen_result(self):
        self.down_payload = ""
        self.tcp_packet_list = []


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
        self.signals_value_list = []  # 信号值对象列表，每一个值的数据结构为：SignalItemInfo
        self.downstream = False  # 是否是下行信号
        self.name = ""
        self.layout_format = ""

    def __repr__(self):
        return f"PDU ID: {self.hex_str_pdu_header}, header_length:{self.hex_str_pdu_header_length}, " \
               f"start_position:{self.start_position}, signal_length:{self.signal_length}, factor:{self.factor}, " \
               f"offset:{self.offset}, sender: {self.sender}, initial_value: {self.initial_value}"


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

    def __init__(self, index, timestamp, ip_src, ip_dst, tcp_port_src, tcp_port_dst, payload,
                 payload_start, payload_length, downstream=True):
        self.index = index
        self.timestamp = timestamp
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.tcp_port_src = tcp_port_src
        self.tcp_port_dst = tcp_port_dst
        self.payload = payload
        self.payload_start = payload_start  # 在总数据包中的起始字节
        self.payload_length = payload_length  # 该以太网帧的data的字节长度
        self.downstream = downstream

    def __repr__(self):
        detail = f"报文序号：{self.index}, 时间戳：{self.timestamp}, 起始位置:{self.payload_start}, " \
                 f"报文长度：{self.payload_length}, 报文内容：{self.payload}"
        return detail


class PcapParseTcpInfo:
    """解析pcap中bgm内部以太网信号的值"""

    def __init__(self, signal_info_dict: dict, tcp_up_mcu_ip, tcp_up_mcu_port, tcp_down_mcu_ip, tcp_down_mcu_port,
                 tcp_down_mpu_ip, tcp_down_mpu_port, tcp_up_mpu_ip, tcp_up_mpu_port):
        self.signal_info_dict = signal_info_dict
        self.tcp_packet_list = []  # 所有tcp数据包的列表
        self.up_payload = ""  # 组装所有tcp上行数据包的payload
        self.down_payload = ""  # 组装所有tcp下行数据包的payload
        self.tcp_up_mcu_ip = tcp_up_mcu_ip
        self.tcp_up_mcu_port = tcp_up_mcu_port
        self.tcp_down_mcu_ip = tcp_down_mcu_ip
        self.tcp_down_mcu_port = tcp_down_mcu_port
        self.tcp_down_mpu_ip = tcp_down_mpu_ip
        self.tcp_down_mpu_port = tcp_down_mpu_port
        self.tcp_up_mpu_ip = tcp_up_mpu_ip
        self.tcp_up_mpu_port = tcp_up_mpu_port

    def parse_pcap_file(self, pcap_file):
        """解析pcap，将上下行tcp payload解析出来"""
        pkt = rdpcap(pcap_file)
        i = 0
        count_syn = 0
        for data in pkt:
            i = i + 1
            if 'TCP' in data:
                if data['TCP'].flags in [0x02, 0x11, 0x04]:  # 忽略客户端的挥手请求、连接建立请求、重置连接
                    count_syn = count_syn + 1
                    continue
                if data['TCP'].flags == 0x10:
                    if count_syn > 0:
                        count_syn = count_syn - 1
                        continue
                if "Raw" not in data:
                    continue

                hex_string = ''.join(hex(b)[2:].zfill(2) for b in data["Raw"].load)
                if (data["IP"].src == self.tcp_up_mcu_ip and data["TCP"].sport == self.tcp_up_mcu_port and
                        data["IP"].dst == self.tcp_up_mpu_ip and data["TCP"].dport == self.tcp_up_mpu_port):
                    # 上行tcp数据包
                    curr_tcp_info = TcpPacket(i, data.time, data["IP"].src, data["IP"].dst, data["TCP"].sport,
                                              data["TCP"].dport, hex_string, len(self.up_payload), int(len(hex_string)),
                                              False)
                    self.up_payload += hex_string
                    self.tcp_packet_list.append(curr_tcp_info)

                elif (data["IP"].src == self.tcp_down_mpu_ip and data["TCP"].sport == self.tcp_down_mpu_port and
                      data["IP"].dst == self.tcp_down_mcu_ip and data["TCP"].dport == self.tcp_down_mcu_port):
                    # 下行tcp数据包
                    curr_tcp_info = TcpPacket(i, data.time, data["IP"].src, data["IP"].dst, data["TCP"].sport,
                                              data["TCP"].dport, hex_string, len(self.down_payload),
                                              int(len(hex_string)), True)
                    self.down_payload += hex_string
                    self.tcp_packet_list.append(curr_tcp_info)

    def parse_signal_info(self, signal_obj: SignalObj):
        """将pcap解出来的上下行payload解析出指定的以太网信号数据"""
        curr_index = 0
        signal_value_list = []
        if signal_obj.downstream:
            payload = self.down_payload
        else:
            payload = self.up_payload
        self.signal_info_dict[signal_obj.name].signals_value_list = []  # 重置信号值列表
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
            signal_item.timestamp, signal_item.sequence = self.get_timestamp(index, signal_obj.downstream)
            if len(result) >= signal_obj.start_position:
                signal_item.signal_value = get_signal_value(result, signal_obj.start_position, signal_obj.signal_length,
                                                            signal_obj.layout_format)
            else:
                continue
            signal_value_list.append(signal_item)
            self.signal_info_dict[signal_obj.name].signals_value_list.append(signal_item)

    def get_timestamp(self, index, downstream: bool):
        """
        获取时间戳和pcap的以太网数据包index
        :param index: signal对象在上下行payload中的index
        :param downstream: 是否下行数据
        :return:
        """
        timestamp = 0
        sequence = 0
        for curr_tcp_info in self.tcp_packet_list:
            if curr_tcp_info.downstream != downstream:
                continue
            if curr_tcp_info.payload_start <= index < curr_tcp_info.payload_start + curr_tcp_info.payload_length:
                timestamp = curr_tcp_info.timestamp
                sequence = curr_tcp_info.index
                break
        return timestamp, sequence


if __name__ == '__main__':
    exp = DataTypeHanding.to_int([1, 1, 0, 1, 12, 9, 0, 10, 9, 15, 14, 9, 14, 4, 4, 10, 14, 15, 15, 10, 10, 5, 9, 14, 3, 4, 4, 8, 13, 9, 13, 0, 11, 10, 3, 4, 4, 3, 1, 6, 13, 0, 9, 12, 7, 12, 15, 3, 9, 2, 0, 14, 4, 4, 13, 3, 9, 11, 3, 3, 13, 6, 9, 12, 15, 2, 0, 8, 2, 13, 8, 15, 1, 15, 4, 15, 2, 3, 5, 9, 11, 13, 10, 13, 8, 5, 0, 5, 14, 2, 13, 1, 7, 8, 6, 10, 12, 11, 11, 3, 9, 5, 9, 4, 1, 6, 13, 8, 7, 5, 14, 3, 6, 2, 11, 15, 5, 0, 2, 2, 10, 9, 12, 13, 3, 0, 15, 4, 5, 12, 3, 9, 3, 11, 7, 6, 1, 5, 13, 4, 13, 15, 0, 5, 5, 9, 8, 0, 0, 13, 4, 8, 5, 8, 7, 1, 4, 10, 2, 1, 6, 11, 15, 12, 0, 6, 12, 6, 4, 6, 7, 1, 14, 3, 13, 5, 8, 5, 3, 4, 9, 12, 12, 5, 15, 14, 1, 8, 10, 0, 12, 13, 7, 2, 7, 10, 5, 2, 4, 12, 9, 1, 15, 15, 7, 1, 4, 13, 14, 0, 3, 4, 8, 13, 15, 14, 14, 0, 2, 8, 1, 11, 14, 6, 7, 6, 14, 10, 11, 5, 1, 10, 13, 14, 15, 9, 3, 2, 11, 14, 13, 14, 15, 15, 14, 1, 0, 2, 5, 4, 12, 6, 3, 13, 11, 0, 15, 2, 6, 12, 14, 6, 11, 8, 10, 9, 11, 13, 11, 1, 13, 8, 10, 3, 6, 1, 11, 4, 8, 13, 2, 1, 1, 4, 2, 2, 4, 4, 2, 10, 6, 8, 13, 1, 1, 7, 6, 14, 12, 1, 8, 10, 15, 3, 4, 12, 15, 0, 6, 15, 3, 11, 12, 2, 15, 4, 13, 7, 12, 9, 15, 5, 1, 13, 12, 11, 12, 14, 2, 5, 4, 14, 2, 12, 1, 5, 3, 8, 6, 0, 15, 14, 7, 14, 9, 12, 3, 2, 13, 10, 11, 7, 5, 13, 14, 5, 15, 10, 0, 7, 5, 4, 15, 5, 6, 7, 0, 6, 9, 4, 12, 7, 1, 9, 0, 11, 1, 7, 12, 8, 5, 2, 4, 4, 4, 6, 15, 11, 12, 9, 15, 7, 15, 9, 10, 7, 12, 15, 8, 4, 5, 1, 15, 3, 7, 3, 0, 14, 13, 10, 6, 12, 12, 14, 0, 11, 11, 11, 3, 3, 12, 2, 14, 15, 7, 14, 2, 0, 5, 3, 1, 8, 14, 6, 4, 7, 13, 10, 0, 10, 12, 7, 15, 7, 7, 4, 15, 12, 4, 3, 4, 3, 10, 11, 6, 7, 10, 14, 5, 2, 3, 15, 10, 2, 7, 8, 15, 1, 14, 12, 5, 9, 9, 11, 5, 8, 6, 13, 12, 1, 2, 9, 14, 5, 1, 12, 9, 15, 3, 2, 2, 7, 12, 9, 3, 4, 6, 10, 10, 11, 10, 7, 12, 7, 9, 1, 13, 2, 9, 8, 10, 9, 6, 11, 10, 7, 10, 15, 9, 6, 14, 3, 3, 1, 3, 11, 4, 5, 9, 14, 3, 6, 8, 15, 7, 10, 15, 10, 15, 14, 5, 7, 6, 9, 13, 2, 8, 4, 0, 9, 13, 4, 1, 6, 3, 9, 6, 12, 8, 4, 4, 1, 4, 14, 0, 13, 10, 13, 12, 6, 1, 14, 2, 0, 8, 8, 4, 8, 12, 2, 12, 2, 2, 14, 2, 6, 14, 13, 7, 2, 9, 15, 9, 13, 10, 0, 1, 1, 7, 13, 10, 1, 8, 11, 14, 0, 12, 11, 10, 4, 15, 6, 9, 6, 5, 0, 14, 13, 7, 6, 9, 2, 4, 3, 1, 7, 5, 11, 1, 7, 14, 14, 13, 5, 12, 3, 13, 0, 5, 15, 3, 9, 4, 15, 13, 10, 0, 7, 4, 12, 7, 1, 11, 2, 4, 2, 14, 4, 8, 2, 12, 6, 2, 2, 3, 2, 6, 3, 14, 1, 3, 12, 8, 0, 10, 11, 0, 7, 2, 5, 5, 3, 11, 4, 9, 4, 10, 6, 2, 13, 12, 5, 13, 1, 8, 11, 3, 4, 1, 9, 13, 13, 9, 9, 13, 3, 5, 0, 7, 7, 1, 3, 11, 2, 3, 2, 2, 11, 3, 7, 6, 13, 6, 7, 13, 13, 15, 8, 6, 15, 0, 0, 5, 8, 0, 15, 1, 14, 0, 2, 7, 11, 0, 1, 4, 8, 3, 14, 10, 11, 12, 12, 1, 6, 11, 11, 3, 7, 7, 3, 3, 2, 7, 6, 1, 9, 9, 1, 2, 1, 11, 8, 6, 1, 9, 11, 3, 2, 0, 13, 9, 8, 1, 6, 3, 9, 10, 4, 9, 6, 11, 13, 11, 0, 7, 6, 14, 12, 6, 1, 10, 0, 12, 1, 6, 9, 14, 3, 0, 0, 12, 1, 7, 0, 15, 14, 5, 3, 14, 8, 4, 15, 13, 1, 9, 10, 15, 6, 15, 5, 9, 7, 5, 6, 0, 8, 8, 9, 14, 15, 0, 6, 8, 3, 14, 3, 9, 7, 3, 5, 7, 4, 4, 2, 3, 5, 4, 0, 6, 5, 3, 4, 4, 14, 9, 2, 14, 12, 15, 13, 6, 13, 14, 3, 7, 14, 10, 14, 0, 11, 10, 10, 7, 5, 7, 7, 7, 8, 12, 4, 15, 7, 11, 1, 8, 2, 9, 14, 9, 8, 2, 10, 0, 3, 5, 13, 8, 5, 4, 8, 3, 12, 2, 10, 12, 0, 10, 7, 11, 7, 8, 7, 6, 3, 0, 9, 9, 9, 12, 11, 14, 11, 0, 6, 5, 12, 7, 9, 6, 13, 9, 3, 3, 12, 12, 3, 15, 8, 12, 6, 9, 9, 12, 6, 4, 1, 11, 5, 14, 4, 14, 4, 5, 3, 7, 10, 9, 3, 5, 11, 4, 11, 6, 15, 15, 10, 8, 11, 13, 13, 15, 9, 8, 9, 3, 6, 14, 6, 4, 8, 7, 4, 5, 0, 0, 3, 12, 12, 5, 13, 1, 1, 9, 3, 7, 4, 0, 9, 15, 1, 1, 0, 8, 4, 12, 7, 3, 6, 7, 10, 3, 14, 5, 7])
    logger.info(exp)
    bgm_eth = BgmEthInternal()
    bgm_eth.update(r'C:\Users\jiabin.zhu\Desktop\2024-05-17_14_04_45_bgm_2024_05_17_14_04_27.pcap')
    bgm_eth.ck_signal_values("LvSocCalibData", [exp])

    # bgm_eth.set_signal("CarConfig", DataTypeHanding.to_int(DataTypeHanding.hexstr_to_inlist("A3 01 81 08 FD 03 02 01 A2 02 09 03 04 02 01 02 84 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 85 82 02 02 01 01 03 02 6E 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 02 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 01 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 01 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 01 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 03 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 02 01 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 01 01 02 01 01 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 01 01 17 03 01 01 01 02 02 02 01 01 03 01 04 01 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 02 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 00 00 01 04 00 00 00 02 01 00 01 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 05 08 08 02 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 02 02 02 01 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 01 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 01 01 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01".replace(" ", ""))))
    # # bgm_eth.set_signal("GenericID", 0xFFFF)
    # bgm_eth.send_pdu(21004)
    # bgm_eth.ck_period_time("ChdLockReLeCtrlHmiReq", 0.05)
