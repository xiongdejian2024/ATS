#!/usr/bin/env python3
"""
@File        : udp_brocaster_socket.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022-04-27 14:45
@Description :
"""

import socket
import threading
# from ecu_simulator.sdk.driver.ethernet_lib.logger import setup_logger as setup_logger
from xat_ecu.legacy.common.logger import logger
import time
import select
import sys


DoIP_Announce_Num = 10

class UdpBroadcast(threading.Thread):
    def __init__(self, name, host="<broadcast>", port=13400, data=[], sock=None, debug="warning", server_ip="169.254.1.200"):
        threading.Thread.__init__(self)
        self.tcp_connection_error = False
        self.name = name
        self.exitFlag = False
        # logger = setup_logger(debug, "UDP Broadcast SOCKET")
        self.server_ip = server_ip
        self.sock = sock
        self.address = (host, port)
        self.create_socket(sock)
        self.data = data
        # self.lock = threading.Lock()

    def create_socket(self, sock):
        if sock is None:
            # create socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        if self.sock:
            try:
                self.sock.bind((self.server_ip, 0))
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            except OSError as e:
                self.close_socket()
                print("Error setup socket rx!!!")
                raise type(e)(str(e) + ' : ip %s, port %s' % self.address)

    def setup_response_callback(self, callBack):
        self.cb = callBack
        return True

    def set_broadcast_data(self, data=[]):
        self.data = data

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
            self.sock.sendto(msgToSend, self.address)
            # self.lock.release()
        except OSError as e:
            logger.error("Tx exception occurred in tcp socket: {}".format(sys.exc_info()[0]))

    def run(self):
        logger.info("Starting " + self.name)
        i = 0
        while (not self.exitFlag) and (i < 10):
            self.send(self.data)
            i += 1
            time.sleep(1)
        if i == 10:
            self.close()
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
                try: data = self.sock.recv(1024*10) #TODO: There is still a problem receiving payload bigger than this
                except OSError as err:
                    logger.error("TCP socket:" + str(err))
                    break
                if data == b'':
                    self.tcp_connection_error = True
                    retries = 10
                    while self.tcp_connection_error is True and retries > 0 and not self.exitFlag:
                        logger.error("TCP connection broken, unable to rx, to= %d, Exit Flag: %d" % (retries, int(self.exitFlag)))
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
        # try:
        #     self.sock.shutdown(socket.SHUT_RDWR)     # UDP socket 不需要，会报错 [Errno 107] Transport endpoint is not connected
        # except OSError as err:
        #     logger.error("socket shutdown error:" + str(err))   
        time.sleep(0.2)     # 0.2 sec is not a magic number. Just some delay is necessary to prevent some race condition
                            # between socket closing and actual thread exit. Tested down to 0.001 sec.
        self.sock.close()

def new_data(data):
    print("Data Rx: %s" % (data))


