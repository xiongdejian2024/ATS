# -*- coding: utf-8 -*-
"""
@File        : decorator.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022-10-23 21:29
@Description : 所有的装饰器存放路径
"""
import os
import sys
from xat_ecu.legacy.common.logger import logger


def information(case_info: dict):
    """
    测试用例装饰器
    :param case_info:
    :return:
    """
    def outer(fun):

        def inner(*args, **kwargs):
            logger.info("jama_id: {}".format(case_info["jama_id"]))
            logger.info("case name: {}".format(case_info["case_name"]))
            logger.info("pre_condition: {}".format(case_info["pre_condition"]))
            logger.info("description: {}".format(case_info["description"]))
            fun(*args, **kwargs)

        return inner

    return outer

