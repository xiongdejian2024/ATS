#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :logmanagment.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :logmanagment能力模拟抽象接口,可以提供自定义日志检查分析接口
"""
import time
import re
import collections

from xat_ecu.legacy.common.logger import logger
from xat_ecu.api import CommonLogManagement
from contextlib import contextmanager


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

    @contextmanager
    def check_jetlog_by_same_keywords(self,
                                      log_type,
                                      keywords=None,
                                      log_print=False,
                                      device_name=None,
                                      equal=False,
                                      timeout=60 * 30):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type=log_type,
            # keywords=keywords,
            unexpect_keywords='必定不会出现的关键字',
            log_print=log_print,
            device_name=device_name,
            timeout=timeout
        )
        time.sleep(2)
        try:
            yield
        finally:
            _, ret = self.log_manage.check_log_by_keywords_stop_thread()
            logger.info(ret)
            ck_dict = dict(collections.Counter(keywords))
            for keyword, count in ck_dict.items():
                rst = re.findall(keyword, ret)
                if rst and len(rst) == count if equal else len(rst) >= count:
                    logger.info("关键字：{} 检查通过".format(keyword))
                else:
                    logger.info("关键字：{keyword} 检查失败，正则匹配结果：{rst}".format(keyword=keyword, rst=rst))
                    assert False
