#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mockmcu.py

@Time         :2024/08/27 10:22

@Author       :dejian.xiong@jiduauto.com

@Description  :mock BGM mcu内部以太网通信的抽象接口

"""
from abc import abstractmethod, ABCMeta


class AbcMockMcu(metaclass=ABCMeta):

    @abstractmethod
    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", host="172.16.5.1", port=30500, **kwargs):
        """
        开启 bgm 内部抓包
        @param name:  抓包存储 文件名 ，最后会加上时间
        @param iface: 抓包的网卡
        @param host: 抓包指定的ip，可以填None，代表不指定ip
        @param port: 抓包指定的port，可以填None，代表不指定port
        @param kwargs:
        @return:
        """

    @abstractmethod
    def stop_tcpdump_and_parse_signal(self, sleep_time=0):
        """
        停止抓包,，复制到本地，并解析信号，同时删除bgm内部的pcap包
        @param sleep_time: 等待多久停止抓包
        """

    @abstractmethod
    def empty(self):
        """
        清空已经装载的信号值信息
        """

    @abstractmethod
    def get_signal_items(self, signal_name):
        """
        获取给到信号的数据列表
        @param signal_name: 指定的信号名
        return: 信号数据列表[(pcap_index, timestamp, signal_value), (), ()...]
        """

    @abstractmethod
    def get_signal_values(self, signal_name):
        """
        获取给到信号的信号值列表
        @param signal_name: 指定的信号名
        return: 信号值列表[value1, value2, value3...]
        """

    @abstractmethod
    def get_last_signal(self, signal_name):
        """
        获取对应信号的最后一个值
        """
    
    @abstractmethod
    def set_signal(self, signal_name: str, value: int, send_pdu_immediately=False):
        """
        设定pdu中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否立即发送一帧
        """
