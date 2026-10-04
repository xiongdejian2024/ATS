#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/12/20 11:23
@Author: lei.tao
@File: network_testing.py
@Software: PyCharm
@Description: 稳定性测试, 统计每12小时断网次数和断网时长
@Example:
"""
import os
import sys
import allure
import datetime
import requests
import time
from contextlib import closing
import paramiko
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.tcam.case_helper.test_base import TestBase

def ssh_tcam(cmd):
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____TCAM_BASETECH_STRESS_TESTING_NETWORK_TESTING_PY_PASSWORD', ""))
            transport = conn.get_transport()
            dest_addr = ("172.16.5.31", 22)
            local_addr = (ip, 22)
            channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

            conn1 = paramiko.SSHClient()
            conn1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn1.connect(hostname="172.16.5.31", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____TCAM_BASETECH_STRESS_TESTING_NETWORK_TESTING_PY_PASSWORD', ""), sock=channel)

            stdin, data, error = conn1.exec_command(cmd)

        except SSHFailException as e:
            logger.error(f'The server connect failed with error {e}')
            raise SSHFailException
        
        finally:
            return data.read().decode('utf-8')


class Test_network(TestBase):
    
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

    def test_network(self, j=60):
        """
        稳定性测试
        bgm_ip: bgm台架ip, 默认172.16.5.1
        j: 统计的总时长, 默认12小时
        """
        logger.info("=" * 100)
        logger.info("在测试上位机先上下电")
        os.system("usbrelay 6QMBS_2=1")
        time.sleep(60)
        os.system("usbrelay 6QMBS_2=0")
        network_info = []
        data = ssh_tcam(cmd="ifconfig | grep rmnet_data")
        if "rmnet_data3" in data:
            logger.info("TCAM为移动网络, 有4路APN")
            for i in ["rmnet_data0", "rmnet_data1", "rmnet_data2", "rmnet_data3"]:
                tcam = ssh_tcam(cmd=f"ping -I {i} www.baidu.com -c 4")
                if "4 packets transmitted, 4 received, 0% packet loss" in tcam:
                    logger.info(f"{i}可以ping通外网")
                    logger.info(f"开始测试{i}网卡的稳定性")
                    data0 = ssh_tcam(cmd=f"ping -I {i} www.baidu.com -c {j}" + '| awk \'{print $0"\t" strftime("%H:%M:%S",systime())}\' ')
                    logger.info("{}稳定性测试信息: {}".format(i, data0.split('\n')[-3])) 
                
                else:
                    tcam1 = ssh_tcam(cmd=f"ping -I {i} 10.90.1.2 -c 4")
                    if "4 packets transmitted, 4 received, 0% packet loss" in tcam1:
                        logger.info(f"{i}可以ping通内网")
                        logger.info(f"开始测试{i}网卡的稳定性")
                        data1 = ssh_tcam(cmd=f"ping -I {i} 10.90.1.2 -c {j}" + '| awk \'{print $0"\t" strftime("%H:%M:%S",systime())}\' ')
                        logger.info("{}稳定性测试信息: {}".format(i, data1.split('\n')[-3])) 
                    else:
                        allure.attach(f"{i}既不能ping通内网,也不能ping通外网")
                        assert False, f"{i}网卡有误,既不能ping通内网,也不能ping通外网"
                    
        elif "rmnet_data0" in data and "rmnet_data3" not in data:
            logger.info("TCAM为联通网络, 只有1路APN")
            tcam2 = ssh_tcam(cmd=f"ping -I rmnet_data0 www.baidu.com -c 4")
            if "4 packets transmitted, 4 received, 0% packet loss" in tcam2:
                logger.info(f"TCAM可以ping通外网")
                logger.info(f"开始测试{i}网卡的稳定性")
                data2 = ssh_tcam(cmd=f"ping -I rmnet_data0 www.baidu.com -c {j}" + '| awk \'{print $0"\t" strftime("%H:%M:%S",systime())}\' ')
                logger.info("{}稳定性测试信息: {}".format(i, data2.split('\n')[-3])) 
            else:
                logger.info(f"TCAM不能ping通外网")
                assert False, f"TCAM联通网卡不能ping通外网"

        else:
            allure.attach("TCAM网卡没有生成, 请先检查网络")
            exit("TCAM网卡没有生成, 请先检查网络")

        


    def test_01(self):
        """
        网卡生成时间 （从上电到 ifconfig出现4个网卡的时间）
        """
        logger.info("在测试上位机先上下电")
        os.system("usbrelay 6QMBS_2=1")
        time.sleep(60)
        os.system("usbrelay 6QMBS_2=0")
        logger.info("=" * 100)
        first_time = datetime.datetime.now()
        logger.info(f"上电时间: {first_time}")
        logger.info("检查3分钟内是否生成网卡")
        _time = 180
        while _time > 0:
            data = ssh_tcam(cmd="ifconfig | grep rmnet_data | wc -l")
            if "4" in data:
                logger.info("TCAM为移动网络, 有4路APN")
                second_time = datetime.datetime.now()
                logger.info(f"移动网卡生成时间: {second_time}")
                time1 = second_time - first_time
                break
            elif "1" in data:
                logger.info("TCAM为联通网络, 只有1路APN")
                second_time = datetime.datetime.now()
                logger.info(f"联通网卡生成时间: {second_time}")
                time1 = second_time - first_time
                break
            else:
                time.sleep(1)
                _time -= 1
        
        else:
            logger.info("3分钟内还未生成网卡, 请检查")
        logger.info(f"移动网卡生成时间: {time1}")
        
        return time1


    def test_02(self):
        """
        默认网卡生成时间 (从上电到route -n 出现 UG时间)
        """
        logger.info("在测试上位机先上下电")
        os.system("usbrelay 6QMBS_2=1")
        time.sleep(60)
        os.system("usbrelay 6QMBS_2=0")
        logger.info("=" * 100)
        first_time = datetime.datetime.now()
        logger.info(f"上电时间: {first_time}")
        while True:
            data = ssh_tcam(cmd="route -n | grep UG")
            if data:
                second_time = datetime.datetime.now()
                logger.info(f"默认网卡生成时间: {second_time}")
                time1 = second_time - first_time
                break
            else:
                time.sleep(1)
        logger.info(f"默认网卡生成时间: {time1}")

        return time1


    def test_03(self):
        """
        网络可用时间(从上电到ping baidu.com 通的时间 )
        """
        logger.info("在测试上位机先上下电")
        os.system("usbrelay 6QMBS_2=1")
        time.sleep(60)
        os.system("usbrelay 6QMBS_2=0")
        logger.info("=" * 100)
        first_time = datetime.datetime.now()
        logger.info(f"上电时间: {first_time}")
        while True:
            data = ssh_tcam(cmd="ping baidu.com -c 4")
            if "4 packets transmitted, 4 received, 0% packet loss" in data:
                second_time = datetime.datetime.now()
                logger.info(f"网络可用时间: {second_time}")
                time1 = second_time - first_time
                break
            else:
                time.sleep(1)
        logger.info(f"网络可用时间: {time1}")
        
        return time1


# 文件下载速率
def down_load(file_url='${XAT_CREDENTIAL_URL_2}' .replace('${XAT_CREDENTIAL_URL_2}', __import__("os").environ['XAT_CREDENTIAL_URL_2']), file_path="./6110110040AE.zip"):
    # 文件开始下载时的时间
    start_time = time.time()  
    with closing(requests.get(file_url, stream=True)) as response:
        # 单次请求最大值):
        chunk_size = 1024  
        # 文件内容体总大小
        content_size = int(response.headers['Content-Length'])  
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                speed = data_count / 1024 / (time.time() - start_time)
                print("\r 文件下载进度：%d%%(%d/%d) 文件下载速度：%dKB/s - %s"
                    % (now_jd, data_count, content_size, speed, file_path), end=" ")
        
        return speed


if __name__ == '__main__':
    # 文件路径
    speed = down_load()
    print(f"文件下载速度: {speed}")
#     print(test_network(j=60))
#     print("从上电到移动网卡生成时间: {}".format(test_01()))
#     print("从上电到默认网卡生成时间: {}".format(test_02()))
#     print("从上电到网络可用时间: {}".format(test_03()))