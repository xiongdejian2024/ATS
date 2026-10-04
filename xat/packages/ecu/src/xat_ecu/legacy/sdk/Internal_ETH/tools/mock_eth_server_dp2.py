# -*- coding: utf-8 -*-

"""
@File        : mock_mpu_tcp.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/09/29 14:51 PM
@Description : BGM内部以太网信号操作
@Examples    : example of how to use it
"""
import os
import time
import socket
import traceback
import threading
from scapy.all import sniff, wrpcap, EDecimal
from typing import List, Dict, Union, Tuple
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.Internal_ETH.tools.utils import stop_thread
from xat_ecu.legacy.sdk.driver.udp_socket import UdpSocketClient
from xat_ecu.legacy.sdk.Internal_ETH.tools.AutoSarCP_pdu_common import EthControlBase
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import SOCKET_IP_PORT

BUFFERSIZE = 1024 * 101


class UdpSocketBusControl(EthControlBase):
    """
    UDP以太网通道管理，包括socket创建，数据发送
    """

    def __init__(self, channel_name: str, quadruple: tuple, veh_type="jupiter", bl_ver="v_0_4_0", **kwargs):
        """

        :param channel_name: 通道名，用于获取数据库,
        :param quadruple: 2个二元组，用于通信, ((mcu_ip, mcu_port), (mpu_ip, mpu_port))
        :param veh_type: 车型，用于获取数据库
        :param bl_ver: 版本，用于获取数据库
        :param **kwargs: 可选参数
            sock: 发送udp的socket，可能之前已经创建，则复用，否则创建新的
        """
        super().__init__(channel_name, veh_type, bl_ver)

        self.server_addr = quadruple[0]
        self.client_addr = quadruple[1]
        self.sock = kwargs.get('sock', None)
        if self.sock is None:
            self.sock = UdpSocketClient(1, "UDP Socket tx", address=self.server_addr)

    def send_data(self, data: List[int]):
        """
        发送报文原子接口
        :param data: 发送的数据，列表形式
        :return:
        """
        try:
            self.sock.send(data, self.client_addr)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
            traceback.print_exc()
            logger.error(e.__repr__())

    def deinit_bus(self):
        """
        停止报文周期发送，关闭 socket
        :return:
        """
        self.stop_running()
        logger.info("running is stopped -- {}".format(self.channel))
        # self.sock.close()


