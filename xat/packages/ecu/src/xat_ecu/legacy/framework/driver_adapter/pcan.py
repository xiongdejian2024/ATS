#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :pcan.py
@Time         :2024/12/6 17:11
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from typing import Union
from can.interfaces.pcan import PcanBus

from xat_ecu.legacy.framework.driver_adapter.abc_adapter import ABCAdapter


class PcanAadpter(ABCAdapter):
    def __init__(self, *args, **kwargs):
        self.pcan = PcanBus
        self.args = args
        self.kwargs = kwargs
        self.pcan_obj: Union[None, PcanBus] = None
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        self.pcan_obj = self.pcan(*self.args, **self.kwargs)
        return

    def stop(self):
        if self.pcan_obj is not None:
            self.pcan_obj.shutdown()

    def send(self, msg):
        self.pcan_obj.send(msg)
        self.callback(msg)

    def recv(self):
        msg = self.pcan_obj.recv()
        yield msg
        self.callback(msg)
