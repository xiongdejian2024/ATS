# -*- coding: utf-8 -*-

"""
@Time    : 2024/11/7 11:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
@Description : 
@Examples    :
"""
import sys
import json
import pickle
import socket
import threading
import time
import traceback

from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.sdk.driver.ethernet_lib.tcp_socket import tcp_socket_client
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_socket import udp_socket_client


class udp_socket_client_enhance(udp_socket_client):
    def __init__(self, threadID, name, multicast_ip, multicast_port):
        super().__init__(threadID, name, sock=None)
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port

    def set_sock_opt(self, local_ip="172.20.5.1", local_port=30501):
        self.sock.bind((local_ip, local_port))


class cycle_frame:
    def __init__(self, frame_name: str, cycle_time_ms: int, payload: list):
        """
        @param frame_name: 帧的名称
        @param cycle_time_ms: 帧的周期，单位毫秒
        @param payload: 帧的payload
        """
        self.frame_name = frame_name
        self.cycle_time_ms = cycle_time_ms
        self.send_flag = True  # 如果为False，则停止周期发送
        self.payload = payload
        self.last_send_time = 0


class channel:
    def __init__(self, channel_name,
                 channel_type: int,
                 local_ip_address,
                 local_port,
                 remote_ip_address,
                 remote_port,
                 handle_receive_message,
                 multicast_ip='239.255.5.1', multicast_port=30501):
        self.channel_name = channel_name
        self.channel_type = channel_type  # 1为TCP、2为UDP
        self.local_ip_address = local_ip_address
        self.local_port = local_port
        self.remote_ip_address = remote_ip_address
        self.remote_port = remote_port
        self.cycle_frame_dict = {}  # key为帧名称，value为帧对象
        self.socket_client = None
        self.send_lock = threading.Lock
        self.handle_receive_message = handle_receive_message
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port
        self.connect_mock_ecu()

    def connect_mock_ecu(self):
        """创建通道、绑定端口、设置回调函数，启动消息的监听"""
        if self.channel_type == 1:  # TCP 通道
            self.socket_client = tcp_socket_client(1, self.channel_name)
            self.socket_client.create_socket(None)
            self.socket_client.sock.bind((self.local_ip_address, self.local_port))
            self.socket_client.connect(self.remote_ip_address, self.remote_port)
        elif self.channel_type == 2:  # UDP 通道
            self.socket_client = udp_socket_client_enhance(1,
                                                           self.channel_name,
                                                           multicast_ip=self.multicast_ip,
                                                           multicast_port=self.multicast_port
                                                           )
            self.socket_client.set_sock_opt(self.local_ip_address, self.local_port)

        self.socket_client.setup_data_callback(self.__receive_message)
        self.socket_client.start()

    def __receive_message(self, data: list):
        """处理通道返回的消息"""
        logger.debug(f"MCU Forward：通道 {self.channel_name} 接收到消息：{data}")
        hex_string = ''.join(hex(b)[2:].zfill(2) for b in data[0])
        decimal_list = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
        self.handle_receive_message(self.channel_name, decimal_list)

    def __send_trigger_frame(self, cycle_frame_obj: cycle_frame, counter: int):
        """
        发送trigger报文
        @param cycle_frame_obj: 报文对象
        @param counter: 发送次数
        """
        send_num = 0
        while send_num < counter:
            self.__send_frame(cycle_frame_obj)
            send_num += 1
            time.sleep(cycle_frame_obj.cycle_time_ms / 1000)

    def __send_frame(self, cycle_frame_obj: cycle_frame):
        """
        发送报文
        @param cycle_frame_obj: 报文对象
        """
        if self.channel_type == 1:
            self.socket_client.send(cycle_frame_obj.payload)
        else:
            if cycle_frame_obj.frame_name.startswith("cycle-multicast-"):
                server = (self.multicast_ip, self.multicast_port)
            else:
                server = (self.remote_ip_address, self.remote_port)
            self.socket_client.send(cycle_frame_obj.payload, server)

    def close(self):
        """
        关闭通道前，先将周期报文的发送停止
        """
        for frame_name in self.cycle_frame_dict:
            self.cycle_frame_dict[frame_name].send_flag = False
        self.socket_client.exitFlag = True
        time.sleep(0.5)
        self.socket_client.close()

    def send_trigger_frame_thread(self, cycle_frame_obj: cycle_frame, counter: int):
        """
        启动一个线程，发送事件帧
        """
        capture_thread = threading.Thread(target=self.__send_trigger_frame,
                                          args=(cycle_frame_obj,
                                                counter),
                                          daemon=True)
        capture_thread.start()

    def send_cycle_frame_thread(self, cycle_frame_obj: cycle_frame):
        """
        周期性发送一个内部以太网报文
        """
        if cycle_frame_obj.frame_name not in self.cycle_frame_dict:
            self.cycle_frame_dict[cycle_frame_obj.frame_name] = cycle_frame_obj
            logger.info(f"开始周期发送：{cycle_frame_obj.frame_name}, "
                        f"周期：{cycle_frame_obj.cycle_time_ms}, payload:{cycle_frame_obj.payload}")
        else:
            # 该周期报文已经在周期发送，则本次仅更新payload的值
            logger.info(f"更新周期发送报文的payload：{cycle_frame_obj.frame_name}, "
                        f"周期：{cycle_frame_obj.cycle_time_ms}, 当前payload:{cycle_frame_obj.payload}")
            self.cycle_frame_dict[cycle_frame_obj.frame_name].payload = cycle_frame_obj.payload  # 更新payload并返回
            return

        def timer_function():
            if cycle_frame_obj.send_flag:
                # before_time = int(time.time() * 1000)
                cycle_frame_obj.last_send_time = int(time.time() * 1000)
                try:
                    self.__send_frame(cycle_frame_obj)  # 发送报文
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/eth_internal_router.py")
                    logger.info(f"{self.channel_name}，周期报文发送异常：{traceback.format_exc()}")
                    time.sleep(1)
                finally:
                    # after_time = int(time.time() * 1000) - 1000
                    threading.Timer(
                        cycle_frame_obj.cycle_time_ms / 1000, function=timer_function).start()
            else:
                logger.info(f"周期发送停止：{cycle_frame_obj.frame_name}, "
                            f"周期：{cycle_frame_obj.cycle_time_ms}, payload:{cycle_frame_obj.payload}")

        threading.Timer(cycle_frame_obj.cycle_time_ms / 1000,
                        function=timer_function).start()  # 首次调度发送

    def stop_frame_send(self, frame_name):
        """
        停止周期性报文的发送
        """
        if frame_name in self.cycle_frame_dict:
            frame = self.cycle_frame_dict.get(frame_name)
            frame.send_flag = False


