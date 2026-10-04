#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProtocolParser.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/19 1:12
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.

from functools import reduce
from collections import namedtuple
from xat_ecu.legacy.protocol.ProtocolServices import *


def generate_dict_data(obj):
    data = dict()
    isflags = getattr(obj, "_flagsenum", False)
    for k, v in obj.items():
        if isinstance(k, str) and k.startswith("_"):
            continue
        if isflags and not v:
            continue

        if not isinstance(v, Container):
            if isinstance(v, ListContainer):
                inner_data = []
                for i in v:
                    inner_data.append(generate_dict_data(i))
                data[k] = inner_data
            else:
                data[k] = v
        else:
            data[k] = generate_dict_data(v)
    return data


def uds_build(data: [namedtuple, bytes, bytearray], tp_type='fr'):
    """
    uds序列化入口函数
    :param data: namedtuple类型数据
    :return:
    """
    return ProtocolBaseBuild(data, tp_type=tp_type, proto_type='uds').get_build_data


def uds_parse(data, tp_type='fr'):
    """
    uds反序列化入口函数
    :param data: bytes, bytearray, list的uds数据
    :return: 解析后的结构体数据
    """
    return ProtocolBaseParse(
        reduce(
            lambda x,
            y: x + y,
            data) if isinstance(
            data,
            list) else data, tp_type=tp_type, proto_type='uds').get_parse_data


def obd_build(data: namedtuple):
    """
    obd序列化入口函数
    :param data: namedtuple类型数据
    :return:
    """
    return ProtocolBaseBuild(data, tp_type='obd', proto_type='uds').get_build_data


def obd_parse(data):
    """
    obd反序列化入口函数
    :param data: bytes, bytearray, list的uds数据
    :return: 解析后的结构体数据
    """
    return ProtocolBaseParse(
        reduce(
            lambda x,
            y: x + y,
            data) if isinstance(
            data,
            list) else data, tp_type='obd', proto_type='uds').get_parse_data


def doip_build(data: dict):
    return ProtocolBaseBuild(data, tp_type='doip', proto_type='doip').get_build_data


def doip_parse(data):
    return ProtocolBaseParse(
        reduce(
            lambda x,
            y: x + y,
            data) if isinstance(
            data,
            list) else data, tp_type='doip', proto_type='doip').get_parse_data


def intelligent_build(data: dict):
    return ProtocolBaseBuild(data, tp_type='Intelligent', proto_type='Intelligent').get_build_data


def intelligent_parse(data):
    return ProtocolBaseParse(
        reduce(
            lambda x,
            y: x + y,
            data) if isinstance(
            data,
            list) else data, tp_type='Intelligent', proto_type='Intelligent').get_parse_data
