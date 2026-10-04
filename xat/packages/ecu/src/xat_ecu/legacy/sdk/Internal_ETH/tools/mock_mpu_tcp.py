# -*- coding: utf-8 -*-

"""
@File        : mock_mpu_tcp.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/06/17 14:51 PM
@Description : BGM内部以太网信号操作
@Examples    : example of how to use it
"""

from scapy.all import *
from socket import *
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
import importlib
from xat_ecu.legacy.interface.nuc_app import exec_shell


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
    # if layout_format == "motorolamsb":
    if True:
        n = 1
        while (n * 8 - 1) < start_index:
            n = n + 1
        result = payload[(n - 1) * 8 - 1 + (8 - start_index % 8): ((n - 1) * 8 - 1 + (8 - start_index % 8) + length)]
    # elif layout_format == "opaque":
    #     dbc_bit_layout = index_change_to_intel(start_index, length)
    #     result = "".join([payload[dbc_bit_to_bin_index(x)] for x in dbc_bit_layout])
    # else:
    #     assert False, f"layout_format:{layout_format}异常"

    return int(result, 2)


def dbc_bit_to_bin_index(bit):
    """dbc中的bit位转成2进制数据中的index"""
    byte_index, bytes_mod = divmod(bit, 8)
    return byte_index * 8 + 7 - bytes_mod


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


def is_socket_connected(client_socket, write_enable):
    """
    判断socket是否连接成功
    :param client_socket: socket对象
    :return: True or False
    """
    if client_socket is None:
        logger.info("socket is None")
        return True
    readable, writable, exceptional = select.select([client_socket], [client_socket], [], 1)  # 1s周期轮询
    # write_enable = False
    read_enable = False

    if client_socket not in readable and client_socket not in writable:
        return False

    if client_socket in readable:
        # 套接字可读
        received_data = client_socket.recv(1024)
        if not received_data:
            read_enable = False  # 不可读
        else:
            read_enable = True  # 可读

    # if client_socket in writable:
    #     # 套接字可写
    #     try:
    #         data_to_send = b"Hello, server"
    #         client_socket.send(data_to_send)
    #         write_enable = True  # 可写
    #     except ConnectionResetError:
    #         logger.info("远程主机已关闭连接，不可写")
    #         write_enable = False  # 不可写
    #     except BrokenPipeError:
    #         logger.info("socket连接已断开，不可写")
    #         write_enable = False  # 不可写
    #     except socket.error as e:
    #         logger.info(f"Socket error:{e}，不可写")
    #         write_enable = False  # 不可写

    if read_enable or write_enable:
        return True
    else:
        return False


