#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: requests_lib.py
@Time: 2022/6/1 14:03
@Author: lei.tao
@Software: PyCharm
@Description: download package from url
@Examples: 
"""
import os
import sys
from xat_ecu.legacy.common.logger import logger
import requests

project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()


class Downloader(object):
    def __init__(self, url, file_path):
        """
        通过url下载刷写包
        :param url: 远程url地址
        :param file_path: 本地保存地址
        :return: None
        """
        self.url = url
        self.file_path = file_path

    def start(self):
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        logger.info(res_length.headers)
        logger.info(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            logger.info("当前：%d 字节， 总共：%d 字节， 已下载：%2.2f%% " % (temp_size, total_size, 100 * temp_size / total_size))
        else:
            temp_size = 0
            logger.info("总共：%d 字节，开始下载..." % (total_size,))

        headers = {'Range': 'bytes=%d-' % temp_size,
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
        res_left = requests.get(self.url, stream=True, headers=headers)

        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
