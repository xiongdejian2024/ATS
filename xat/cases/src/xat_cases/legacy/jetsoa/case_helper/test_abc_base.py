# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""
import re
import os
import sys
from threading import Thread
import time
project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase


def cmd_root():
    cmd="ps -ef|grep -i defunct|grep -v grep|awk '{printf $3\"\\n\"}'|xargs kill -9;ps -ef|grep -i defunct"
    time.sleep(20)
    print(f"执行命令：{cmd}")
    data = os.Popen(cmd).read()
    print(f"执行结果：{data}")



class TestABCBase(CommonABCTestBase):

    def after_class_teardown(self, ecu):
        super().after_class_teardown(self, ecu)
        t1 = Thread(target=cmd_root, args=(),daemon=True)
        t1.start()
        # t1.join()