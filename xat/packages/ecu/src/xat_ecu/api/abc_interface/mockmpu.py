#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mockmpu.py

@Time         :2024/06/24 10:00

@Author       :songjian.lin@jiduauto.com

@Description  :mock BGM mpu与mcu内部以太网通信的抽象接口

"""
from abc import abstractmethod, ABCMeta
from typing import Union, List, Tuple


class AbcMockMpuMock(metaclass=ABCMeta):

    @abstractmethod
    def get_pm_socket(self):
        """
        获取pm socket
        @return:
        @rtype:
        """

    @abstractmethod
    def get_s2s_socket(self):
        """
        获取s2s socket
        @return:
        @rtype:
        """

    @abstractmethod
    def get_mcu_log_socket(self):
        """
        获取mcu log socket
        @return:
        @rtype:
        """

    @abstractmethod
    def get_doip_socket(self):
        """
        获取doip socket
        @return:
        @rtype:
        """

    @abstractmethod
    def get_udp_socket(self):
        """
        获取udp socket
        @return:
        @rtype:
        """

    @abstractmethod
    def set_signal(self, signal_name, signal_value, send_frame=1, send_cycle=50, send_type_immediately=True):
        """
        发送ETH signal信号给到MCU，此接口主要用于Trigger PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_frame：int 信号发送帧数 如果PDU报文发送类型为：trigger,默认值为1 frame
        :param send_type_immediately 信号是否立即发送,默认值为True
        :param send_cycle 如果PDU报文发送类型为：trigger,参考此参数,此参数默认值为50ms
        """

    @abstractmethod
    def send_pdu(self, signal_name, is_cycle=False):
        """
        发送ETH Message 报文
        param: signal_name 通过signal name判断ETH PDU是否是周期报文
        """

    @abstractmethod
    def send_all_cycle_pdu(self):
        """
        调用此function 需要发送ETH 所有cycle 报文
        """

    @abstractmethod
    def change_signal(self, signal_name, signal_value, send_type=0):
        """
        更改ETH Signal信号给到MCU，此接口主要用于Cycle PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_type 信号发送类型：0-表示信号改变后等到固定周期在发送 1-表示插帧,会立即发送变化信号,但是信号周期保持不变
        """

    @abstractmethod
    def close_socket(self):
        """
        关闭创建的socket连接
        @return:
        @rtype:
        """