class TcpSocketBusControl(EthControlBase):
    """
    TCP以太网通道管理，包括socket更新，数据发送，数据接收并解析
    """

    def __init__(self, channel_name: str, quadruple: tuple,
                 veh_type="jupiter", bl_ver="v_0_4_0", **kwargs):
        """
        :param channel_name: 通道名，用于获取数据库
        :param quadruple: 2个二元组，用于通信, ((mcu_ip, mcu_port), (mpu_ip, mpu_port))
        :param veh_type: 车型，用于获取数据库
        :param bl_ver: 版本，用于获取数据库
        :param kwargs:
            :iface: 网卡，容器执行默认veth0.52，配置的路由是走这个
        """
        super().__init__(channel_name, veh_type, bl_ver)

        self.sock: Union[socket, None] = None
        self.server_addr = quadruple[0]
        self.client_addr = quadruple[1]
        self.pcap_packets = []  # sniff抓包存储的数据，用于保存成pcap文件
        self.start_sniff_flag = False
        self.t_errors = []  # 记录线程中报错的信息
        self._t_capture = None
        self.sum_time = 0  # 抓包数据解析的时延汇总
        self.count = 0  # 抓包计数
        self.down_payload = b''  # 下行tcp数据包
        self.connection_established = False
        self._listen_pdu_data_flag = False
        self.auto_empty = True  # 配置是否自动清除缓存，防止存储的pcap文件过大  # todo 暂未使用
        self._iface = kwargs.get('iface', 'veth0.52')  # 容器中和CCU连接使用的虚拟网卡

    def deinit_bus(self):
        """
        停止报文周期发送，关闭 socket
        :return:
        """
        self.stop_running()
        self.reset_socket()

    def send_data(self, data: List[int]):
        """
        发送报文原子接口
        :param data: 发送的数据，列表形式
        :return:
        """
        try:
            self.sock.send(bytes(data))
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
            traceback.print_exc()
            logger.error(e.__repr__())

    def update_socket(self, sock: socket):
        """
        更新self.sock对应的socket实例，主要用于client断开后重新连接，需要更新socket fd
        :param sock: tcp socket对象
        :return:
        """
        self.sock = sock
        self.connection_established = True
        if not self.start_sniff_flag:  # 如果之前已经抓包了就不用重起线程抓包，client异常断开时会出现
            self._start_sniff()
        else:
            self.down_payload = b''  # 防止异常断开前有长数据只传了一半，和新数据放一起拼接有问题
        self._start_listen_pdu_data()
        self.start_send_all_cycle_pdu()
        self.resume_send_all_cycle_pdu()

    def reset_socket(self):
        """重置socket，用于client异常断开的情况，以及测试完成的情况"""
        self.connection_established = False
        self.stop_running()
        try:
            if self.sock is not None:
                self._listen_pdu_data_flag = False
                self.sock.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
            traceback.print_exc()
            logger.error(e.__repr__())
        self.sock = None

    def _start_sniff(self):
        """
        先清空各缓存，再开始抓包
        :return:
        """
        self.down_payload = b''
        host_and_port = f"tcp and host {self.client_addr[0]} and port {self.client_addr[1]}"
        self.start_sniff_flag = True
        self._t_capture = threading.Thread(target=self._capture_thread,
                                           args=(host_and_port, self._iface),
                                           daemon=True,
                                           name=f"{self.client_addr}->{self.server_addr}:sniff")
        self._t_capture.start()

    def stop_sniff(self, write_file=False):
        """
        停止抓包
        @param write_file: 是否写入文件
        """
        if self.start_sniff_flag:
            try:
                stop_thread(self._t_capture)  # todo: 存在堵塞问题
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
                traceback.print_exc()
                logger.error(e.__repr__())
            self.start_sniff_flag = False
            self._reset_count_time()
            if write_file:
                self.write_pcap()

    def write_pcap(self):
        """将存储的以太网抓包数据保持成文件"""
        if not os.path.isdir('/root/eth_log'):
            os.system('mkdir /root/eth_log')
        time_format = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        server_name = next(key for key, value in SOCKET_IP_PORT.items() if value == self.server_addr)
        client_name = next(key for key, value in SOCKET_IP_PORT.items() if value == self.client_addr)
        pcap_name = f"/root/eth_log/{time_format}_{server_name}_{client_name}.pcap"
        logger.info(f"抓包保存地址{pcap_name}")
        wrpcap(pcap_name, self.pcap_packets)

    def empty(self):
        """
        清空已经装载的信号值信息
        """
        for signal_name in self.db.sig_info_dict:
            self.db.sig_info_dict[signal_name].signals_value_list = []
        self.pcap_packets = []
        self.down_payload = b''
        self._reset_count_time()

    def _reset_count_time(self):
        """清空时延数据和抓包计数"""
        if self.count:
            logger.info(f"平均时延{self.sum_time / self.count}")
        self.count = 0
        self.sum_time = 0

    def _capture_thread(self, my_filter, iface):
        """
        捕获数据包的线程函数
        :param my_filter: sniff接口传入的过滤参数
        :param iface: 指定抓包网卡
        :return:
        """
        logger.info(f"开始抓包，过滤参数{iface}---{my_filter}")
        sniff(filter=my_filter, iface=iface, prn=self._parse_pkg)

    def _start_listen_pdu_data(self):
        """开始监听下行TCP pdu报文"""
        t_listen_tcp = threading.Thread(target=self._listen_data_thread,
                                        name=f"{self.client_addr}",
                                        daemon=True)
        self._listen_pdu_data_flag = True
        t_listen_tcp.start()

    def _listen_data_thread(self):
        """
        Mock MCU监听MPU发送过来的TCP报文的线程
        """
        while self._listen_pdu_data_flag:
            if not self.connection_established:
                continue
            try:
                data = self.sock.recv(BUFFERSIZE)
                # todo: 当前没有解析的需求，但是不recv则发送缓冲区会满，导致对端数据无法发送
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
                pass

    def _parse_pkg(self, pkt):
        """解析数据包中的信号"""
        try:
            self.pcap_packets.append(pkt)
            if (pkt["IP"].src == self.client_addr[0] and pkt["TCP"].sport == self.client_addr[1] and
                    pkt["IP"].dst == self.server_addr[0] and pkt["TCP"].dport == self.server_addr[1]):
                flags = pkt['TCP'].flags
                if flags & 1 or flags & 2 or flags & 4:  # 分别对应Fin，Syn，Reset
                    return
                if "Raw" not in pkt:
                    return
                self.down_payload += pkt["Raw"].load
                self.count += 1
                delta_time = round(time.time() - pkt.time, 6)
                self.sum_time += delta_time
                # logger.info(f"耗时{delta_time}收到{DataTypeHanding.to_hexstr(pkt['Raw'].load)}")
                while True:
                    curr_len = DataTypeHanding.to_int(self.down_payload[4: 8])
                    if len(self.down_payload) >= (curr_len + 8):
                        self.db.parse_signal(self.down_payload[0: 8 + curr_len], float(pkt.time))
                        self.down_payload = self.down_payload[curr_len + 8:]
                    else:
                        break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_eth_server_dp2.py")
            traceback.print_exc()
            logger.error(e.__repr__())

    # def _check_client_socket_connected(self, conn_timeout):
    #     """
    #     校验客户端连接状态
    #     :param conn_timeout: 等待连接时间
    #     :return:
    #     """
    #     wait_time = 0
    #     while wait_time < conn_timeout:
    #         if self.connection_established:
    #             return True
    #         time.sleep(0.2)
    #         wait_time = wait_time + 0.2
    #     else:
    #         raise TimeoutError("TCP 连接建立超时，无法发送PDU报文")


