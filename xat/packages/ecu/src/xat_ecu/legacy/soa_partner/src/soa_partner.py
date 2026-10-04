#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :soa.py
@Time         2023-12-12 13:18:28.241119
@Author       :songjian.lin@jiduauto.com
@Description  :soa通信能力模拟 实现接口
"""


from enum import Enum, auto


class FailType(Enum):
    FAILTYPE_SUCCESS = 0
    FAILTYPE_TIMEOUT = -1
    FAILTYPE_SERVICE_BUSY = -2
    FAILTYPE_SERVICE_UNAVAILIABLE = -3
    FAILTYPE_TIME_OUT = 600  # operation timed out


class SoaBasePartner:

    def __init__(self, soa_partner):
        """
        实例化S2sBaseClass
        """
        self.soa_partner = soa_partner
