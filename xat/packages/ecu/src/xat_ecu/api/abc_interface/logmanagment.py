#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :logmanagment.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :logmanagment能力模拟抽象接口,可以提供自定义日志检查分析接口
"""
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import List, Union


class AbcLogManagement(metaclass=ABCMeta):

    @abstractmethod
    @contextmanager
    def check_jetlog_by_keywords(self,
                                 log_type,
                                 keywords: Union[None, List] = None,
                                 unexpect_keywords: Union[None, List] = None,
                                 log_print: bool = False,
                                 device_name: Union[None, str] = None,
                                 timeout: Union[int, float] = 10):
        """
        检查jetlog的关键字

        :params log_type: 日志类型，必选，例如:rvc
        :params keywords: 查询关键字，支持多个关键字查询，必选，列表或者字符串
        :params unexpect_keywords: 查询不期望的关键字，支持多个关键字查询，可选，列表或者字符串
        :params log_print: 设备上的原生日志是否打印，默认不打印
        :params device_name: 设备类型
        :params timeout: 超时时间，如果超时时间之后未查询到关键字会返回False，否则返回True
        :return:
        """
        pass

    @abstractmethod
    def start_record_log(self, case_name: str):
        """
        异步录制log
        :params case_name: 用例名称
        :return:None
        """
        pass

    @abstractmethod
    def stop_record_log(self):
        """
        停止录制log
        :return:None
        """
        pass

    @abstractmethod
    def start_record_soa_partner_log(self):
        """
        开始录制soa_partner日志
        """
        pass

    @abstractmethod
    def stop_record_soa_partner_log(self):
        """
        停止录制soa_partner日志
        """
        pass
