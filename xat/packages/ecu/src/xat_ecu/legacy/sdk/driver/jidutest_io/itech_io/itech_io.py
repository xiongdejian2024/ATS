#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : itech_io.py

**********************

------------------------------------------------------------------
@Time    : 2024/11/28 19:08
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import time
import serial

from xat_ecu.legacy.common.logger import logger


class ItechIo(object):

    def __init__(self, serial_port=None, baud_rate=9600):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.serial = self.connect_serial(self.serial_port, self.baud_rate)
        self.send_serial_utf(f"SYSTem:REM\n")

    @staticmethod
    def connect_serial(port, baud_rate):
        """
        连接串口
        """
        if not port:
            logger.info(f"未找到串口设备")
            return None
        try:
            ser = serial.Serial(
                port=port,
                baudrate=baud_rate,
                parity='N',
                bytesize=8,
                stopbits=1,
                timeout=3)
            logger.info(f"已连接串口：{ser.portstr}")
            return ser
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/itech_io/itech_io.py")
            logger.warning(f"串口设备连接异常：{e}")

    def send_serial_utf(self, command):
        """
        向串口发送命令,格式为 UTF-8
        """
        logger.info(f"发送的指令是：{command.encode('utf-8')}")
        self.serial.write(command.encode('utf-8'))
        return self.serial.readline()

    def voltage_status_off(self):
        """
        设置可编程电源输出为关闭
        """
        self.send_serial_utf(f"OUTP 0\n")

    def voltage_status_on(self):
        """
        设置可编程电源输出为打开
        """
        self.send_serial_utf(f"OUTP 1\n")

    def set_volt(self, ch, value):
        """
        设置电压
        :param ch: 设置通道，如：1/2/3
        :param value: 如：12
        :return:
        """
        self.send_serial_utf(f"APPL CH{ch};VOLT {value}\n")

    def get_volt(self, ch):
        """
        获取电压的值
        :param ch: 通道，如：1/2/3
        :return:
        """
        result = self.send_serial_utf(f"APPL CH{ch};MEASure:VOLTage?\n")
        return float(result.decode().replace("\n", "")) if result else None

    def set_curr(self, ch, value):
        """
        设置电流
        :param ch: 设置通道，如：1/2/3
        :param value: 如：12
        :return:
        """
        self.send_serial_utf(f"APPL CH{ch};CURR {value}\n")

    def get_curr(self, ch):
        """
        获取电流的值
        :param ch: 通道，如：1/2/3
        :return:
        """
        result = self.send_serial_utf(f"APPL CH{ch};MEASure:CURR?\n")
        return float(result.decode().replace("\n", "")) if result else None
