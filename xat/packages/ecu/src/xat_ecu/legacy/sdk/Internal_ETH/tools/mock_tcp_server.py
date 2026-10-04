# -*- coding: utf-8 -*-
"""
@File        : mock_server.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2024/09/03 13:51 PM
@Description : 模拟mcu作为tcp server端给SOC进行交互，发送tcp数据，接收tcp请求，上下行为两个socket
@Examples    : example of how to use it
"""
import time
import socket
import threading
import traceback
from socket import *
from xat_ecu.legacy.common.logger import logger

BUFFERSIZE = 1024 * 101


def is_socket_connected(client_socket):
    """
    判断socket是否连接成功
    :param client_socket: socket对象
    :return: True or False
    """
    if client_socket is None:
        logger.info("socket is None")
        return False
    # readable, writable, exceptional = select.select([client_socket], [client_socket], [], 1)  # 1s周期轮询
    # logger.info(f"{client_socket}\n readable: {readable}\n writable: {writable}\n exceptional: {exceptional}")
    """
    即使对端socket异常关闭，writable也不会是[]，只是发送送数据会报错。正常情况下writable为空是在发送缓冲区满的情况下，返回[]
    且readable不能通过recv报错来判断是否socket还正常，因为多线程调用recv，会导致业务接收线程拿不到有效数据
    """
    try:
        data_to_send = b"Hello, client"
        client_socket.send(data_to_send)
        return True
    except ConnectionResetError:
        logger.error("远程主机已关闭连接")
        return False
    except BrokenPipeError:
        logger.error("socket连接已断开")
        return False
    except socket.error as e:
        logger.error(f"Socket error:{e}")
        return False
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
        traceback.print_exc()
        logger.error(e)
        return False


