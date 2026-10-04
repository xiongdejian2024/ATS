#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : DoipServerGateway.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/10 14:51
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.socket_client.SocketData import SocketData
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.socket_client.UdpServer import UdpServer
from xat_ecu.legacy.socket_client.SocketService import SocketService
from xat_ecu.legacy.protocol.ProtocolConfigData import *


class DoipServerGateway(object):

    def __init__(self, uds_host="172.16.9.21", uds_port=13400):
        self.uds_host = uds_host
        self.uds_port = uds_port
        self.udp_server_sock = None
        self.tcp_server_sock = None

    def new_tcp_connect_start(self):
        self.tcp_server_sock = SocketService(self.uds_host, self.uds_port)
        self.tcp_server_sock.start()

    def new_udp_connect_start(self):
        self.udp_server_sock = UdpServer(self.uds_host, self.uds_port)
        self.udp_server_sock.start()
