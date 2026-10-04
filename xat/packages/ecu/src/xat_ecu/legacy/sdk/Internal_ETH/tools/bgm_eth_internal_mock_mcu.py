# -*- coding: utf-8 -*-

"""
@File        : bgm_eth_internal.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/02/04 14:51 PM
@Description : BGM内部以太网信号操作
@Examples    : example of how to use it
"""
import queue

from scapy.all import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu import S2sCombinationSendPdu
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_tcp_server import MockSocketServer
from xat_ecu.legacy.sdk.Internal_ETH.tools.utils import stop_thread
from xat_ecu.legacy.sdk.Internal_ETH.tools.bgm_eth_internal import BgmEthInternal, SignalItemInfo, get_signal_value, \
    index_change_to_intel, dbc_bit_to_bin_index


class BgmEthInternalMockMcu(BgmEthInternal):
    """
    bgm内部以太网控制，包括下行抓包解析，上行模拟udp或tcp数据发送
    """

    def __init__(self,
                 ipdu=None,
                 **kwargs):
        """
        初始化通信双方的ip、端口，以及总线信号控制和电源控制
        !!!! 如果不传递实参，则可以离线解析pcap数据
        @param ipdu: 总线信号控制模块, 默认None
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
        self.bl_ver = kwargs.get("bl_ver", "v_2_1_0")

        self.pcap_name = ""  # 抓包存储的名称，父类抓包接口会用到
        self.bgm_ssh = BGM_SSH(connect_type="vlan")
        self.mock_socket_server = None
        self.cspdu = None

        self.signal_info_dict = {}  # 信号数据集合{signal1: SignalObj1, signal2: SignalObj2, ....}
        self.signal_pduid_mapping = {}  # signal和pduid的映射 {signal1: pduid1, signal2: pduid1, signal3: pduid2}
        self.pduid_obj_mapping = {}  # pduid与pdu对象的映射{5311：BGMIntEthPDU5311}
        self.pduid_signalobj_mapping = {}  # pduid和信号对象的映射{5311: [signal1, signal2]}
        self._get_signal_dict()

        self.pcap_packets = []  # scapy抓包数据列表
        self.packets_queue = queue.Queue()  # 存放临时数据包，解析成字符串
        self.start_sniff = False  # 是否开始抓包
        self.capture_thread = None  # 抓包线程
        self.handle_pkg_thread = None  # 解包线程

        self.up_payload = ""  # 上行tcp数据包
        self.down_payload = b''  # 下行tcp数据包
        self.tcp_packet_list = []  # tcp数据帧

    def env_pre_process(self):
        """环境前处理，推送tcpdump至bgm内，修改s2s.json配置，根据ip端口配置确认是否要模拟mcu的udp或tcp数据发送，如需则启动模拟"""

        logger.info("开始启动mcu tcp的模拟发送")
        self.mock_socket_server = MockSocketServer(self.tcp_up_mcu_ip, self.tcp_up_mcu_port,
                                                   self.tcp_down_mcu_ip, self.tcp_down_mcu_port,
                                                   self.tcp_down_mpu_ip, self.tcp_down_mpu_port,
                                                   self.tcp_up_mpu_ip, self.tcp_up_mpu_port)
        self.mock_socket_server.start_mock_mcu()

        logger.info("开始启动mcu udp的模拟发送")
        self.cspdu = S2sCombinationSendPdu(self.ipdu, address=(self.udp_mcu_ip, self.udp_mcu_port))
        self.cspdu.continuous_combinationpdu_start()
        self.cspdu.s2ssendpdu_start(tar_address=(self.udp_mpu_ip, self.udp_mpu_port))

    def env_post_process(self):
        """环境后处理，包括停tcp收到socket，恢复bgm配置"""
        self.mock_socket_server.stop_mock_mcu()
        self.cspdu.s2ssendpdu_stop()
        self.cspdu.continuous_combinationpdu_stop()

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
                pdu_header_id_list.extend(pdu_length_list)
                pdu_header_id_list.extend(new_list)
                self.mock_socket_server.up_server.mock_mcu_send_pdu(pdu_header_id_list, send_cyclic, send_num)

    def empty(self):
        """
        清空已经装载的信号值信息
        """
        for signal_name in self.signal_info_dict:
            self.signal_info_dict[signal_name].signals_value_list = []
        self.pcap_packets = []
        self.packets_queue.queue.clear()
        self.down_payload = b''

    def get_signal_items(self, signal_name):
        """
        获取给到信号的数据列表
        @param signal_name: 指定的信号名
        return: 信号数据列表[(pcap_index, timestamp, signal_value), (), ()...]
        """
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
        if len(self.signal_info_dict[signal_name].signals_value_list) > 1:
            signal_value = self.signal_info_dict[signal_name].signals_value_list[-1]
            return signal_value.sequence, signal_value.timestamp, signal_value.signal_value
        else:
            return None, None, None

    def parse_signal(self, load: bytes, timestamp: EDecimal, index):
        """
        解析信号
        :param load: 一帧下行tcp数据，pdu_id(4 bytes) + pdu_len(4 bytes) + payload
        :param timestamp: tcp发送时间戳(代码运行所在系统的时间)
        :param index: tcp发送在pcap中所处编号
        :return:
        """
        pdu_id = DataTypeHanding.to_int(load[0: 4])
        payload_hex_string = DataTypeHanding.to_hexstr(load[8:])
        payload_bin_string = bin(int(payload_hex_string, 16))[2:].rjust(8 * DataTypeHanding.to_int(load[4: 8]), '0')
        for signal_obj in self.pduid_signalobj_mapping[pdu_id]:
            signal_item = SignalItemInfo()
            signal_item.timestamp, signal_item.sequence = timestamp, index
            signal_item.signal_value = get_signal_value(payload_bin_string,
                                                        signal_obj.start_position,
                                                        signal_obj.signal_length,
                                                        signal_obj.layout_format)
            self.signal_info_dict[signal_obj.name].signals_value_list.append(signal_item)

    def __handle_pkg_thread(self):
        """解析数据包"""
        while self.start_sniff or self.packets_queue.qsize() > 0:
            try:
                index, pkt = self.packets_queue.get_nowait()
            except queue.Empty:
                continue
            try:
                if pkt['TCP'].flags != 0x18:
                    continue
                if (pkt["IP"].src == self.tcp_down_mpu_ip and pkt["TCP"].sport == self.tcp_down_mpu_port and
                        pkt["IP"].dst == self.tcp_down_mcu_ip and pkt["TCP"].dport == self.tcp_down_mcu_port):
                    self.down_payload += pkt["Raw"].load
                    while True:
                        curr_len = DataTypeHanding.to_int(self.down_payload[4: 8])
                        if len(self.down_payload) >= (curr_len + 8):
                            self.parse_signal(self.down_payload[0: 8 + curr_len], pkt.time, index)
                            self.down_payload = self.down_payload[curr_len + 8:]
                        else:
                            break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/bgm_eth_internal_mock_mcu.py")
                traceback.print_exc()
                raise e

    def __capture_thread(self, my_filter, iface):
        """
        捕获数据包的线程函数
        :param my_filter: sniff接口传入的过滤参数
        :param iface: 指定抓包网卡
        :return:
        """
        logger.info(f"开始抓包，过滤参数{my_filter}")
        logger.info(f"开始抓包，过滤参数{iface}")
        pkt = sniff(filter=my_filter, iface=iface, prn=self.__pkt_callback)

    def __pkt_callback(self, pkt):
        """sniff抓包的回调，添加到pcap_packets列表中供生成pcap文件，添加到packets_queue用于实时信号解析"""
        self.pcap_packets.append(pkt)
        self.packets_queue.put((len(self.pcap_packets), pkt))

    def start_tcpdump(self, iface="veth0", host="172.16.5.1", port=30500, **kwargs):
        """
        先清空各缓存，再开始抓包
        :param iface: 抓包网卡号
        :param host: 过滤的ip
        :param port: 过滤的端口
        :param kwargs: 其他参数
        :return:
        """
        if self.start_sniff:
            logger.error("之前的抓包未停止，请检查脚本")
            self.stop_tcpdump()
        self.empty()
        if host is not None and port is not None:
            host_and_port = f"tcp and host {host} and port {port}"
        elif host is not None and port is None:
            host_and_port = f"tcp and host {host}"
        elif host is None and port is not None:
            host_and_port = f"tcp and port {port}"
        else:
            host_and_port = ""
        self.start_sniff = True
        self.capture_thread = threading.Thread(target=self.__capture_thread, args=(host_and_port, iface), daemon=True)
        self.capture_thread.start()
        self.handle_pkg_thread = threading.Thread(target=self.__handle_pkg_thread, daemon=True)
        self.handle_pkg_thread.start()

    def stop_tcpdump(self):
        """停止抓包"""
        stop_thread(self.capture_thread)
        self.start_sniff = False
        self.handle_pkg_thread.join()
        time_format = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        pcap_name = f"/root/bgm_log/bgm_{time_format}.pcap"
        wrpcap(pcap_name, self.pcap_packets)
        logger.info(f"抓包保存地址{pcap_name}")


if __name__ == '__main__':
    sniff(filter='tcp and host 172.16.5.1 and port 30500', count=1, timeout=1)
    # pkts = rdpcap(r'C:\Users\jiabin.zhu\Desktop\2024-08-03_02_03_48_bgm_2024_08_03_02_03_28.pcap')
    # count = 0
    # for pkt1 in pkts:
    #     count += 1
    #     if count == 471:
    #         print(1)
    #     if pkt1['TCP'].flags != 0x18:
    #         continue
    #     if pkt1["IP"].src == '172.16.5.1' and pkt1["TCP"].sport == 30500:
    #         print('1')

    # bgm_eth.set_signal("CarConfig", DataTypeHanding.to_int(DataTypeHanding.hexstr_to_inlist("A3 01 81 08 FD 03 02 01 A2 02 09 03 04 02 01 02 84 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 85 82 02 02 01 01 03 02 6E 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 02 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 01 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 01 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 01 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 03 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 02 01 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 01 01 02 01 01 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 01 01 17 03 01 01 01 02 02 02 01 01 03 01 04 01 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 02 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 00 00 01 04 00 00 00 02 01 00 01 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 05 08 08 02 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 02 02 02 01 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 01 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 01 01 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01".replace(" ", ""))))
    # # bgm_eth.set_signal("GenericID", 0xFFFF)
    # bgm_eth.send_pdu(21004)
    # bgm_eth.ck_period_time("ChdLockReLeCtrlHmiReq", 0.05)
