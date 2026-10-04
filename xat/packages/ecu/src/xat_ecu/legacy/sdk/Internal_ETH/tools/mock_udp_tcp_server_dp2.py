# -*- coding: utf-8 -*-
"""
@File        : mock_udp_tcp_server_dp2.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2024/09/25 13:08 PM
@Description : 模拟LCUL，LCUR，CD_MCU,AD_MCU
@Examples    : example of how to use it
"""
import time
import socket
import threading
import traceback
import copy
from socket import *
from typing import Union, Dict, List
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_tcp_server import is_socket_connected
from xat_ecu.legacy.sdk.Internal_ETH.tools.utils import stop_thread, ck_start_value, is_interrupt
from xat_ecu.legacy.sdk.Internal_ETH.tools.AutoSarCP_pdu_common import channel_name_to_quadruple, SignalItemInfo
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import TcpChannel, TCP_SC_CONFIGS, SOCKET_IP_PORT
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_eth_server_dp2 import MockServer, TcpSocketBusControl, \
    UdpSocketBusControl


class TcpServerManager:
    """TCP服务端管理，可能存在一个server连多个client"""

    def __init__(self, server_name='CdMcuTCPServer', veh_type="jupiter", bl_ver="v_0_4_0", **kwargs):
        """
        :param server_name: 服务端名称，以此读取所有数据库，再根据返回的client的ip地址，映射对应的数据库
        :param kwargs:
            ip_port: 用于测试时server_name不在网络拓扑内，需要指定ip_port否则找不到
        """
        self._server_name = server_name
        self._invalid_server = False  # 是否是无效server，为True则是测试构造的非网络拓扑中的server
        self.addr_busCtrl_map: Dict[tuple, TcpSocketBusControl] = {}  # 用于监听client连接后更新busCtrl的socket
        self.channel_busCtrl_map: Dict[str, TcpSocketBusControl] = {}  # 用于暴露到上层MockTcp，方便通过channel调用busCtrl能力
        self.sig_busCtrl_map: Dict[str, TcpSocketBusControl] = {}  # 用于给定信号快速找到bus->db->signal_values

        if server_name not in TCP_SC_CONFIGS:
            self._invalid_server = True
        if not self._invalid_server:
            self._server_addr = SOCKET_IP_PORT[server_name]
        else:
            try:
                self._server_addr = kwargs["ip_port"]
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_udp_tcp_server_dp2.py")
                raise ValueError(f"{server_name}不在仿真的网络拓扑内，必须要要传参ip_port")

        self.t_errors = []  # 记录线程中报错的信息

        self._server_socket = None
        self._listen_client_connect_flag = False  # 是否在监控客户端连接
        self._monitor_client_socket_flag = False
        self._t_listen_client = None
        self._t_monitor_client = None

        self.veh_type = veh_type
        self.bl_ver = bl_ver
        self._init_tcp_bus()
        self.start_manager()

    def stop_manager(self):
        """停止监听客户端连接，socket状态监控，停止接收tcp数据， 关闭管理器socket，查看线程是否有Error"""
        self._stop_monitor_client()
        self._stop_listen_client()
        for addr, tcp_bus in self.addr_busCtrl_map.items():
            tcp_bus.stop_sniff(write_file=True)
            tcp_bus.deinit_bus()
        try:
            self._server_socket.close()
            logger.info(f"{self._server_name}-socket已关闭")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_udp_tcp_server_dp2.py")
            traceback.print_exc()
            logger.error(e.__repr__())
        # 线程中Error检查
        for exception in self.t_errors:
            raise exception
        for addr, tcp_bus in self.addr_busCtrl_map.items():
            for exception in tcp_bus.t_errors:
                raise exception

    def start_manager(self):
        """开始监听客户端连接，socket状态监控，以及接收tcp数据。注意server init时自启动，无需调用"""
        self._establish_listen_socket()
        self._start_listen_client()
        self._start_monitor_client()

    def _start_listen_client(self):
        """启动监听客户端连接"""
        self._t_listen_client = threading.Thread(target=self._get_client_socket_thread,
                                                 name=f"{self._server_name}::listen_client",
                                                 daemon=True)
        self._listen_client_connect_flag = True
        self._t_listen_client.start()

    def _stop_listen_client(self):
        """结束监听客户端连接"""
        self._listen_client_connect_flag = False
        stop_thread(self._t_listen_client)
        # self._t_listen_client.join()

    def _start_monitor_client(self):
        """启动监控client socket的状态"""
        self._t_monitor_client = threading.Thread(target=self._monitor_client_socket_thread,
                                                  name=f"{self._server_name}::monitor_client",
                                                  daemon=True)
        self._monitor_client_socket_flag = True
        self._t_monitor_client.start()

    def _stop_monitor_client(self):
        """结束监控client socket的状态，一般服务端停止时才调用"""
        self._monitor_client_socket_flag = False
        stop_thread(self._t_monitor_client)
        # self._t_monitor_client.join()

    def _init_tcp_bus(self):
        """实例化TCPSocketBus对象"""
        if self._invalid_server:
            return
        for strClient in TCP_SC_CONFIGS[self._server_name]:
            client_addr = SOCKET_IP_PORT[strClient]
            channel = self._server_name + "_" + strClient
            bus = TcpSocketBusControl(channel, (self._server_addr, client_addr),
                                      veh_type=self.veh_type, bl_ver=self.bl_ver)
            self.addr_busCtrl_map[client_addr] = bus
            self.channel_busCtrl_map[channel] = bus
            for signal in bus.db.sig_info_dict:
                if signal in self.sig_busCtrl_map:
                    raise ValueError(f"server存在多个client发送相同信号名的信号{signal}，请排查脚本")
                self.sig_busCtrl_map[signal] = bus

    def _establish_listen_socket(self, client_max_num=5, m_timeout=3):
        """
        建立服务器socket监听客户端连接
        :param client_max_num:  最大客户端连接数量， 当前使用一般只会有一个客户端
        :param m_timeout: socket超时时间, 适用于send,recv,connect,accept
        :return:
        """
        self._server_socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind(self._server_addr)
        self._server_socket.settimeout(m_timeout)
        self._server_socket.listen(client_max_num)

    def _get_client_socket_thread(self):
        """
        监听客户端连接的线程，考虑对端可能重启，会有重连情况
        """
        while self._listen_client_connect_flag:
            try:
                client_socket, addr = self._server_socket.accept()
                logger.info(f"监听到的socket port:{addr}已连接！")

                if addr not in self.addr_busCtrl_map:
                    msg = f'{time.time()}--{addr}不应该与{self._server_name}进行连接'
                    logger.error(msg)
                    self.t_errors.append(ValueError(msg))
                    continue
                client_socket.settimeout(5)
                self.addr_busCtrl_map[addr].update_socket(client_socket)
            except OSError as e:
                pass  # accept 3s检测不到就会报socket.timeout即OSError
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_udp_tcp_server_dp2.py")
                traceback.print_exc()
                logger.error(e.__repr__())
        else:
            logger.info("get client socket thread exit by test end")

    def _monitor_client_socket_thread(self):
        """监控client socket的状态，识别对端重连的情况"""
        while self._monitor_client_socket_flag:
            time.sleep(1)
            for addr, tcp_bus in self.addr_busCtrl_map.items():
                sock = tcp_bus.sock
                if sock is None:
                    continue
                if not is_socket_connected(sock):
                    logger.warning(f'注意socket port:{addr}已断开！')
                    tcp_bus.reset_socket()
        else:
            logger.info("monitor socket status thread exit by test end")

    def get_signal_values(self, signal_name):
        """
        获取给到信号的信号值列表
        :param signal_name: 指定的信号名
        :return: 信号值列表[value1, value2, value3...]
        """
        signal_value_tuple_list = []
        signal_items = []
        bus = self.sig_busCtrl_map[signal_name]
        for signal_item in bus.db.sig_info_dict[signal_name].signals_value_list:  # SignalItemInfo
            signal_value_tuple_list.append(signal_item.signal_value)
            signal_items.append((signal_item.timestamp, signal_item.signal_value))
        logger.info(f"{signal_name}信号数据>>>> {signal_items}")
        logger.info(f"{signal_name}信号值>>>> {signal_value_tuple_list}")
        return signal_value_tuple_list


