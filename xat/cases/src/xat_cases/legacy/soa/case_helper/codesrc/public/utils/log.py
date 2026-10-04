#!/usr/bin/python3
# -*- coding=utf-8 -*-
# (C) Copyright Jidu Auto 2023-2023.
# @author: Edison

'''
架构元素：code/public/utils

dependencies:
    python(>=3.5)
'''

import os
import logging


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../../..'))
LOG_PATH = os.path.join(BASE_PATH, 'build_results', 'log')


class MonitorLogger(logging.Logger):
    def __init__(
        self,
        name='soa_logger',
        level=logging.INFO,
        file_path=None,
        format='%(asctime)s - %(levelname)s - %(message)s',
        show_in_terminal=False
    ):
        '''
        @param name:
        @param level:
        @param file_path: 保存位置
        @param format:
        @param show_in_terminal: 是否开启终端打印
        '''
        super().__init__(name, level)
        formatter = logging.Formatter(format)
        if file_path is not None:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

        if show_in_terminal:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.addHandler(stream_handler)

    def __del__(self):
        pass


# 日志对外接口，可以通过 show_in_terminal 参数开启终端打印
logger = MonitorLogger(show_in_terminal=True)


def get_base_path():
    return BASE_PATH
