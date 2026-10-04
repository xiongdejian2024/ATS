#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :serial.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :串口通信能力模拟 实现接口
"""
from xat_ecu.api import CommonSerial


class Serial(CommonSerial):

    def send(self, command, pattern=None, timeout=10, sync=True):
        return self.serial.send(command, pattern, timeout, sync)

    def receive(self):
        return self.serial.receive_data()
