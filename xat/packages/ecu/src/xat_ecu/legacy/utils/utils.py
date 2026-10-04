#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utils.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/19 1:32
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.

import time
import json
import functools
from datetime import datetime
from functools import reduce
from subprocess import Popen, PIPE, STDOUT
from xat_ecu.legacy.common.logger import logger


def tcpdump_to_file(file_path):
    cmd = f'tcpdump -i any  -w {file_path}.pcap'
    Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    logger.info(f"已运行：{cmd} 命令，抓包开始...")


def kill_tcpdump_process():
    Popen("ps -ef | grep -v grep| grep tcpdump| awk '{print $2}' | xargs kill -9", shell=True, stdout=PIPE, stderr=PIPE)
    logger.info("已结束tcpdump抓包...")


def wait_until_function_return_result(timeout=10, interval=0.5):
    def inner_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return wait_until_success(func, timeout, interval, *args, **kw)

        return wrapper

    return inner_func


def wait_until_success(getter, timeout, interval, *args, **kwargs):
    start_time = datetime.now()
    while True:
        try:
            if args or kwargs:
                result = getter(*args, **kwargs)
            else:
                result = getter()
        except AttributeError as ae:
            raise AssertionError("Invalid keywords.", ae)
        except OSError as oe:
            raise AssertionError("Invalid invocation.", oe)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/utils.py")
            raise e

        if result and result is not None:
            return result

        duration = datetime.now() - start_time
        if duration.seconds >= int(timeout):
            logger.warning(f"在设置的时间内没有收到期望值。")
            return
        time.sleep(float(interval))


class SingleMeta(type):

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super(SingleMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingleMeta, cls).__call__(*args, **kwargs)
        return cls._instance


def json_pretty(json_data, **kwargs):
    if not json_data:
        return ''
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            pass
    if isinstance(json_data, object):
        return json.dumps(
            json_data,
            indent=2,
            sort_keys=False,
            ensure_ascii=False,
            **kwargs)
    return json_data


def struct_pretty(struct_data):
    return json_pretty(struct_data, cls=StructJSONEncoder)


class StructJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            try:
                return obj.decode("utf-8")
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/utils.py")
                return bytes.hex(obj)
        return json.JSONEncoder.default(self, obj)


class CustomIterator(object):
    def __init__(self, end: int, start=0):
        self.start = start
        self.end = end

    def __iter__(self):
        return self

    def set_cursor(self, seq: int):
        self.start = seq

    def __next__(self):
        if self.start < self.end:
            self.start += 1
            return self.start
        else:
            self.start = 0
            return self.start


def get_crc2_data(data):
    crc2_value = 0
    for i in data:
        crc2_value += ((i >> 1) | ((i & 0x1) << 7))
    return crc2_value & 0xff


def get_crc1_data(data):
    return 0xff - reduce(lambda x, y: (x + y) & 0xff, data)


def exec_shell_command(cmd: str, exec_timeout=300, shell=True, ignore_error=False):
    """
    执行shell命令，默认报错不会继续执行
    @ cmd:需要执行的adb命令行
    @ exec_timeout:执行超时时间，默认300s
    @ shell:以shell方式运行，默认True
    @ ignore_error:设置报错后是否继续执行，默认为False即报错后不会继续执行
    """
    p = Popen(
        args=cmd,
        stdin=None,
        stdout=PIPE,
        stderr=STDOUT,
        shell=shell)
    start_time = time.time()
    try:
        while p.poll() is None:
            try:
                line_out = p.stdout.readline().decode('utf-8')
            except UnicodeError:
                try:
                    line_out = p.stdout.readline().decode('gbk')
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/utils.py")
                    logger.warning(f'error stdout with: {e}')
                    line_out = ''
            except BaseException as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/utils.py")
                logger.warning(f'error stdout with: {e}')
                line_out = ''
            if line_out:
                logger.info(line_out)
            if exec_timeout:
                end_time = time.time()
                if end_time - start_time >= exec_timeout:
                    logger.warning('Exec command time out')
                    break

        if p.returncode != 0 and not ignore_error:
            logger.warning(f'Execute command :{cmd} failed! with code:{p.returncode}')
        elif p.returncode != 0 and ignore_error:
            logger.warning(f'Execute command :{cmd} failed! with code:{p.returncode}')
        else:
            logger.info(f'Execute command :{cmd} successful')
    finally:
        p.terminate()
        p.kill()