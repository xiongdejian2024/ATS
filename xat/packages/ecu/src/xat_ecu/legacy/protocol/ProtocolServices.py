#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : services.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/19 11:25
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
import copy
import math

import six
import zlib
import importlib
from copy import deepcopy
from abc import abstractmethod

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.protocol.ProtocolStruct import *
from xat_ecu.legacy.protocol.ProtocolConfigData import *
from xat_ecu.legacy.utils.utils import CustomIterator


class ProtocolMeta(type):
    REGISTRY = {}

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super(ProtocolMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProtocolMeta, cls).__call__(*args, **kwargs)
        return cls._instance

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return cls.REGISTRY

    @classmethod
    def uninstall_registry(cls, name: str):
        return cls.REGISTRY.pop(name)


class ProtocolParser(object):
    protocol_lib = importlib.import_module('.protocol.ProtocolStruct', package='ecu_simulator')
    uds_services = ProtocolMeta.REGISTRY

    def __init__(self):
        self._objects = {}

    def clone(self, **attrs):
        obj = self.__class__()
        obj.__dict__.update(attrs)
        return obj

    @abstractmethod
    def protocol_build(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def protocol_parse(self, data, frame_obj=None):
        raise NotImplementedError

    @classmethod
    def get_engine_obj(cls):
        try:
            if cls.__name__.startswith("Doip"):
                frame_obj = getattr(cls.protocol_lib, f"uds_doip_frame_struct")
            elif cls.__name__.startswith("Intelligent"):
                frame_obj = getattr(cls.protocol_lib, f"Intelligent_ambient_light_with_0x{cls.__name__[-3:]}")
            else:
                frame_obj = getattr(cls.protocol_lib, f"uds_frame_struct_with_0x{cls.__name__[-2:]}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(e)
        else:
            return frame_obj


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid10(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid35(ProtocolParser):
    compress_flag = 0
    encryp_flag = 0

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            cls.compress_flag = data['DataFormatIdentifier']['CompressionMethod']
            cls.encryp_flag = data['DataFormatIdentifier']['EncryptingMethod']
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid34(ProtocolParser):
    compress_flag = 0
    encryp_flag = 0

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            cls.compress_flag = data['DataFormatIdentifier']['CompressionMethod']
            cls.encryp_flag = data['DataFormatIdentifier']['EncryptingMethod']
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid36(ProtocolParser):
    iter_36 = CustomIterator(end=0xff)

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            if cls.uds_services.get('UdsServiceSid34').encryp_flag or \
                    cls.uds_services.get('UdsServiceSid35').encryp_flag == 1:
                # data['TransferData'] = rsa_encrypt(data['TransferData'])
                pass
            if cls.uds_services.get('UdsServiceSid34').compress_flag or \
                    cls.uds_services.get('UdsServiceSid35').compress_flag == 1:
                data['TransferData'] = zlib.compress(data['TransferData'])
            max_block_data_value = cls.uds_services.get(
                'UdsServiceSid74').max_block_data_value
            logger.info(f"Data value len is:{len(data['TransferData'])}")
            logger.info(f'Allow block max value is:{max_block_data_value}')
            if len(data['TransferData']) > max_block_data_value:
                remainder = len(data['TransferData']) % max_block_data_value
                integer = len(data['TransferData']) // max_block_data_value
                loop_count = integer if remainder == 0 else integer + 1
                result = []
                transfer_data = deepcopy(data['TransferData'])
                for _ in range(loop_count):
                    data['BlockSequenceCounter'] = next(cls.iter_36)
                    data['TransferData'] = transfer_data[:max_block_data_value]
                    logger.info(f'Block 0x36 data is: \n{data}')
                    InitStruct.uds_service_with_0x36_len = len(
                        data['TransferData'])
                    result.append(cls.get_engine_obj().build(data))
                    transfer_data = transfer_data[max_block_data_value:]
                cls.iter_36.set_cursor(0)
            else:
                data['BlockSequenceCounter'] = next(cls.iter_36)
                InitStruct.uds_service_with_0x36_len = len(
                    data['TransferData'])
                result = cls.get_engine_obj().build(data)

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = []
            for index, single_obj in enumerate(frame_obj):
                if cls.uds_services.get('UdsServiceSid34').compress_flag or \
                        cls.uds_services.get('UdsServiceSid35').compress_flag == 1:
                    data[index] = zlib.decompress(data[index])
                if cls.uds_services.get('UdsServiceSid34').encryp_flag or \
                        cls.uds_services.get('UdsServiceSid35').encryp_flag == 1:
                    # data[index] = rsa_decrypt(data[index], None)
                    pass
                InitStruct.uds_service_with_0x36_len = single_obj.MessageInfo.FrameLen - 2
                sigle_parse_data = cls.get_engine_obj().parse(data)
                result.append(sigle_parse_data)
                data = data[single_obj.MessageInfo.FrameLen:]
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid50(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid30(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid70(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid3e(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid7e(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid7f(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid27(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x27_len = len(data['SecretKey'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid67(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x67_len = frame_obj[0].MessageInfo.FrameLen - 2
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid11(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid54(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid51(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid28(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid68(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid6e(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid14(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x14_len = len(data['OpDTC'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x67_len = frame_obj[0].MessageInfo.FrameLen - 1
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid19(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid59(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x59_len = len(data['ConSecutiveInfo'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            if (frame_obj[0].MessageInfo.FrameLen - 3) % 4 != 0:
                InitStruct.uds_service_with_0x59_len = frame_obj[0].MessageInfo.FrameLen - 3
            else:
                InitStruct.uds_service_with_0x59_len = (
                    frame_obj[0].MessageInfo.FrameLen - 3) // 4
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid2f(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid6f(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class FlowFrameService(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = uds_flow_control_frame_struct.build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = uds_flow_control_frame_struct.parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid22(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid74(ProtocolParser):
    max_block_data_value = 1024

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            cls.max_block_data_value = int(bytes.hex(result.MaxDataValue), 16)
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid75(ProtocolParser):
    max_block_data_value = 1024

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            cls.max_block_data_value = int(bytes.hex(result.MaxDataValue), 16)
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid76(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x76_len = len(data['TransferData'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x76_len = frame_obj[0].MessageInfo.FrameLen - 2
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid37(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x37_len = len(data['TransferData'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x37_len = frame_obj[0].MessageInfo.FrameLen - 1
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid77(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x77_len = len(data['TransferData'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x77_len = frame_obj[0].MessageInfo.FrameLen - 1
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid31(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x31_len = len(
                data['routineControlOptionRecord'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x31_len = frame_obj[0].MessageInfo.FrameLen - 4
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid71(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x71_len = len(
                data['routineControlOptionRecord'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x71_len = frame_obj[0].MessageInfo.FrameLen - 4
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid85(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSidc5(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid62(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x62_len = frame_obj[0].MessageInfo.FrameLen - 3
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class UdsServiceSid2e(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            InitStruct.uds_service_with_0x2e_len = len(data['DataIdData'])
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
            raise e
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x2e_len = frame_obj[0].MessageInfo.FrameLen - 3
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid01(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid41(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid02(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid03(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid42(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid04(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid44(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid43(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid06(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid46(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            frame_obj = frame_obj if isinstance(
                frame_obj, list) else [frame_obj]
            InitStruct.uds_service_with_0x46_len = frame_obj[0].MessageInfo.FrameLen - 1
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid07(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid47(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid08(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid48(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid09(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class ObdServiceSid49(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result
        


@six.add_metaclass(ProtocolMeta)
class DoipServiceSid(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class IntelligentServiceSid111(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


@six.add_metaclass(ProtocolMeta)
class IntelligentServiceSid101(ProtocolParser):

    @classmethod
    def protocol_build(cls, data: dict):
        try:
            result = cls.get_engine_obj().build(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data build error, with: {e}')
        else:
            return result

    @classmethod
    def protocol_parse(
            cls,
            data,
            frame_obj=None) -> dict:
        try:
            result = cls.get_engine_obj().parse(data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/protocol/ProtocolServices.py")
            logger.warning(f'Data parse error, with: {e}')
            raise e
        else:
            return result


class ProtocolBaseParse(object):
    def __init__(self, data, tp_type: str = 'fr', proto_type: str = 'uds'):
        self.data = data
        self.tp_type = tp_type
        self.proto_type = proto_type
        self.frame_obj = None
        self.service_pre_name = f'{proto_type.capitalize()}ServiceSid'
        self.services = ProtocolMeta.REGISTRY
        if self.services is None:
            raise AssertionError('Not found uds service can use.')

    def can_tp_handler(self):
        if self.data[0] >> 4 == 3:
            return self.control_frame_parse()
        elif self.data[0] >> 4 == 1:
            return self.multi_frame_parse()
        elif self.data[0] >> 4 == 2:
            raise AssertionError('Data not support continuity is 2 with start')
        elif self.data[0] >> 4 == 0:
            return self.single_frame_parse()
        else:
            raise AssertionError(
                f'Not support parse type ,got: {self.data[0] >> 4}')

    def fr_tp_handler(self):
        fr_frame_obj = fr_tp_frame_raw_struct.parse(self.data)
        return fr_frame_obj

    def doip_frame_handler(self):
        return self.services.get(f'{self.service_pre_name}').protocol_parse(self.data)

    def intelligent_frame_handler(self):
        if self.data[:2] == b'\x00\xa0':
            return self.services.get(f'{self.service_pre_name}101').protocol_parse(self.data)
        elif self.data[:2] == b'\x00\xe0':
            return self.services.get(f'{self.service_pre_name}111').protocol_parse(self.data)

    @property
    def get_parse_data(self):
        if self.tp_type == "can":
            return self.can_tp_handler()
        elif self.tp_type == "fr":
            return self.fr_tp_handler()
        elif self.tp_type == "doip":
            return self.doip_frame_handler()
        elif self.tp_type == "Intelligent":
            return self.intelligent_frame_handler()
        else:
            raise AssertionError(f"Not currently supported tp type, got:{self.tp_type}")

    def single_frame_parse(self):
        """
        :return: 解析后的单帧数据
        """
        if self.tp_type == "can":
            self.frame_obj = uds_single_frame_raw_struct.parse(
                bytes([self.data[0] & 0xf]))
            return self.services.get(f'{self.service_pre_name}{bytes.hex(self.data[1:2]).lower()}')\
                .protocol_parse(self.data[1:], self.frame_obj)
        elif self.tp_type == "fr":
            pass
        elif self.tp_type == "doip":
            pass

    def multi_frame_parse(self):
        """
        根据多帧定义的结构体，返回解析后的多帧数据
        :return: 解析后的数据
        """
        if self.tp_type == "can":
            if len(self.data) % 8 != 0:
                raise AssertionError(
                    f'Parse data len error, got: {len(self.data)}')
            parse_obj = self.services.get(
                f'{self.service_pre_name}{bytes.hex(self.data[2:3]).lower()}')

            if parse_obj is None:
                raise AssertionError(
                    f'Not found {self.service_pre_name}{bytes.hex(self.data[2:3])} service')
            multi_parse_frame_data_list = []
            multi_parsedata_list = []
            multi_frame_count = 0
            for index in range(len(self.data) // 8):
                if self.data[0] >> 4 == 0x1:
                    multi_parse_frame_data_list.append(self.data[:2])
                    multi_parsedata_list.append(self.data[2:8])
                    multi_frame_count += 1
                else:
                    multi_parse_frame_data_list.append(self.data[:1])
                    multi_parsedata_list.append(self.data[1:8])

                self.data = self.data[8:]
            InitStruct.uds_service_with_muilt_count = multi_frame_count
            self.frame_obj = uds_multi_frame_raw_struct.parse(
                b''.join(multi_parse_frame_data_list))
            return parse_obj.protocol_parse(
                b''.join(multi_parsedata_list),
                self.frame_obj)
        elif self.tp_type == "fr":
            pass

    def control_frame_parse(self):
        if self.tp_type == "can":
            return self.services.get('FlowFrameService').protocol_parse(self.data, None)
        elif self.tp_type == "fr":
            pass
        elif self.tp_type == "doip":
            pass


class ProtocolBaseBuild(object):
    _iter = CustomIterator(end=15)

    def __init__(self, data, tp_type: str = 'fr', proto_type: str = 'uds'):
        self.data = data
        self.tp_type = tp_type
        self.proto_type = proto_type
        self.service_pre_name = f'{proto_type.capitalize()}ServiceSid'
        self.services = ProtocolMeta.REGISTRY
        if self.services is None:
            raise AssertionError('Not found uds service can use.')

    def handler_can_tp_build(self):
        if self.data.extends_data is not None:
            body_build_data = self.data.extends_data
            if not isinstance(body_build_data, list):
                body_build_data = [body_build_data]
            return self._get_build_data(body_build_data)

        service_id = self.data.raw_data.get('ServiceID')
        if service_id is None:
            return self.control_frame_build()
        else:
            service_id_hex = f'0{hex(service_id)[2:].lower()}' if len(
                hex(service_id)[2:].lower()) == 1 else hex(service_id)[2:].lower()
            use_service = self.service_pre_name + service_id_hex

            body_build_data = self.services.get(
                f"{use_service}").protocol_build(self.data.raw_data)

            if body_build_data is None:
                raise AssertionError('Build data return None.')
            if not isinstance(body_build_data, list):
                body_build_data = [body_build_data]
            return self._get_build_data(body_build_data)

    def handler_fr_tp_build(self, single_frame_max_len=14, mt_frame_max_len=16):
        if not isinstance(self.data, (bytes, bytearray)):
            raise AssertionError(f"Not currently supported type for fr:{type(self.data)}")

        body_build_data = self.data
        if not isinstance(body_build_data, list):
            body_build_data = [body_build_data]

        result_list = []
        for sigle_body_build_data in body_build_data:
            maximum_load = copy.deepcopy(len(sigle_body_build_data))
            if len(sigle_body_build_data) <= single_frame_max_len:
                _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                _sg_data["RawData"] = sigle_body_build_data
                _sg_data["MessageInfo"]["EffectiveLength"] = len(sigle_body_build_data)
                _sg_data["MessageInfo"]["MaximumLoad"] = len(sigle_body_build_data)
                sigle_result = fr_tp_frame_raw_struct.build(_sg_data)
                result_list.append(sigle_result)
            else:
                _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                _sg_data["RawData"] = sigle_body_build_data[:single_frame_max_len]
                _sg_data["MessageInfo"]["EffectiveLength"] = single_frame_max_len
                _sg_data["MessageInfo"]["MaximumLoad"] = len(sigle_body_build_data)
                sigle_result = fr_tp_frame_raw_struct.build(_sg_data)
                result_list.append(sigle_result)
                sigle_body_build_data = sigle_body_build_data[single_frame_max_len:]

                _range_len = math.ceil(len(sigle_body_build_data)/mt_frame_max_len)
                if _range_len == 1:
                    _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                    _sg_data["FrameType"]["C_PCIType"] = 5
                    _sg_data["FrameType"]["Ctr_Status"] = next(self._iter)
                    _sg_data["MessageInfo"]["EffectiveLength"] = len(sigle_body_build_data)
                    _sg_data["MessageInfo"]["MaximumLoad"] = maximum_load
                    _sg_data["RawData"] = sigle_body_build_data
                    mutil_result = fr_tp_frame_raw_struct.build(_sg_data)
                    result_list.append(mutil_result)

                    _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                    _sg_data["FrameType"]["C_PCIType"] = 9
                    _sg_data["FrameType"]["Ctr_Status"] = 0
                    _sg_data["MessageInfo"]["EffectiveLength"] = 0
                    _sg_data["MessageInfo"]["MaximumLoad"] = maximum_load
                    _sg_data["RawData"] = b""
                    mutil_result = fr_tp_frame_raw_struct.build(_sg_data)
                    result_list.append(mutil_result)
                else:
                    for _ in range(_range_len-1):
                        _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                        _sg_data["FrameType"]["C_PCIType"] = 5
                        _sg_data["FrameType"]["Ctr_Status"] = next(self._iter)

                        _sg_data["MessageInfo"]["EffectiveLength"] = mt_frame_max_len
                        _sg_data["MessageInfo"]["MaximumLoad"] = maximum_load
                        _sg_data["RawData"] = sigle_body_build_data[:mt_frame_max_len]
                        mutil_result = fr_tp_frame_raw_struct.build(_sg_data)
                        result_list.append(mutil_result)
                        sigle_body_build_data = sigle_body_build_data[mt_frame_max_len:]
                    _sg_data = copy.deepcopy(fr_tp_frame_raw_data)
                    _sg_data["FrameType"]["C_PCIType"] = 9
                    _sg_data["FrameType"]["Ctr_Status"] = 0
                    _sg_data["MessageInfo"]["EffectiveLength"] = len(sigle_body_build_data)
                    _sg_data["MessageInfo"]["MaximumLoad"] = maximum_load
                    _sg_data["RawData"] = sigle_body_build_data if len(sigle_body_build_data) else b""
                    mutil_result = fr_tp_frame_raw_struct.build(_sg_data)
                    result_list.append(mutil_result)
            self._iter.set_cursor(0)

        if len(result_list) == 1:
            return result_list[0]
        else:
            finally_result = []
            for sigle_packge_result in result_list:
                if isinstance(sigle_packge_result, list):
                    for sigle_frame_data in sigle_packge_result:
                        finally_result.append(sigle_frame_data)
                else:
                    finally_result.append(sigle_packge_result)
            return finally_result

    def handler_doip_build(self):
        if not isinstance(self.data, dict):
            raise AssertionError(f"Not currently supported type expect dict,got:{type(self.data)}")
        return self.services.get(f'{self.service_pre_name}').protocol_build(self.data)

    def handler_salm_build(self):
        if not isinstance(self.data, dict):
            raise AssertionError(f"Not currently supported type expect dict,got:{type(self.data)}")
        if self.data.get('ProtocolType') == 0x00e0:
            return self.services.get(f'{self.service_pre_name}111').protocol_build(self.data)
        elif self.data.get('ProtocolType') == 0x00a0:
            return self.services.get(f'{self.service_pre_name}101').protocol_build(self.data)

    @property
    def get_build_data(self):
        """
        :return: 根据实例化传入的数据返回对应序列化后诊断数据
        """
        if self.tp_type == "can":
            return self.handler_can_tp_build()
        elif self.tp_type == "fr":
            return self.handler_fr_tp_build()
        elif self.tp_type == "doip":
            return self.handler_doip_build()
        elif self.tp_type == "Intelligent":
            return self.handler_salm_build()
        else:
            raise AssertionError(f"Not currently supported tp type, got:{self.tp_type}")

    def _get_build_data(self, body_build_data):
        """
        :param body_build_data: 有效的序列化数据
        :return: 返回NPU所需的序列化数据
        """
        result_list = []
        for sigle_body_build_data in body_build_data:
            if len(sigle_body_build_data) <= 7:
                sigle_result = self.single_frame_build(sigle_body_build_data)
                result_list.append(sigle_result)
            else:
                mutil_result = self.multi_frame_build(sigle_body_build_data)
                result_list.append(mutil_result)
            self._iter.set_cursor(0)

        if len(result_list) == 1:
            return result_list[0]
        else:
            finally_result = []
            for sigle_packge_result in result_list:
                if isinstance(sigle_packge_result, list):
                    for sigle_frame_data in sigle_packge_result:
                        finally_result.append(sigle_frame_data)
                else:
                    finally_result.append(sigle_packge_result)
            return finally_result

    @staticmethod
    def single_frame_build(data, reverse_data=b'\xCC'):
        """
        :param data:有效序列化单帧数据
        :param reverse_data:保留数据
        :return: 8个字节的单帧数据
        """
        if len(data) > 7:
            logger.warning(
                f'Single frame data len must less 7, got {data};len: {len(data)}')

        single_data = deepcopy(uds_single_frame_raw_data)
        single_data['MessageInfo']['FrameLen'] = len(data)
        data = data + (7 - len(data)) * reverse_data
        full_build_data = uds_single_frame_raw_struct.build(
            single_data) + data
        return full_build_data

    def multi_frame_build(
            self,
            data,
            sigle_message=False,
            reverse_data=b'\xCC'):
        """
        多帧数据组包，
        :param data: 序列化后的多帧数据
        :param sigle_message: 是否返回一个长度序列化后数据，默认false，否则返回list
        :param reverse_data: 保留数据
        :return:
        """
        multi_data = deepcopy(uds_multi_frame_raw_data)
        multi_data['MessageInfo']['FrameLen'] = len(data)
        seq_count = (len(data) - 6) // 7 if (len(data) - 6)\
            % 7 == 0 else (len(data) - 6) // 7 + 1

        if self.data.seq_num:
            self._iter.set_cursor = int(self.data.seq_num)
        multi_data['ConSecutiveInfo'] = [
            {'NameType': 2, 'SequenceNumber': next(self._iter)} for _ in range(seq_count)]
        full_packge_list = []
        InitStruct.uds_service_with_muilt_count = 1
        multi_frame_data = uds_multi_frame_raw_struct.build([multi_data])
        full_packge_list.append(multi_frame_data[:2] + data[:6])
        data = data[6:]

        for item in multi_frame_data[2:]:
            if len(data) < 7:
                full_packge_list.append(
                    bytes([item]) + data + (7 - len(data)) * reverse_data)
            else:
                full_packge_list.append(bytes([item]) + data[:7])
                data = data[7:]
        return b''.join(
            full_packge_list) if sigle_message else full_packge_list

    def control_frame_build(self):
        """
        :return: 序列化后的控制帧数据
        """
        return self.services.get(
            'FlowFrameService').protocol_build(self.data.raw_data)
