#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :tosun_driver.py
@Time         :2024/12/6 16:55
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""


class ToSunDriver(object):
    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value
