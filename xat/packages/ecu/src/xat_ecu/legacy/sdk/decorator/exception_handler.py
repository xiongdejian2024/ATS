# -*- coding: utf-8 -*-

"""
@Time    : 2022/5/24 11:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""
import datetime
import json
import os
import sys
import time
import traceback
import inspect
import types

from xat_ecu.legacy.common.logger import logger


def is_function(obj):
    return isinstance(obj, types.FunctionType)


def monitor(sync_cloud=False):
    """
    监控SDK的执行
    @param sync_cloud: 执行结果是否同步云端
    """
    def timer(func):
        def wrapper(*args, **kwargs):
            frame = inspect.currentframe()
            module_path = ""
            module_name = ""
            if frame is not None:
                back_frame = frame.f_back
                if back_frame is not None:
                    module_name = sys.modules.get(back_frame.f_globals.get('__name__'))
                    module_path = module_name.__file__.split('ecu_simulator')[-1]
                    module_name = module_name.__file__.split(os.path.sep)[-1]
            start_time = datetime.datetime.now()
            function_name = func.__name__
            parameter_info = ""
            if args:
                parameter_type = f"{type(args[0])}"
                if parameter_type.startswith("<class"):
                    if len(args) > 1:
                        parameter_info += f"一般参数：{args[1:]}"
                else:
                    parameter_info += f"一般参数：{args}"
            if kwargs:
                parameter_info += f"，字典参数：{kwargs}"
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/decorator/exception_handler.py")
                exception_type = e.__repr__()
                exception_detail = traceback.format_exc()
                exceptionInfo = ExceptionInfo(module_path, module_name, function_name, parameter_info,
                                              start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                                              "FAIL", exception_type=exception_type, exception_detail=exception_detail)
                exceptionInfo.to_string()
                if sync_cloud:
                    add_sdk_run_record(exceptionInfo)
                return None
            else:
                stop_time = datetime.datetime.now()
                exceptionInfo = ExceptionInfo(module_path, module_name, function_name, parameter_info,
                                              start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                                              "PASS", end_time=stop_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                # if sync_cloud:
                #     add_sdk_run_record(exceptionInfo)
                run_info = f"{module_path}{os.path.sep}{module_name} 的 {function_name} 方法"
                if parameter_info:
                    run_info += f"，入参: {parameter_info}"
                run_info += f", 返回结果: {res}"
                run_info_dict = {"模块路径": module_name, "模块名称": module_name, "函数名": function_name}
                if parameter_info:
                    run_info_dict["执行入参"] = parameter_info
                run_info_dict["返回结果"] = res
                logger.info(json.dumps(run_info_dict, indent=2, ensure_ascii=False))
                return res

        return wrapper

    return timer


class ExceptionInfo:
    def __init__(self, module_path, module_name, function_name, parameter_info, start_time, run_result, end_time="",
                 exception_type="", exception_detail=""):
        self.modulePath = module_path
        self.moduleName = module_name
        self.functionName = function_name
        self.parameterInfo = parameter_info
        self.startTime = start_time
        self.runResult = run_result
        self.exceptionType = exception_type
        self.exceptionDetail = exception_detail
        self.endTime = end_time

    def to_string(self):
        logger.info(f"执行{self.modulePath}{self.moduleName}的{self.functionName}方法时发生异常")
        logger.info(f"参数信息: {self.parameterInfo}")
        logger.info(f"异常类型: {self.exceptionType}")
        logger.info(f"异常明细:\n{self.exceptionDetail}")


@monitor()
def add_sdk_run_record(exceptionInfo: ExceptionInfo):
    import requests
    headers = {'Connection': 'keep-alive',
               'Content-Type': 'application/json;charset=utf-8', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = f"http://10.80.51.28:8887/msCaseException/add"
    try:
        response = requests.post(url, json.dumps(vars(exceptionInfo)), headers=headers, timeout=30)
        resp_body = json.loads(str(response.content, 'utf-8'))
        return resp_body
    except Exception:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/decorator/exception_handler.py")
        logger.info(traceback.format_exc())
