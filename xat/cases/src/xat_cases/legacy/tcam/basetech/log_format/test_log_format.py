#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_log_format.py
@Time: 2023/02/01 09:35
@Author: lei.tao
@Software: PyCharm
@Description: 日志格式规范测试用例
@Examples:
"""

import os
import sys
from datetime import datetime
import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.tcam.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH


@allure.feature("SAT")
@allure.story("TCAM台架的日志管理测试用例")
class Test_Log_Format(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip, data
        ip = self.tc_config.get('gateway_ip')
        data = TCAM_SSH().exec(cmd="cat /mnt/sdcard/log/jetlog_messages | head -n 10", bgm_ip=ip).split('\n')
        data = [i for i in data if i != '']

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348403?projectId=46")
#     @allure.title("日志格式规范_时间_001")
#     def test_caseid_1348403(self):
#         failed = []
#         def validate(date_text):
#             try:
#                 if date_text != datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S.%f'):
#                     raise ValueError
#                 return True
#             except ValueError:
#                 return False
#         for line in data:
#             log_date = line.split(' ')[0] + ' ' + line.split(' ')[1] + '000'
            
#             result = validate(log_date)
#             if result == False:
#                 failed.append(line)
        
#         with allure.step(f"check行日志的时间:"):
#             if len(failed) != 0:  
#                 allure.attach(f"时间格式有误的行为: {failed}")
#             else:
#                 allure.attach("时间格式OK")
#         assert len(failed) == 0,f"TCAM日志的时间格式有误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348404?projectId=46")
#     @allure.title("日志格式规范_进程ID_002")
#     def test_caseid_1348404(self):
#         failed = []
#         for line in data:
#             pid = line.split(' ')[2]
#             tid = line.split(' ')[3]
#             if tid.isdigit():
#                 if not pid.isdigit():
#                     failed.append(line)

#         with allure.step(f"check行日志的进程ID:"):
#             if len(failed) != 0:  
#                 allure.attach(f"进程ID格式有误的行为: {failed}")
#             else:
#                 allure.attach("进程ID格式OK")
#         assert len(failed) == 0,f"TCAM日志的进程pid有误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348405?projectId=46")
#     @allure.title("日志格式规范_TID_003")
#     def test_caseid_1348405(self):
#         failed = []
#         for line in data:
#             pid = line.split(' ')[2]
#             tid = line.split(' ')[3]
#             if pid.isdigit():
#                 if not tid.isdigit():
#                     failed.append(line)

#         with allure.step(f"check行日志的TID:"):
#             if len(failed) != 0:  
#                 allure.attach(f"TID格式有误的行为: {failed}")
#             else:
#                 allure.attach("TID格式OK")
#         assert len(failed) == 0,f"TCAM日志的tid有误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348406?projectId=46")
#     @allure.title("日志格式规范_日志级别_004")
#     def test_caseid_1348406(self):
#         """
#         日志输出应该包含ERROR/WARN/INFO/DEBUG/Verbose
#         """
#         failed = []
#         for line in data:
#             level = line.split(' ')[4]
#             if level not in ['E', 'W', 'I', 'D', 'V']:
#                 failed.append(line)

#         with allure.step(f"check行日志的级别:"):
#             if len(failed) != 0:  
#                 allure.attach(f"日志级别格式有误的行为: {failed}")
#             else:
#                 allure.attach("日志级别格式OK")
#         assert len(failed) == 0,f"TCAM日志的日志级别有误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348409?projectId=46")
#     @allure.title("日志格式规范_日志内容_007")
#     def test_caseid_1348409(self):
#         """
#         日志内容输出格式为：  
#         [trace_id] [span_id] [parent_span_id] [network] [user_id] msg 其中前5项可选
#         """
#         failed = []
#         for line in data:
#             level = line.split('[')
#             if len(level) > 6:
#                 failed.append(line)

#         with allure.step(f"check行日志的内容:"):
#             if len(failed) != 0:  
#                 allure.attach(f"日志内容格式有误的行为: {failed}")
#             else:
#                 allure.attach("日志内容格式OK")
#         assert len(failed) == 0,f"TCAM日志的日志内容有误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348410?projectId=46")
#     @allure.title("日志存储_单文件大小_001")
#     def test_caseid_1348410(self):
#         """
#         单个日志文件上限100M
#         """
#         failed = []
#         data1 = TCAM_SSH().exec(cmd="ls -lh /mnt/sdcard/log/| grep jetlog_messages | awk '{print $5}'", bgm_ip=ip).split('\n')
#         data = [j for j in data1 if j != '']
#         for i in data:
#             if int(i.split('.')[0]) > 100:
#                 failed.append(i)

#         with allure.step(f"check单文件日志大小:"):
#             allure.attach(f"单个日志文件大小为: {data}")
#             if len(failed) != 0:  
#                 allure.attach(f"单个日志文件大小超过100M的为: {failed}")
#             else:
#                 allure.attach("单个日志文件大小不超过100M")
        
#         assert len(failed) == 0,f"单个日志文件大小超过100M"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348411?projectId=46")
#     @allure.title("日志存储_文件个数_002")
#     def test_caseid_1348411(self):
#         """
#         当个类型文件最多有10个
#         """
#         failed = []
#         data = TCAM_SSH().exec(cmd="ls -lh /mnt/sdcard/log/| grep jetlog_messages | wc -l", bgm_ip=ip).strip()
#         if int(data) > 10:
#             failed.append(data)

#         with allure.step(f"check日志文件的个数:"):
#             allure.attach(f"日志文件的个数为: {data}")
        
#         assert len(failed) == 0,f"日志文件的个数超过10个"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1348413?projectId=46")
#     @allure.title("日志存储_日志文件名_001")
#     def test_caseid_1348413(self):
#         """
#         查看日志文件名: TCAM:jetlog_messages
#         """
#         failed = []
#         data1 = TCAM_SSH().exec(cmd="ls /mnt/sdcard/log/| grep jetlog_messages", bgm_ip=ip).split('\n')
#         data = [j for j in data1 if j != '']
#         for i in data:
#             if "jetlog_messages" not in i:
#                 failed.append(i)

#         with allure.step(f"check日志文件名:"):
#             allure.attach(f"日志文件名为: {data}")
        
#         assert len(failed) == 0,f"日志文件名错误"

#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1435133?projectId=46")
#     @allure.title("日志存储_存储大小_001")
#     def test_caseid_1435133(self):
#         """
#         查看日志文件名: jetlog_messages占用的磁盘空间
#         """
#         data1 = TCAM_SSH().exec(cmd="ls -lh /mnt/sdcard/log/| grep jetlog_messages | awk '{print $5}'", bgm_ip=ip).split('\n')
#         data = [j for j in data1 if j != '']
#         j = 0
#         for i in data:
#             j = j + int(i.strip().split('.')[0])

#         with allure.step(f"check日志存储大小:"):
#             allure.attach(f"日志存储大小为: {j}")
        
#         assert j <= 1000,f"日志文件名错误"

# if __name__ == '__main__':
#     pytest.main()