class MockUdp(MockServer):
    """JET2.0上模拟LCUL、LCUR、MCU建立上行的数据通路，该对象包含所有的udp通路（不包括cdd打包总线数据）"""

    def __init__(self, channel_dict: Dict[str, Union[tuple, None]] = None, veh_type="jupiter", bl_ver="v_0_4_0"):
        """
        基于配置，启动所有的通道
        :param channel_dict: key为通道名称，value为2个server和client的ip,port二元组或None，为None则使用默认地址
            举例1  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
            举例2  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: None
        """
        super().__init__(veh_type, bl_ver)
        self.server_sock_map = {}  # server端与socket的map，因为存在MCU既发单播，也发组播，使用的一个sock但是是两路数据库
        if channel_dict is not None:
            self.update_channel(channel_dict)

    def update_channel(self, channel_dict: Dict[str, Union[tuple, None]]):
        """
        新增以太网channel仿真发送
        :param channel_dict: key为通道名称，value为2个server和client的ip,port二元组或None，为None则使用默认地址
            举例1  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
            举例2  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: None
        :return:
        """
        for channel, quadruple in channel_dict.items():
            if channel in self.channel_busCtrl_map:
                logger.warn(f"{channel}已仿真，无法重复仿真")
                return
            server_name, client_name = channel.split('_')
            if quadruple is None:
                quadruple = channel_name_to_quadruple(channel)
            if server_name in self.server_sock_map:
                self.channel_busCtrl_map[channel] = UdpSocketBusControl(channel, quadruple, self.veh_type, self.bl_ver,
                                                                        sock=self.server_sock_map[server_name])
            else:
                self.channel_busCtrl_map[channel] = UdpSocketBusControl(channel, quadruple, self.veh_type, self.bl_ver)
                self.server_sock_map[server_name] = self.channel_busCtrl_map[channel].sock
            self.channel_busCtrl_map[channel].start_send_all_cycle_pdu()

    def stop_mock(self):
        """停止模拟UDP并关闭所有发送线程和socket"""
        for channel in self.channel_busCtrl_map:
            self.channel_busCtrl_map[channel].deinit_bus()
        for sock in self.server_sock_map.values():
            sock.close()


