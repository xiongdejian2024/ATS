#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_system.supervisor.py
@time         : 2024/3/18
@author       : o_kaijin.yao@external.jiduauto.com
'''

import os
import sys
import time

import allure
import pytest
import re
from datetime import datetime
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger


@allure.feature("软件平台/健康监控")
class TestCertificate(TestABCBase):
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
    
    @pytest.mark.sanity
    def test_caseid_1985773(self):
        allure.attach("cpu_load和mem采集")
        self.ssh.check_metric_data("cat /mnt/sdcard/persistent/metric_data.log", ip, '"event":"cpu_load"', '"event":"mem"')#采集cpu_load和mem采集

    @pytest.mark.sanity
    def test_caseid_1985762(self):
        allure.attach("timestamp和value正常采集")
        self.ssh.check_metric_data("cat /mnt/sdcard/persistent/metric_data.log", ip, '"ts":"', '"v":') #正常采集timestamp和value正常采集

    @pytest.mark.sanity
    def test_caseid_1985767(self):
         #kill进程模拟生成coredump
        self.ssh.tcam_ssh.exec("pkill -6 rvc", ip)
        time.sleep(30)
        #有coredump持久化数据生成
        metric_coredump = self.ssh.tcam_ssh.exec('ls /mnt/sdcard/persistent | grep metric_coredump_data.log', ip)
        logger.info(f'metric_coredump文件名:{metric_coredump}')
        allure.step('查看文件是否存在')
        assert metric_coredump == "metric_coredump_data.log", f"metric_coredump文件名:{metric_coredump},/mnt/sdcard/persistent/metric_coredump_data.log文件不存在"
    
    @pytest.mark.sanity
    def test_caseid_1985759(self):  
        allure.step("查看coredump文件信息格式")
        self.ssh.check_metric_data("cat /mnt/sdcard/persistent/metric_coredump_data.log", ip, '"error_id"','"event":"ERROR"','"extra_info"','"msg":"Coredump","tag"') #查看coredump数据文件信息
    

    @pytest.mark.sanity
    def test_caseid_1985771(self):
        data = self.ssh.tcam_ssh.exec('/oemapp/bin/zstdcat  /mnt/sdcard/log/jetlog_messages |grep "str size:" |  head -2', ip)
        logger.info(data)
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'  # 匹配日期时间格式
        match = re.findall(pattern, data) #查找上传时间
        format = "%Y-%m-%d %H:%M:%S"
        time1 = datetime.strptime(match[0], format)
        time2 = datetime.strptime(match[1], format)
        time_difference=time2 - time1 #计算相邻上传时间差
        result = time_difference.seconds / 60
        assert result >= 3 and result < 4 , '时间不在3min和4min之间' #时间在3min和4min之间
        

    @pytest.mark.full
    def test_caseid_1985753(self):
        #查找cpu load
        cpuload = self.ssh.tcam_ssh.exec("top -b -n 1 | grep monitor_agent/" + " | awk '{print $8}' ", ip)
        allure.step("monitor_agent进程cpu使用率在2%以下")
        assert float(cpuload) <= float(2.0),"cpu使用率不在2%以下"
    
    @pytest.mark.full
    def test_caseid_1985763(self):
        allure.step("重启TCAM,数据仍存在")
        self.io.tcam_power_off()
        time.sleep(30)
        self.io.tcam_power_on()
        time.sleep(240)      
        metric_data = self.ssh.tcam_ssh.exec('ls /mnt/sdcard/persistent | grep metric_data.log', ip)
        allure.step('查看文件是否存在')
        assert metric_data == "metric_data.log"

# pytest basetech/system_supervisor/test_system_supervisor.py::TestCertificate::test_caseid_1985759