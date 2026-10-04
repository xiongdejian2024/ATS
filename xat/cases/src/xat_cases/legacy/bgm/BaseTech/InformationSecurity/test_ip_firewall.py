#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_ip_firewall.py
@Time: 2024/03/19 10:31
@Author: O_jingyuan.chen
@Software: vscode
@Description: ip防火墙模块的测试用例
@Examples:
"""
import base64
import os
import sys
import allure
import pytest
from subprocess import Popen, PIPE, STDOUT
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.constant import *
from xat_ecu.legacy.driver.adb_client import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
usr_bgm = base64.b64decode(BGM_CONSTANT.BGM_USERNAME.encode()).decode()
pwd_bgm = base64.b64decode(BGM_CONSTANT.BGM_PASSWORD.encode()).decode() 
hostname = base64.b64decode(BGM_CONSTANT.BGM_HOSTNAME.encode()).decode()


@allure.feature('BGM BaseTech/数字安全/系统安全')
@allure.story('IP防火墙')
class Test_IP_Firewall(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip, data
        ip = self.tc_config.get('gateway_ip')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.sanity
    @allure.title("1985250_BGM端口80放行")
    def test_caseid_1985250(self):
        failed = []
        with allure.step("进入BGM查看端口80"):
            data = self.ssh.type_commands(DeviceName.BGM,"telnet 172.16.5.21 80",timeout=120)
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功{data}", "返回信息:")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")   
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1985249_BGM端口81不放行")
    def test_caseid_1985249(self):
        failed = []
        with allure.step("进入BGM查看端口81"):
            data = self.ssh.type_commands(DeviceName.BGM,"telnet 172.16.5.21 81",timeout=180)
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功{data}", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")         
        assert len(failed) == 0

    @pytest.mark.smoke
    @allure.title("1985257_BGM_端口22放行")
    def test_caseid_1985257(self):
        failed = []
        with allure.step("进入BGM连接22端口"):
            cmd = f"sshpass -p {pwd_bgm} ssh {usr_bgm}@{hostname} -p 22 'pwd'"
            data = os.popen(cmd).read()
        with allure.step("检查是否连接成功"):
            if data:
                allure.attach(f"连接成功{data}", "返回信息:")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("1985248_BGM_获取时间")
    def test_caseid_1985248(self):
        with allure.step(f"查看BGM的时间"):
            data = self.ssh.type_commands(DeviceName.BGM,"date")
            logger.info("BGM输出的内容为: {}".format(data))
            sys_time = datetime.datetime.strptime(data, "%a %b %d %H:%M:%S %Z %Y")
            logger.info("BGM系统时间为: {}".format(sys_time))
            allure.attach("{0}".format(sys_time), f"BGM时间情况")
            logger.info("BGM的当前时间为: {}".format(sys_time + datetime.timedelta(hours=8)))
            
            loc_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info("当前北京时间为: {}".format(loc_time))
            
        assert abs(datetime.datetime.strptime(loc_time, '%Y-%m-%d %H:%M:%S') - (sys_time + datetime.timedelta(hours=8))) < datetime.timedelta(minutes=1), f"【BGM】的时间不是当前系统时间"
                
    @pytest.mark.full
    @allure.title("1985256_BGM端口23不放行")
    def test_caseid_1985256(self):
        failed = []
        with allure.step("进入BGM连接23端口"):
            cmd = f"sshpass -p {pwd_bgm} ssh {usr_bgm}@{hostname} -p 23 'pwd'"
            data = os.popen(cmd).read()
        with allure.step("检查是否连接成功"):
            if data:
                allure.attach(f"连接成功{data}", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1985252_BGM端口443放行")
    def test_caseid_1985252(self):
        failed = []
        with allure.step("进入BGM连接443端口"):
            data = self.ssh.type_commands(DeviceName.BGM,"curl -v jadmc-staging.jiduapp.cn:443",timeout=120)
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功{data}", "返回信息:")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")
                failed.append("连接不成功")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1985251_BGM端口444不放行")
    def test_caseid_1985251(self):
        failed = []
        with allure.step("进入BGM连接444端口"):
            data = self.ssh.type_commands(DeviceName.BGM,"curl -v jadmc-staging.jiduapp.cn:444",timeout=180)
            allure.attach(f"{data}", "返回信息:")
            logger.info(f"返回信息: {data}")
        with allure.step("检查是否连接成功"):
            if "Connected" in data:
                allure.attach(f"连接成功{data}", "返回信息:")
                failed.append("连接成功")
            else:
                allure.attach(f"连接不成功{data}", "返回信息:")   
        assert len(failed) == 0

    @pytest.mark.smoke
    @allure.title("1985246_BGM_软件包下载(蜂窝)")
    def test_caseid_1985246(self):
        """
        连接TCAM下载软件包
        """      
        with allure.step("ssh连接BGM下载软件包"):
            failed=[]
            cmd2 = f"curl -O https://t-ivs-fota.cdn.bcebos.com/staging/encrypt/479/artifactory-ha/filestore/0e/0e116da573b58451835b45aba290d4fc897c1871/6110110065ABF.bin?authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2022-12-02T11%3A47%3A42Z%2F-1%2F%2F98d320cc32b9ae1a14a64042f60dba7c140e8da3c1dd8f895eab305eab29f84a"
            data = BGM_SSH().type_commands(cmd2,timeout=360,alias="x0")
            # time.sleep(300)
            if "100" in data:
                logger.info(f"软件包下载完成")
                allure.attach(f"软件包下载完成")
                failed.append(f"软件包下载完成")
            else:
                logger.info(f"软件包下载失败")
                allure.attach(f"软件包下载失败")
                assert "100" not in data,f"BGM软件包下载失败"

    @pytest.mark.sanity
    @allure.title("1985247_BGM_软件包下载(wifi)")
    def test_caseid_1985247(self):
        """
        连接CDC下载软件包
        """      
        with allure.step("ssh连接BGM下载软件包"):
            failed=[]
            cmd2 = f"curl -O https://t-ivs-fota.cdn.bcebos.com/staging/encrypt/479/artifactory-ha/filestore/0e/0e116da573b58451835b45aba290d4fc897c1871/6110110065ABF.bin?authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2022-12-02T11%3A47%3A42Z%2F-1%2F%2F98d320cc32b9ae1a14a64042f60dba7c140e8da3c1dd8f895eab305eab29f84a"
            data = BGM_SSH().type_commands(cmd2,timeout=360,alias="x1")
            # time.sleep(300)
            if "100" in data:
                logger.info(f"软件包下载完成")
                allure.attach(f"软件包下载完成")
                failed.append(f"软件包下载完成")
            else:
                logger.info(f"软件包下载失败")
                allure.attach(f"软件包下载失败")
                assert "100" not in data,f"BGM软件包下载失败"

    @pytest.mark.smoke
    @allure.title("1985258_BGM_端口13400诊断")
    def test_caseid_1985258(self):
        '''
        BGM端口13400诊断
        '''
        self.sd_tester.send_data_and_check(0x1001, "22f1ae", "62f1ae")

    @pytest.mark.smoke
    @allure.title("1985259_BGM_端口13400公告")
    def test_caseid_1985259(self):
        '''
        端口13400车辆公告
        '''
        with allure.step("物理寻址发送1101"):
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.send_data([0x11,0x01])
            before = time.time()
        with allure.step("获取1101第一条车辆公告发出时间"):
            after = self.sd_tester.wait_vehicle_announcement()
        assert after - before < 20, f"公告发出时间与当前时间相差大于10s"

# pytest -vs -p no:warnings ip_firewall/test_ip_firewall.py::Test_IP_Firewall::test_caseid_110533
#pytest BaseTech/InformationSecurity/test_ip_firewall.py::Test_IP_Firewall::test_caseid_1912711
