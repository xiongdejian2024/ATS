#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/19 14:21  
@Author: lei.tao
@File: test_rvs.py
@Software: PyCharm
@Description: 
@Example: 
"""
import sys
import allure
import os, time
import pytest
from threading import Thread
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)


@allure.feature("SAT")
@allure.story("校验BGM台架数据上报的RVS用例")
class Test_rvs(object):
    def task1(self):
        os.system("python test_case/gb32960/cpu_loader.py")

    def task2(self):
        os.system("python basic_data_report/Grpc_message.py")

    @allure.title("此用例用来校验杀死之前启动的soa进程")
    def test_01(self):
        cmd = "ps -ef|grep -i soa|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i soa"
        print(cmd)
        os.system(f"{cmd}")
        time.sleep(2)

    @allure.title("验证GB32960数据上报测试")
    def test_02(self):
        Thread(target=self.task1).start()
        time.sleep(85)
        # t.threadLock = False
        # Thread(target=t.task1).join()

        Thread(target=self.task2).start()
        time.sleep(5)
        with open(os.path.join(project_root, "logs", "RVS_result.log"), mode='r') as f:
            assert "3232" in f.read(), f"【BGM】RVS数据上报失败"
