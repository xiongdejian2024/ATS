#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : SocketService.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/6/17 19:36
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
import sys
import time
import types
import socket
import selectors
from threading import Thread
from collections import deque, defaultdict
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.socket_client.SocketData import SocketData


class SocketService:

    def __init__(self, host="0.0.0.0", port=30500):
        self.host = host
        self.port = port
        self.listen_flag = False
        self.accept_max_number = 10000
        self.to_be_send_message = defaultdict(deque)
        self.max_bytes = 1024 * 10
        self.register_sock_set = set()
        self.sel = None
        self.error_count = 0

    def stop(self, need_to_flag=True):
        try:
            for _sk in self.register_sock_set:
                if hasattr(_sk, 'close'):
                    self.sel.unregister(_sk)
                    _sk.close()
            self.sel.close()
            self.register_sock_set.clear()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
            logger.warning(f"handle socket server stop error:{e}")
        self.tcp_server_clear_data()
        self.to_be_send_message.clear()
        if need_to_flag:
            self.listen_flag = False

    def create_listen_socket(self, timeout=10):
        try:
            lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            lsock.bind((self.host, self.port))
            lsock.listen()
            logger.info(f"listening on ({self.host, self.port})", )
            lsock.setblocking(False)

            self.sel = selectors.DefaultSelector()
            self.sel.register(lsock, selectors.EVENT_READ, data=None)
            self.register_sock_set.add(lsock)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
            logger.warning(f"create and register socker error,got:{e}")
            if self.error_count < 8:
                self.stop(need_to_flag=False)
                self.create_listen_socket()
            else:
                sys.exit(-1)
            self.error_count += 1

        while self.listen_flag:
            try:
                events = self.sel.select(timeout=timeout)
                for key, mask in events:
                    if key.data is None:
                        conn, addr = key.fileobj.accept()
                        logger.info(f"accepted connection from {addr}")
                        conn.setblocking(False)
                        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
                        events = selectors.EVENT_READ | selectors.EVENT_WRITE
                        self.sel.register(conn, events, data=data)
                        self.register_sock_set.add(conn)
                        self.to_be_send_message[conn] = deque([], maxlen=1000)
                    else:
                        self.service_connection(key, mask)

            except KeyboardInterrupt:
                logger.info("caught keyboard interrupt, exiting")
                try:
                    for _sk in self.register_sock_set:
                        self.sel.unregister(_sk)
                        _sk.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                    logger.warning(f"tcp server sock down handler error:{e}")
                self.register_sock_set.clear()
                raise AssertionError("caught keyboard interrupt, exiting")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                logger.warning(f"socket error:{e}")
                time.sleep(SocketData.RECONNECT_TIME)
                self.create_listen_socket()
        logger.info(f"tcp server socket stop and exit 0.")

    def start(self, timeout=10):
        if not self.listen_flag:
            self.listen_flag = True
            Thread(target=self.create_listen_socket, args=(timeout,), daemon=True).start()

    def tcp_server_clear_data(self, sock_id=None):
        if not sock_id:
            SocketData.TCP_SERVER_DATA.clear()
        else:
            if sock_id in SocketData.TCP_SERVER_DATA:
                SocketData.TCP_SERVER_DATA[sock_id].clear()

    def async_send_message(self, sock, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        elif isinstance(message, (bytes, bytearray)):
            message = message
        else:
            raise AssertionError('to bo send message type error, must bytes or str!')

        self.to_be_send_message[sock].append(message)
        # logger.debug(f"tcp server send data:{message.hex()}")

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(self.max_bytes)
                if recv_data:
                    data.outb += recv_data
                    logger.debug(f"{sock.getpeername()} tcp server accept data:{recv_data.hex()}")

                    if sock not in SocketData.TCP_SERVER_DATA:
                        SocketData.TCP_SERVER_DATA[sock] = deque([recv_data], maxlen=self.accept_max_number)
                    else:
                        SocketData.TCP_SERVER_DATA[sock].append(recv_data)
                else:
                    del SocketData.TCP_SERVER_DATA[sock]
                    logger.warning(f"closing connection to {data.addr}")
                    try:
                        self.sel.unregister(sock)
                        sock.close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                        logger.warning(f"tcp server sock down handler error:{e}")

                    if sock in self.register_sock_set:
                        self.register_sock_set.remove(sock)
            except ConnectionResetError:
                try:
                    self.sel.unregister(sock)
                    sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                    logger.warning(f"tcp server sock down handler error:{e}")

                if sock in self.register_sock_set:
                    self.register_sock_set.remove(sock)
                logger.warning("client force exit")
                raise AssertionError(f"client force exit")
            except ConnectionAbortedError:
                try:
                    self.sel.unregister(sock)
                    sock.close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                    logger.warning(f"tcp server sock down handler error:{e}")

                if sock in self.register_sock_set:
                    self.register_sock_set.remove(sock)
                logger.warning("client exception exit")
                raise AssertionError("client exception exit")
        if mask & selectors.EVENT_WRITE:
            for k, v in self.to_be_send_message.items():
                if v:
                    while self.to_be_send_message[k]:
                        try:
                            _data = self.to_be_send_message[k].popleft()
                            k.send(_data)
                            logger.debug(f"{k.getpeername()} tcp server send data:{_data.hex()}")
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/socket_client/SocketService.py")
                            logger.warning(f"socker error,got:{e}")
