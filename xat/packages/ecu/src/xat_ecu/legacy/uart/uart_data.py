#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : crc_data.py

**********************

------------------------------------------------------------------
@Time    : 2024/9/26 15:48
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
from collections import deque, defaultdict


class UartData:
    DIAG_DATA_FLAG = "00a0"
    RUN_DATA_FLAG = "00e0"
    RUN_DATA = defaultdict(deque)
