#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :call_tracker.py
@Time         :2023/11/5 11:00
@Author       :dejian.xiong@jiduauto.com
@Description  :对象被调用前触发该模块，启动前置条件
"""
from abc import ABCMeta
from typing import List, Dict

from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger

import threading


class SingletonMeta(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class CallTrackerMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                attrs[attr_name] = cls.wrap_method(name, attr_name, attr_value)
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def wrap_method(class_name, method_name, method):
        def wrapper(self, *args, **kwargs):
            if method_name != '__init__':
                logger.debug(f"{self}调用了类 {class_name} {method_name} 方法")
                oe = ObjExecutor()
                oe.start_obj(self, class_name, method_name, *args)
            return method(self, *args, **kwargs)

        return wrapper


class ObjExecutor(metaclass=SingletonMeta):
    """
    对象执行器，用于记录当前哪些对象已经被start，如果未启动会主动进行启动
    """

    def __init__(self):
        self.start_cache = []
        self.start_partner_cache: List = []
        self.error_obj: Dict = {}

    def start_obj(self, obj, class_name, method_name=None, *args):
        if class_name not in self.start_cache:
            if class_name == 'BusComm':
                logger.info(f'开始启动总线')
                try:
                    obj.start_all_cyclic_msg()
                except (exception_error.CmdExecuteError, Exception) as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/call_tracker.py")
                    logger.error(f'总线启动失败')
                    self.start_cache.append(class_name)
                    self.error_obj[class_name] = (exception_error.BusAppError, str(e))
                    raise exception_error.BusAppError(e)
                else:
                    logger.info(f'总线启动成功')
            elif class_name == 'Soa':
                # 调用update接口才会启动服务
                if method_name == 'update' and not self.start_partner_cache:
                    self.start_partner_cache.append(*args)
                elif method_name != 'update' and not self.start_partner_cache:
                    err_msg = f"soa对象未调用update接口，无法使用服务"
                    logger.error(err_msg)
                    raise exception_error.SoaError(err_msg)
            elif class_name == 'DiagMock':
                logger.info(f'开始启动诊断Server模拟')
                obj.all_start()
                logger.info(f'诊断Server模拟启动成功')
            elif class_name == 'SdTest':
                logger.info(f'开始启动诊断仪')
                obj.start_sd_tester()
                logger.info(f'诊断仪启动成功')
            elif class_name == 'Io':
                logger.info(f'开始启动IO')
                obj.start_io()
                logger.info(f'IO启动成功')
            elif class_name == 'DigitalKeyCommon':
                logger.info(f'开始启动数字钥匙')
                obj.start_dk()
                logger.info(f'数字钥匙启动成功')
            elif class_name == 'Serial':
                logger.info(f'开始启动串口')
                obj.start_serial()
                logger.info(f'串口启动成功')
            elif class_name == 'MockMcu':
                logger.info(f'开始MockMcu')
                obj.start_mock()
                logger.info(f'MockMcu启动成功')
            elif class_name == 'LogTriggerHandler' and method_name not in ['start_socket', 'stop_socket']:
                logger.info(f'开始启动日志专项')
                obj.start_socket()
                logger.info(f'日志专项启动成功')
            self.start_cache.append(class_name)
        else:
            if class_name == 'BusComm' and method_name in ['stop_record_trace_log', 'start_record_trace_log']:
                return
            err_class = self.error_obj.get(class_name)
            if err_class:
                raise err_class[0](err_class[1])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.start_cache.clear()
        self.error_obj.clear()


class BaseABCMeta(CallTrackerMeta):
    pass
