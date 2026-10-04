# -*- coding: utf-8 -*-
"""
@File        : time_handle.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/05 16:00
@Description :
@Examples    :
"""

import os
import time
from time import sleep
import datetime


def get_6_list_datetime_and_current_time():
    '''
    # :return1  list_datatime 全局时间戳：年（1byte，只表示年份的后两位，如2022的22；） 月（1byte) 日（1byte) 时（1byte) 分（1byte) 秒（1byte)
    # :return2  start_time    时间戳
    # run result print:
    # start_time: 1649173493.0166256
    # localtime: time.struct_time(tm_year=2022, tm_mon=4, tm_mday=5, tm_hour=23, tm_min=44, tm_sec=53, tm_wday=1, tm_yday=95, tm_isdst=0)
    # list_datatime: [22, 4, 5, 23, 44, 53]
    '''

    start_time = time.time()
    localtime = time.localtime(start_time)
    year = localtime.tm_year - 2000
    mon = localtime.tm_mon
    mday = localtime.tm_mday
    hour = localtime.tm_hour
    min = localtime.tm_min
    sec = localtime.tm_sec
    list_datatime = [year, mon, mday, hour, min, sec]

    return list_datatime, start_time


def get_time_str_now():
    '''
    # return :  str   such as  2022_10_31_23_43_01
    '''
    date_time = datetime.datetime.now()
    # time_str = date_time.strftime(f"%Y_%m_%d_%H_%M_%S_%f")
    time_str = date_time.strftime(f"%Y_%m_%d_%H_%M_%S")
    return time_str


# ---------------------------  不通用  -------------------------------------------
def get_time_str_year_month():
    '''
    # return :  str   such as  202304
    '''
    date_time = datetime.datetime.now()
    time_str = date_time.strftime(f"%Y%m")

    return time_str


def get_time_str_year_month_day():
    '''
    # return :  str   such as  20230405
    '''
    date_time = datetime.datetime.now()
    time_str = date_time.strftime(f"%Y%m%d")

    return time_str


if __name__ == "__main__":
    timestr = get_time_str_year_month()
    print(timestr)
