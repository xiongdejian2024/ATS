#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : UdpClient.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/7 15:59
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import time
import socket
from threading import Thread
from collections import deque

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.socket_client.SocketData import SocketData


class UdpClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.recv_flag = False
        self.recv_broad_cast_flag = False
        self.sock = None
        self.sock_broad_cast = None
        self.accept_max_number = 5000
        self.accept_broadcast_host = None
        self.socket_connect_status = False

    def udp_send(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise AssertionError(f"发送数据类型错误，得到：{type(data)}")
        logger.debug(f"udp client send:{data.hex()}")
        self.sock.sendto(data, (self.host, self.port))

    def _udp_recv(self):
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while self.recv_flag:
            try:
                recv_data, addr = self.sock.recvfrom(1024)
                if recv_data == b'':
                    self.socket_connect_status = False
                    raise RuntimeError("socket connection broken")
                self.socket_connect_status = True
                if self not in SocketData.UDP_CLIENT_DATA:
                    SocketData.UDP_CLIENT_DATA[self] = deque([recv_data], maxlen=self.accept_max_number)
                else:
                    logger.debug(f"udp client accept:{recv_data.hex()}")
                    SocketData.UDP_CLIENT_DATA[self].append(recv_data)
            except KeyboardInterrupt:
                logger.warning("caught keyboard interrupt, exiting")
                try:
                    self.sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                    logger.warning(f"udp client close error:{e}")
                raise AssertionError(f"caught keyboard interrupt, exiting")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                logger.warning(f"udp recv data error:{e}")
                try:
                    self.sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                    logger.warning(f"udp client close error:{e}")
                time.sleep(0.01)
                self._udp_recv()
        logger.info(f"udp client socket stop and exit 0.")

    def clear_udp_client_data(self):
        if self in SocketData.UDP_CLIENT_DATA:
            SocketData.UDP_CLIENT_DATA[self].clear()

    def start(self):
        if not self.recv_flag:
            self.recv_flag = True
            Thread(target=self._udp_recv, daemon=True).start()

    def stop(self):
        self.recv_flag = False
        try:
            self.sock.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
            logger.warning(f"udp client close error:{e}")
        self.clear_udp_client_data()

    def stop_broad_cast(self):
        self.recv_broad_cast_flag = False
        try:
            self.sock_broad_cast.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
            logger.warning(f"udp client close error:{e}")
        self.clear_udp_client_data()

    def clear_udp_broadcast_client_data(self):
        if self in SocketData.UDP_BROADCAST_CLIENT_DATA:
            SocketData.UDP_BROADCAST_CLIENT_DATA[self].clear()

    def start_recv_udp_broadcast(self):
        if not self.recv_broad_cast_flag:
            self.recv_broad_cast_flag = True
            Thread(target=self._udp_recv_broadcast, daemon=True).start()

    def _udp_recv_broadcast(self):
        self.sock_broad_cast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_broad_cast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_broad_cast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_broad_cast.bind(('', self.port))
        while self.recv_broad_cast_flag:
            try:
                recv_data, addr = self.sock_broad_cast.recvfrom(1024)
                if recv_data == b'':
                    raise RuntimeError("socket connection broken")
                if self not in SocketData.UDP_BROADCAST_CLIENT_DATA:
                    SocketData.UDP_BROADCAST_CLIENT_DATA[self] = deque([{time.time(): recv_data}], maxlen=self.accept_max_number)
                else:
                    self.accept_broadcast_host = addr.getpeername()
                    logger.debug(f"{addr.getpeername()} udp client accept:{recv_data.hex()}")
                    SocketData.UDP_BROADCAST_CLIENT_DATA[self].append({time.time(): recv_data})
            except KeyboardInterrupt:
                logger.warning("caught keyboard interrupt, exiting")
                try:
                    self.sock_broad_cast.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                    logger.warning(f"udp broadcast client close error:{e}")
                raise AssertionError(f"caught keyboard interrupt, exiting")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                logger.warning(f"udp broadcast recv data error:{e}")
                try:
                    self.sock_broad_cast.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpClient.py")
                    logger.warning(f"udp broadcast client close error:{e}")
                time.sleep(SocketData.RECONNECT_TIME)
                self._udp_recv_broadcast()
        logger.info(f"udp broadcast client socket stop and exit 0.")
