# -*- coding: utf-8 -*-

"""
@File        : utils.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2024/09/04 15:51 PM
@Description : BGM内部以太网相关的接口
@Examples    : example of how to use it
"""
import os
import json
import ctypes
import inspect
from copy import deepcopy


s2s_json = {
    "mcuIpTcp": "172.16.5.2",
    "mpuIpTcp": "172.16.5.1",
    "mcuIpUdp": "172.16.5.2",
    "mpuIpUdp": "172.16.5.1",
    "tcpReqClientPort": 30500,
    "tcpReqServerPort": 30500,
    "tcpResClientPort": 30501,
    "tcpResServerPort": 30501,
    "udpResClientPort": 30502,
    "udpResServerPort": 30502,
    "waitTime": 4,
    "E2ECheckFlag": True,
    "TimeOutCheckFlag": True,
    "FrameCountFlag": True,
    "SyncTCPFlag": True,
    "LogStorageFlag": True,
    "Threads": {
        "ServerStartPool": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "TimerLoop": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "S2sTimer0": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "S2sTimer1": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "S2sParse": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "Internal": {
            "policy": 2,
            "priority": 20,
            "nice": -20
        },
        "S2storage": {
            "policy": 0,
            "priority": 255,
            "nice": 255
        },
        "ReqLoop": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "ResLoop": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "RecLoop": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        },
        "s2s_service": {
            "policy": 2,
            "priority": 20,
            "nice": 255
        }
    }
}
s2s_path = os.path.join(os.path.dirname(__file__), "s2s.json")


def write_s2s_json(new_info: dict):
    """
    为在同级目录写s2s.json写入新内容
    @param new_info: 以键值对形式对标准的s2s.json文件进行update并更新
    """
    tmp_json = deepcopy(s2s_json)
    tmp_json.update(new_info)
    with open(s2s_path, "w") as f:
        f.write(json.dumps(tmp_json) + "\n")


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        pass
        # raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    """杀线程"""
    _async_raise(thread.ident, SystemExit)


def ck_start_value(values, ck_value):
    """校验数据以指定值开始，返回剩余数据"""
    nums = 0
    for i, value in enumerate(values):
        if value == ck_value:
            nums += 1
        else:
            return nums, values[i:]
    else:
        return nums, []


def is_interrupt(values: list, ck_nums: int, idle: int):
    """
    判断是否被打断
    :param values: 列表中信号依次打断
    :param ck_nums: 正常发送帧数(正负偏差1帧可接受)
    :param idle: 有效数据发送后周期发送的idle值
    :return: 当前校验值，校验帧数，剩余校验值
    """
    if len(values) == 1:
        return values.pop(0), [ck_nums - 1, ck_nums, ck_nums + 1], values
    else:
        same_cnt = 1
        while len(values) > 1 and values[0] == values[1]:
            same_cnt += 1
            values.pop(0)
        if same_cnt != 1:  # 有相同值打断，按照最少x+1帧，最多x*n帧
            if len(values) == 1 or values[1] == idle:  # 长度1即后面不会被打断，后面为idle说明也不是打断
                return values.pop(0), list(range(same_cnt + ck_nums - 1, ck_nums * same_cnt)), values
            else:  # 说明后面被打断了
                return values.pop(0), list(range(same_cnt, ck_nums * same_cnt)), values
        else:  # 没有相同值打断
            if values[1] == idle:
                return values.pop(0), [ck_nums - 1, ck_nums, ck_nums + 1], values
            else:
                return values.pop(0), list(range(1, ck_nums)), values