class MockMpuSocketClient:
    """
    模拟MPU与MCU进行TCP Socket交互，端口：上行为30501，下行为30500
    """

    def __init__(self, tcp_up_mcu_ip="172.16.5.2", tcp_up_mcu_port=30501, tcp_down_mcu_ip="172.16.5.2",
                 tcp_down_mcu_port=30500, tcp_down_mpu_ip="172.16.5.1", tcp_down_mpu_port=30500,
                 tcp_up_mpu_ip="172.16.5.1", tcp_up_mpu_port=30501, auto_connect=True, veh_type="mars1",
                 bl_ver="v_2_0_0"):

        self.tcp_up_mcu_ip = tcp_up_mcu_ip
        self.tcp_up_mcu_port = tcp_up_mcu_port
        self.tcp_down_mcu_ip = tcp_down_mcu_ip
        self.tcp_down_mcu_port = tcp_down_mcu_port
        self.tcp_down_mpu_ip = tcp_down_mpu_ip
        self.tcp_down_mpu_port = tcp_down_mpu_port
        self.tcp_up_mpu_ip = tcp_up_mpu_ip
        self.tcp_up_mpu_port = tcp_up_mpu_port

        # 连接配置
        self.UP_ADDRESS = (tcp_up_mpu_ip, tcp_up_mpu_port)
        self.UP_SERVER_ADDRESS = (tcp_up_mcu_ip, tcp_up_mcu_port)
        self.DOWN_ADDRESS = (tcp_down_mpu_ip, tcp_down_mpu_port)  # 下行MPU绑定的IP端口
        self.DOWN_SERVER_ADDRESS = (tcp_down_mcu_ip, tcp_down_mcu_port)  # 下行MCU绑定的IP端口
        # 创建监听socket

        self.upTcpClientSocket = socket(AF_INET, SOCK_STREAM)
        self.downTcpClientSocket = socket(AF_INET, SOCK_STREAM)
        self.write_enable = False
        self.cycle_message_sending_list = []
        # 绑定IP地址和固定端口
        retry_num = 30
        while retry_num > 0:
            retry_num -= 1
            try:
                self.upTcpClientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                self.upTcpClientSocket.bind(self.UP_ADDRESS)
                break
            except OSError as e:
                logger.info(f"绑定 {self.UP_ADDRESS} 异常: {e.__repr__()}, 2秒后重试")
                time.sleep(2)

        retry_num = 30
        while retry_num > 0:
            retry_num -= 1
            try:
                self.downTcpClientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                self.downTcpClientSocket.bind(self.DOWN_ADDRESS)
                break
            except OSError as e:
                logger.info(f"绑定 {self.DOWN_ADDRESS} 异常: {e.__repr__()}, 2秒后重试")
                time.sleep(2)

        # 设置超时时间，3s连接不上就抛异常，避免一直阻塞
        self.upTcpClientSocket.settimeout(3)
        self.downTcpClientSocket.settimeout(3)

        # 连接保持
        self.stop_client_connect = False
        self.start_monitor_and_reconnect = False  # 是否启动了重连线程、监听线程
        self.up_connection_established = False  # 上行socket client 连接状态
        self.down_connection_established = False  # 下行socket client 连接状态

        # 信号数据字典
        self.signal_info_dict = {}  # 信号数据集合{signal1: SignalObj1, signal2: SignalObj2, ....}
        self.signal_pduid_mapping = {}  # signal和pduid的映射 {signal1: pduid1, signal2: pduid1, signal3: pduid2}
        self.pduid_obj_mapping = {}  # pduid与pdu对象的映射{5311：BGMIntEthPDU5311}
        self.veh_type = veh_type
        self.bl_ver = bl_ver
        self.cycle_pdu_list = []  # 发送方为SoC带有周期属性的帧列表
        self.auto_send_cycle_pdu_list = {}  # 需要周期性发送的帧列表
        self.__get_signal_dict()

        self.up_payload = ""  # 从MCU接收到的TCP报文
        self.tcp_packet_list = []

        if auto_connect:
            self.start_connect()

    def start_connect(self):
        """创建socket连接：建立TCP上行客户端、TCP下行客户端 的连接，启动重连、监听线程"""
        try:
            self.upTcpClientSocket.connect(self.UP_SERVER_ADDRESS)
            logger.info(f"连接{self.tcp_up_mcu_ip}:{self.tcp_up_mcu_port}成功")
            self.up_connection_established = True
        # except socket.timeout as e:
        #     self.up_connection_established = False
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
            self.up_connection_established = False
            logger.info(f"kkkkk:{e.__repr__()},{self.UP_SERVER_ADDRESS}")

        try:
            self.downTcpClientSocket.connect(self.DOWN_SERVER_ADDRESS)
            logger.info(f"连接{self.tcp_down_mcu_ip}:{self.tcp_down_mcu_port}成功")
            self.down_connection_established = True
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
            logger.info(f"首次连接异常，异常类型：{type(e)}")
            self.down_connection_established = False

        self.__start_cycle_single_send()  # socket建立连接后，开始周期型信号的发送线程
        self.__start_reconnect_monitor_thread()

    def change_signal(self, signal_name, signal_value, send_type=0):
        """
        更改ETH Signal信号给到MCU，此接口主要用于Cycle PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_type 信号发送类型：0-表示信号改变后等到固定周期在发送 1-表示插帧,会立即发送变化信号,但是信号周期保持不变
        """
        send_pdu_immediately = True if send_type == 1 else False
        self.set_cycle_signal_value(signal_name, signal_value, send_pdu_immediately)

    def set_signal(self, signal_name, signal_value, send_frame=1, send_cycle=50, send_type_immediately=True):
        """
        发送ETH signal信号给到MCU，此接口主要用于Trigger PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_frame：int 信号发送帧数 如果PDU报文发送类型为：trigger,默认值为1 frame
        :param send_type_immediately 信号是否立即发送,默认值为True
        :param send_cycle 如果PDU报文发送类型为：trigger,参考此参数,此参数默认值为50ms
        """
        self.set_trigger_signal_value(signal_name, signal_value, send_type_immediately, send_frame, send_cycle)

    def start_send_all_cycle_frame(self):
        """触发发送所有周期型pdu报文"""
        for ethernet_pdu_name in self.cycle_pdu_list:
            ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)
            ethernet_pdu.send_flag = True

    def stop_send_all_cycle_frame(self):
        """停发所有周期型pdu报文"""
        for ethernet_pdu_name in self.cycle_pdu_list:
            ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)
            ethernet_pdu.send_flag = False

    def set_cycle_signal_value(self, signal_name, signal_value, send_pdu_immediately=False):
        """
        设定周期类型帧中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否尽快发送
        """
        for ethernet_pdu_name in self.cycle_pdu_list:
            ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)
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
                setattr(ethernet_pdu, "send_flag", True)  # 确保信号对应的报文可发送
                # setattr(ethernet_pdu, "change_flag", True)  # 确保信号对应的报文的pdu_data 重新计算
                ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)  # 更新其值
                time.sleep(0.01)
                if send_pdu_immediately:
                    ethernet_pdu_cycle = int(ethernet_pdu.send_type.replace("Cyclic-", "").replace("ms", ""))
                    if getattr(ethernet_pdu, "last_send_time") != 0:
                        setattr(ethernet_pdu, "last_send_time", int(time.time() * 1000) - ethernet_pdu_cycle)

    def start_send_cycle_frame(self, pdu_id: int):
        """单独设置一个周期型帧的发送"""
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"send_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        setattr(ethernet_pdu, "send_flag", True)
        setattr(ethernet_pdu, "change_flag", True)

    def stop_send_single_cycle_frame(self, pdu_id: int):
        """单独设置一个周期型帧的发送"""
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"send_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        setattr(ethernet_pdu, "send_flag", False)

    def set_trigger_signal_value(self, signal_name, signal_value, send_pdu_immediately=False, send_num=1, cycle_time=5):
        """
        设定Event Trigger类型帧中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否立即发送
        @param send_num: 如果立即发送，指定发送次数，默认1次
        @param cycle_time: 如果立即发送，指定发送周期，默认5ms
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
            self.send_trigger_frame(self.signal_pduid_mapping[signal_name], send_num, cycle_time)

    def send_trigger_frame(self, pdu_id: int, send_num=1, cycle_time=5):
        """
        创建一个线程，并发送事件型的PDU报文

        :param pdu_id: 报文ID, 数据类型：int，为excel的PDU Header ID列
        :param send_num: 发送次数，默认为1
        :param cycle_time: 发送周期，默认5ms
        """
        if pdu_id not in self.pduid_obj_mapping:
            logger.info(f"send_pdu失败，入参pdu_id：{pdu_id} 不存在")
            return
        # pdb.set_trace()
        ethernet_pdu = self.pduid_obj_mapping[pdu_id]
        pdu_data = self.__calculation_pdu_data(ethernet_pdu)
        self.__mock_mpu_send_pdu(pdu_data, cycle_time, send_num)

    def send_pdu(self, signal_name):
        pdu_header_id = None
        is_cycle = False
        for ethernet_pdu_name in dir(self.bgm_eth_internal):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
            if "BGMIntEthPDU" in ethernet_pdu_name:  # 报文
                ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)  # pdu对象，如BGMIntEthPDU0001
                # 获取pdu对象的属性
                pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
                sender = getattr(ethernet_pdu, "sender")
                if "Cyclic-" in getattr(ethernet_pdu, "send_type"):
                    is_cycle = True
                else:
                    is_cycle = False
                if signal_name in dir(ethernet_pdu):
                    break
        else:
            logger.error(f"{signal_name} 不存在")

        if not is_cycle:
            self.send_trigger_frame(pdu_header_id)
        else:
            self.start_send_cycle_frame(pdu_header_id)

    def start_listen_mcu_message(self, timeout_second):
        """启动监听线程：监听从MCU发出的TCP报文"""
        thread = threading.Thread(
            target=self.__mock_mpu_listen_mcu_message,
            name="mock mpu send pdu",
            args=(timeout_second,),
            daemon=True
        )
        thread.start()

    def get_signal_items(self, signal_name):
        """
        获取给到信号的数据列表
        @param signal_name: 指定的信号名
        return: 信号数据列表[(pcap_index, timestamp, signal_value), (), ()...]
        """
        self.__reload_signal_value_list()
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
        self.__reload_signal_value_list()
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
        self.__reload_signal_value_list()
        if len(self.signal_info_dict[signal_name].signals_value_list) > 1:
            signal_value = self.signal_info_dict[signal_name].signals_value_list[-1]
            return signal_value.sequence, signal_value.timestamp, signal_value.signal_value
        else:
            return None, None, None

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

    def empty_listen_result(self):
        """
        清空已经装载的信号值信息
        """
        for signal_name in self.signal_info_dict:
            self.signal_info_dict[signal_name].signals_value_list = []
        self.__empty_listen_result()  # 清空实时监听的结果

    # def reset_client_socket(self):
    #     """重置socket连接:上行、下行 socket client"""
    #     self.up_connection_established = False
    #     self.down_connection_established = False

    def stop_client_socket(self):
        """关闭socket连接: 上下行客户端socket"""
        self.stop_client_connect = True
        time.sleep(0.5)  # 确保重连线程、监听线程已退出
        self.upTcpClientSocket.close()
        self.downTcpClientSocket.close()
        time.sleep(0.5)

    def __start_reconnect_monitor_thread(self):
        """启动重连线程、监听线程"""
        if self.start_monitor_and_reconnect is False:
            thread1 = threading.Thread(target=self.__reconnect_socket_server, name="client reconnect thread",
                                       daemon=True)
            thread1.start()

            thread2 = threading.Thread(target=self.__monitor_socket_status, name="monitor socket status", daemon=True)
            thread2.start()
            self.start_monitor_and_reconnect = True

    def __reconnect_socket_server(self):
        """用于上行客户端socket、下行客户端socket连接失败后，自动重连"""
        while self.stop_client_connect is False:
            time.sleep(1)
            try:
                if not self.up_connection_established:  # 上行连接未建立成功
                    self.upTcpClientSocket.close()
                    time.sleep(0.5)
                    self.upTcpClientSocket = socket(AF_INET, SOCK_STREAM)
                    try:
                        # 绑定IP地址和固定端口
                        retry_num = 30
                        while retry_num > 0:
                            retry_num -= 1
                            try:
                                self.upTcpClientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                                self.upTcpClientSocket.bind(self.UP_ADDRESS)
                                break
                            except OSError as e:
                                logger.info(f"上行，绑定 {self.UP_ADDRESS} 异常: {e.__repr__()}, 2秒后重试")
                                time.sleep(2)
                        self.upTcpClientSocket.settimeout(3)
                        logger.info(f"上行，尝试连接 {self.UP_SERVER_ADDRESS}")
                        self.upTcpClientSocket.connect(self.UP_SERVER_ADDRESS)
                        logger.info(f"上行，与{self.tcp_up_mcu_ip}:{self.tcp_up_mcu_port}重连成功......")
                        self.up_connection_established = True
                    except socket.timeout as e:
                        logger.info(f"上行，{self.UP_SERVER_ADDRESS}连接失败")
                        self.up_connection_established = False

                if not self.down_connection_established:  # 下行连接未建立成功
                    self.downTcpClientSocket.close()
                    time.sleep(0.5)
                    self.downTcpClientSocket = socket(AF_INET, SOCK_STREAM)
                    try:
                        retry_num = 30
                        while retry_num > 0:
                            retry_num -= 1
                            try:
                                self.downTcpClientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                                self.downTcpClientSocket.bind(self.DOWN_ADDRESS)
                                break
                            except OSError as e:
                                logger.info(f"下行，绑定 {self.DOWN_ADDRESS} 异常: {e.__repr__()}, 2秒后重试")
                                time.sleep(2)
                        self.downTcpClientSocket.settimeout(3)
                        logger.info(f"下行，尝试连接 {self.DOWN_SERVER_ADDRESS}")
                        self.downTcpClientSocket.connect(self.DOWN_SERVER_ADDRESS)
                        logger.info(f"下行，与{self.tcp_down_mcu_ip}:{self.tcp_down_mcu_port}重连成功......")
                        self.down_connection_established = True
                    except socket.timeout as e:
                        logger.info(f"下行，{self.DOWN_SERVER_ADDRESS}连接失败")
                        self.down_connection_established = False
            except OSError as e:
                logger.debug(f"socket OSError: {e}")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
                logger.debug(f"socket Exception: {e}")
        else:
            logger.info("get client socket thread exit by test end")

    def __monitor_socket_status(self):
        """监听socket状态状态：判断连接是否断开"""
        while self.stop_client_connect is False:
            time.sleep(2)
            try:
                self.upTcpClientSocket.getsockopt(SOL_SOCKET, SO_ERROR)
                if is_socket_connected(self.upTcpClientSocket, True):
                    self.up_connection_established = True
                else:
                    logger.info(f"2-1: 连接{self.tcp_up_mcu_ip}:{self.tcp_up_mcu_port}检测到已经断开......")
                    self.up_connection_established = False

            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
                logger.info(f"2-2: 连接{self.tcp_up_mcu_ip}:{self.tcp_up_mcu_port}检测到已经断开......{type(e)}")
                self.up_connection_established = False
                time.sleep(2)

            try:
                if is_socket_connected(self.downTcpClientSocket, self.write_enable):
                    self.down_connection_established = True
                else:
                    logger.info(f"3-1: 连接{self.tcp_down_mcu_ip}:{self.tcp_down_mcu_port}检测到已经断开......")
                    self.down_connection_established = False
                    time.sleep(2)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
                logger.info(f"3-2: 连接{self.tcp_down_mcu_ip}:{self.tcp_down_mcu_port}检测到已经断开......{type(e)}")
                self.down_connection_established = False
        else:
            logger.info("monitor socket status thread exit by test end")

    def __get_signal_dict(self):
        """
        从内部以太网数据库中根据以太网报文名称获取报文的初始值
        """
        module_name = f"xat_ecu.legacy.sdk.data.{self.veh_type}.Internal_ETH.{self.bl_ver}.bgm_eth_internal"
        logger.info(f"当前使用的DB文件为：{module_name}")
        self.bgm_eth_internal = importlib.import_module(module_name)
        for ethernet_pdu_name in dir(self.bgm_eth_internal):  # dir内置函数返回对象的所有属性和方法名称的列表，全部是str类型
            if "BGMIntEthPDU" in ethernet_pdu_name:  # 报文
                ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)  # pdu对象，如BGMIntEthPDU0001

                pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
                pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
                sender = getattr(ethernet_pdu, "sender")
                if sender == "SoC" and "Cyclic-" in getattr(ethernet_pdu, "send_type"):
                    if self.tcp_down_mpu_port == 30504:
                        if pdu_header_id == 20021:
                            self.cycle_pdu_list.append(ethernet_pdu_name)
                        else:
                            continue
                    if self.tcp_down_mpu_port != 30504:
                        if pdu_header_id != 20021:
                            self.cycle_pdu_list.append(ethernet_pdu_name)
                        else:
                            continue
                # 获取pdu对象的属性
                setattr(ethernet_pdu, "send_flag", False)  # 设置PDU不自动发送
                setattr(ethernet_pdu, "change_flag", True)  # 初始为True，每次计算pdu_data后，修改为False
                setattr(ethernet_pdu, "pdu_data", None)
                setattr(ethernet_pdu, "last_send_time", 0)
                pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
                pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
                binary_string_pdu_header_id = ''.join(hex(b)[2:].zfill(2) for b in pdu_header_id_list)
                bin_pdu_length_list = ''.join(hex(b)[2:].zfill(2) for b in pdu_length_list)

                # 解析eth信号对象
                for pdu_attr_name in dir(ethernet_pdu):
                    if "__" not in pdu_attr_name and pdu_attr_name not in ["send_flag", "change_flag", "pdu_data",
                                                                           "last_send_time"]:
                        pdu_sub_obj = getattr(ethernet_pdu, pdu_attr_name)
                        if not isinstance(pdu_sub_obj, int):
                            if not isinstance(pdu_sub_obj, str):
                                if not isinstance(pdu_sub_obj, dict):
                                    # 不是int，str，dict则是eth信号对象，此时的pdu_attr_name为eth信号名
                                    signal = SignalObj()
                                    signal.start_position = getattr(pdu_sub_obj, 'start_position')
                                    signal.signal_length = getattr(pdu_sub_obj, 'signal_length')
                                    signal.layout_format = getattr(pdu_sub_obj, 'layout_format')
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

    def __start_cycle_single_send(self):
        """启动周期信号设置线程、周期信号发送线程"""
        try:
            logger.info(f"开始设置发送方是Soc的需要自动周期发送的帧")
            thread = threading.Thread(
                target=self.__all_cycle_frame_calculation_pdu_data,
                name="mock mpu send pdu",
                args=(),
                daemon=True
            )
            thread.start()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
            logger.info(e.__repr__())
            logger.info("设置发送方是Soc的需要自动周期发送的帧异常")

        try:
            logger.info("遍历自动发送列表，按给定周期发送信号")
            thread = threading.Thread(
                target=self.__auto_send_cycle_pdu_data,
                name="mock mpu send pdu",
                args=(),
                daemon=True
            )
            thread.start()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
            logger.info(e.__repr__())

    def __calculation_pdu_data(self, ethernet_pdu):
        """重新计算并返回帧报文的pdu_data，发送周期"""
        pdu_length = getattr(ethernet_pdu, "pdu_length_bytes")
        pdu_header_id = getattr(ethernet_pdu, "pdu_header_id")
        pdu_header_id_list = DataTypeHanding.to_intlist(pdu_header_id, 4)
        pdu_length_list = DataTypeHanding.to_intlist(pdu_length, 4)
        bytes_list = DataTypeHanding.to_intlist(0, pdu_length)
        binary_string = ''.join(bin(b)[2:].zfill(8) for b in bytes_list)
        pdu_value_list = list(binary_string)
        for pdu_attr_name in dir(ethernet_pdu):
            if "__" not in pdu_attr_name and pdu_attr_name not in ["send_flag", "change_flag", "pdu_data",
                                                                   "last_send_time"]:
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

                            # if pdu_sub_obj.layout_format == "Motorola MSB":  # 格式为6,5,4,3,2
                            if True:  # 格式为6,5,4,3,2
                                index = 0
                                for signal_value_bit in signal_value_list:
                                    seq = signal_bytes_position * 8 - 1 + (8 - start_position % 8) + index
                                    pdu_value_list[seq] = signal_value_bit
                                    index = index + 1
                            # else:
                            #     res = index_change_to_intel(start_position, signal_length)  # 假设为7，6,10,9,8
                            #     for i, signal_value_bit in enumerate(signal_value_list):
                            #         bit_index = res[i]
                            #         seq = dbc_bit_to_bin_index(bit_index)
                            #         pdu_value_list[seq] = signal_value_bit
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

    def __all_cycle_frame_calculation_pdu_data(self):
        """
            放在线程中，设置发送方是Soc的需要自动周期发送的帧
            1、判断是否正在发送：维护正在发送列表；
            2、计算、更新pdu_data、send_type；
        """
        while True:
            for ethernet_pdu_name in self.cycle_pdu_list:
                ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)
                if ethernet_pdu.send_flag:
                    if ethernet_pdu.change_flag:
                        if ethernet_pdu.pdu_data is None:
                            time.sleep(0.005)  # 控制首次周期报文发送，使其发送时间分散
                        ethernet_pdu.pdu_data = self.__calculation_pdu_data(ethernet_pdu)  # 更新其值
                        ethernet_pdu.change_flag = False
                    ethernet_pdu_cycle = int(ethernet_pdu.send_type.replace("Cyclic-", "").replace("ms", ""))
                    self.auto_send_cycle_pdu_list[ethernet_pdu_name] = [ethernet_pdu.pdu_data, ethernet_pdu_cycle]
                else:  # 从自动发送列表移除
                    if ethernet_pdu_name in self.auto_send_cycle_pdu_list:
                        logger.info(f"deal:{ethernet_pdu_name}")
                        del self.auto_send_cycle_pdu_list[ethernet_pdu_name]
            else:
                time.sleep(0.02)

    def __auto_send_cycle_pdu_data(self):
        """放在线程中，遍历自动发送列表，按给定周期发送信号"""
        while not self.stop_client_connect:
            if self.down_connection_established:
                for ethernet_pdu_name in list(self.auto_send_cycle_pdu_list.keys()):
                    if ethernet_pdu_name not in self.cycle_message_sending_list:
                        self.send_cycle_message(ethernet_pdu_name)
                        self.cycle_message_sending_list.append(ethernet_pdu_name)
                else:
                    time.sleep(0.1)  # 每次周期型帧报文遍历发送后，暂停100ms
            else:
                logger.info("连接已断开，1秒后再次检测")
                time.sleep(1)

    def send_cycle_message(self, ethernet_pdu_name):
        """
         周期性发送报文：ethernet_pdu_name
        """

        def timer_function():
            ethernet_pdu = getattr(self.bgm_eth_internal, ethernet_pdu_name)
            if ethernet_pdu.send_flag and not self.stop_client_connect and self.down_connection_established:
                before_time = int(time.time() * 1000)
                ethernet_pdu.last_send_time = int(time.time() * 1000)
                try:
                    self.downTcpClientSocket.send(bytes(self.auto_send_cycle_pdu_list.get(ethernet_pdu_name)[0]))
                    self.write_enable = True
                except ConnectionResetError:
                    logger.info(f"{self.DOWN_ADDRESS}远程主机已关闭连接，不可写")
                    self.write_enable = False  # 不可写
                    time.sleep(5)
                except BrokenPipeError:
                    logger.info(f"{self.DOWN_ADDRESS} socket连接已断开，不可写")
                    self.write_enable = False  # 不可写
                    time.sleep(2)
                except socket.error as e:
                    logger.info(f"{self.DOWN_ADDRESS} Socket error:{e}，不可写")
                    self.write_enable = False  # 不可写
                    time.sleep(1)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
                    logger.info(f"{self.DOWN_ADDRESS} 报文发送异常，异常类型{type(e)}")
                    self.write_enable = False  # 不可写
                    time.sleep(1)
                finally:
                    after_time = int(time.time() * 1000)
                    threading.Timer(
                        (self.auto_send_cycle_pdu_list.get(ethernet_pdu_name)[1] - (after_time - before_time)) / 1000,
                        function=timer_function).start()
            else:
                if ethernet_pdu_name in self.cycle_message_sending_list:
                    self.cycle_message_sending_list.remove(f"{ethernet_pdu_name}")
                logger.info(f"stop send {ethernet_pdu_name}")

        threading.Timer(self.auto_send_cycle_pdu_list.get(ethernet_pdu_name)[1] / 1000, function=timer_function).start()

    def __send_pdu(self, data, send_cyclic, send_num):
        if not self.stop_client_connect:
            for i in range(send_num):
                self.downTcpClientSocket.send(bytes(data))
                time.sleep(send_cyclic / 1000)

    def __mock_mpu_send_pdu(self, pdu_data: list, send_cyclic=0, send_num=1, conn_timeout=5):
        """模拟mpu发送tcp下行数据"""
        wait_time = 0
        while wait_time < conn_timeout:
            if self.up_connection_established and self.down_connection_established:
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
                name="mock mpu send pdu",
                args=(pdu_data, send_cyclic, send_num),
                daemon=True
            )
            thread.start()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_tcp.py")
            logger.info(e.__repr__())
            self.downTcpClientSocket.close()

    def __mock_mpu_listen_mcu_message(self, timeout_second):
        """
        Mock MCU监听MPU发送过来的TCP报文
        @param timeout_second: 超时时间，单位秒
        @return:
        """
        time_start = time.time()
        listen_flag = True
        i = 1
        while listen_flag:
            data = self.upTcpClientSocket.recv(1024 * 101)
            hex_string = ''.join(hex(b)[2:].zfill(2) for b in data)
            curr_tcp_info = TcpPacket(i, time.time(), self.tcp_up_mcu_ip, self.tcp_up_mpu_ip,
                                      self.tcp_up_mcu_port,
                                      self.tcp_up_mpu_port, hex_string, len(self.up_payload), int(len(hex_string)))
            self.up_payload += hex_string
            self.tcp_packet_list.append(curr_tcp_info)
            i = i + 1

            time_now = time.time()
            listen_flag = (time_now - time_start) < timeout_second
        else:
            logger.info("------------------TCP上行监听到的字节长度---------------------")
            logger.info(self.up_payload)
            logger.info(self.tcp_packet_list)

    def __empty_listen_result(self):
        self.up_payload = ""
        self.tcp_packet_list = []

    def __reload_signal_value_list(self):
        """重新装载信号值信息"""
        pcap_parse_tcp = PcapParseTcpInfo(self.signal_info_dict, self.tcp_up_mcu_ip, self.tcp_up_mcu_port,
                                          self.tcp_down_mcu_ip, self.tcp_down_mcu_port, self.tcp_down_mpu_ip,
                                          self.tcp_down_mpu_port, self.tcp_up_mpu_ip, self.tcp_up_mpu_port)
        pcap_parse_tcp.down_payload = self.up_payload
        pcap_parse_tcp.tcp_packet_list = self.tcp_packet_list

        # 逐个信号解析
        for signal_name in self.signal_info_dict:
            signal_obj = self.signal_info_dict.get(signal_name)
            pcap_parse_tcp.parse_signal_info(signal_obj)
        self.signal_info_dict = pcap_parse_tcp.signal_info_dict


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
                 payload_start, payload_length, downstream=False):
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

    def parse_signal_info(self, signal_obj: SignalObj):
        """将pcap解出来的上下行payload解析出指定的以太网信号数据"""
        curr_index = 0
        signal_value_list = []
        if signal_obj.downstream:
            payload = self.down_payload
        else:
            payload = self.up_payload
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
            signal_item.timestamp, signal_item.sequence = self.__get_timestamp(index, signal_obj.downstream)
            if len(result) >= signal_obj.start_position:
                signal_item.signal_value = get_signal_value(result, signal_obj.start_position, signal_obj.signal_length,
                                                            signal_obj.layout_format)
            else:
                continue
            signal_value_list.append(signal_item)
            self.signal_info_dict[signal_obj.name].signals_value_list.append(signal_item)  # 解析结果存放在对应信号的列表中

    def __get_timestamp(self, index, downstream: bool):
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


if __name__ == "__main__":
    logger = Logger().get_logger("test")

    res_str = exec_shell('ifconfig').get('output')
    logger.info("00000000000000")
    for ip in ['172.16.5.1', '172.16.9.1']:
        if res_str.find(ip) == -1:
            vlan = ip.split('.')[2]
            logger.info("nnnnn")
            if res_str.find(f'eth0.{vlan}') and vlan != 9:
                exec_shell(f'ip link delete eth0.{vlan}')
            exec_shell(f'ip link add link enx68da73a2a994 name eth0.{vlan} type vlan id {vlan}')
            exec_shell(f'ip addr add {ip}/24 dev eth0.{vlan}')
            logger.info(f'ip addr add {ip}/24 dev eth0.{vlan}')
            exec_shell(f'ip link set dev eth0.{vlan} address 02:00:00:00:10:01')
            exec_shell(f'ifconfig eth0.{vlan} netmask 255.255.255.0 broadcast 172.16.{vlan}.255')
            exec_shell(f'ifconfig eth0.{vlan} up')
        else:
            logger.info("环境网络重置完成")
    client1 = MockMpuSocketClient(tcp_down_mpu_port=30504, tcp_up_mpu_port=30505)
    client1.send_trigger_frame(pdu_id=20018)  # boot complete的PDU ID
    time.sleep(0.2)
    client1.start_send_cycle_frame(pdu_id=20021)  # 心跳的PDU ID报文

    # client2 = MockMpuSocketClient(tcp_up_mpu_port=30506, tcp_down_mpu_port=30507)
    # time.sleep(5)
    # client2.start_listen_mcu_message(5)

    client2 = MockMpuSocketClient()
    client2.start_send_all_cycle_frame()
    logger.info("主线程延时3600秒")
    print(f" Task executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    time.sleep(3600)
    logger.info(f"总发送次数：{client2.send_counter}，超过四毫秒数：{len(client2.ge_three_num)}")
    logger.info(f"{client2.ge_three_num}")
