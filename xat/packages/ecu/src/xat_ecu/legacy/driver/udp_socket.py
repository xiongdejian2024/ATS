#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File        : udp_socket.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/05 22:38 PM
@Description : udp_socket basic function

"""

import socket
import logging
import threading
import time


class UdpSocketClient(threading.Thread):
    def __init__(self, threadID, name, address=("127.0.0.1", 30502), sock=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.exitFlag = False
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock

        self.sock.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
        # self.sock.settimeout(10)  # 设置一个时间提示，如果10秒钟没接到数据进行提示

        self.log = logging.getLogger(__name__)

    def setup_data_callback(self, callBack):
        self.cb = callBack
        return True

    def send(self, msg, server):
        if isinstance(msg, list):
            msgToSend = bytes(msg)
        elif isinstance(msg, bytes):
            msgToSend = msg
        else:
            self.log.error("Invalid data type to send")
            raise RuntimeError("Invalid data type to send")
        totalsent = 0
        msg_len = len(msg)
        while totalsent < msg_len:
            sent = self.sock.sendto(msgToSend[totalsent:],server)
            if sent == 0:
                raise RuntimeError("TCP socket connection broken")
            totalsent = totalsent + sent

    def run(self):
        self.log.info("Starting " + self.name)
        self.receive()
        self.log.info("Exiting " + self.name)

    def receive(self):
        while(self.exitFlag == False):
            chunk = self.sock.recvfrom(4096)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            data = list(chunk)
            self.cb(data)
        return

    def print_rx_data(self, data):
        print("Data Rx: %s" % (data))

    def not_print_rx_data(self, data):
        pass

    def close(self):
        self.exitFlag = True
        time.sleep(0.1)
        self.sock.close()

# ****************************************************************************************
#                                UDP Socket Unit Testing
# ****************************************************************************************
def new_data(data):
    print("Data Rx: %s" % (data))

if __name__ == '__main__':
    s = UdpSocketClient(1,"UDP Socket rx")
    s.setup_data_callback(new_data)
    s.start()
    s.send([0x02,0x02^0xFF,0x80,0x01,0x00,0x00,0x00,0x06,0x0E,0x80,0x00,0x05,0x10,0x01],("127.0.0.1", 30502))
    while(True):
        try:
            time.sleep(.1)
            s.send([0x02, 0x02 ^ 0xFF, 0x80, 0x01, 0x00, 0x00, 0x00, 0x06, 0x0E, 0x80, 0x00, 0x05, 0x10, 0x01],("127.0.0.1", 30502))
        except KeyboardInterrupt:
            s.close()
            time.sleep(1)