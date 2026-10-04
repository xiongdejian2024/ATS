#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/12/05 09:23
@Author: lei.tao
@File: cdd_parse_tool.py
@Software: PyCharm
@Description:
@Example:
"""
import argparse
import openpyxl
import os
import sys

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import Logger
from scapy.all import *
from cdd_pdu_parser import *

logger = Logger().get_logger(name='cdd_paser')


def check_gap_between_massages(first_timestamp, last_timestamp):
    """
    每帧报文之间的间隙应该小于等于10ms
    """
    error_str = ''
    first = int(last_timestamp.replace(' ', ''), 16)
    last = int(first_timestamp.replace(' ', ''), 16)
    if last - first > 10:
        error_str = f"每帧报文之间的间隙应该小于等于10ms，第一个报文时间戳{first_timestamp}，最后一个报文时间戳{last_timestamp}"
    return error_str


def check_massages_length(data):
    """
    每帧报文的payload长度应小于等于1400 bytes
    """
    error_str = ''
    if len(data) > 1400:
        error_str = f"每帧报文的payload长度应小于等于1400 bytes，该报文的长度为{len(data)}"
    return error_str


def ms_ts_check(ms):
    """
    每帧报文的毫秒时间戳应小于等于1000 ms
    """
    error_str = ''
    ms = int(ms.replace(' ', ''), 16)
    error_str = ""
    if ms > 1000:  # ms should not larger than 1000
        error_str = f"ms time should not large than 1000, actual {ms}"
    return error_str


def frame_length_check(bus_id, f_len):
    """
    每帧报文的长度校验
    """
    error_str = ""
    if int(f_len.replace(' ', ''), 16) == 0:
        error_str = f"frame length error: {f_len}"
    else:
        if int(bus_id, 16) in range(41, 48):  # LIN
            if int(f_len.replace(' ', ''), 16) > 8:  # 暂且认为LIN长度不超过8
                error_str = f"frame length error: {f_len} for LIN: {bus_id}"
        elif int(bus_id, 16) in range(2, 13):  # CAN&CAN FD
            if int(f_len.replace(' ', ''), 16) > 64:
                error_str = f"frame length error: {f_len} for CAN: {bus_id}"
        elif int(bus_id, 16) == 1:  # FlexRay
            if int(f_len.replace(' ', ''), 16) > 32:
                error_str = f"frame length error: {f_len} for FlexRay: {bus_id}"
        else:
            error_str = f"bus_id error: {bus_id}"
    return error_str


def paser_pcap(file):
    packets = rdpcap(file)
    data_list = []
    file_name = file.split('.')[0]
    for data in packets:
        if 'UDP' in data and 'Raw' in data:
            per_data = []
            # print(data.time)
            result = data['Raw'].load.hex()
            # print(result)
            for i in range(0, len(result), 2):
                aa = result[i] + result[i + 1]
                per_data.append(aa)
            check_str = gen_comment(err_str=check_massages_length(per_data))
            if check_str != '':
                logger.error("报文的payload长度应超过1400 bytes")
                exit()

            if per_data[-1] == 'fe':
                data_list.append(per_data)

    logger.info(f"文件{file}解析的数据为{len(data_list)}帧")
    return file_name, data_list


def get_data(r_data, dl):
    data = r_data[:dl]
    raw_data = r_data[dl:]
    return data, raw_data


def create_excel(data, file, sheetname):
    """
    创建excel表格，插入第一帧数据及表头
    :param data: 插入excel的数据
    :param file: 插入的excel名称
    :param sheetname: 插入的sheet名
    """
    result = paser_data(data)
    first_timestamp = result[0][3]
    last_timestamp = result[-1][3]
    # check每帧报文之间的间隙
    check_str = gen_comment(err_str=check_gap_between_massages(first_timestamp, last_timestamp))
    if check_str != '':
        logger.error("每帧报文之间的间隙不应该超过10ms")
        exit()

    # check每帧报文的毫秒时间戳
    for i in range(len(result)):
        timestamp = result[i][3]
        check_str = gen_comment(err_str=ms_ts_check(timestamp))
        if check_str != '':
            logger.error("每帧报文的毫秒时间戳不应该超过1000ms")
            exit()

    # check每帧报文的长度
    for i in range(len(result)):
        bus_id = result[i][1]
        f_len = result[i][4]
        check_str = gen_comment(err_str=frame_length_check(bus_id, f_len))
        if check_str != '':
            logger.error("frame length error")
            exit()

    wb = openpyxl.Workbook()  # 一个实例
    sheet = wb.create_sheet(title=sheetname, index=0)  # 工作簿名称
    header = ('全局时间戳', '总线编号', '报文ID', '毫秒时间戳', '报文长度', '报文原始数据')
    # 插入表头
    for i in range(1, 7):
        sheet.cell(1, i, header[i-1])

    datalist = [[]] + result
    # 插入第一帧数据
    for row in range(2, len(datalist)):  # 行
        for col in range(1, 7):  # 列
            sheet.cell(row, col, str(datalist[row][col-1]))

    wb.save(file)  # 最后一定要保存，否则无效


class CaseParser(object):
    def __init__(self, case_f):
        self.case_f = case_f
        self.workbook = openpyxl.load_workbook(case_f)
        self.sheets = self.workbook.sheetnames

    def max_row(self, sheet_name):
        return self.workbook[sheet_name].max_row


def insert_excel(data, file, sheetname):
    """
    新增第二帧之后的所有数据，不包括表头
    :param data: 插入excel的数据
    :param file: 插入的excel名称
    :param sheetname: 插入的sheet名
    """
    row = CaseParser(file).max_row(sheetname) + 1
    wb = openpyxl.load_workbook(file)
    sheet = wb[sheetname]
    result = paser_data(data)
    first_timestamp = result[0][3]
    last_timestamp = result[-1][3]
    # check每帧报文之间的间隙
    check_str = gen_comment(err_str=check_gap_between_massages(first_timestamp, last_timestamp))
    if check_str != '':
        logger.error("frame gap error")
        exit()

    # check每帧报文的毫秒时间戳
    for i in range(len(result)):
        timestamp = result[i][3]
        check_str = gen_comment(err_str=ms_ts_check(timestamp))
        if check_str != '':
            logger.error("frame ms_ts error")
            exit()

    # check每帧报文的长度
    for i in range(len(result)):
        bus_id = result[i][1]
        f_len = result[i][4]
        check_str = gen_comment(err_str=frame_length_check(bus_id, f_len))
        if check_str != '':
            logger.error("frame length error")
            exit()

    # 插入数据
    i = 0
    for row in range(row, row+len(result)):  # 行
        for col in range(1, 7):  # 列
            sheet.cell(row, col, str(result[i][col-1]))
        i += 1

    wb.save(file)   # 最后进行保存


def paser_data(data):
    """
    解析读取到的pcap包数据
    :param data:
    """
    glo_timestr, raw_data = get_data(data, 6)
    logger.info(f"全局时间戳:{glo_timestr}")
    data_list = []
    try:
        while len(raw_data) > 0:
            result = [' '.join(glo_timestr)]
            bus_id_raw, raw_data = get_data(raw_data, 1)  # bus id是1byte
            bus_id = bus_id_raw[0]

            if int(bus_id, 16) in range(41, 48):  # lin, 报文id为1byte
                logger.info("{}".format("**" * 40))
                logger.info(f'总线编号:{bus_id_raw}')
                result.append(' '.join(bus_id_raw))
                f_id, raw_data = get_data(raw_data, 1)
                logger.info(f'报文ID:{f_id}')
                result.append(' '.join(f_id))
                ms_ts, raw_data = get_data(raw_data, 2)  # ms时间戳 2 byte
                logger.info(f'毫秒时间戳: {ms_ts}')
                result.append(' '.join(ms_ts))
                f_len, raw_data = get_data(raw_data, 1)  # 报文长度 1 byte
                logger.info(f'报文长度: {f_len}')
                result.append(' '.join(f_len))
                f_len = int(f_len[0], 16)
                logger.info(f'即{f_len}个bytes')
                f_data, raw_data = get_data(raw_data, f_len)
                logger.info(f'报文内容:{f_data}')
                result.append(' '.join(f_data))
            elif int(bus_id, 16) in range(2, 13):  # CAN/CANFD, 报文ID为2byte
                logger.info("{}".format("**" * 40))
                logger.info(f'总线编号:{bus_id_raw}')
                result.append(' '.join(bus_id_raw))
                f_id, raw_data = get_data(raw_data, 2)
                logger.info(f'报文ID:{f_id}')
                result.append(' '.join(f_id))
                ms_ts, raw_data = get_data(raw_data, 2)  # ms时间戳 2 byte
                logger.info(f'毫秒时间戳: {ms_ts}')
                result.append(' '.join(ms_ts))
                f_len, raw_data = get_data(raw_data, 1)  # 报文长度 1 byte
                logger.info(f'报文长度: {f_len}')
                result.append(' '.join(f_len))
                f_len = int(f_len[0], 16)
                logger.info(f'即{f_len}个bytes')
                f_data, raw_data = get_data(raw_data, f_len)
                logger.info(f'报文内容:{f_data}')
                result.append(' '.join(f_data))
            elif int(bus_id, 16) == 1:  # FR, 报文id为4byte
                logger.info("{}".format("**" * 40))
                logger.info(f'总线编号:{bus_id_raw}')
                result.append(' '.join(bus_id_raw))
                f_id, raw_data = get_data(raw_data, 4)
                logger.info(f'报文ID:{f_id}')
                result.append(' '.join(f_id))
                ms_ts, raw_data = get_data(raw_data, 2)  # ms时间戳 2 byte
                logger.info(f'毫秒时间戳: {ms_ts}')
                result.append(' '.join(ms_ts))
                f_len, raw_data = get_data(raw_data, 1)  # 报文长度 1 byte
                logger.info(f'报文长度: {f_len}')
                result.append(' '.join(f_len))
                f_len = int(f_len[0], 16)
                logger.info(f'即{f_len}个bytes')
                f_data, raw_data = get_data(raw_data, f_len)
                logger.info(f'报文内容:{f_data}')
                result.append(' '.join(f_data))
            elif int(bus_id, 16) == 254 and len(raw_data) == 0:  # 结束符
                exit('发现结束符fe')
            else:
                logger.error(f"bus_id error {bus_id}!!!")
                exit('bus_id error')
            data_list.append(result)

    except Exception as fe:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/main.py")
        logger.error(str(fe))

    finally:
        return data_list


def main(file_path, result_path):
    """

    :param file_path: pcap文件存储路径
    :param result_path: 生成的excel文件存储路径
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    file_list = os.listdir(file_path)
    logger.info(f"需要解析的文件列表为: {file_list}")
    if len(file_list) == 0:
        logger.error("请先确认pcap包是否存在")
        exit()
    else:
        for file in file_list:
            logger.info("{}".format("==" * 40))
            file_name, data_list = paser_pcap(os.path.join(file_path, file))

            for i in range(len(data_list)):
                if i == 0:
                    create_excel(data=data_list[0], file=f'{os.path.join(result_path, os.path.splitext(file)[0])}.xlsx',
                                 sheetname='报文解析')

                else:
                    time.sleep(0.1)
                    insert_excel(data=data_list[i], file=f'{os.path.join(result_path, os.path.splitext(file)[0])}.xlsx',
                                 sheetname='报文解析')

            logger.info("{}".format("==" * 40))
            logger.info(f"文件{file}解析完成")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CDD data parser from pcap file")
    parser.add_argument('-f', type=str, help='f: pcap file path')
    parser.add_argument('-o', type=str, help='f: xlsx file path')
    args = parser.parse_args()

    main(file_path=args.f, result_path=args.o)
