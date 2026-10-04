#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : SocketClient.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/6/17 19:36
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
import ssl
import time
import socket
import selectors
import types
import time
import sys
import random
from threading import Thread
from collections import deque
from xat_ecu.legacy.socket_client.SocketData import SocketData
from xat_ecu.legacy.common.logger import logger


class SocketClient:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.is_stop = True
        self.accept_max_number = 10000
        self.to_be_send_message = deque(maxlen=10000)
        self.max_bytes = 1024 * 10
        self.register_sock_set = set()
        self.sock_start_time = None
        self.sock_start_to_close_time_list = []
        self.sel = None
        self.ssl_communication = False
        self.certfile = None
        self.keyfile = None
        self.ca_cert_file = None
        self.socket_connect_status = False
        self.ssl_waite_time = 0.1

    def stop(self):
        try:
            for _sock in self.register_sock_set:
                if hasattr(_sock, 'close'):
                    self.sel.unregister(_sock)
                    _sock.close()
            self.sel.close()
            self.sel = None
            self.register_sock_set.clear()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketClient.py")
            logger.warning(f"handle socket client stop error:{e}")
        self.tcp_client_clear_data()
        self.sock_start_time = None
        self.sock_start_to_close_time_list.clear()
        self.is_stop = True

    def reset_sock_start_time(self):
        self.sock_start_time = time.time()

    def get_sock_start_to_close_time(self):
        if self.sock_start_to_close_time_list:
            return self.sock_start_to_close_time_list.pop()
        else:
            logger.warning(f"没有发现socket开始到断联的计时。")

    def async_send_message(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        elif isinstance(message, (bytes, bytearray)):
            message = message
        else:
            raise AssertionError('to bo send message type error, must bytes or str!')

        self.to_be_send_message.append(message)

    def tcp_client_clear_data(self):
        if self in SocketData.TCP_CLIENT_DATA:
            SocketData.TCP_CLIENT_DATA[self].clear()

    def handle_message(self, key, mask):
        sock = key.fileobj
        data = key.data
        if not all([mask & selectors.EVENT_READ, mask & selectors.EVENT_WRITE]):
            self.socket_connect_status = False

        if mask & selectors.EVENT_READ:
            if self.ssl_communication:
                time.sleep(self.ssl_waite_time)
            recv_data = sock.recv(self.max_bytes)
            if recv_data:
                self.socket_connect_status = True
                try:
                    logger.debug(f"{sock.getpeername()} tcp client accept data:{recv_data.hex()}")
                    data.recv_total += len(recv_data)
                    if self not in SocketData.TCP_CLIENT_DATA:
                        SocketData.TCP_CLIENT_DATA[self] = deque([recv_data], maxlen=self.accept_max_number)
                    else:
                        SocketData.TCP_CLIENT_DATA[self].append(recv_data)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketClient.py")
                    logger.warning(f"doip parse error,with:{recv_data.hex()},got:{e}")

            if not recv_data:
                self.socket_connect_status = False
                if self.sock_start_time is not None:
                    self.sock_start_to_close_time_list.append(round(time.time() - self.sock_start_time, 2))
                raise AssertionError(f"socket service close.")
        if mask & selectors.EVENT_WRITE:
            if self.ssl_communication:
                time.sleep(self.ssl_waite_time)
            if self.to_be_send_message:
                message = self.to_be_send_message.popleft()
                sock.send(message)
                logger.debug(f"{sock.getpeername()} tcp client send data:{message.hex()}")

    def start(self, timeout=10):
        if self.is_stop:
            self.is_stop = False
            Thread(target=self.main, args=(timeout,), daemon=True).start()

    def set_ca_cert_file(self, certfile, keyfile, ca_cert_file):
        self.certfile = certfile
        self.keyfile = keyfile
        self.ca_cert_file = ca_cert_file

    def main(self, timeout=10, connid=None):
        if self.ssl_communication:
            server_addr = (self.host, self.port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(self.certfile, self.keyfile)
            ssl_context.load_verify_locations(cafile=self.ca_cert_file)
            ssl_context.check_hostname = False
            ssl_context = ssl_context.wrap_socket(sock, server_hostname=self.host)
            ssl_context.connect_ex(server_addr)
            ssl_context.setblocking(False)
            logger.info(f"connect addr:{server_addr}")
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(messages=b"", outb=b"", recv_total=0,
                                         connid=random.randint(1, 0xff) if connid is None else int(connid))
            self.sel = selectors.DefaultSelector()
            self.sel.register(ssl_context, events, data=data)
            self.register_sock_set.add(ssl_context)
            self.sock_start_time = time.time()
        else:
            server_addr = (self.host, self.port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            logger.info(f"connect addr:{server_addr}")
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(messages=b"", outb=b"", recv_total=0,
                                         connid=random.randint(1, 0xff) if connid is None else int(connid))
            self.sel = selectors.DefaultSelector()
            self.sel.register(sock, events, data=data)
            self.register_sock_set.add(sock)
            self.sock_start_time = time.time()

        while not self.is_stop:
            try:
                events = self.sel.select(timeout=timeout)
                if events:
                    for key, mask in events:
                        self.handle_message(key, mask)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.warning("caught keyboard interrupt, exiting")
                try:
                    for _sk in self.register_sock_set:
                        self.sel.unregister(_sk)
                        _sk.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketClient.py")
                    logger.warning(f"tcp server sock down handler error:{e}")
                self.register_sock_set.clear()
                raise AssertionError(f"caught keyboard interrupt, exiting")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketClient.py")
                logger.warning(f"socket error:{e}")
                try:
                    for _sk in self.register_sock_set:
                        self.sel.unregister(_sk)
                        _sk.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketClient.py")
                    logger.warning(f"tcp server sock down handler error:{e}")
                time.sleep(SocketData.RECONNECT_TIME)
                self.register_sock_set.clear()
                self.main()
        logger.info(f"tcp client socket stop and exit 0.")
