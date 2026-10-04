#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :serial.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :串口通信能力模拟 抽象接口
"""
from abc import ABCMeta, abstractmethod


class AbcSerial(metaclass=ABCMeta):
    @abstractmethod
    def send(self, command, pattern=None, timeout=10, sync=True):
        """
        朝串口发送命令
        向串口发送指令，同时根据指定的模式pattern来观察串口的输出是否是期望的值。

        :param str/bytes/list command: 命令，可以是str/bytes/list, list会当做二进制字节流拼接成bytes进行发送
        :param str pattern: 要匹配的串口输出
        :param int timeout: 超时设置，最多等这么多时间
        :param bool sync: 同步执行命令或异步执行命令

        :rtype: (bool, str)
        :return: 返回真假值和串口输出
        """
        pass

    @abstractmethod
    def receive(self):
        """接收串口返回"""
        pass
