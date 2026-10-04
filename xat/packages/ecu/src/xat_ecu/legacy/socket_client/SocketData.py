#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : SocketData.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/7 16:34
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
from collections import deque, defaultdict


class SocketData:
    RECONNECT_TIME = 1
    UDP_CLIENT_DATA = defaultdict(deque)
    UDP_SERVER_DATA = defaultdict(deque)
    TCP_CLIENT_DATA = defaultdict(deque)
    TCP_SERVER_DATA = defaultdict(deque)
    UDP_BROADCAST_CLIENT_DATA = defaultdict(deque)
