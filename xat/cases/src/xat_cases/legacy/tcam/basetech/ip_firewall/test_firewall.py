#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_log_format.py
@Time: 2023/03/30 16:35
@Author: lei.tao
@Software: PyCharm
@Description: ip防火墙模块的测试用例
@Examples:
"""
import base64
import os
import sys
import allure
import pytest
from subprocess import Popen, PIPE, STDOUT
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.constant import TCAM_CONSTANT


username = base64.b64decode(TCAM_CONSTANT.TCAM_USERNAME.encode()).decode()
hostname = base64.b64decode(TCAM_CONSTANT.TCAM_HOSTNAME.encode()).decode()
password = base64.b64decode(TCAM_CONSTANT.TCAM_PASSWORD.encode()).decode()

def con_tcam(cmd):
    args = f"sshpass -p {password} ssh {username}@{hostname} '{cmd}'"
    p = Popen(args, stdout=PIPE, stderr=STDOUT, shell=True)
    data = ''
    i = 0
    while i < 10:
        buff = p.stdout.readline().decode("utf8", errors="ignore").rstrip()
        if buff is not None:
            data += (buff + '\n')
            i += 1
        else:
            break
    os.system("ps -ef|grep -i curl|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9")
    
    return data


def con_ACU(cmd, ip_acu):
    args = f"sshpass -p caros ssh caros@{ip_acu} '{cmd}'"
    p = Popen(args, stdout=PIPE, stderr=STDOUT, shell=True)
    data = ''
    i = 0
    while i < 10:
        buff = p.stdout.readline().decode("utf8", errors="ignore").rstrip()
        if buff is not None:
            data += (buff + '\n')
            i += 1
        else:
            break
    os.system("ps -ef|grep -i curl|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9")
    
    return data


@allure.feature("架构基础")
@allure.story("BaseTech/数字安全/入侵检查及防御/IP防火墙")
class Test_IP_Firewall(TestABCBase):

    def before_class(self, ecu):
        self.io.tcam_power_off()
        time.sleep(30)
        self.io.tcam_power_on()
        time.sleep(200)
        super().before_class(self, ecu)
        global ip, data
        ip = self.tc_config.get('gateway_ip')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("100291_TCAM端口22放行_001")
    def test_caseid_100291(self):
        failed = []
        with allure.step("进入TCAM连接22端口"):
            cmd = f"sshpass -p {password} ssh {username}@{hostname} -p 22 'pwd'"
            data = os.popen(cmd).read()
        with allure.step("检查是否连接成功"):
            if data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0
    
    @pytest.mark.sanity
    @allure.title("1980979_TCAM端口80不放行")
    def test_caseid_1980979(self):
        failed = []
        with allure.step("进入TCAM连接80端口"):
            data = con_tcam("curl -v openapi.sixents.com:80" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")
        assert len(failed) == 0
    
    @pytest.mark.full
    @allure.title("1912625_TCAM_下载软件包(蜂窝)_001")
    def test_caseid_1912625(self):
        """
        连接TCAM下载软件包
        """
        with allure.step("ssh连接TCAM进入/mnt/sdcard目录"):
            cmd1 = f"cd /mnt/sdcard"
            self.ssh.tcam_ssh.type_commands(cmd1,alias="x0")
            
        with allure.step("ssh连接TCAM下载软件包"):
            failed=[]
            cmd2 = f"curl -O https://t-ivs-fota.cdn.bcebos.com/staging/encrypt/479/artifactory-ha/filestore/0e/0e116da573b58451835b45aba290d4fc897c1871/6110110065ABF.bin?authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2022-12-02T11%3A47%3A42Z%2F-1%2F%2F98d320cc32b9ae1a14a64042f60dba7c140e8da3c1dd8f895eab305eab29f84a"
            data = self.ssh.tcam_ssh.type_commands(cmd2,timeout=360,alias="x0")
            # time.sleep(300)
            if "100" in data:
                logger.info(f"软件包下载完成")
                allure.attach(f"软件包下载完成")
                failed.append(f"软件包下载完成")
            else:
                logger.info(f"软件包下载失败")
                allure.attach(f"软件包下载失败")
                assert "100" not in data,f"TCAM软件包下载失败"

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1912624_TCAM_下载软件包(WIFI)_001")
    def test_caseid_1912624(self):
        """
        需要四域台架环境测试
        """
        with allure.step("ssh连接TCAM进入/mnt/sdcard目录"):
            cmd1 = f"cd /mnt/sdcard"
            self.ssh.tcam_ssh.type_commands(cmd1,alias="x1")
            
        with allure.step("ssh连接TCAM下载软件包"):
            failed=[]
            cmd2 = f"curl -O https://t-ivs-fota.cdn.bcebos.com/staging/encrypt/479/artifactory-ha/filestore/0e/0e116da573b58451835b45aba290d4fc897c1871/6110110065ABF.bin?authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2022-12-02T11%3A47%3A42Z%2F-1%2F%2F98d320cc32b9ae1a14a64042f60dba7c140e8da3c1dd8f895eab305eab29f84a"
            data = self.ssh.tcam_ssh.type_commands(cmd2,timeout=360,alias="x1")
            # time.sleep(300)
            if "100" in data:
                logger.info(f"软件包下载完成")
                allure.attach(f"软件包下载完成")
                failed.append(f"软件包下载完成")
            else:
                logger.info(f"软件包下载失败")
                allure.attach(f"软件包下载失败")
                assert "100" not in data,f"TCAM软件包下载失败"
                
    @pytest.mark.sanity
    @allure.title("100746_TCAM端口18883放行_001")
    def test_caseid_100746(self):
        failed = []
        with allure.step("进入TCAM连接188883端口"):
            data = con_tcam("curl -v vehicle-staging.jiduapp.cn:18883" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100967_TCAM端口18884不放行_001")
    def test_caseid_100967(self):
        failed = []
        with allure.step("进入TCAM连接188884端口"):
            data = con_tcam("curl -v vehicle-staging.jiduapp.cn:18884" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")
        assert len(failed) == 0       

    @pytest.mark.full
    @allure.title("101009_TCAM端口19007放行_001")
    def test_caseid_101009(self):
        failed = []
        with allure.step("进入TCAM连接19007端口"):
            data = con_tcam("curl -v 123.127.164.36:19007" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100662_TCAM端口19008不放行_001")
    def test_caseid_100662(self):
        failed = []
        with allure.step("进入TCAM连接19008端口"):
            data = con_tcam("curl -v 123.127.164.36:19008" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("100549_TCAM端口23不放行_001")
    def test_caseid_100549(self):
        failed = []
        with allure.step("进入TCAM连接23端口"):
            cmd = f"sshpass -p {password} ssh {username}@{hostname} -p 23 'pwd'"
            data = os.popen(cmd).read()
        with allure.step("检查是否连接成功"):
            if data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100946_TCAM端口29476放行_001")
    def test_caseid_100946(self):
        failed = []
        with allure.step("进入TCAM连接29476端口"):
            data = con_tcam('curl -v 120.48.11.173:29476')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100775_TCAM端口29477不放行_001")
    def test_caseid_100775(self):
        failed = []
        with allure.step("进入TCAM连接29477端口"):
            data = con_tcam("curl -v 120.48.11.173:29477" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("100612_TCAM端口443放行_001")
    def test_caseid_100612(self):
        failed = []
        with allure.step("进入TCAM连接443端口"):
            data = con_tcam("curl -v 123.127.164.36:443" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100948_TCAM端口444不放行_001")
    def test_caseid_100948(self):
        failed = []
        with allure.step("进入TCAM连接444端口"):
            data = con_tcam("curl -v 123.127.164.36:444" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("100987_TCAM端口8009放行_001")
    def test_caseid_100987(self):
        failed = []
        with allure.step("进入TCAM连接8009端口"):
            data = con_tcam("curl -v supervision-staging.jiduapp.cn:8009" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connection refused" in data:
                allure.attach(f"连接被拒绝，但是IP防火墙功能是正常的，GB32960的连接需要双向认证", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100796_TCAM端口8010不放行_001")
    def test_caseid_100796(self):
        failed = []
        with allure.step("进入TCAM连接8010端口"):
            data = con_tcam("curl -v supervision-staging.jiduapp.cn:8010" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1986740_TCAM端口18443放行_001")
    def test_caseid_1986740(self):
        failed = []
        with allure.step("进入TCAM连接18443端口"):
            data = con_tcam("curl -v evc-gb32960.test.geely.com:18443" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100446_TCAM端口8878不放行_001")
    def test_caseid_100446(self):
        failed = []
        with allure.step("进入TCAM连接8878端口"):
            data = con_tcam("curl -v evc-gb32960.test.geely.com:8878" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("100986_TCAM端口8877不放行_001")
    def test_caseid_100986(self):
        failed = []
        with allure.step("进入TCAM连接8877端口"):
            data = con_tcam("curl -v evc-gb32960.test.geely.com:8877" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1988429_TCAM端口18444不放行_001")
    def test_caseid_1988429(self):
        failed = []
        with allure.step("进入TCAM连接18444端口"):
            data = con_tcam("curl -v evc-gb32960.test.geely.com:18444" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1988430_TCAM端口18443放行_002")
    def test_caseid_1988430(self):
        failed = []
        with allure.step("进入TCAM连接18443端口"):
            data = con_tcam("curl -v jidu-gb32960.geely.com:18443" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")     
                failed.append("连接不成功") 
        #assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1988431_TCAM端口18444不放行_002")
    def test_caseid_1988431(self):
        failed = []
        with allure.step("进入TCAM连接18444端口"):
            data = con_tcam("curl -v jidu-gb32960.geely.com:18444" )
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.sanity
    @pytest.mark.four_domain
    @allure.title("100678_Orin1_端口80放行_001")
    def test_caseid_100678(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口80"):
            data = con_ACU("curl -v openapi.sixents.com:80", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100319_Orin1_端口81不放行_001")
    def test_caseid_100319(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口81"):
            data = con_ACU("curl -v openapi.sixents.com:81", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")         
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100269_Orin1_端口8007放行_001")
    def test_caseid_100269(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口8007"):
            data = con_ACU("nc -z -v vrs.sixents.com 8007", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100632_Orin1_端口8006不放行_001")
    def test_caseid_100632(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口8006"):
            data = con_ACU("nc -z -v vrs.sixents.com 8006", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.sanity
    @pytest.mark.four_domain
    @allure.title("101007_Orin1_端口443放行_001")
    def test_caseid_101007(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口443"):
            data = con_ACU("curl -v sixa.sixents.com:443", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100477_Orin0_端口444不放行_001")
    def test_caseid_100477(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口444"):
            data = con_ACU("curl -v sixa.sixents.com:444", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.sanity
    @pytest.mark.four_domain
    @allure.title("100648_Orin1_端口18883放行_001")
    def test_caseid_100648(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口18883"):
            data = con_ACU("nc -z -v vehicle-staging.jiduapp.cn 18883", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100396_Orin1_端口18884不放行_001")
    def test_caseid_100396(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU查看端口18884"):
            data = con_ACU("nc -z -v vehicle-staging.jiduapp.cn 18884", '172.16.5.23')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1989550_Orin0_端口80不放行_001")
    def test_caseid_1989550(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口80"):
            data = con_ACU("curl -v openapi.sixents.com:80", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1988420_Orin0_端口8007不放行_001")
    def test_caseid_1988420(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口8007"):
            data = con_ACU("nc -z -v vrs.sixents.com 8007", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain    
    @allure.title("100974_Orin1_端口444不放行_001")
    def test_caseid_100974(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口444"):
            data = con_ACU("curl -v sixa.sixents.com:444", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.sanity
    @pytest.mark.four_domain
    @allure.title("100883_Orin0_端口443放行_001")
    def test_caseid_100883(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口443"):
            data = con_ACU("curl -v sixa.sixents.com:443", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:") 
                failed.append("连接不成功")  
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100984_Orin0_端口18883放行_001")
    def test_caseid_100984(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口18883"):
            data = con_ACU("nc -z -v vehicle-staging.jiduapp.cn 18883", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:") 
                failed.append("连接不成功")  
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1988421_Orin0_端口18884不放行_001")
    def test_caseid_1988421(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入ACU,登录Orin0查看端口18884"):
            data = con_ACU("nc -z -v vehicle-staging.jiduapp.cn 18884", '172.16.5.21')
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")  
            else:
                allure.attach(f"连接不成功", "返回信息:") 
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100659_CDC_端口80放行_001")
    def test_caseid_100659(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口80"):
            data = Adb(serialno='1234567').shell("curl -v https://vehiclesvc-staging.jiduapp.cn/api:80")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:") 
                failed.append("连接不成功")  
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100506_CDC_端口81不放行_001")
    def test_caseid_100506(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口81"):
            data = Adb(serialno='1234567').shell("curl -v https://vehiclesvc-staging.jiduapp.cn/api:81")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")  
            else:
                allure.attach(f"连接不成功", "返回信息:") 
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1988423_CDC_端口54不放行_001")
    def test_caseid_1988423(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口54"):
            data = Adb(serialno='1234567').shell("telnet 8.8.8.8:54")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")  
            else:
                allure.attach(f"连接不成功", "返回信息:") 
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("1988422_CDC_端口53放行_001")
    def test_caseid_1988422(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口53"):
            data = Adb(serialno='1234567').shell("telnet 8.8.8.8:53")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:") 
                failed.append("连接不成功")  
        assert len(failed) == 0

    @pytest.mark.sanity
    @pytest.mark.four_domain
    @allure.title("100483_CDC_端口443放行_001")
    def test_caseid_100483(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口443"):
            data = Adb(serialno='1234567').shell("curl -v https://vehiclesvc-staging.jiduapp.cn:443/api")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
            else:
                allure.attach(f"连接不成功", "返回信息:") 
                failed.append("连接不成功")  
        assert len(failed) == 0

    @pytest.mark.full
    @pytest.mark.four_domain
    @allure.title("100937_CDC_端口444不放行_001")
    def test_caseid_100937(self):
        """
        需要四域台架环境测试
        """
        failed = []
        with allure.step("进入CDC安卓查看端口444"):
            data = Adb(serialno='1234567').shell("curl -v https://vehiclesvc-staging.jiduapp.cn:444/api")
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功", "返回信息:")
                failed.append("连接成功")  
            else:
                allure.attach(f"连接不成功", "返回信息:") 
        assert len(failed) == 0



if __name__ == '__main__':
    pytest.main()
# pytest basetech/ip_firewall/test_firewall.py
