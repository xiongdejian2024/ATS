#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/19 14:09  
@Author: lei.tao
@File: test_digital_security.py
@Software: PyCharm
@Description: 数字安全冒烟用例
@Example: 
"""

import allure
import os
import sys
import pytest
import time
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pexpect
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.common.logger import logger


def con_tcam(cmd, timeout=None):
    try:
        args = f"ssh root@172.16.5.31 {cmd}"
        logger.info("执行命令{}".format(cmd))
        root = pexpect.spawn(args)
        if root.expect('password:') == 0:
            root.sendline('oelinux123')
            time.sleep(1)
        if timeout:
            time.sleep(timeout)
            root.sendcontrol('c')

        out = root.readlines()
        data = []
        for i in out:
            data.append(i.decode())
        return ''.join(data)
    except SSHFailException as e:
        logger.error(f'The server connect failed with error {e}')
        raise SSHFailException


@allure.feature("SAT")
@allure.story("TCAM台架的数字安全证书测试")
class Test_time(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        os.system("ps -ef|grep -i ssh|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i ssh")
        logger.debug("清除所有ssh进程")
        super().after_class(self, ecu)

    @allure.title("查看TCAM是否联网")
    def test01(self):
        """
        校验:TCAM能否联网
        """
        with allure.step(f"查看TCAM能否ping通百度"):
            res = con_tcam(cmd="ping baidu.com -c 4")
            print(res)
            allure.attach("{0}".format(res), f"TCAM联网情况")
        assert "4 packets transmitted, 4 received, 0% packet loss" in res, f"【TCAM】不能联网"


    @allure.title("查看TCAM是否连通BGM")
    def test02(self):
        """
        校验:TCAM能否ping通BGM
        """
   
        with allure.step(f"查看TCAM能否ping通BGM"):
            res = con_tcam(cmd="ping 172.16.5.1 -c 4")
            print(res)
            allure.attach("{0}".format(res), f"TCAM与BGM联通情况")
        assert "4 packets transmitted, 4 received, 0% packet loss" in res, f"【TCAM】与【BGM】连通失败"


    # @allure.title("查看TCAM是否连通后台")
    # def test03(self):
    #     """
    #     校验:TCAM能否连通后台
    #     """
    #     with allure.step(f"删除TCAM中v2trouter.log文件内容"):
    #         con_tcam(cmd="rm /mnt/sdcard/log/jetlog_messages")
    #     with allure.step(f"等待150s后查看jetlog_messages文件"):
    #         time.sleep(150)
    #     with allure.step(f"查看两分钟内TCAM是否有连通后台标志"):
    #         res = con_tcam(cmd="cat /mnt/sdcard/log/jetlog_messages | grep v2t | grep MQTT")
    #         print(res)
    #         allure.attach("{0}".format(res), f"TCAM连接后台情况")
    #     assert "MQTT Server status is connected" in res, f"【TCAM】连接后台失败"
