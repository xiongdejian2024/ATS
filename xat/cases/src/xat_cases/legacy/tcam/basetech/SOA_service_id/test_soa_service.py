#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_cellular_network.py
@Time: 2022/10/17 10:21
@Author: lei.tao
@Software: PyCharm
@Description: 蜂窝网络测试用例
@Examples:
"""
import json
import os
import sys
import time
import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("架构基础")
@allure.story("BaseTech/数字安全/SOA服务鉴权")
class Test_SOA_Service(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("100740_SOA服务鉴权_文件检查process_config")
    def test_caseid_100740(self):
        failed = []
        data = self.ssh.tcam_ssh.exec("ls /oemapp/etc/bootes/process_config.json -lh | awk '{print $5}'", ip).strip()
        allure.step("查看process_config.json文件是否存在")
        if data:
            logger.info("process_config.json文件存在")
            allure.attach("/oemapp/etc/bootes/process_config.json文件存在", "查询process_config.json")
            allure.step("查看process_config.json文件的大小")
            if data == "0":
                logger.info("process_config.json文件大小为0")
                allure.attach(0, "查询process_config.json大小")
                failed.append("大小为0")
            else:
                logger.info(f"process_config.json文件大小为:{data}")
                allure.attach(f"{data}", "查询process_config.json大小")
        else:
            logger.info("process_config.json文件不存在")
            allure.attach("/oemapp/etc/bootes/process_config.json文件不存在", "查询process_config.json")
            failed.append("文件不存在")
        assert len(failed) == 0

    @pytest.mark.smoke
    @allure.title("100382_SOA服务鉴权_文件检查service_monitor_client")
    def test_caseid_100382(self):
        failed = []
        data = self.ssh.tcam_ssh.exec("ls /oemapp/etc/bootes/service_monitor_client.json -lh | awk '{print $5}'", ip).strip()
        allure.step("查询service_monitor_client.json文件是否存在")
        if data:
            logger.info("查询service_monitor_client.json文件存在")
            allure.attach("/oemapp/etc/bootes/service_monitor_client.json文件存在", "查询service_monitor_client.json")
            allure.step("查询service_monitor_client.json文件的大小")
            if data == "0":
                logger.info("service_monitor_client.json文件大小为0")
                allure.attach(0, "service_monitor_client.json大小")
                failed.append("大小为0")
            else:
                logger.info(f"service_monitor_client.json文件大小为:{data}")
                allure.attach(f"{data}", "service_monitor_client.json大小")
        else:
            logger.info("service_monitor_client.json文件不存在")
            allure.attach("/oemapp/etc/bootes/service_monitor_client.json文件不存在", "查询service_monitor_client.json")
            failed.append("文件不存在")
        assert len(failed) == 0
    
    @pytest.mark.smoke

    @allure.title("100499_SOA服务鉴权_文件检查service_monitor")
    def test_caseid_100499(self):
        failed = []
        data = self.ssh.tcam_ssh.exec("ls /oemapp/etc/bootes/service_monitor.json -lh | awk '{print $5}'", ip).strip()
        allure.step("查看service_monitor.json文件是否存在")
        if data:
            logger.info("service_monitor.json文件存在")
            allure.attach("/oemapp/etc/bootes/service_monitor.json文件存在", "查询service_monitor.json")
            allure.step("查看service_monitor.json文件的大小")
            if data == '0':
                logger.info("service_monitor.json文件大小为0")
                allure.attach(0, "查询service_monitor.json大小")
                failed.append("大小为0")
            else:
                logger.info(f"service_monitor.json文件大小为:{data}")
                allure.attach(f"{data}", "查询service_monitor.json大小")
        else:
            logger.info("service_monitor.json文件不存在")
            allure.attach("/oemapp/etc/bootes/service_monitor.json文件不存在", "查询service_monitor.json")
            failed.append("文件不存在")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1912626_SOA服务鉴权_文件说明service_monitor_client")
    def test_caseid_1912626(self):
        failed = []
        data = self.ssh.tcam_ssh.exec("cat /oemapp/etc/bootes/service_monitor_client.json", ip)
        print(data)
        if '"service_monitor_address":"ipc:///tmp/service_monitor"' in data:
            logger.info("查询的内容正确")
            allure.attach("内容正确", "查询文件service_monitor_client.json的内容")
        else:
            logger.info("查询的内容错误")
            allure.attach("内容错误", "查询文件service_monitor_client.json的内容")
            failed.append("查询的内容错误")
        assert len(failed) == 0
    
    @pytest.mark.full
    @allure.title("100364_SOA服务鉴权_文件说明process_config")
    def test_caseid_100364(self):
        failed = []
        data = self.ssh.tcam_ssh.exec("cat /oemapp/etc/bootes/process_config.json | grep bootes_id", ip).split('\n')
        data = [i for i in data if i !=""]
        logger.info(f"process_config.json文件的内容:\n{data}")
        SOA_data = ['"netstat_service"','"gnss_service"','"rvc"','"ua_server_app"','"tconstable"','"gb32960_service"','"config_service"','"rtc"','"em"','"v2trouter"','"misc"','"xcall_service"','"prop"',
                    '"sample_server"','"app_service_manager"','"em2"','"vehicle_data_mining_engine"','"CertificateMgr"','"remote_log"','"network_manager"','"CellNetworkManager"','"phc2sys"','"net_resource_manager"','"monitor_agent"']
        for i in data:
            if i.split(',')[0].split(":")[-1]  not in SOA_data:
                failed.append(i.split(',')[0].split(":")[-1])
        if len(failed) == 0:
            logger.info("查询的内容正确")
            allure.attach("内容正确", "查询文件process_config.json的内容")
        else:
            logger.info("查询的内容错误")
            allure.attach("内容错误", "查询文件process_config.json的内容")
            logger.error(failed)
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("101037_SOA服务鉴权_服务启动service_monitor")
    def test_caseid_101037(self):
        failed = []
        data = self.ssh.tcam_ssh.exec(" ps aux | grep service_monitor | grep -v grep", ip)
        if data:
            logger.info("service_monitor进程存在")
            allure.attach("进程存在", "查询service_monitor进程")
        else:
            logger.info("service_monitor进程不存在")
            allure.attach("进程不存在", "查询service_monitor进程")
            failed.append("service_monitor进程不存在")
        assert len(failed) == 0

    @pytest.mark.full
    @allure.title("1990441_SOA服务鉴权_bootes_config.json文件只读权限")
    def test_caseid_1990441(self):
        data = self.ssh.tcam_ssh.exec("touch /oemapp/etc/bootes/bootes_config.json", ip)
        logger.info(f"{data}")
        assert "touch: /oemapp/etc/bootes/bootes_config.json: Read-only file system" in data, f"bootes_config.json文件权限错误, 不是只读权限"

    @pytest.mark.full
    @allure.title("1990442_SOA服务鉴权_service_monitor_client.json文件只读权限")
    def test_caseid_1990442(self):
        data = self.ssh.tcam_ssh.exec("touch /oemapp/etc/bootes/service_monitor_client.json", ip)
        logger.info(f"{data}")
        assert "touch: /oemapp/etc/bootes/service_monitor_client.json: Read-only file system" in data, f"service_monitor_client.json文件权限错误, 不是只读权限"

    @pytest.mark.full
    @allure.title("1990443_SOA服务鉴权_process_config.json文件只读权限")
    def test_caseid_1990443(self):
        data = self.ssh.tcam_ssh.exec("touch /oemapp/etc/bootes/process_config.json", ip)
        logger.info(f"{data}")
        assert "touch: /oemapp/etc/bootes/process_config.json: Read-only file system" in data, f"process_config.json文件权限错误, 不是只读权限"

    @pytest.mark.full
    @allure.title("1903214_SOA服务鉴权_服务连接service_monitor")
    def test_caseid_1903214(self):
        failed = []
        data = ""
        service_list = []
        with allure.step("先删除jetlog_bts重启TCAM"):
            logger.info("删除jetlog")
            self.ssh.tcam_ssh.exec("rm /mnt/sdcard/log/jetlog_bts", ip)
            logger.info("重启TCAM")
            self.ssh.tcam_ssh.exec("reboot", ip)
            time.sleep(200)
        logger.info("重启后查看tcam是否唤醒")
        
        while True:
            try:
                aa = self.ssh.tcam_ssh.exec("pwd", ip)
                if aa:
                    logger.info(f"tcam已唤醒{aa}")
                    break
            except:
                logger.info("tcam没有唤醒, 等待30s")
                time.sleep(30)
                continue
        with allure.step("查询/mnt/sdcard/log/jetlog_bts初始化成功的service name"):
            while True:
                jet = self.ssh.tcam_ssh.exec("ls /mnt/sdcard/log/jetlog_bts", ip)
                if jet:
                    logger.info("tcam重启后jetlog已生成")
                    break
                else:
                    logger.info("tcam重启后jetlog没有生成, 等待30s")
                    time.sleep(30)
            data = self.ssh.tcam_ssh.exec("/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_bts | grep 'InitProxy initialize success' | grep -v grep | awk '{print $10}' ", ip)
            if data:
                data2 = data.split('\n')
                data2 = [i.split(':')[0] for i in data2 if i !=""]
                logger.info(f"查询到初始化成功的服务名称为: {data2}")
                allure.attach(f"{data2}", "查询到的service name")
            else:
                logger.error("没有查询到初始化成功的service name, 请手动删除jetlog_messages后再次重试")
                allure.attach("暂无", "查询到的service name")
                failed.append("重启后没有查询到初始化成功的service name")
        with allure.step("查询tcam的service_monitor.json文件中对应service_id的service name"):
            service_list2 = []
            service2 = self.ssh.tcam_ssh.exec(" cat /oemapp/etc/bootes/service_monitor.json | grep 'service_id'", ip)
            data3 = service2.strip().split('\n')
            print(data3)
            for i in data3:
                if i !="":
                    service_list2.append(i.split('"')[3])
            logger.info(f"查询到tcam中service_monitor.json文件中的服务有: {service_list2}")
            allure.attach(str(service_list2), "tcam中service_monitor.json文件中的服务")
        with allure.step("查询bgm的service_monitor.json文件中对应service_id的service name"):
            service_list1 = []
            service1 = self.ssh.bgm_ssh.type_commands("cat /app/etc/service_monitor.json")
            data1 = json.loads(service1).get("service_list")
            for i in data1:
                service_list1.append(i.get("service_id"))
            logger.info(f"查询到bgm中service_monitor.json文件中的服务有: {service_list1}")
            allure.attach(str(service_list1), "bgm中service_monitor.json文件中的服务")
        
        with allure.step("验证jetlog_messages中初始化成功的服务是否都在service_monitor.json文件中"):
            service_list = service_list1 + service_list2
            if data:
                for j in data2:
                    if j in service_list:
                        logger.info(f"服务{j}在service_monitor.json文件中")
                        allure.attach("存在service_monitor.json文件中", f"服务名称{j}")
                    else:
                        logger.info(f"服务{j}不在service_monitor.json文件中")
                        allure.attach("不存在service_monitor.json文件中", f"服务名称{j}")
                        failed.append(f"服务{j}不在service_monitor.json文件中")
        assert len(failed) ==0
    


if __name__ == '__main__':
    pytest.main()