class MockTcp(MockServer):
    """JET2.0上模拟LCUL、LCUR、MCU建立下行TCP的数据通路"""

    def __init__(self, channel_dict: Dict[str, Union[tuple, None]] = None, veh_type="jupiter", bl_ver="v_0_4_0"):
        """
        基于配置，启动所有的通道
        :param channel_dict: key为通道名称，value为2个server和client的ip,port二元组或None，为None则使用默认地址
            举例1  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
            举例2  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: None
        """
        super().__init__(veh_type, bl_ver)
        self.server_manager_map: Dict[str, TcpServerManager] = {}  # 不同的server端对应的服务端管理
        if channel_dict is not None:
            self.update_channel(channel_dict)

    def update_channel(self, channel_dict: Dict[str, Union[tuple, None]]):
        """
        新增以太网channel仿真发送
        :param channel_dict: key为通道名称，value为2个server和client的ip,port二元组或None，为None则使用默认地址
            举例1  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
            举例2  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: None
        :return:
        """
        for channel, quadruple in channel_dict.items():
            if channel in self.channel_busCtrl_map:
                logger.warn(f"{channel}已仿真，无法重复仿真")
                return
            if quadruple is None:
                quadruple = channel_name_to_quadruple(channel)
            server_name, client_name = channel.split('_')
            if server_name not in self.server_manager_map:
                self.server_manager_map[server_name] = TcpServerManager(server_name, self.veh_type, self.bl_ver,
                                                                        ip_port=quadruple[0])
            self.channel_busCtrl_map[channel] = self.server_manager_map[server_name].channel_busCtrl_map[channel]

    def wait_client_reconnect(self, channel, timeout=20):
        """
        用于等待客户端连接，用于kill客户端场景
        :param channel: channel
        :param timeout: 等待连接的超时时间，s
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.channel_busCtrl_map[channel].connection_established:
                return True
            time.sleep(0.1)
        else:
            raise TimeoutError(f"{channel} TCP连接建立超时{timeout}s")

    def stop_mock(self):
        """停止模拟TCP并关闭所有发送线程和socket"""
        for server, manager in self.server_manager_map.items():
            manager.stop_manager()

    def get_signal_values(self, channel, signal_name):
        """
        获取给到信号的信号值列表
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return: 信号值列表[value1, value2, value3...]
        """
        signal_values = []
        signal_items = self.get_signal_items(channel, signal_name)
        for signal_item in signal_items:
            signal_values.append(signal_item.signal_value)
        logger.info(f"{signal_name}信号值>>>> {signal_values}")
        return signal_values

    def get_signal_items(self, channel, signal_name) -> List[SignalItemInfo]:
        """
        获取给到信号的数据列表
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return: 信号数据列表[SignalItemInfo, SignalItemInfo, SignalItemInfo...]
        """
        signal_items = self.channel_busCtrl_map[channel].db.sig_info_dict[signal_name].signals_value_list
        logger.info(f"{signal_name}以太网数据>>>> {signal_items}")
        return signal_items

    def get_last_signal(self, channel, signal_name):
        """
        获取对应信号的最后一个值
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return
        """
        signal_items = self.get_signal_items(channel, signal_name)
        if signal_items:
            return signal_items[-1].signal_value
        else:
            return None

    def ck_signal_values(self, channel, signal_name: str, ck_values: list):
        """
        针对明确知道pcap数据包中信号值的场景，校验信号值的数量和值是否符合预期，一般用于事件型信号
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :param ck_values: 信号值列表
        :return:
        """
        assert self.get_signal_values(channel, signal_name) == ck_values

    def ck_period_time(self, channel, signal_name: str, period, deviation=0.2, permit_fail_times=0):
        """
        用于周期性信号校验，但是考虑插帧场景，允许一定次数失败，返回失败次数
        :param channel: 通道名
        :param signal_name: 信号名
        :param period: 期望周期, 单位s
        :param deviation: 默认±20%为可接受偏差
        :param permit_fail_times: 允许失败的次数，默认0次
        :return: 失败次数
        """
        items = self.get_signal_items(channel, signal_name)
        fail_timestamps = []
        last_time = None
        for item in items:
            if last_time is None:
                last_time = item.timestamp
            else:
                if abs(item.timestamp - last_time - period) / period > deviation:
                    fail_timestamps.append(item.timestamp)
                    assert len(fail_timestamps) <= permit_fail_times, f"周期偏差次数过多, 失败时间戳{fail_timestamps}"
                last_time = item.timestamp
        return len(fail_timestamps)

    def ck_ordered_array(self, channel, signal_name: str, ck_array: list):
        """
        校验周期下行pdu中信号为有序数组，无异常跳变，用于触发信号跳变后以新值继续周期发送的case
        从获取到ck_array第一个信号开始校验，因为抓tcpdump开始的数据可能还没有下发服务请求，不是期望值
        一直校验到pcap中最后的一个信号值
        :param channel: 通道名
        :param signal_name: 信号名
        :param ck_array: 信号数组
        """
        tmp = copy.deepcopy(ck_array)
        curr_ck_value = ck_array.pop(0)
        start_ck = False
        last_ck_value = None
        values = self.get_signal_values(channel, signal_name)

        if not values:
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
        if curr_ck_value != last_ck_value:
            assert False, f"校验完{last_ck_value}未校验到{curr_ck_value}"
        logger.info(f"校验有序数组{tmp} -- True")

    def ck_period_signal_trigger(self, channel, signal_name: str, idle_value: int, trigger_values: list):
        """
        校验周期下发的报文中有顺序的信号跳变, 用于下行几帧信号后回到idle的case
        :param channel: 通道名
        :param signal_name: 信号名
        :param idle_value: 周期下发的报文中触发指定value后回到的idle值，如0
        :param trigger_values: 触发的非idle值列表，如发送3帧3，再发一帧1回到idle，[3, 3, 3, 1]
        """
        values = self.get_signal_values(channel, signal_name)
        valid_values = [x for x in values if x != idle_value]
        assert trigger_values == valid_values, f"校验值{trigger_values} != 抓取信号{valid_values}"
        logger.info(f"校验跳变信号{trigger_values} -- True")

    def empty_channel(self, channel):
        """
        清除某个通道的抓包数据
        :param channel: 通道名
        :return:
        """
        self.channel_busCtrl_map[channel].empty()

    def empty(self):
        """清除所有通道的抓包数据"""
        for channel, bus in self.channel_busCtrl_map.items():
            bus.empty()

    def ck_interrupt(self, channel, signal_name: str, ordered_array: list, ck_nums: int, idle=None):
        """
        校验周期下行的报文打断逻辑
        :param channel: 通道名
        :param signal_name: 信号名
        :param ordered_array: 信号发送顺序，例：
            [1, 2, 3]表示1被2打断，再被3打断，
            [1,2]表示1被2打断，
            [] 无打断，保持idle发送
        :param ck_nums: 正常发送帧数
        :param idle: idle值，如果为None则为事件帧，否则为周期帧的idle
        """
        tmp = copy.deepcopy(ordered_array)
        values = self.get_signal_values(channel, signal_name)
        if not values:
            assert False, "未获取到数据"
        if idle is not None:
            nums, values = ck_start_value(values, idle)
            assert nums != 0, f"初始数据无idle值{idle}"

        while ordered_array:
            curr_ck, exp_nums, ordered_array = is_interrupt(ordered_array, ck_nums, idle)
            nums, values = ck_start_value(values, curr_ck)
            assert nums in exp_nums, f"{curr_ck}帧数为{nums}，不为预期{exp_nums}帧"
        else:
            if idle is not None:
                nums, values = ck_start_value(values, idle)
                if tmp:
                    assert nums != 0, f"未恢复idle"
            assert values == [], f"idle后有异常数据"
        logger.info(f"校验打断信号{tmp} -- True")
