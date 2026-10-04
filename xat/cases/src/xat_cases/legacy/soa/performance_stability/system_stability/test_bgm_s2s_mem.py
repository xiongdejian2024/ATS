# -*- coding: utf-8 -*-
"""
@File        : test_bgm_check.py
@Author      : lei.tao@jiduatuo.com
@Time        : 2023/05/10 15:00 PM
@Description : 检测S2S的内存稳定性
"""
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import pytest
import allure
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.cdc.cdcq_ssh import CDCQ_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.interface.cdc.cdca_adb import CDCA_ADB
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.driver.ssh_interface import command_send


@allure.feature("性能稳定性")
@allure.story("系统稳定性/内存占用")
class TestS2SRes(TestBase):
    def hander_top(self, bgm_cpu_file):
        result_list = []
        with open(bgm_cpu_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if "s2s_ser+" in line:
                    result = [i.strip() for i in line.strip().split(' ') if i.strip()]
                    res = float(result[5])
                    if res not in result_list:
                        result_list.append(int(res))
        logger.info(f"进程重启后，s2s内存{result_list}")
        if len(result_list) < 120:
            return True
        else:
            for i in range (len(result_list)-1):
                if result_list[i+1] <= result_list[i]:
                    logger.info("进程重启后，s2s内存没有出现持续增长现象")
                    return True
            else:
                return False
    
    def get_s2s_res(self, domain, process, timeout=60*60):
        bgm = BGM_SSH()
        bgm.type_commands(commands="(top -b|grep s2s_service) > /data/s2s_res.txt &")
        t = time.time()
        while time.time()- t < timeout:
            if 'BGM' in str(domain):
                domain.type_commands(commands=f"ps -ef|grep -i {process}|grep -v grep"+"""|awk '{printf $2}'|xargs kill -9""")
            elif 'TCAM' in str(domain):
                domain.type_commands(commands=f"ps -ef|grep -i {process}|grep -v grep"+"""|awk '{printf $1}'|xargs kill -9""")
            elif 'CDCQ' in str(domain):
                domain.type_commands(commands=f"pidin | grep {process} | grep -v grep | awk 'NR == 1'| cut -d ' ' -f 2|xargs kill -9")
            else:
                domain.type_commands(commands=f"ps -ef|grep -i {process}|grep -v grep"+"""|awk '{printf $2}'|xargs kill -9""")
            time.sleep(30)
        else:
            cmd = "ps -ef | grep top | grep -v grep | awk '{print $2}' | xargs kill -9"
            bgm.type_commands(cmd, timeout=10)
        with allure.step(f"校验是否有coredump文件："):
            coredump_list = bgm.get_bgm_coredump()
            if len(coredump_list) != 0:
                logger.info(f"获取coredump文件>>>{coredump_list}")
                assert False,f"有coredump文件产生{coredump_list}"
        local_path = os.path.dirname(__file__)
        bgm_cpu_file = bgm.scp_bgm_log_to_local("s2s_res.txt",log_path=local_path,save_log_name=None,del_flag=True,path="/data")
        # 处理数据
        flag = self.hander_top(bgm_cpu_file)
        os.system(f"rm -rf {bgm_cpu_file}")
        return flag

    @pytest.mark.soa
    @allure.title("bgm域控rke进程重启，s2s内存保持不变")
    def test_caseid_1985142(self):
        bgm = BGM_SSH()
        flag = self.get_s2s_res(bgm, "/app/bin/rke")
        assert flag,f"bgm域控rke进程重启后，s2s内存出现持续增长现象"

    @pytest.mark.soa
    @allure.title("tcam域控v2trouter进程重启，s2s内存保持不变")
    def test_caseid_1985141(self):
        tcam = TCAM_SSH()
        flag = self.get_s2s_res(tcam, "/oemapp/bin/v2trouter")
        assert flag,f"tcam域控v2trouter进程重启后，s2s内存出现持续增长现象"

    @allure.title("cdc域控a侧进程car_input_service重启，s2s内存保持不变")
    def test_caseid_1985140(self):
        cdca = CDCA_ADB()
        flag = self.get_s2s_res(cdca, "car_input_service")
        assert flag,f"cdc域控a侧进程car_input_service后，s2s内存出现持续增长现象"


    @allure.title("cdc域控a侧进程car_serivce重启，s2s内存保持不变")
    def test_caseid_1985139(self):
        cdcq = CDCQ_SSH()
        flag = self.get_s2s_res(cdcq, "car_serivce")
        assert flag,f"cdc域控a侧进程car_serivce后，s2s内存出现持续增长现象"


LOGMASTER_SERVICE_CLIENT = "AcuSentryManagerService_server"

@allure.feature("SOA服务接口")
@allure.story("架构基础/LogMasterService")
class TestLogMasterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("AcuSentryManagerService", "server")], domin="bgm")
        self.partner.method_default_timeout = 10
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文

    def before_each_func(self, ecu):
        super().before_each_func(self, ecu)
        logger.info(f"case开始运行")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行")
        super().after_each_func(self, ecu)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def get_acu_manager(self):
        command_send(device_name="ACU",cmd="sudo top -b -d 1 -c -w 512 -i | grep acu_manager > /opt/data/acu_manager.txt")

    @pytest.mark.smoke
    @allure.title("常规模式和哨兵模式互切一小时，检查acu_manager进程是否有内存泄漏")
    def test_caseid_1988858(self): 
        data_now = time.time()
        threading.Thread(target=self.get_acu_manager, args=())
        while time.time() - data_now < 10*60:
            self.partner.send_event_notify(LOGMASTER_SERVICE_CLIENT, "NotifySentryManagerReq", {"req":1})
            command_send(device_name="ACU",alias="1", expect="mode 0", cmd="tail -f /opt/log/jidu_output/acu_manager/acu_mode_manager.log")
            time.sleep(30)
            command_send(device_name="ACU",alias="2", expect="mode 2", cmd="tail -f /opt/log/jidu_output/acu_manager/acu_mode_manager.log")
            self.partner.send_event_notify(LOGMASTER_SERVICE_CLIENT, "NotifySentryManagerReq", {"req":2})
            command_send(device_name="ACU",alias="3", expect="mode 2", cmd="tail -f /opt/log/jidu_output/acu_manager/acu_mode_manager.log")
            time.sleep(30)
            command_send(device_name="ACU",alias="4", expect="mode 0", cmd="tail -f /opt/log/jidu_output/acu_manager/acu_mode_manager.log")