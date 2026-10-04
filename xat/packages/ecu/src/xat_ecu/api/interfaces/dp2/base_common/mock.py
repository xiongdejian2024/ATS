#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mock.py
@Time         :2024/11/6 17:46
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from xat_ecu.api.interfaces.dp2.interface import CommonMock
from xat_ecu.api.interfaces.dp2.base_common.constants.common_data import *
from typing import Dict, Union


class Mock(CommonMock):
    def update_channel(self, channel_dict: Dict[Union[TcpChannel, UdpChannel], Union[tuple, None]]):
        """
        新增以太网channel仿真发送
        :param channel_dict: key为通道名称，value为2个server和client的ip,port二元组或None，为None则使用默认地址
            举例1  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: (('172.20.5.12', 30503), ('172.20.5.11', 30513))
            举例2  TcpChannel.CdMcuTCPServer_CdNadTCPClient1: None
        :return:
        """
        tcp_dict = {}
        udp_dict = {}
        for channel in channel_dict:
            if isinstance(channel, TcpChannel):
                tcp_dict.update({channel.value: channel_dict[channel]})
            else:
                udp_dict.update({channel.value: channel_dict[channel]})
        self.udp.update_channel(udp_dict)
        self.tcp.update_channel(tcp_dict)
    
    def stop_mock(self):
        """停止模拟UDP、TCP并关闭所有发送线程和socket"""
        self.udp.stop_mock()
        self.tcp.stop_mock()
    
    def _ret_mock_instance(self, channel: Union[TcpChannel, UdpChannel]):
        """根据channel返回不同的实例对象"""
        if isinstance(channel, TcpChannel):
            return self.tcp
        else:
            return self.udp
        
    def wait_client_reconnect(self, channel: TcpChannel, timeout=20):
        """
        等待客户端重连
        :param channel: 通道名
        :param timeout: 超时时间
        :return: 
        """
        self.tcp.wait_client_reconnect(channel=channel.value, timeout=timeout)
    
    def get_signal_values(self, channel: TcpChannel, signal_name: str):
        """
        获取给到信号的信号值列表
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return: 信号值列表[value1, value2, value3...]
        """
        return self.tcp.get_signal_values(channel.value, signal_name)
    
    def get_signal_items(self, channel: TcpChannel, signal_name: str):
        """
        获取给到信号的数据列表
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return: 信号数据列表[SignalItemInfo, SignalItemInfo, SignalItemInfo...]
        """
        return self.tcp.get_signal_items(channel.value, signal_name)

    def get_last_signal(self, channel: TcpChannel, signal_name: str):
        """
        获取对应信号的最后一个值
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :return
        """
        return self.tcp.get_last_signal(channel.value, signal_name)

    def ck_signal_values(self, channel: TcpChannel, signal_name: str, ck_values: list):
        """
        针对明确知道pcap数据包中信号值的场景，校验信号值的数量和值是否符合预期，一般用于事件型信号
        :param channel: 通道名
        :param signal_name: 指定的信号名
        :param ck_values: 信号值列表
        :return:
        """
        self.tcp.ck_signal_values(channel.value, signal_name, ck_values)
    
    def ck_period_time(self, channel: TcpChannel, signal_name: str, period, deviation=0.2, permit_fail_times=0):
        """
        用于周期性信号校验，但是考虑插帧场景，允许一定次数失败，返回失败次数
        :param channel: 通道名
        :param signal_name: 信号名
        :param period: 期望周期, 单位s
        :param deviation: 默认±20%为可接受偏差
        :param permit_fail_times: 允许失败的次数，默认0次
        :return: 失败次数
        """
        self.tcp.ck_period_time(channel.value, signal_name, period, deviation, permit_fail_times)

    def ck_ordered_array(self, channel: TcpChannel, signal_name: str, ck_array: list):
        """
        校验周期下行pdu中信号为有序数组，无异常跳变，用于触发信号跳变后以新值继续周期发送的case
        从获取到ck_array第一个信号开始校验，因为抓tcpdump开始的数据可能还没有下发服务请求，不是期望值
        一直校验到pcap中最后的一个信号值
        :param channel: 通道名
        :param signal_name: 信号名
        :param ck_array: 信号数组
        """
        self.tcp.ck_ordered_array(channel.value, signal_name, ck_array)

    def ck_period_signal_trigger(self, channel: TcpChannel, signal_name: str, idle_value: int, trigger_values: list):
        """
        校验周期下发的报文中有顺序的信号跳变, 用于下行几帧信号后回到idle的case
        :param channel: 通道名
        :param signal_name: 信号名
        :param idle_value: 周期下发的报文中触发指定value后回到的idle值，如0
        :param trigger_values: 触发的非idle值列表，如发送3帧3，再发一帧1回到idle，[3, 3, 3, 1]
        """
        self.tcp.ck_period_signal_trigger(channel.value, signal_name, idle_value, trigger_values)
    
    def set_signal(self, channel: Union[TcpChannel, UdpChannel], signal_name: str, signal_value: Union[int, float]):
        """
        设置信号值
        :param channel: 通道名
        :param signal_name: 信号名
        :param signal_value: 信号值，如果是float就是物理值，如果是int就是总线值
        :return:
        """
        self._ret_mock_instance(channel).set_signal(channel.value, signal_name, signal_value)
    
    def stop_send_cycle_pdu(self, channel: Union[TcpChannel, UdpChannel], pduid: int):
        """
        停止指定通道的周期发送报文
        :param channel: 通道名
        :param pduid: 周期报文id
        :return:
        """
        self._ret_mock_instance(channel).stop_send_cycle_pdu(channel.value, pduid)
    
    def stop_send_all_cycle_pdu(self, sender=None):
        """停止所有周期发送报文"""
        self.udp.stop_send_all_cycle_pdu(sender)
        self.tcp.stop_send_all_cycle_pdu(sender)
    
    def resume_send_cycle_pdu(self, channel: Union[TcpChannel, UdpChannel], pduid: int):
        """
        恢复周期发送报文
        :param channel: 通道名
        :param pduid: 周期报文id
        :return:
        """
        self._ret_mock_instance(channel).resume_send_cycle_pdu(channel.value, pduid)
    
    def resume_send_all_cycle_pdu(self, sender=None):
        """恢复所有周期发送报文"""
        self.udp.resume_send_all_cycle_pdu(sender)
        self.tcp.resume_send_all_cycle_pdu(sender)
    
    def set_signal_and_send(self, channel: Union[TcpChannel, UdpChannel], signal_name, signal_value, 
                            send_pdu_immediately=False, send_num=1, cycle_time=5):
        """
        设定Event Trigger类型帧中的指定信号的数值
        :param channel:  通道名，即EthChannel
        :param signal_name:  信号名
        :param signal_value:  信号设定的值
        :param send_pdu_immediately: 是否立即发送
        :param send_num: 如果立即发送，指定发送次数，默认1次
        :param cycle_time: 如果立即发送，指定发送周期，默认5ms
        """
        self._ret_mock_instance(channel).set_signal_and_send(channel.value, signal_name, signal_value, send_pdu_immediately, send_num, cycle_time)
    
    def send_pdu(self, channel: Union[TcpChannel, UdpChannel], pduid: int, send_num=1, cycle_time=5):
        """
        给指定通道发送指定pduid报文
        :param channel: 通道名，即EthChannel
        :param pduid: 报文id
        :param send_num: 指定发送次数，默认1次
        :param cycle_time: 指定发送周期，默认5ms
        :return:
        """
        self._ret_mock_instance(channel).send_pdu(channel.value, pduid, send_num, cycle_time)
    
    def empty_channel(self, channel):
        """
        清除某个通道的抓包数据
        :param channel: 通道名
        :return:
        """
        self.tcp.empty_channel(channel)

    def empty(self):
        """清除所有通道的抓包数据"""
        self.tcp.empty()
    
    def ck_interrupt(self, channel: TcpChannel, signal_name: str, ordered_array: list, ck_nums: int, idle=None):
        """
        校验周期下行的报文打断逻辑
        :param channel: 通道名
        :param signal_name: 信号名
        :param ordered_array: 信号发送顺序(不含idle)，例：[1, 2, 3]表示1被2打断，再被3打断，[1,2]表示1被2打断
        :param ck_nums: 正常发送帧数
        :param idle: idle值，如果为None则为事件帧，否则为周期帧的idle
        """
        self.tcp.ck_interrupt(channel.value, signal_name, ordered_array, ck_nums, idle)
        

