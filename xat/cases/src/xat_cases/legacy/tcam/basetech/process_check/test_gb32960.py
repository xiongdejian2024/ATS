#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/19 14:05  
@Author: lei.tao
@File: test_gb32960.py
@Software: PyCharm
@Description: 
@Example: 
"""
import allure
import os
import time
import sys
from threading import Thread

import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)


@allure.feature("SAT")
@allure.story("TCAM台架的数据上报GB32960模块测试")
class Test_GB32960(object):

    def task1(self):
        os.system("\npython GB32960/GB32960_Data_receiver.py")

    def task2(self):
        os.system(". venv/bin/activate")
        os.system("pytest -vs -p no:waring test_case/gb32960/test_gb32960_tcam.py")

    @allure.title("此用例用来校验并杀死之前启动的进程")
    def test_01(self):
        cmd = "\nps -ef|grep -i soa|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i soa"
        print(cmd)
        os.system(f"{cmd}")
        time.sleep(2)
        cmd = "ps -ef|grep -i GB|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i GB"
        print(cmd)
        os.system(f"{cmd}")
        time.sleep(2)

    @allure.title("验证GB32960数据上报测试")
    def test_02(self):
        with allure.step(f"查看GB32960数据上报是否成功"):
            Thread(target=self.task1).start()
            Thread(target=self.task2).start()
            time.sleep(320)
            allure.attach.file("{0}".format(os.path.join(project_root, "logs", "GB32960_result.log")), f"GB32960数据上报情况", allure.attachment_type.TEXT)
        with open(os.path.join(project_root, "logs", "GB32960_result.log"), mode='r') as f:
            assert "3232" in f.read(), f"【TCAM】GB32960数据上报失败"

