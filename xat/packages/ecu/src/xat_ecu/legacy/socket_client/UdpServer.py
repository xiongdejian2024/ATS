#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : UdpServer.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/7 16:00
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


class UdpServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.listen_flag = False
        self.sock = None
        self.accept_max_number = 10000

    def udp_data(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise AssertionError(f"发送数据类型错误，得到：{type(data)}")
        self.sock.sendto(data, (self.host, self.port))

    def _udp_recv(self):
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        while self.listen_flag:
            try:
                recv_data, addr = self.sock.recvfrom(1024)
                if recv_data == b'':
                    raise RuntimeError("socket connection broken")

                if self not in SocketData.UDP_SERVER_DATA:
                    SocketData.UDP_SERVER_DATA[self] = deque([recv_data], maxlen=self.accept_max_number)
                else:
                    SocketData.UDP_SERVER_DATA[self].append(recv_data)
            except KeyboardInterrupt:
                logger.info("caught keyboard interrupt, exiting")
                try:
                    self.sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpServer.py")
                    logger.warning(f"udp server close error:{e}")
                raise AssertionError("caught keyboard interrupt, exiting")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpServer.py")
                logger.warning(f"udp recv data error:{e}")
                try:
                    self.sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpServer.py")
                    logger.warning(f"udp server close error:{e}")
                time.sleep(SocketData.RECONNECT_TIME)
                self._udp_recv()
        logger.info(f"udp server socket stop and exit 0.")

    def udp_server_clear_data(self):
        if self in SocketData.UDP_SERVER_DATA:
            SocketData.UDP_SERVER_DATA[self].clear()

    def start(self):
        if not self.listen_flag:
            self.listen_flag = True
            Thread(target=self._udp_recv, daemon=True).start()

    def stop(self):
        self.listen_flag = False
        try:
            self.sock.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/UdpServer.py")
            logger.warning(f"udp server close error:{e}")
        self.udp_server_clear_data()
