#!/usr/bin/env python3
"""
@File        : tcp_server_socket.py
@Author      : songjian.lin@jiduauto.com
@Time        : 2021-09-22 01:45
@Description :
"""
import logging
import socket
import sys
import threading
import time
import datetime
import operator

SEND_BUF_SIZE = 256
RECV_BUF_SIZE = 256


class TcpSocketServer(threading.Thread):
    def __init__(self, name, testcase, ip="172.16.5.222", port=30500):
        threading.Thread.__init__(self)
        self.tcp_connection_error = False
        self.name = name
        self.exitFlag = False
        self.sock = socket.socket()
        self.testcase = testcase
        self.get_from_mpu = []
        self.expected = []
        self.expected.extend(convert_int_to_list(int(self.testcase.channel), 4))
        self.expected.extend(convert_int_to_list(int(self.testcase.message_id), 4))
        self.expected.extend(convert_int_to_list(int(self.testcase.signal_value), int(self.testcase.message_id)))
        try:
            ip_port = ('172.16.5.222', 30500)
            # print("starting listen on ip %s, port %s" % ip_port)
            self.sock.bind(ip_port)

            # set a new buffer size
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, SEND_BUF_SIZE)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, RECV_BUF_SIZE)

            # get the new buffer size
            s_send_buffer_size = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            s_recv_buffer_size = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            # print("socket send buffer size[new] is %d" % s_send_buffer_size)
            # print("socket receive buffer size[new] is %d" % s_recv_buffer_size)

        except OSError as e:
            print("Error setup socket rx!!!")
            raise type(e)(str(e) + ' : ip %s, port %s' % ip_port)
        self.server_address = (ip, port)
        self.connected_flag = None

    def setup_response_callback(self, callBack):
        self.cb = callBack
        return True

    # def send(self, msg):
    #     if isinstance(msg, list):
    #         msgToSend = bytes(msg)
    #     elif isinstance(msg, bytes):
    #         msgToSend = msg
    #     else:
    #         logging.error("Invalid data type to send")
    #         raise RuntimeError("Invalid data type to send")
    #     try:
    #         # self.lock.acquire()
    #         self.sock.sendall(msgToSend)
    #         # self.lock.release()
    #     except OSError as e:
    #         logging.error("Tx exception occurred in tcp socket: {}".format(sys.exc_info()[0]))

    def run(self):
        # start listening, allow only one connection
        try:
            self.sock.listen(1)  # 设置并启动 TCP 监听器
        except socket.error as e:
            print("fail to listen on port %s" % e)
            sys.exit(1)
        while True:
            # print("waiting for connection")
            client, addr = self.sock.accept()  # 被动接受 TCP 客户端连接，一直等待直到连接到达（阻塞）
            self.sock.close()
            self.sock = client
            self.connected_flag = True
            # print("========================={}=====================".format(addr))
            # print("having a connection")
            break
        self.receive()
        # logging.info("Exiting " + self.name)

    def receive(self):
        while not self.exitFlag:
            try:
                data = self.sock.recv(1024 * 101)
                # my_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                list_data = list(data)
                if operator.eq(list_data[0:4], self.expected[0:4]):
                    self.get_from_mpu = list_data
                    self.exitFlag = True
                    self.close()
                #if is_first:
                #   response_data = [0x02, 0xfd, 0x00, 0x06, 0x00, 0x00, 0x00, 0x09, 0x0e, 0x90, 0x14, 0x44, 0x10,
                #                    0x00, 0x00, 0x00, 0x00]
                #   is_first = False
                #   self.send(response_data)
            except OSError as err:
                logging.error("TCP socket:" + str(err))
                break
            if data == b'':
                self.tcp_connection_error = True
                retries = 10
                while self.tcp_connection_error is True and retries > 0 and not self.exitFlag:
                    logging.error("TCP connection broken, unable to rx, to= %d, Exit Flag: %d"
                                  % (retries, int(self.exitFlag)))
                    time.sleep(1)
                    retries -= 1
                if retries == 0:
                    break
                # data = list(data)
                # self.cb(data)
            # else:
            #     logging.info("Socket timeout")
        logging.debug("doip:tcp_socket(%d):receive:Exit" % self.sock.fileno())
        return

    def close(self):
        if not self.exitFlag:
            self.exitFlag = True
            self.close_socket()

    def close_socket(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError as err:
            logging.error("TCP socket shutdown error:" + str(err))
        time.sleep(0.2)  # 0.2 sec is not a magic number. Just some delay is necessary to prevent some race condition
        # between socket closing and actual thread exit. Tested down to 0.001 sec.
        self.sock.close()
        # print("TCP_SOCKET: Closed")


def new_data(data):
    print("Data Rx: %s" % data)


def convert_int_to_list(input_str, length):
    a = int(input_str)
    if 0 <= a <= 2147483647:
        result = hex(a)[2::].upper()
        first = []
        for _ in range(length):
            first.append(0)
        index = len(result)
        i = len(first)
        while True:
            if index - 2 >= 0:
                first[i - 1] = int(result[index - 2:index], 16)
            elif index - 2 == -1:
                first[i - 1] = int(result[index - 1:index], 16)
            else:
                break
            i -= 1
            index -= 2
        return first


if __name__ == '__main__':
    print("Hello ")
    # s = tcp_socket_server(1, "TCP Socket rx")
    # s.connect("10.118.49.81", 13400)
    # s.setup_data_callback(new_data)
    # s.start()
    # s.send([0x02, 0x02 ^ 0xFF, 0x80, 0x01, 0x00, 0x00, 0x00, 0x06, 0x0E, 0x80, 0x00, 0x05, 0x10, 0x01])
    # while True:
    #     try:
    #         time.sleep(.1)
    #         s.send([0x02, 0x02 ^ 0xFF, 0x80, 0x01, 0x00, 0x00, 0x00, 0x06, 0x0E, 0x80, 0x00, 0x05, 0x10, 0x01])
    #     except KeyboardInterrupt:
    #         s.close()
    #         time.sleep(1)
    print(convert_int_to_list('5', 1))