class EthInternalRouter:
    """
        内部以太网路由器，创建一个TCP SERVER端，
    """
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(10000)  # 设置永不超时
        self.server_socket.bind((self.server_ip, self.server_port))

        self.server_socket.listen(5)
        self.client_socket = None  # 客户端socket对象的引用
        self.channel_name_dict = {}
        self.listen_client_request()

    def create_channel(self, channel_info: dict):
        """
        创建通道
        {"channelName": "CCUMCUCD-SocketCdMcuTCPServer-CCUSOCCD-SocketCdSocPMTCPClient", "channelConfig":
        {"channelType": 1, "localIpAddress": "172.20.5.11", "localPort": 30504,
        "remoteIpAddress": "172.20.5.12", "remotePort": 30503}}
        """
        channel_name = channel_info["channelName"]
        channel_type = channel_info["channelConfig"]["channelType"]
        local_ip_address = channel_info["channelConfig"]["localIpAddress"]
        local_port = channel_info["channelConfig"]["localPort"]
        remote_ip_address = channel_info["channelConfig"]["remoteIpAddress"]
        remote_port = channel_info["channelConfig"]["remotePort"]
        channel_new = channel(channel_name,
                              channel_type,
                              local_ip_address,
                              local_port,
                              remote_ip_address,
                              remote_port,
                              self.handle_channel_receive_message  # 通道接收到的frame处理
                              )
        self.channel_name_dict[channel_name] = channel_new

    def delete_channel(self, channel_name):
        """删除通道"""
        if channel_name in self.channel_name_dict:
            self.channel_name_dict[channel_name].close()

    def handle_channel_receive_message(self, channel_name, data):
        """处理各个通道返回的消息"""
        logger.debug(f"EthInternalRouter：通道 {channel_name} 接收到消息：{data}")
        # 创建要传输的对象
        args_content = {"msg": {"channelName": channel_name, "timeStamp": time.time(), "payload": data}}
        messageFromMCU = {'action': 'event',
                          'function': 'UpdatemessageFromMCUEvent',
                          'args': f'{json.dumps(args_content)}',
                          'failtype': '',
                          'timestamp': time.time()}
        # 序列化对象并发送
        self.client_socket.sendall(pickle.dumps(messageFromMCU))

    def listen_client_request(self):
        self.client_socket, addr = self.server_socket.accept()
        self.client_socket.settimeout(10000)
        logger.info(f"接收到客户端连接请求，地址: {addr}")

        while True:
            data = self.client_socket.recv(1024 * 10)
            if not data:
                logger.info(f"{addr} 异常，退出业务处理")
                break
            command_receive = pickle.loads(data)
            logger.info(f"接收到的指令: {command_receive}")
            self.handle_command_from_client(command_receive)
        self.close_socket()

    def handle_command_from_client(self, command_dict: dict):
        """
            处理从客户端发来的指令
        """
        command_dict['args'] = json.loads(command_dict['args'])
        if command_dict['function'] == "createChannel":
            self.create_channel(command_dict['args'])
        elif command_dict['function'] == "deleteChannel":
            self.delete_channel(command_dict['args']['channelName'])
        elif command_dict['function'] == "startSendMessage":
            if command_dict['args']['channelName'] in self.channel_name_dict:  # 通道已创建
                msgAttr = command_dict['args']['msgAttr']
                frame = cycle_frame(msgAttr['msgName'], msgAttr['ivl'], command_dict['args']['payload'])  # 创建帧对象
                channel_obj = self.channel_name_dict[command_dict['args']['channelName']]
                if msgAttr['msgName'].startswith("cycle-"):  # 周期性报文
                    capture_thread = threading.Thread(target=channel_obj.send_cycle_frame_thread,
                                                      args=(frame,),
                                                      daemon=True)
                    capture_thread.start()
                else:  # 事件型报文
                    channel_obj.send_trigger_frame_thread(frame, msgAttr['cnt'])
        elif command_dict['function'] == "stopSendMessage":
            if command_dict['args']['channelName'] in self.channel_name_dict:  # 通道已创建
                channel_obj = self.channel_name_dict[command_dict['args']['channelName']]
                channel_obj.stop_frame_send(command_dict['args']['msgName'])

    def close_socket(self):
        # 关闭客户端连接
        self.client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    logger = Logger().get_logger("router")
    logger.info(f"MCU Forward 的IP地址为：{sys.argv[1]}, 端口为{sys.argv[2]}")
    test = EthInternalRouter(sys.argv[1], int(sys.argv[2]))
