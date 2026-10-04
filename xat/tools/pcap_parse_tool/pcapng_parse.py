#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : pcapng_parse.py

**********************

------------------------------------------------------------------
@Time    : 2024/9/10 17:35
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import os
import sys
import argparse
from loguru import logger
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket


logger.remove()
logger.add(sys.stdout,
                format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                       "<level>{message}</level>",  # 日志内容
                level="INFO"
                )


def _parse_pcap(file):
    with open(file, 'rb') as fp:
        scanner = FileScanner(fp)
        doip_data_list = []
        for block in scanner:
            if isinstance(block, EnhancedPacket):
                raw_data = block.packet_data.hex()
                if "02fd" in raw_data:
                    doip_data = "02fd" + raw_data.split("02fd")[1]
                    doip_data_list.append(doip_data)

        return doip_data_list


def check_doip_data(doip_data_list, file_path):
    count_flag = {}
    for index, value in enumerate(expect_doip_line_list):
        count_flag[index] = False
        for j in doip_data_list:
            if value[0] in j and value[1] in j:
                count_flag[index] = True
                break
    for k, v in count_flag.items():
        if not v:
            logger.error(f"{file_path} 文件中，没有发现:{expect_doip_line_list[k]},在抓包数据中!!!")
    logger.info(f"==="*20)


def parse_pcapng(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if str(file_path).endswith("pcapng"):
                doip_data_list = _parse_pcap(file_path)
                check_doip_data(doip_data_list, file_path)


if __name__ == "__main__":
    expect_doip_line_list = []
    with open('一键擦除数据.txt', 'r') as f:
        for line in f:
            if line:
                data = line.replace("\n", "").strip()
                data = [i for i in data.split(" ") if i]
                if data:
                    expect_doip_line_list.append([data[0], data[1]])
                    expect_doip_line_list.append([data[0], data[2]])

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir_path', type=str, default=r"", help="指定pcapng路径")
    args = parser.parse_args()
    if not args.dir_path:
        raise AssertionError(f"没有发现指定pcapng目录路径")

    pcapng_path = args.dir_path
    parse_pcapng(pcapng_path)
