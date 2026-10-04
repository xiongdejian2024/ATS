#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/19 14:19  
@Author: lei.tao
@File: test_digital_security.py
@Software: PyCharm
@Description: 
@Example: 
"""
import allure
import datetime
import os
import sys
import pytest


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.driver.serial_client import get_device_name, BaseSerial
from xat_ecu.legacy.driver.can_listener import *
from xat_ecu.legacy.common.logger import logger


def con_bgm(cmd=None):
    try:
        conn = SSHClient(hostname=ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____BGM_PROCESS_CHECK_TEST_DIGITAL_SECURITY_PY_PASSWORD', ""))
        stdout, stderr = conn.exec_cmd(cmd)
        return stdout
    except SSHFailException as e:
        logger.error(f'The server connect failed with error {e}')
        raise SSHFailException


@allure.feature("SAT")
@allure.story("校验台架的数字安全用例")
class Test_Digital_security(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        os.system("ps -ef|grep -i ssh|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i ssh")
        logger.debug("清除所有ssh进程")
        super().after_class(self, ecu)

    @allure.title("查看目标文件夹中证书安装个数及大小")
    def test01(self):
        """
        校验:证书安装的个数及大小
        """
        # failed = []
        # port = get_device_name()
        # com = BaseSerial(port, baudrate=115200, timeout=0.1)
        # with allure.step(f"查看证书安装的个数"):
        #     com.send(f"ls /app/etc/certificate/ | wc -l", timeout=int(0.5))
        #     msg = com.receive_data().split('\r')[-2]
        #     logger.info("BGM台架证书安装的个数为: {}".format(msg))
        #     allure.attach("{0}".format(msg), f"证书安装的个数")
        #     if int(msg) == 0:
        #         logger.error("没有安装证书，请检查")
        #         assert int(msg) != 0, f"【BGM】证书文件没有安装"
        #     else:
        #         with allure.step(f"查看证书安装的大小"):
        #             for file in ['rootCA.crt', 'ServiceCA.crt', 'OTAService.crt', 'BGMSk.key']:
        #                 com.send(f"ls -l /app/etc/certificate/ | grep {file}" + " | awk '{print $5}' ",
        #                          timeout=int(0.5))
        #                 msg = com.receive_data()
        #                 logger.info("串口输出的内容为: {}".format(msg))
                        
        #                 if "root@imx8dxl-bgm-mars1:~#" in msg:
        #                     allure.attach("证书{0} : {1}".format(file, msg), f"证书安装的大小")
        #                 else:
        #                     allure.attach("证书{}".format(file), f"证书安装失败")
        #                     failed.append(file)
        #     assert len(failed) == 0;f"BGM证书安装失败"
        
        failed = []
        with allure.step(f"查看证书安装的个数"):
            data = con_bgm(f"ls /app/etc/certificate/ | wc -l")
            logger.info("BGM台架证书安装的个数为: {}".format(data))
            allure.attach("{0}".format(data), f"证书安装的个数")
            if int(data) == 0:
                logger.error("没有安装证书，请检查")
                assert int(data) != 0, f"【BGM】证书文件没有安装"
            else:
                with allure.step(f"查看证书安装的大小"):
                    for file in ['rootCA.crt', 'ServiceCA.crt', 'OTAService.crt', 'BGMSk.key']:
                        crt = con_bgm(f"ls -l /app/etc/certificate/ | grep {file}" + " | awk '{print $5}' ")
                        logger.info("证书{0}安装的大小为: {1}".format(file, crt))
                        
                        if crt:
                            allure.attach("证书{0} : {1}".format(file, crt), f"证书安装的大小")
                        else:
                            allure.attach("证书{}安装失败".format(file), f"证书安装情况")
                            failed.append(file)
            assert len(failed) == 0;f"BGM证书安装失败"

    @allure.title("查看BGM的当前时间")
    def test02(self):
        """
        校验:BGM端查看时间是否是当前时间
        """
        # %a星期的简写。如 星期三为Web
        # %A星期的全写。如 星期三为Wednesday
        # %b月份的简写。如4月份为Apr
        # %B月份的全写。如4月份为April
        # %c: 日期时间的字符串表示。（如： 04/07/10 10:43:39）
        # %d: 日在这个月中的天数（是这个月的第几天）
        # %f: 微秒（范围[0,999999]）
        # %H: 小时（24小时制，[0, 23]）
        # %I: 小时（12小时制，[0, 11]）
        # %j: 日在年中的天数 [001,366]（是当年的第几天）
        # %m: 月份（[01,12]）
        # %M: 分钟（[00,59]）
        # %p: AM或者PM
        # %S: 秒（范围为[00,61]，为什么不是[00, 59]，参考python手册~_~）
        # %U: 周在当年的周数当年的第几周），星期天作为周的第一天
        # %w: 今天在这周的天数，范围为[0, 6]，6表示星期天
        # %W: 周在当年的周数（是当年的第几周），星期一作为周的第一天
        # %x: 日期字符串（如：04/07/10）
        # %X: 时间字符串（如：10:43:39）
        # %y: 2个数字表示的年份
        # %Y: 4个数字表示的年份
        # %z: 与utc时间的间隔 （如果是本地时间，返回空字符串）
        # %Z: 时区名称（如果是本地时间，返回空字符串）

        with allure.step(f"查看BGM的时间"):
            data = con_bgm(cmd="date")
            logger.info("BGM输出的内容为: {}".format(data))
            sys_time = datetime.datetime.strptime(data, "%a %b %d %H:%M:%S %Z %Y")
            logger.info("BGM系统时间为: {}".format(sys_time))
            allure.attach("{0}".format(sys_time), f"BGM时间情况")
            logger.info("BGM的当前时间为: {}".format(sys_time + datetime.timedelta(hours=8)))
            
            loc_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info("当前北京时间为: {}".format(loc_time))
            
        assert abs(datetime.datetime.strptime(loc_time, '%Y-%m-%d %H:%M:%S') - (sys_time + datetime.timedelta(hours=8))) < datetime.timedelta(minutes=1), f"【BGM】的时间不是当前系统时间"

    @allure.title("查看BGM与TCAM的联通状况")
    def test03(self):
        """
        校验:从BGM端能否ping通TCAM
        """

        with allure.step(f"查看BGM是否与TCAM联通"):
            data = con_bgm(cmd="ping 172.16.5.31 -c 4")
            logger.info("BGM输出的内容为: {}".format(data))
            allure.attach("{}".format(data), f"BGM与TCAM联通情况")
        assert "4 packets transmitted, 4 received" in data, f"【BGM】与【TCAM】联通失败"

    @allure.title("查看BGM的联网状况")
    def test04(self):
        """
        校验:从BGM端能否ping通 baidu.com
        """

        with allure.step(f"查看BGM是否联网"):
            data = con_bgm(cmd="ping -I eth0.32 www.baidu.com -c 4")
            logger.info("BGM输出的内容为: {}".format(data))
            allure.attach("{}".format(data), f"BGM联网情况")
        assert "4 packets transmitted, 4 received" in data, f"【BGM】联网失败"
