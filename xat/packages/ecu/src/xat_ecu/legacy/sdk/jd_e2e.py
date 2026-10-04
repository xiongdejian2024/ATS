# -*- coding: utf-8 -*-
"""
@File        : jd_e2e.py
@Author      : quan.sun@jiduauto.com
@Time        : 2023/02/10 8:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
from typing import Tuple, Union
from xat_ecu.legacy.common.logger import logger


def crc8(data: list, div=0x11D):
    '''
    **CRC8 algorithm used is defined by SAE (refer to SAE-J1850), using the division
    polynomial x8+x4+x3+x2+1    div = 0x11D
    :data is list , such as [0x11,0x22]
    Algorithm：CRC-8-SAE J1850；
    Polynominal：0x1D(𝑥8+𝑥4+𝑥3+𝑥2+1)；
    Start Value: 0x00；
    XOR Value：0x00；
    '''
    Start_Value = 0
    XOR_Value = 0
    
    t_crc = Start_Value
    i = 0
    while i < len(data):
        t_crc ^= data[i]
        b = 0
        while b < 8:
            if (t_crc & 0x80) != 0:
                t_crc <<= 1
                t_crc ^= div
            else:
                t_crc <<= 1
            b += 1
        i += 1
    t_crc ^= XOR_Value
    return t_crc

def get_crc_countdata(data_id:int, counter:int, sig_value_length:list) -> list:
    # sig_value_length  type:list   such as   [(20,7), (311,10)]
    crc_data = data_id.to_bytes(2, 'little')
    crc_data += counter.to_bytes(1, 'little')
    for value, length in sig_value_length:
        crc_data += value.to_bytes(((length-1) // 8)+1, 'little')
    return list(crc_data)

