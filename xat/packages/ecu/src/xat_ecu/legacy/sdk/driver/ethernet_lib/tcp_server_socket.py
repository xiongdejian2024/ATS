#!/usr/bin/env python3
"""
@File        : tcp_socket.py
@Author      : quan.sun@jiduauto.com
@Time        : 2021-05-31 01:45
@Description :
"""

import socket
import sys
import errno
import threading
import time
import select  # for select.select
# from ecu_simulator.sdk.driver.ethernet_lib.logger import setup_logger as setup_logger
from xat_ecu.legacy.common.logger import logger


SEND_BUF_SIZE = 256
RECV_BUF_SIZE = 256


class TcpSocketServer(threading.Thread):
    def __init__(
        self, name, ip="169.254.12.97", port=13400, sock=None, debug="warning"
    ):
        threading.Thread.__init__(self)
        self.tcp_connection_error = False
        self.name = name
        self.exitFlag = False
        # logger = setup_logger(debug, "TCP SOCKET")
        self.sock = sock
        self.server_address = (ip, port)
        self.create_socket(sock)
        self.connected_flag = None
        # self.lock = threading.Lock()

    def create_socket(self, sock):
        if sock is None:
            # create socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        if self.sock:
            try:
                # set a new buffer size  &  获得端口重用
                self.sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEPORT, SEND_BUF_SIZE
                )
                self.sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, RECV_BUF_SIZE
                )

                # bind port
                print("starting listen on ip %s, port %s" % self.server_address)
                self.sock.bind(self.server_address)

                # get the new buffer size
                s_send_buffer_size = self.sock.getsockopt(
                    socket.SOL_SOCKET, socket.SO_SNDBUF
                )
                s_recv_buffer_size = self.sock.getsockopt(
                    socket.SOL_SOCKET, socket.SO_RCVBUF
                )
                print("socket send buffer size[new] is %d" % s_send_buffer_size)
                print("socket receive buffer size[new] is %d" % s_recv_buffer_size)

            except OSError as e:
                print("Error setup socket rx!!!")
                raise type(e)(str(e) + " : ip %s, port %s" % self.server_address)

    def setup_response_callback(self, callBack):
        self.cb = callBack
        return True

    def send(self, msg):
        if isinstance(msg, list):
            msgToSend = bytes(msg)
        elif isinstance(msg, bytes):
            msgToSend = msg
        else:
            logger.error("Invalid data type to send")
            raise RuntimeError("Invalid data type to send")
        try:
            # self.lock.acquire()
            self.sock.sendall(msgToSend)
            # self.lock.release()
        except OSError as e:
            logger.error(
                "Tx exception occurred in tcp socket: {}".format(sys.exc_info()[0])
            )

    def run(self):
        logger.info("Starting " + self.name)

        # start listening, allow only one connection
        try:
            self.sock.listen(1)
        except socket.error as e:
            print("fail to listen on port %s" % e)
            sys.exit(1)
        while True:
            print("waiting for connection")
            client, addr = self.sock.accept()
            self.sock.close()
            self.sock = client
            self.connected_flag = True
            print("========================={}=====================".format(addr))
            print("having a connection")
            break
        print("welcome to tcp server")
        self.receive()

        logger.info("Exiting " + self.name)

    def receive(self):
        while not self.exitFlag:
            try:
                timeout = 1
                readable, _, _ = select.select([self.sock], [], [], timeout)
                if readable:
                    do_read = bool(readable[0])
                else:
                    # print("TCP_SOCKET: Nothing to read, Exit Flag: ", self.exitFlag, "Socket No: ", self.sock.fileno())
                    do_read = False
            except socket.error:
                # print("TCP_SOCKET: Select error")
                do_read = False
            if do_read:
                try:
                    data = self.sock.recv(
                        1024 * 101
                    )  # TODO: There is still a problem receiving payload bigger than this
                except OSError as err:
                    logger.error("TCP socket:" + str(err))
                    break
                if data == b"":
                    self.tcp_connection_error = True
                    retries = 10
                    while (
                        self.tcp_connection_error is True
                        and retries > 0
                        and not self.exitFlag
                    ):
                        logger.error(
                            "TCP connection broken, unable to rx, to= %d, Exit Flag: %d"
                            % (retries, int(self.exitFlag))
                        )
                        time.sleep(1)
                        retries -= 1
                    if retries == 0:
                        break
                data = list(data)
                self.cb(data)
            else:
                logger.debug("Socket timeout")
        logger.debug("doip:tcp_socket(%d):receive:Exit" % self.sock.fileno())
        return

    def close(self):
        logger.debug("TCP_SOCKET: Closing tcp socket(%d)" % self.sock.fileno())
        if self.exitFlag == True:
            logger.warning("doip_tcp_client flag bit has been turned off")
        else:
            self.exitFlag = True
            self.close_socket()

    def close_socket(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError as err:
            logger.error("TCP socket shutdown error:" + str(err))
        time.sleep(
            0.2
        )  # 0.2 sec is not a magic number. Just some delay is necessary to prevent some race condition
        # between socket closing and actual thread exit. Tested down to 0.001 sec.
        self.sock.close()
        # print("TCP_SOCKET: Closed")


def new_data(data):
    print("Data Rx: %s" % (data))


if __name__ == "__main__":
    s = tcp_socket_server(1, "TCP Socket rx")
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
