#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :logmanagment.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :logmanagment能力模拟抽象接口,可以提供自定义日志检查分析接口
"""
import time
from contextlib import contextmanager

from xat_ecu.api.interfaces.dp2.interface import CommonLogManagement


class LogManagement(CommonLogManagement):
    @contextmanager
    def check_jetlog_by_keywords(self,
                                 log_type,
                                 keywords=None,
                                 unexpect_keywords=None,
                                 log_print=False,
                                 device_name=None,
                                 timeout=10):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type=log_type,
            keywords=keywords,
            unexpect_keywords=unexpect_keywords,
            log_print=log_print,
            device_name=device_name,
            timeout=timeout
        )
        time.sleep(2)
        try:
            yield
        finally:
            assert self.log_manage.check_log_by_keywords_stop_thread()[0]
