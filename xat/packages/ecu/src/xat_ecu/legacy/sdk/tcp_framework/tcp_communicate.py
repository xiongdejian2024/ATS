# -*- coding: utf-8 -*-

"""
@Time    : 2024/2/28 11:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""
import abc
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM, error
from xat_ecu.legacy.common.logger import logger


def int_to_bytes_list(int_data, bytes_length):
    bytes_list = []
    for i in range(bytes_length-1):
        bytes_list.append(int_data >> (bytes_length - i - 1) * 8 & 0xFF)
    else:
        bytes_list.append(int_data & 0xFF)
    return bytes_list


class SocketClient:
    def __init__(self,  local_ip, local_port, server_ip, server_port):
        LOCAL_ADDRESS = (local_ip, local_port)
        self.SERVER_ADDRESS = (server_ip, server_port)
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        self.tcp_client.bind(LOCAL_ADDRESS)
        self.server_connect_flag = False
        self.received_data = ""

    def connect_server(self):
        if not self.server_connect_flag:
            self.tcp_client.connect(self.SERVER_ADDRESS)
            self.server_connect_flag = True

    def reconnect_server(self):
        self.server_connect_flag = False
        self.connect_server()

    def send_data_to_server(self, data):
        self.connect_server()
        try:
            self.tcp_client.sendall(bytes(data))
        except error:
            logger.info(f"Socket connection with {self.SERVER_ADDRESS} occur exception during send, reconnect!")
            self.reconnect_server()
            self.send_data_to_server(data)

    def __listen_result(self):
        self.connect_server()
        while True:
            try:
                data = self.tcp_client.recv(1024)
                hex_string = ''.join(hex(b)[2:].zfill(2) for b in data)
                self.received_data += hex_string
            except error:
                logger.info(f"Socket connection with {self.SERVER_ADDRESS} occur exception during receive, reconnect!")
                self.reconnect_server()

    def listen_data_from_server(self):
        before_thread = threading.Thread(target=self.__listen_result, )
        before_thread.setDaemon(True)
        before_thread.start()


class SocketServer:
    def __init__(self, local_ip, local_port):
        ADDRESS = (local_ip, local_port)
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(ADDRESS)
        self.start_listen_flag = False
        self.get_client_socket_flag = False
        self.clients = {}   # 所有的TCP客户端连接
        self.clients_received_data = {}  # 从各个客户端获取到的数据

    def start_listen(self):
        """
        启动客户端连接的监听
        """
        if self.start_listen_flag is False:
            self.server_socket.listen(5)
            self.start_listen_flag = True

    def get_client_socket(self):
        """
        持续创建或更新有效的客户端socket连接
        """
        if self.get_client_socket_flag is False:
            thread = threading.Thread(
                target=self.__get_client_socket_thread,
                name="get client socket thread",
                daemon=True
            )
            thread.start()
            self.get_client_socket_flag = True

    def __get_client_socket_thread(self):
        """
        持续监听各个客户端的TCP连接请求，server端对于每一个客户端IP地址仅维护一个socket连接
        """
        while True:
            result = self.server_socket.accept()
            client_host_addr = result[1][0]
            self.clients[client_host_addr] = result[0]
            if client_host_addr not in self.clients_received_data:
                self.clients_received_data[client_host_addr] = []  # 对应socket的监听数据初始化

    def send_data_to_client(self, data: list, client_host_addr):
        """
        发送数据到对应的TCP客户端
        """
        if client_host_addr in self.clients:
            try:
                self.clients[client_host_addr].send(bytes(data))
            except ConnectionResetError as e:
                logger.info(f"与{client_host_addr}的连接已断开，无法再发送信息")
        else:
            logger.info(f"{client_host_addr}没有与当前主机建立TCP连接")

    def __listen_result(self, client_host_addr):
        self.start_listen()
        self.get_client_socket()
        listen_flag = True
        while listen_flag:
            if client_host_addr in self.clients:  # 与客户端已建立连接
                data = self.clients[client_host_addr].recv(1024)
                self.clients_received_data[client_host_addr].append(data)  # 保存数据
            else:
                time.sleep(3)  # 3秒后重试

    def listen_data_from_client(self, target_client):
        """
        监听客户端发来的数据，每个客户端创建一个监听守护线程

        """
        before_thread = threading.Thread(target=self.__listen_result, args=(target_client,))
        before_thread.setDaemon(True)
        before_thread.start()


class Protocol(metaclass=abc.ABCMeta):
    """
    TCP通信协议的抽象父类
    """
    @abc.abstractmethod
    def pack(self, **kwargs):
        """
        封包
        """
        pass

    @abc.abstractmethod
    def unpack(self, data):
        """
        TCP数据拆包，返回值为字典

        @param data: 从网络上接收到的socket字节流
        """
        pass


class v2tRouterProtocol(Protocol):
    def __init__(self):
        self.frame_id = 4   # 4个字节
        self.frame_length = 4  # 4个字节
        self.frame_id_value_list = {"12345678": []}

    def pack(self, **kwargs):
        """
        TCP数据封包，返回值为列表

        @param kwargs: 需要包含frame_id(其值为int)、frame_data(列表类型)
        """
        pack_result = []
        frame_id_value = kwargs.get("frame_id", None)
        if frame_id_value is None:
            return None, f"缺少入参frame_id"
        else:
            pack_result.extend(int_to_bytes_list(frame_id_value, self.frame_id))

        frame_data_list = kwargs.get("frame_data", None)
        if frame_data_list is None:
            return None, f"缺少入参frame_data"
        elif not isinstance(frame_data_list, list):
            return None, f"frame_data的值类型必须为列表"
        else:
            pack_result.extend(int_to_bytes_list(len(frame_data_list), self.frame_length))
            pack_result.extend(frame_data_list)
            return pack_result

    def unpack(self, data):
        """
        TCP数据拆包，返回值为字典

        @param data: 从网络上接收到的socket字节流的16进制字符串
        """
        for frame_id_value in self.frame_id_value_list:
            curr_index = 0
            while True:
                try:
                    index = data.index(frame_id_value, curr_index)
                    if index+16 <= len(data):
                        length = int(data[index+8:index+16], 16)
                        if index+16+length*2 <= len(data):
                            frame_data = data[index+16:index+16+length*2]
                            self.frame_id_value_list[frame_id_value].append(frame_data)
                            curr_index = index + 1
                        else:
                            break
                    else:
                        break
                except ValueError:
                    break
