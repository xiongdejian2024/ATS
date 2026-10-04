#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :pcan.py
@Time         :2024/12/6 17:06
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import abc


class ABCAdapter(object):

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def send(self, msg):
        pass

    @abc.abstractmethod
    def recv(self):
        pass

    def start_record_log(self):
        pass

    def stop_record_log(self):
        pass