class SocketServer:
    def __init__(self, ip, port, client_max_num=50, timeout=3, server_name=''):
        """

        :param ip: 服务端ip
        :param port: 服务端端口
        :param client_max_num: 最大客户端连接数量
        :param timeout: server socket recv接口超时时间
        :return:
        """
        self._server_ip = ip
        self._server_port = port
        self._server_name = server_name
        self._server_socket = None
        self._client_socket = None
        self._listen_client_connect_flag = False
        self._listen_pdu_data_flag = False
        self._monitor_client_socket_flag = False
        self._connection_established = False
        self._t_listen_client = None
        self._t_monitor_client = None

        self._establish_listen_socket(client_max_num, timeout)

    def _establish_listen_socket(self, client_max_num=50, timeout=3):
        """
        建立服务器socket监听客户端连接
        :param client_max_num:  最大客户端连接数量， 当前使用一般只会有一个客户端
        :param timeout: recv接口超时时间
        :return:
        """
        self._server_socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind((self._server_ip, self._server_port))
        self._server_socket.settimeout(timeout)  # 适用于send,recv,connect,accept
        self._server_socket.listen(client_max_num)

    def __get_client_socket_thread(self):
        """
        监听客户端连接的线程，考虑对端可能重启，会有重连情况
        """
        while self._listen_client_connect_flag:
            try:
                # logger.info("等待socket连接")
                self._client_socket, addr = self._server_socket.accept()
                self._client_socket.settimeout(5)
                self._connection_established = True
                logger.info(f"监听到的socket port:{addr}")
            except OSError as e:
                pass  # accept 3s检测不到就会报socket.timeout即OSError
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
                traceback.print_exc()
                logger.error(e.__repr__())
        else:
            logger.info("get client socket thread exit by test end")

    def start_listen_client(self):
        """启动监听客户端连接"""
        self._t_listen_client = threading.Thread(target=self.__get_client_socket_thread,
                                                 name=f"{self._server_name}::get_client_socket_thread",
                                                 daemon=True)
        self._listen_client_connect_flag = True
        self._t_listen_client.start()

    def stop_listen_client(self):
        """结束监听客户端连接"""
        self._listen_client_connect_flag = False
        self._t_listen_client.join()

    def __monitor_client_socket_thread(self):
        """监控client socket的状态，识别对端重连的情况"""
        while self._monitor_client_socket_flag:
            time.sleep(1)
            try:
                if self._client_socket is None:
                    continue
                if not is_socket_connected(self._client_socket):
                    self._connection_established = False
                    self._client_socket.close()
                    self._client_socket = None
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
                traceback.print_exc()
                logger.error(e.__repr__())
        else:
            logger.info("monitor socket status thread exit by test end")

    def start_monitor_client(self):
        """启动监控client socket的状态"""
        self._t_monitor_client = threading.Thread(target=self.__monitor_client_socket_thread,
                                                  name=f"{self._server_name}::monitor_client_socket_thread",
                                                  daemon=True)
        self._monitor_client_socket_flag = True
        self._t_monitor_client.start()

    def stop_monitor_client(self):
        """结束监控client socket的状态，一般服务端停止时才调用"""
        self._monitor_client_socket_flag = False
        self._t_monitor_client.join()

    def __send_pdu_atom(self, data: list, send_cyclic, send_num):
        """
        发送数据原子能力
        :param data: 发送数据列表
        :param send_cyclic: 发送周期
        :param send_num: 发送次数
        :return:
        """
        for i in range(send_num):
            self._client_socket.send(bytes(data))
            time.sleep(send_cyclic / 1000)

    def __check_client_socket_connected(self, conn_timeout):
        """
        校验客户端连接状态
        :param conn_timeout: 等待连接时间
        :return:
        """
        wait_time = 0
        while wait_time < conn_timeout:
            if self._connection_established:
                return True
            time.sleep(1)
            wait_time = wait_time + 1
        else:
            raise TimeoutError("TCP 连接建立超时，无法发送PDU报文")

    def mock_mcu_send_pdu(self, pdu_data: list, send_cyclic=0, send_num=1, conn_timeout=5):
        """模拟mcu发送tcp上行数据"""
        try:
            self.__check_client_socket_connected(conn_timeout)
            logger.info(f"开始发送的pdu数据为：{pdu_data}, 发送周期为{send_cyclic}ms, 发送次数为{send_num}")
            thread = threading.Thread(target=self.__send_pdu_atom,
                                      name=f"{self._server_name}::send tcp pdu",
                                      args=(pdu_data, send_cyclic, send_num),
                                      daemon=True)
            thread.start()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
            traceback.print_exc()
            logger.error(e.__repr__())

    def __listen_data_thread(self):
        """
        Mock MCU监听MPU发送过来的TCP报文的线程
        """
        while self._listen_pdu_data_flag:
            if not self._connection_established:
                continue
            try:
                data = self._client_socket.recv(BUFFERSIZE)
                # todo: 当前没有解析的需求
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
                pass

    def start_listen_pdu_data(self):
        """开始监听下行TCP pdu报文"""
        t_listen_tcp = threading.Thread(target=self.__listen_data_thread, daemon=True)
        self._listen_pdu_data_flag = True
        t_listen_tcp.start()

    def stop_listen_tcp(self):
        """停止监听下行TCP pdu报文"""
        self._listen_pdu_data_flag = False

    def start_server(self):
        """开始监听客户端连接，socket状态监控，以及"""
        self.start_listen_client()
        self.start_monitor_client()
        self.start_listen_pdu_data()

    def stop_server(self):
        """关闭socket服务器"""
        self.stop_listen_tcp()
        self.stop_monitor_client()
        self.stop_listen_client()
        try:
            self._client_socket.close()
            logger.info("_client_socket已关闭")
        except Exception:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
            pass
        try:
            self._server_socket.close()
            logger.info("_server_socket已关闭")
        except Exception:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_tcp_server.py")
            pass


class MockSocketServer:
    """JET1.0上模拟mcu上行和下行的两个socket总控制"""

    def __init__(self, up_mcu_ip, up_mcu_port, down_mcu_ip, down_mcu_port,
                 down_mpu_ip, down_mpu_port, up_mpu_ip, up_mpu_port):
        # 上行mcu和mpu的ip和port
        self.up_mcu_ip = up_mcu_ip
        self.up_mcu_port = up_mcu_port
        self.up_mpu_ip = up_mpu_ip
        self.up_mpu_port = up_mpu_port

        # 下行mcu和mpu的ip和port
        self.down_mcu_ip = down_mcu_ip
        self.down_mcu_port = down_mcu_port
        self.down_mpu_ip = down_mpu_ip
        self.down_mpu_port = down_mpu_port

        # 服务端socket
        self.up_server = SocketServer(self.up_mcu_ip, self.up_mcu_port, server_name='up_server')
        self.down_server = SocketServer(self.down_mcu_ip, self.down_mcu_port, server_name='down_server')

    def start_mock_mcu(self):
        """启动上下行服务器和连接"""
        self.up_server.start_server()
        self.down_server.start_server()

    def stop_mock_mcu(self):
        """关闭上下行服务器和连接"""
        self.up_server.stop_server()
        self.down_server.stop_server()

