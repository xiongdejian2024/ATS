#!/usr/bin/env python3
"""
@File        : tcp_socket.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-05-31 01:45
@Description :
"""

import socket
import sys
import errno
import threading
import time
from time import sleep
import select  # for select.select

# from ecu_simulator.sdk.driver.ethernet_lib.logger import setup_logger as setup_logger
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.utils.utils import struct_pretty


class tcp_socket_client(threading.Thread):
    def __init__(self, threadID, name, sock=None, debug="warning"):
        threading.Thread.__init__(self)
        self.tcp_connection_error = False
        self.threadID = threadID
        self.name = name
        self.exitFlag = False
        # self.log = setup_logger(debug, "TCP SOCKET")
        self.sock = sock
        self.create_socket(sock)
        self.receive_timeout = 8
        # self.lock = threading.Lock()

    def create_socket(self, sock):
        if sock is None:
            with error_check(StatusCode.DOIP_INIT_ERR, exception_error.DOIPError):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        if self.sock:
            with error_check(StatusCode.DOIP_ADDR_OR_PORT_MULTIPLEX_ERR, exception_error.DOIPError):
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # try:
            #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # except OSError as e:
            #     logger.error("Error setup socket rx!!!")
            #     raise type(e)(str(e) + ' : %s' % self.port_id)

    def connect(self, host, port):
        # logger.debug(
        #     "Connecting to %s:%d, using socket: %d" % (host, port, self.sock.fileno())
        # )
        logger.debug(
            "连接到 %s:%d, 使用socket: %d" % (host, port, self.sock.fileno())
        )
        self.tcp_host = host
        self.tcp_port = port
        retries = 20  # It will make 20 retries every .5 seconds (see time.sleep below)
        final_exception = None
        while retries > 0:
            try:
                self.sock.connect((host, port))
            except socket.timeout as e:
                logger.exception("连接超时 %s 到host %s:%d" % (str(e), host, port))
                self.tcp_connection_error = True
                final_exception = e
            except socket.error as e:
                logger.exception("socket错误 %s 到host %s:%d" % (str(e), host, port))
                self.tcp_connection_error = True
                final_exception = e
            except Exception as e:
                logger.exception("连接错误 %s 到host %s:%d" % (str(e), host, port))
                self.tcp_connection_error = True
                final_exception = e
            else:
                self.tcp_connection_error = False
                final_exception = None
                break

            if self.tcp_connection_error is True:
                retries -= 1
                self.close_socket()
                self.create_socket(None)
                time.sleep(0.5)

        if final_exception is not None:
            with error_check(StatusCode.DOIP_CONNECT_ERR, exception_error.DOIPError):
                raise AssertionError(f"连接到 {host}:{port} 错误 {final_exception}")
        # if final_exception is not None:
        #     logger.error(
        #         "Connect error %s to Host %s:%d after 20 retries"
        #         % (str(final_exception), host, port)
        #     )
        #     raise type(final_exception)(
        #         str(final_exception) + ' : %s:%d' % (host, port)
        #     )
        return 0

    def setup_response_callback(self, callBack):
        self.cb = callBack
        return True

    def send(self, msg):
        if isinstance(msg, list):
            msgToSend = bytes(msg)
        elif isinstance(msg, bytes):
            msgToSend = msg
        else:
            with error_check(StatusCode.DOIP_SEND_DATA_TYPE_ERR, exception_error.DOIPError):
                raise AssertionError(f"发送数据类型错误")
            # logger.error("Invalid data type to send")
            # raise RuntimeError("Invalid data type to send")

        try:
            # self.lock.acquire()
            self.sock.sendall(msgToSend)
            # self.lock.release()
        except OSError as e:
            self.tcp_connection_error = True
            self.close_socket()
            logger.error("tcp socket 发送数据出错，主动关闭socket")
            logger.error(
                "Tx exception occurred in tcp socket: {}".format(sys.exc_info()[0])
            )

        # totalsent = 0
        # msg_len = len(msg)
        # sent = 0
        # while totalsent < msg_len:
        #     try:
        #         self.lock.acquire()
        #         sent = self.sock.send(msgToSend[totalsent:])
        #         self.lock.release()
        #         if sent == 0:
        #             raise RuntimeError("TCP socket connection broken")
        #     except OSError as e:
        #         logger.error("Tx exception occurred in tcp socket: {}".format(sys.exc_info()[0]))
        #         self.tcp_connection_error = True
        #     if self.tcp_connection_error == True:
        #         logger.warning("Trying to reconnect to %s: %d" % (self.tcp_host, self.tcp_port))
        #         self.close_socket()
        #         retries = 5
        #         result = None
        #         while retries > 0:
        #             try:
        #                 logger.warning("TCP_SOCKET: Reconnect")
        #                 result = self.connect(self.tcp_host, self.tcp_port)
        #             except OSError as e:
        #                 logger.error("TCP connect error: {}".format(sys.exc_info()[0]))
        #             if result is 0:
        #                 self.send(msg)
        #                 break
        #             else:
        #                 retries -= 1
        #                 time.sleep(1)
        #     totalsent = totalsent + sent
        #     return totalsent

    def run(self):
        logger.info("Tcp Socket Starting " + self.name)
        self.receive()
        logger.info("Tcp Socket Exiting " + self.name)

    def receive(self):
        i = self.receive_timeout  # 8 s 内没有任何数据，就直接关停
        while not self.exitFlag and self.tcp_connection_error is not True:
            try:
                timeout = 1
                readable, _, _ = select.select([self.sock], [], [], timeout)
                if readable:
                    do_read = bool(readable[0])
                else:
                    # print("TCP_SOCKET: Nothing to read, Exit Flag: ", self.exitFlag, "Socket No: ", self.sock.fileno())
                    do_read = False
            except socket.error:
                do_read = False
                # logger.info("TCP_SOCKET: Select error")
                logger.info("Tcp socket select error")
            if do_read:
                try:
                    data = self.sock.recv(
                        1024 * 10
                    )  # TODO: There is still a problem receiving payload bigger than this
                except OSError as err:
                    self.tcp_connection_error = True
                    self.close_socket()
                    logger.warning(f"tcp socket 错误，{err}")
                    # logger.error("TCP socket:" + str(err))
                    # logger.warning("关闭socket")
                    break
                if data == b'':
                    self.tcp_connection_error = True
                    self.close_socket()
                    logger.warning("对端 TCP socket 断连, 关闭socket")
                    break

                    # retries = 10
                    # while self.tcp_connection_error is True and retries > 0 and not self.exitFlag:
                    #     logger.error("TCP connection broken, unable to rx, to= %d, Exit Flag: %d" % (retries, int(self.exitFlag)))
                    #     time.sleep(1)
                    #     retries -= 1
                    # if retries == 0:
                    #     break
                # logger.debug(f"接收到tcp数据：{data.hex()}")
                data = list(data)
                for cb_obj in self.cb:
                    cb_obj(data)
                i = self.receive_timeout
            else:
                i -= 1
                if i < 0:
                    self.tcp_connection_error = True
                    self.close_socket()
                    logger.info("Socket timeout, 主动关闭Socket")
                    break
                logger.debug(f"Socket timeout, 计数：{i}")
        logger.debug("doip:tcp_socket(%d):receive:Exit" % self.sock.fileno())
        # logger.info(f"doip tcp socket {self.sock.fileno()} 接收数据退出")
        return

    def set_receive_timeout(self, receive_timeout):
        self.receive_timeout = receive_timeout

    def close(self):
        # logger.debug("TCP_SOCKET: Closing tcp socket(%d)" % self.sock.fileno())
        if self.exitFlag == True:
            # logger.warning("doip_tcp_client flag bit has been turned off")
            logger.warning("doip tcp/ip已经关闭")
        else:
            self.exitFlag = True
            self.close_socket()

    def close_socket(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError as err:
            logger.exception("TCP socket shutdown error:" + str(err))
        time.sleep(
            0.2
        )  # 0.2 sec is not a magic number. Just some delay is necessary to prevent some race condition
        # between socket closing and actual thread exit. Tested down to 0.001 sec.
        self.sock.close()
        # print("TCP_SOCKET: Closed")


def new_data(data):
    print("Data Rx: %s" % (data))


if __name__ == '__main__':
    s = tcp_socket_client(1, "TCP Socket rx")
    s.connect("10.118.49.81", 13400)
    s.setup_data_callback(new_data)
    s.start()
    s.send(
        [
            0x02,
            0x02 ^ 0xFF,
            0x80,
            0x01,
            0x00,
            0x00,
            0x00,
            0x06,
            0x0E,
            0x80,
            0x00,
            0x05,
            0x10,
            0x01,
        ]
    )
    while True:
        try:
            time.sleep(0.1)
            s.send(
                [
                    0x02,
                    0x02 ^ 0xFF,
                    0x80,
                    0x01,
                    0x00,
                    0x00,
                    0x00,
                    0x06,
                    0x0E,
                    0x80,
                    0x00,
                    0x05,
                    0x10,
                    0x01,
                ]
            )
        except KeyboardInterrupt:
            s.close()
            time.sleep(1)