class MockServer:
    """承载UDP和TCP模拟服务端的通用接口"""

    def __init__(self, veh_type="jupiter", bl_ver="v_0_4_0"):
        self.channel_busCtrl_map: Dict[str, Union[UdpSocketBusControl, TcpSocketBusControl]] = {}
        self.veh_type = veh_type
        self.bl_ver = bl_ver

    def set_signal(self, channel: str, signal_name: str, signal_value: Union[int, float]):
        """
        设置信号值
        :param channel: 通道名
        :param signal_name: 信号名
        :param signal_value: 信号值，如果是float就是物理值，如果是int就是总线值
        :return:
        """
        self.channel_busCtrl_map[channel].db.set_signal(signal_name, signal_value)

    # def start_channel_send_cycle_pdu(self, channel):
    #     """启动指定通道的周期报文发送"""
    #     self.channel_busCtrl_map[channel].start_send_all_cycle_pdu()
    #     self.channel_busCtrl_map[channel].resume_send_all_cycle_pdu()

    def stop_send_cycle_pdu(self, channel: str, pduid: int):
        """停止指定通道的周期发送报文"""
        self.channel_busCtrl_map[channel].stop_send_cycle_pdu(pduid)

    def stop_send_all_cycle_pdu(self, sender=None):
        """
        停止所有周期发送报文
        :param sender: 指定发送端，数据库中pdu的sender属性
        :return:
        """
        for channel, bus in self.channel_busCtrl_map.items():
            bus.stop_send_all_cycle_pdu(sender)

    def resume_send_cycle_pdu(self, channel: str, pduid: int):
        """恢复周期发送报文"""
        self.channel_busCtrl_map[channel].resume_send_cycle_pdu(pduid)

    def resume_send_all_cycle_pdu(self, sender=None):
        """
        恢复所有周期发送报文
        :param sender: 指定发送端，数据库中pdu的sender属性
        :return:
        """
        for channel, bus in self.channel_busCtrl_map.items():
            bus.resume_send_all_cycle_pdu(sender)

    def set_signal_and_send(self, channel: str, signal_name, signal_value,
                            send_pdu_immediately=False, send_num=1, cycle_time=5):
        """
        设定Event Trigger类型帧中的指定信号的数值
        :param channel:  通道名，即EthChannel
        :param signal_name:  信号名
        :param signal_value:  信号设定的值
        :param send_pdu_immediately: 是否立即发送
        :param send_num: 如果立即发送，指定发送次数，默认1次
        :param cycle_time: 如果立即发送，指定发送周期，默认5ms
        """
        self.channel_busCtrl_map[channel].set_signal_and_send(signal_name, signal_value,
                                                              send_pdu_immediately, send_num, cycle_time)

    def send_pdu(self, channel: str, pduid: int, send_num=1, cycle_time=5):
        """
        给指定通道发送指定pduid报文
        :param channel: 通道名，即EthChannel
        :param pduid: 报文id
        :param send_num: 指定发送次数，默认1次
        :param cycle_time: 指定发送周期，默认5ms
        :return:
        """
        self.channel_busCtrl_map[channel].send_pdu(pduid, send_num, cycle_time)


if __name__ == "__main__":
    logger = Logger().get_logger("test")

    # pdu_config = {"AdMcuTCPServer_AdSocTCPClient2": ("172.16.5.21", 8001, "172.16.5.1", 8901)}
    #
    # pdu = MockUdp(pdu_config, veh_type="jupiter", bl_ver="v_0_4_0")
