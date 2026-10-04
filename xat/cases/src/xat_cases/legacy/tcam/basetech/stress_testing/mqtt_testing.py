#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/12/25 13:23
@Author: lei.tao
@File: mqtt_testing.py
@Software: PyCharm
@Description: 车云链路压力测试
@Example:
"""

import os
import sys
import datetime
import paramiko
import time
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.tcam.case_helper.test_base import TestBase
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException

def ssh_tcam(cmd):
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____TCAM_BASETECH_STRESS_TESTING_MQTT_TESTING_PY_PASSWORD', ""))
            transport = conn.get_transport()
            dest_addr = ("172.16.5.31", 22)
            local_addr = (ip, 22)
            channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

            conn1 = paramiko.SSHClient()
            conn1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn1.connect(hostname="172.16.5.31", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____TCAM_BASETECH_STRESS_TESTING_MQTT_TESTING_PY_PASSWORD', ""), sock=channel)

            stdin, data, error = conn1.exec_command(cmd)

        except SSHFailException as e:
            logger.error(f'The server connect failed with error {e}')
            raise SSHFailException
        
        finally:
            return data.read().decode('utf-8')


class Test_mqtt(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')
        logger.info(ip)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        os.system("ps -ef|grep -i ssh|awk '{logger.infof $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i ssh")
        logger.debug("清除所有ssh进程")
        super().after_class(self, ecu)

    def test_mqtt(self, time_len=300):
        """
        不同模式下车云连接稳定性(每12小时mqtt断连次数&时长)
        ip: bgm台架ip, 默认172.16.5.1
        time_len: 压测的时间长短,单位s,12小时即43200秒, 默认60秒
        """
        global disconn, conn
        logger.info("开始测试车云连接的稳定性…………")
        logger.info("开始时间: {}".format(datetime.datetime.now()))
        logger.info("运行时长:{}秒".format(time_len))

        data = ssh_tcam(cmd="cat /mnt/sdcard/log/jetlog_messages | grep connected!")
        if not data:
            conned = 0
        else:
            conned = len(data.split('\n'))
        logger.info("jetlog中已连接的次数: {}".format(conned - 1))
        if time_len < 120:
            exit('车云连接必须超过2分钟')
        else:
            disconn = 0
            conn = 0
            while time_len > 0:
                time.sleep(120)
                data = ssh_tcam(cmd="cat /mnt/sdcard/log/jetlog_messages | grep connected! | awk '{logger.info $12}' ")
                if data:
                    if len(data.split('\n')) == 1:
                        conn += 1
                        conned = 0
                        logger.info("已成功连接{}次".format(conn))
                    elif len(data.split('\n')) > (conned + conn):
                        conn += 1
                        logger.info("已成功连接{}次".format(conn))
                    else:
                        data1 = ssh_tcam(cmd="cat /mnt/sdcard/log/jetlog_messages1 | grep disconnected! | awk '{logger.info $12}' ")
                        if data1:
                            disconn += 1
                            logger.info("已断连{}次".format(disconn))
                    
                time_len -= 120
                
            logger.info(f"在运行时间内mqtt连接的次数: {conn}")
        
        logger.info("{}时间内mqtt断连次数: {}, 断连时间: {}秒".format(time_len, data, data * 120))



if __name__ == '__main__':
    time_len=500
    Test_mqtt().test_mqtt(time_len=time_len)
    