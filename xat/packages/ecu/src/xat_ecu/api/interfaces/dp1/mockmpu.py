#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :diagmock.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :整车 server ecu 诊断能力模拟抽象接口
"""
from xat_ecu.api import CommonMockMpu
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_mpu_tcp import MockMpuSocketClient


class MockMpu(CommonMockMpu):

    def get_pm_socket(self):
        """
        获取pm socket
        @return:
        @rtype:
        """
        if self.pm_socket is None:
            self.pm_socket = MockMpuSocketClient(tcp_down_mpu_port=30504, tcp_up_mpu_port=30505)

        return self.pm_socket

    def get_s2s_socket(self):
        """
        获取s2s socket
        @return:
        @rtype:
        """
        if self.s2s_socket is None:
            self.s2s_socket = MockMpuSocketClient()

        return self.s2s_socket

    def get_mcu_log_socket(self):
        """
        获取mcu log socket
        @return:
        @rtype:
        """

    def get_doip_socket(self):
        """
        获取doip socket
        @return:
        @rtype:
        """

    def get_udp_socket(self):
        """
        获取udp socket
        @return:
        @rtype:
        """

    def start_heart_beat(self):
        self.get_pm_socket().send_trigger_frame(20018)
        self.get_pm_socket().start_send_cycle_frame(20021)

    def set_signal(self, signal_name, signal_value, send_frame=1, send_cycle=50, send_type_immediately=True):
        """
        发送ETH signal信号给到MCU，此接口主要用于Trigger PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_frame：int 信号发送帧数 如果PDU报文发送类型为：trigger,默认值为1 frame
        :param send_type_immediately 信号是否立即发送,默认值为True
        :param send_cycle 如果PDU报文发送类型为：trigger,参考此参数,此参数默认值为50ms
        """
        self.get_s2s_socket().set_trigger_signal_value(signal_name, signal_value, send_type_immediately,
                                                       send_frame, send_cycle)

    def send_pdu(self, signal_name):
        """
        发送ETH Message 报文
        param: signal_name 通过signal name判断ETH PDU是否是周期报文
        """
        self.get_s2s_socket().send_pdu(signal_name)

    def send_all_cycle_pdu(self):
        """
        调用此function 需要发送ETH 所有cycle 报文
        """
        self.get_s2s_socket().start_send_all_cycle_frame()

    def change_signal(self, signal_name, signal_value, send_type=0):
        """
        更改ETH Signal信号给到MCU，此接口主要用于Cycle PDU Message

        :param signal_name：string 信号名称
        :param signal_value：int 信号发送值
        :param send_type 信号发送类型：0-表示信号改变后等到固定周期在发送 1-表示插帧,会立即发送变化信号,但是信号周期保持不变
        """
        self.get_s2s_socket().change_signal(signal_name, signal_value, send_type)

    def close_socket(self):
        """
        关闭创建的socket连接
        @return:
        @rtype:
        """

        if self.pm_socket is not None:
            self.pm_socket.stop_client_socket()
        if self.s2s_socket is not None:
            self.s2s_socket.stop_client_socket()
