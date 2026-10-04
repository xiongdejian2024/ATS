#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :data_handle.py
@Time         :2023/10/31 10:00
@Author       :hui.zhao@jiduauto.com
@Description  :数据数据，包括总线数据,文本数据,excel数据等等
"""

import os
import time
import subprocess
import re
from time import sleep
from xat_ecu import reporting as allure
import csv
import math
import random
import datetime
import yaml
from functools import wraps
from typing import List, Union, Dict, Tuple
from xat_ecu.api.constants.common import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.common.file_handle import *
from xat_ecu.legacy.common import exception_error
# 项目固定在sat 下
sat_abspath = os.path.dirname(os.path.realpath(__file__)).split("sat")[0] + "sat"
# work dir 固定是在 sat/xat_cases/legacy/xxx 下
workdir_abspath = os.getcwd()


def get_signal_times_interval(ori_data, check_signal_value):
    """
    功能：检测信号的值是否一直为某个值。
    @param check_signal_parameter_tuple:参数类型为元组，要检测的信号以及值，例如：("backbonefr.CemBackBoneFr07",'WipgInfoWipgSpdInfo', 0,"timeout=5"),
        表示检测信号WipgInfoWipgSpdInfo再5秒钟内是否一直为0
    :return:
    """
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
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/common/common.py")
        time_interval_max = 0
        time_interval_min = 0
    return (signal_account_last, time_interval_max, time_interval_min)


def check_all_value_is(ori_data, check_value):
    if check_value == "any":
        logger.info("不需要check具体的信号值")
        for i in range(len(ori_data)):
            if isinstance(ori_data[i][0],int) != True:
                logger.info(f"-------------------------->获取的信号值为{ori_data[i][0]},不是整型,判断失败")
                return False
        return True
    else:
        for i in range(len(ori_data)):
            if ori_data[i][0] != check_value:
                logger.info(f"-------------------------->获取的信号值为{ori_data[i][0]},期望的所有的信号值为{check_value},判断失败")
                return False
        return True

def check_signal_value_exist(ori_data, check_value):
    for i in range(len(ori_data)):
        if ori_data[i][0] == check_value:
            logger.info(f"-------------------------->信号值为{check_value}存在")
            return True
    return False

def calculate_signal_times_and_duration(ori_data):
    signal_account = len(ori_data)
    timestamp_first = ori_data[0][1]
    timestamp_last = ori_data[signal_account - 1][1]
    duration = timestamp_last - timestamp_first
    return (signal_account, duration)

def check_signal_num(ori_data, signal_value = 0):
    """
    检查获取到的数据中连续信号值相等的个数
    """
    num = 0
    timestamp_first = 0
    for signal_value_result, timestamp in ori_data:
        if signal_value == signal_value_result:
            if num == 0:
                timestamp_first = timestamp
            num += 1
        elif signal_value_result != signal_value_result and num != 0:
            return num, timestamp_first
    return num, timestamp_first



def parse_excel_to_signal_routing_csv(excel_path, csv_path):
    '''
    把 信号路由的excel 表处理成需要的csv 文件
    @param self:
    @param excel_path: 原表路径
    @param csv_path: 保存的csv 文件路径
    @return:
    '''
    # 读取excel文件
    import xlrd
    t1 = time.time()
    workbook = xlrd.open_workbook(excel_path)
    logger.info(f"解析excel 表耗时{time.time() - t1}")
    table = workbook.sheet_by_name('Matrix')
    header_list = [item.strip().replace(" ", "") for item in table.row_values(0)]
    header = []
    for item in header_list:
        if "FrameID" in item:
            header.append("FrameID")
        elif "FrameRate" in item:
            header.append("FrameRate")
        else:
            header.append(item)
    # 经过bgm的 路由信号
    data_info_dict = {
        # "ALM10Flt": {
        #     "TX": {},
        #     "GW": [{}, {}]
        # }
    }
    # 存放crc 的信号名字
    chks_sig_set = set()
    # 存放 counter 的信号名字
    cntr_sig_set = set()
    # 便利该表，使用nrows，和ncols代表当前表的有效行列数。
    for row in range(1, table.nrows):
        row_data = [str(item) for item in table.row_values(row)]
        data_info = dict(zip(header, row_data))
        sig_name = data_info.get("Sig")
        # 判断是不是带crc 或者counter
        if sig_name.endswith("Chks"):
            chks_sig_set.add(sig_name[:-4])
        if sig_name.endswith("Cntr"):
            cntr_sig_set.add(sig_name[:-4])
        tx_type = data_info.get("TxType")
        tx_com_ecu = data_info.get("TxComEcu")
        # 过滤 bgm 发送的，不是路由的信号
        if tx_type.lower() == 'tx' and tx_com_ecu.lower() == "bgm":
            continue
        # 过滤非bgm 路由的信号
        if tx_type.lower() == 'gw' and tx_com_ecu.lower() != "bgm":
            continue
        if sig_name in data_info_dict:
            if tx_type in data_info_dict[sig_name]:
                data_info_dict[sig_name][tx_type].append(data_info)
            else:
                data_info_dict[sig_name][tx_type] = [data_info]
        else:
            data_info_dict[sig_name] = {}
            data_info_dict[sig_name][tx_type] = [data_info]
    csv_header = [
        'SignalName',
        'Tx_BusChannel',
        'Tx_ECUName',
        'Tx_MessageName',
        'Tx_MessageID',
        'Tx_MessageCyclic',
        'EnableUB', 'crc', "counter",
        'Rx_BusChannel',
        'Rx_ECUName',
        'Rx_MessageName',
        'Rx_MessageID',
        'Rx_MessageCyclic',
        "Len",
        "repeat",
    ]
    # 写入 csv 表
    try:
        with open(csv_path, "w", newline='') as csv_f:
            csv_writer = csv.writer(csv_f)
            # 写入 表头
            csv_writer.writerow(csv_header)
            for signal_name, value_info in data_info_dict.items():
                # print(value_info)
                send_item_list = value_info.get("Tx")
                if send_item_list is None:
                    continue
                recv_item_info = value_info.get("Gw")
                if recv_item_info is None:
                    continue
                writer_data = []
                writer_data.append(signal_name)

                send_item = send_item_list[0]

                Tx_BusChannel = send_item['Bus']
                writer_data.append(Tx_BusChannel)

                Tx_ECUName = send_item['TxEcu']
                writer_data.append(Tx_ECUName)

                Tx_MessageName = send_item['Frame']
                writer_data.append(Tx_MessageName)

                Tx_MessageID = str(send_item['FrameID'])
                Tx_MessageID = Tx_MessageID.replace("-", "=")
                writer_data.append(Tx_MessageID)

                Tx_MessageCyclic = str(send_item['FrameRate']).replace(",", "").replace("，", "")

                if "EventTriggered".lower() in Tx_MessageCyclic.lower():
                    Tx_MessageCyclic = Tx_MessageCyclic
                elif "/" in Tx_MessageCyclic:
                    Tx_MessageCyclic = [
                        int(float(item) / 1000) for item in Tx_MessageCyclic.split("/")
                    ]
                else:
                    Tx_MessageCyclic = int(float(Tx_MessageCyclic) / 1000)
                writer_data.append(Tx_MessageCyclic)

                EnableUB = str(send_item['SigUB']).strip()
                writer_data.append(EnableUB)
                # 判断带不带 crc
                crc = ""
                for name in chks_sig_set:
                    if name in signal_name:
                        crc = True
                        break
                writer_data.append(crc)
                # 判断带不带counter
                counter = ''
                for name in cntr_sig_set:
                    if name in signal_name:
                        counter = True
                        break
                writer_data.append(counter)

                #
                recv_list = set()
                for recv_item in recv_item_info:
                    recv_data_list = []
                    Rx_BusChannel = recv_item['Bus']
                    recv_data_list.append(Rx_BusChannel)

                    Rx_ECUName = recv_item['RxEcu']
                    recv_data_list.append(Rx_ECUName)
                    if Rx_ECUName.lower() == "S2SReceiver".lower():
                        continue

                    Rx_MessageName = recv_item['Frame']
                    recv_data_list.append(Rx_MessageName)

                    Rx_MessageID = str(recv_item['FrameID'])
                    Rx_MessageID = Rx_MessageID.replace("-", "=")
                    recv_data_list.append(Rx_MessageID)
                    # Rx_MessageCyclic = recv_item['FrameRate']
                    # recv_data_list.append(Rx_MessageCyclic)
                    Rx_MessageCyclic = str(recv_item['FrameRate']).replace(",", "").replace("，", "")

                    if "EventTriggered".lower() in Rx_MessageCyclic.lower():
                        Rx_MessageCyclic = Rx_MessageCyclic
                    elif "/" in Rx_MessageCyclic:
                        Rx_MessageCyclic = [
                            int(float(item) / 1000) for item in Rx_MessageCyclic.split("/")
                        ]
                    else:
                        Rx_MessageCyclic = int(float(Rx_MessageCyclic) / 1000)
                    recv_data_list.append(Rx_MessageCyclic)
                    #
                    sig_len = recv_item['Len']
                    recv_data_list.append(sig_len)
                    # 标记重复的
                    # 接收通道和id 都一样的 算重复
                    temp = (Rx_BusChannel, Rx_MessageID)
                    if temp in recv_list:
                        repeat = '1'
                    else:
                        repeat = '0'
                    recv_list.add(temp)

                    recv_data_list.append(repeat)

                    datd_list = writer_data + recv_data_list
                    csv_writer.writerow(datd_list)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/common/common.py")
        string_log = f"生成 csv 失败》》{str(e)}"
        logger.error(string_log)
        # 删除csv 文件 必须执行的
        os.system(f"rm -rf {csv_path}")
        assert 0, string_log
    return csv_path


def read_signal_routing_info(path=None, select_cond='cycle'):
    '''
    读取信号路由的相关信息
    @param path: csv 文件路径
    @param select_cond: 根据条件筛选 ["cycle", "event", "ub", "crc", "counter"]
    @return: 返回列表
    '''
    # csv_header = [
    #     'SignalName',
    #     'Tx_BusChannel',
    #     'Tx_ECUName',
    #     'Tx_MessageName',
    #     'Tx_MessageID',
    #     'Tx_MessageCyclic',
    #     'EnableUB', 'crc','counter',
    #     'Rx_BusChannel',
    #     'Rx_ECUName',
    #     'Rx_MessageName',
    #     'Rx_MessageID',
    #     'Rx_MessageCyclic',
    #     "Len",
    #     "repeat",
    # ]
    condition = ["cycle", "event", "ub", "crc", "counter"]

    select_cond_info = str(select_cond).strip().lower()
    if select_cond_info not in condition:
        assert 0, f"参数不对，select_cond 可以选的有{condition}"
    logger.info(f"过滤数据 select_cond={select_cond_info} ")
    new_dict = dict(zip(condition, [[], [], [], [], []]))
    with open(path, 'r') as file:
        csv_data = csv.reader(file)
        csv_data_list = list(csv_data)
        header = csv_data_list[0]
        for row in csv_data_list[1:]:
            dic = dict(zip(header, row))
            # 重复的不执行
            if int(dic["repeat"]):
                continue
            if dic["SignalName"].endswith('Chks') or dic["SignalName"].endswith('Cntr'):
                continue

            item_cycle = dic["Tx_MessageCyclic"]
            item_ub = dic["EnableUB"]
            item_crc = dic.get("crc")
            item_counter = dic.get("counter")
            # 根据周期分类
            if str(item_cycle).lower() == "EventTriggered".lower():
                new_dict["event"].append(dic)
            else:
                new_dict["cycle"].append(dic)
            # 根据ub 分类
            if str(item_ub).strip():
                new_dict["ub"].append(dic)

            # 根据 crc 分类
            if str(item_crc).strip():
                new_dict["crc"].append(dic)

            # 根据 conter 分类
            if str(item_counter).strip():
                new_dict["counter"].append(dic)

    return new_dict.get(select_cond_info)


def log_and_allure_step(log_string: str, level=LogLevel.INFO):
    '''
    打印日志，并写allure 步骤
    @param log_string:
    @param level:
    @return:
    '''
    with allure.step(log_string):
        if level == LogLevel.INFO:
            logger.info(log_string)
        elif level == LogLevel.DEBUG:
            logger.debug(log_string)
        elif level == LogLevel.WARNING:
            logger.warning(log_string)
        elif level == LogLevel.ERROR:
            logger.error(log_string)
        elif level == LogLevel.CRITICAL:
            logger.critical(log_string)
        else:
            logger.info(log_string)


def crc8(datas: List[int]):
    """
    计算数据的CRC8校验码，
    :param datas:
    :return:
    """
    length = len(datas)
    crc = 0xAA
    for i in range(length):
        crc = (crc ^ datas[i]) & 0xFF  # 其余的均将上次的CRC8结果与本次数据异或
        poly = 0x07  # 多项式x^8 + x^2 + x^1 + 1，即0x107，（根据原理）省略了最高位1而得0x07
        for _ in range(8):
            if ((crc & 0x80) >> 7) == 1:  # 判断最高位是否为1，如果是需要异或，否则仅左移
                crc = (crc << 1) ^ poly
            else:
                crc = (crc << 1)
        crc = crc & 0xFF  # 再计算CRC8
    return crc & 0xFF

def get_current_time_delayed_timestamp(delay_seconds: int = 300, ignore_seconds: bool=True):
    """
    获取当前时间 + （delay_seconds秒）的时间戳并返回
    :param delay_seconds: 延时时间，单位：秒
    :param ignore_seconds: 获取当前时间时是否忽略秒，默认忽略秒
    :return: int类型的时间戳
    """
    current_time = datetime.datetime.now()
    new_time = (current_time + datetime.timedelta(seconds=delay_seconds)).timestamp()
    new_timestamp = int(new_time) - int(new_time) % 60 if ignore_seconds else int(new_time)
    return new_timestamp

def dealwithDID(did:[str,int]):
    if isinstance(did,int):
        did_str = format(did,'#06X')[2:]
    elif isinstance(did,str):
        if did.startswith("0x") or did.startswith("0X"):
            did_str = did[2:]
        else:
            did_str = did
    return did_str

def transferDTCtoBytes(dtc_str:str):
    hex_array = [int(dtc_str[i:i+2], 16) for i in range(0, len(dtc_str), 2)]
    return hex_array


def retry_on_failure(max_retry_count: int = -1, delay: int = 2):
    """
    函数失败重试装饰器
    :param max_retry_count: 函数最大失败重试次数，默认-1，即不限制最大失败重试次数
                            当max_retry_count小于0时，不限制最大失败重试次数
                            当max_retry_count大于等于0时，函数失败重试次数最多为max_retry_count次
    :param delay: 重试间隔时间 默认2s
    :return: func result or None
    """

    def _retry_on_failure(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if max_retry_count < 0:
                while True:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/common/common.py")
                        logger.error(f"函数{func.__name__}执行报错：{e}，重新执行！")
                        time.sleep(delay)
            else:
                for retry_count in range(max_retry_count):
                    logger.info(f"execute count {retry_count + 1}")
                    try:
                        task_result = func(*args, **kwargs)
                        return task_result
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/common/common.py")
                        logger.error(f"函数{func.__name__}执行报错：{e}，重新执行！")
                        time.sleep(delay)
        return wrapper
    return _retry_on_failure

def set_bench_vlan9_ip(target_ip):
    '''
    设置台架vlan9 ip为target_ip
    :param target_ip:目标id
    :return:
    '''
    get_vlan9_cmd = f"ip addr show label eth0.9"
    pi = subprocess.Popen(get_vlan9_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read()
    bench_vlan9_ip = re.findall(r'inet (.*?)/24', stdout)[0].strip()
    if bench_vlan9_ip == target_ip:
        logger.info(f"bench vlan9  is already {target_ip}, No need to set")
    else:
        set_vlan9_cmd = f"ip addr flush dev eth0.9;ip addr add {target_ip}/24 dev eth0.9;ifconfig eth0.9 up;ifconfig eth0.9 hw ether 02:00:00:00:10:21"
        pi = subprocess.Popen(set_vlan9_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        stdout = pi.stdout.read()
        if not stdout:
            logger.info(f"set vlan9 ip：{target_ip} success")
        else:
            logger.error(f"set vlan9 ip：{target_ip} fail，error message: {stdout}")

def start_process(cmd, waittime=0.5):
    """
    启动进程，并等待进程结束
    
    Args:
        cmd (str): 命令行
        waittime (float, optional): 启动后等待时间，单位：秒，默认为0.5秒
    
    Returns:
        subprocess.Popen: 进程对象
    
    Raises:
        exception_error.CmdExecuteError: 当cmd执行失败时抛出异常
    
    """
    logger.info(f"start process {cmd}")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    time.sleep(waittime)
    if not p.returncode:
        logger.info(f"=======================  cmd start success ======================")
    else:
        err_msg = f"cmd初始化失败，原因是:{p.stdout.read()}"
        p.terminate()
        logger.error(err_msg)
        raise exception_error.CmdExecuteError(err_msg)
    return p
    
def stop_process(process_obj, waittime=1):
    """
    终止进程，并等待进程结束
    
    Args:
        process_obj (subprocess.Process): 进程对象
        waittime (int, optional): 终止后等待时间，单位：秒。默认为1。
    
    Returns:
        None
    
    Raises:
        exception_error.CmdExecuteError: 如果进程终止失败则抛出此异常
    """
    logger.info(f"stop process {process_obj}")
    exitcode = process_obj.poll()
    if exitcode is None:
        process_obj.terminate()
    process_obj.wait(timeout=waittime)  # 设置超时时间，避免无限等待
    if process_obj.poll() is None:  # 如果进程仍在运行
        process_obj.kill()  # 强制杀死进程
        logger.info(f"======================= 强制去杀死进程 ======================")


def data_field_to_dict(str_data):
    pattern = r'(\w+)=([^,\[\]]+)|(\w+)=\[([^\]]+)\]'
    matches = re.findall(pattern, str_data.replace('{', '').replace('}', '').replace(',', ', ').replace(' ', ''))
    # 创建一个空字典来存储结果
    result_dict = {}
    # 遍历匹配项，并构建字典
    for match in matches:
        key = match[0] or match[2]
        if key:
            if match[1]:  # 如果值不是列表
                result_dict[key] = match[1]
            else:  # 如果值是列表
                # 将列表的字符串转换为实际的列表（这里假设列表中的元素都是字符串）
                result_dict[key] = match[3].split(',')
    return result_dict


def check_gb_data_extremumData(gb_data_list, warning_level, warning_list):
    """
    检查GB数据内的各个字段内容是否正确
    """
    for data in gb_data_list:
        warning_data = data_field_to_dict(data['extremumData'])
        logger.info(f'解析的warning数据：{warning_data}')
        # 1： 检查报警等级
        assert warning_data.get('最高报警等级') == str(warning_level), f"检查的最高报警等级错误, 预期：{warning_level}, 实际：{warning_data.get('最高报警等级')}"
        # 2： 检查报警列表
        
        # 实际warning列表
        actual_warning_list = warning_data.get('通用报警标志',[])
        if len(actual_warning_list) == 0:
            assert False, f'实际获取的警告列表为空，actual_warning_list：{actual_warning_list}'
        actual_warning_str,actual_warning_list = actual_warning_list[0], actual_warning_list[1:]
        actual_warning_set = set(actual_warning_list)  
        warning_set = set(warning_list) 
        assert warning_set == actual_warning_set
        assert len(warning_list) == len(actual_warning_set)
        assert len(warning_list) == actual_warning_str.count('1')

def get_signals_info_and_send_with_time(excel_path, sheet_name, ids=False):
    """
    从指定Excel表格中读取信号信息并发送，同时记录发送时间。
    
    Args:
        excel_path (str): Excel文件的路径。
        sheet_name (str): Excel文件中要读取的工作表名称。
        ids (bool, optional): 是否仅返回测试用例ID列表。默认为False，表示返回发送信号后的测试结果。
    
    Returns:
        Union[List[int], List[List[Any]]]:
            - 当ids为True时，返回一个包含测试用例ID的列表。
            - 当ids为False时，返回一个列表，每个元素是一个包含测试用例详细信息的列表，
                其结构为[case_id, jama_id, channel_id, message_id, message_name, signal_name_alias, signal_value]。
    
    """
    import xlrd
    bus_name_dict = {
                        1: "backbonefr",
                        2: "infoanfd",
                        3: "adcanfd",
                        4: "propulsioncan",
                        5: "chassiscan1",
                        6: "chassiscan2",
                        7: "passivesafetycan",
                        8: "connectivitycanfd",
                        9: "bodycan",
                        10: "bodyexposedcanfd",
                        41: "cem_lin1",
                        42: "cem_lin2",
                        43: "cem_lin3",
                        44: "cem_lin4",
                        45: "cem_lin5",
                        46: "cem_lin6",
                        47: "cem_lin7",
                    }
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/mining/data_drive"
    excel_path = os.path.join(parent_dir, excel_path)
    print(excel_path)
    wb1 = xlrd.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    signals_info = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue
        jama_id = sheet1.cell_value(j1, 1)  # 获取 “jama_id”
        if isinstance(jama_id, float):
            jama_id = int(jama_id)
        signal_name = sheet1.cell_value(j1, 2) if len(sheet1.cell_value(j1, 2)) > 0 else ""  # 获取 “信号名称”
        signal_name_alias = sheet1.cell_value(j1, 3) if len(sheet1.cell_value(j1, 3)) > 0 else signal_name
        if len(signal_name_alias) == 0:
            continue

        channel_id = sheet1.cell_value(j1, 5)   # 获取channel_id
        if isinstance(channel_id, float):
            channel_id = int(channel_id)
        if isinstance(channel_id, int):
            channel_id =  bus_name_dict.get(channel_id, "unknown_bus_name")
            if not channel_id:
                continue
        else:
            continue
        message_id = sheet1.cell_value(j1, 6) if len(sheet1.cell_value(j1, 6)) > 0 else ""  # 获取 “message_id”
        if len(message_id) == 0:
            continue
        message_name = sheet1.cell_value(j1, 9) if len(sheet1.cell_value(j1, 9)) > 0 else ""  # 获取 “message_name”
        tx_node = sheet1.cell_value(j1, 10) if len(sheet1.cell_value(j1, 10)) > 0 else ""  # 获取 “tx_node”
        if len(tx_node) == 0 or tx_node.strip().upper() == 'BGM':
            continue
        signal_value = sheet1.cell_value(j1, 11)
        if not isinstance(signal_value, float):
            continue
        try:
            signal_value = float(signal_value)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/common/common.py")
            continue

        if ids:
            id_list.append(int(case_id))
        else:
            test_case = [case_id, jama_id, channel_id, message_id, message_name, signal_name_alias, signal_value]
            signals_info.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"数据埋点下，信号用例个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return signals_info
    
def get_skip_ecu_list(vin):
    with open('../bgm/config/SOA_QA_Vehicle.yaml', 'r') as f:
        conf = yaml.safe_load(f)
    skip_ecu_list = conf[vin]['faulty_ecu']
    logger.info(skip_ecu_list)
    return skip_ecu_list

def next_occurrence_timestamp(time_str):
    """
    计算距离当前时间最近的指定时间（格式为"HH:MM"）的秒级时间戳（UNIX时间戳）

    参数:
    time_str (str): 时间字符串，格式为"HH:MM"

    返回:
    int: 距离当前时间最近的指定时间的UNIX时间戳
    """
    # 获取当前时间
    now = datetime.datetime.now()

    # 将时间字符串转换为时间对象
    target_hour, target_minute = map(int, time_str.split(':'))
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    # 如果目标时间已经过了今天，则设置为明天的目标时间
    if target_time <= now:
        target_time += datetime.timedelta(days=1)

    # 返回目标时间的UNIX时间戳
    return int(target_time.timestamp())

def get_timestamp_after_minutes(minutes, current_time=None):
    # 解析输入字符串，获取分钟数
    # 获取当前时间
    if not current_time:
        current_time = datetime.datetime.now()
    elif isinstance(current_time, int):
        current_time = datetime.datetime.fromtimestamp(current_time)
    # 计算至少这么多分钟后的时间
    future_time = current_time + datetime.timedelta(minutes=minutes)

    # 向上取整到最近的分钟
    rounded_future_time = future_time.replace(second=0, microsecond=0)

    # 如果当前时间的秒数不为0，则需要再加一分钟以确保是整分
    if current_time.second > 0 or current_time.microsecond > 0:
        rounded_future_time += datetime.timedelta(minutes=1)

    # 转换为时间戳（秒）
    timestamp = int(rounded_future_time.timestamp())

    return timestamp