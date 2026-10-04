#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :ssh通信能力模拟 实现接口
"""
from xat_ecu.api.interfaces.dp2 import *
from xat_ecu.api.interfaces.dp2.interface import CommonSsh


class Ssh(CommonSsh):
    def type_commands(self, device_name: DeviceName, commands: str, timeout: int = 60) -> str:
        return self.device_dict[device_name].type_commands(commands=commands, timeout=timeout)
