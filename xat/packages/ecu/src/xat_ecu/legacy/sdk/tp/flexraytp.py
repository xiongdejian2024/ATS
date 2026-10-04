#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : flexraytp.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/17 13:00
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.

import copy
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.protocol.ProtocolConfigData import *


class FlexRayTp:

    @staticmethod
    def construct_parse_frames_data(data):
        return uds_parse(data)

    @staticmethod    
    def construct_tx_signal_frames(data):
        return list(uds_build(bytes(data)))[4:]
    
    @staticmethod     
    def construct_tx_multi_frames(data):
        return [list(single_data[4:]) for single_data in uds_build(bytes(data))]

    @staticmethod 
    def construct_tx_flow_frame():
        data = copy.deepcopy(fr_tp_flow_control_frame_raw_data)
        return uds_build(data)[4:]
    
    @staticmethod 
    def deconstruct_rx_signal_frames(msg):
        pass
    
    @staticmethod     
    def deconstruct_rx_first_frame(msg):
        pass

    @staticmethod 
    def deconstruct_rx_consecutive_frame(msg):
        pass

    @staticmethod 
    def deconstruct_rx_flow_frame(msg):
        pass
