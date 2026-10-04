# -*- coding: utf-8 -*-
"""
@File        : data_handle.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/06 00:30
@Description :
@Examples    :
"""


def int_to_2_bytes_list(int_data):
    # such as    386 ---->> [0x01, 0x82]
    bytes_list = [int_data >> 8] + [int_data & 0xFF]
    return bytes_list

def int_to_4_bytes_list(int_data):
    # such as    386 ---->> [0x01, 0x82]
    bytes_list = [(int_data >> 24) & 0xFF] + [(int_data >> 16) & 0xFF] + [(int_data >> 8) & 0xFF] + [int_data & 0xFF]
    return bytes_list


def get_signal_times_interval(ori_data, check_signal_value):
    signal_account = 0
    signal_account_last = 0
    time_interval = []
    time_interval_last = []
    for i in range(len(ori_data)):
        if ori_data[i][0] == check_signal_value:
            signal_account = signal_account + 1
            if signal_account > 1:
                time_interval.append(ori_data[i][1] - ori_data[i - 1][1])
        else:
            if signal_account >= signal_account_last:
                signal_account_last = signal_account
                time_interval_last = time_interval
                signal_account = 0
                time_interval = []
            else:
                signal_account = 0
                time_interval = []

    try:
        time_interval_max = max(time_interval_last)
        time_interval_min = min(time_interval_last)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/data_handle.py")
        time_interval_max = 0
        time_interval_min = 0
    return (signal_account_last, time_interval_max, time_interval_min)


def check_all_value_is(ori_data, check_value):
    for i in range(len(ori_data)):
        if ori_data[i][0] != check_value:
            return False
    return True

def calculate_signal_times_and_duration(ori_data):
    signal_account = len(ori_data)
    timestamp_first = ori_data[0][1]
    timestamp_last = ori_data[signal_account-1][1]
    duration = timestamp_last - timestamp_first
    return(signal_account,duration)