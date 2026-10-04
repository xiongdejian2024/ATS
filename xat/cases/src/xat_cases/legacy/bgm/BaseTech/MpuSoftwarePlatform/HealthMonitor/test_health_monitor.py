#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : tmp.py
@time         : 2024/05/07 16:44
@author       : o_lijing.pan@external.jiduauto.com
@description  : 健康监控  
'''

import re
import json
import allure
import pytest
import datetime
from xat_ecu.api.abc_interface import *
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.common.logmanagment.logmanager import logger


class Test_Health_Monitor(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("初始化环境")
        self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        logger.info("case开始运行*******************************************************")
 
    def after_each_func(self, ecu):
        logger.info("case结束运行*******************************************************")
        self.ssh.set_airplane_mode(isOn.Off)
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")
    
    @pytest.mark.smoke
    @allure.title("主动上报系统状态内容")
    def test_caseid_1984968(self):
        jtd = []
        std_start_key = "time"
        time_sync_key = "use"
        mem_key = ["buff", "cached", "free", "used"]
        disk_info_key = ["app", "data", "dev", "dev_shm", "etc_machine_id","log", "mnt", "root", "run", "sys_fs_cgroup", "tmp", "update"]
        cpu_load_key = ["idle", "io", "irq", "nic", "sys", "user"]
        search_key = ["mem", "disk_info", "cpu_load", "std_start", "time_sync"]
        cmds = [f"grep {k} /data/monitor_agent/metric_data.log | head -1" for k in search_key]
        self.sd_tester.reset_bgm()
        sleep(10)

        for cmd in cmds:
            result = self.ssh.bgm_ssh.type_commands(cmd)
            assert result, f"命令：{cmd}返回值为空"
            jtd.append(json.loads(result))

        for k in mem_key:
            assert jtd[0]["v"][k] != "", f"{jtd[0]}的{k}没有数据"
        for k in disk_info_key:
            assert jtd[1]["v"][k] != "", f"{jtd[1]}的{k}没有数据"
        for k in cpu_load_key:
            assert jtd[2]["v"][k] != "", f"{jtd[2]}的{k}没有数据"
        assert jtd[3]["v"][std_start_key] != "", f"{d}的{std_start_key}没有数据"
        assert jtd[4]["v"][time_sync_key] != "", f"{d}的{time_sync_key}没有数据"

    @pytest.mark.Sanity
    @allure.title("数据统计间隔时间")
    def test_caseid_1984967(self):
        result = self.ssh.bgm_ssh.type_commands("grep 'mem' /data/monitor_agent/metric_data.log | head -2")
        ts = re.findall(r'\d{10}', result)
        interval = int(ts[1]) - int(ts[0])
        assert interval == 10, f"相邻两次统计数据的时间{interval} != 10s"

    @pytest.mark.Sanity
    @allure.title("主动上报系统状态上传周期")    
    def test_caseid_1984966(self):
        self.ssh.type_commands(DeviceName.BGM, "ping c -1 acu-monitor-staging.jiduapp.cn")
        ts = ''
        cmd = '/app/bin/zstdcat /log/jetlog_messages |grep "url:https://acu-monitor-staging.jiduapp.cn/api/acu-monitor/api/v2/monitor/metricPush" | tail -2'
        # cmd = '/app/bin/zstdcat /log/jetlog_messages | grep "str size" | grep "mem" | grep -v "error_code" | tail -2'
        str_size = self.ssh.type_commands(DeviceName.BGM,cmd)
        if len(str_size) < 2:
            logger.info(f"str_size长度{len(str_size)}")
            sleep(400)
            str_size = self.ssh.type_commands(DeviceName.BGM,cmd)
        ts = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}\S\d{2}\S\d{2}', str_size)
        logger.info(f"ts结果:{ts}")
        convert_ts = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in ts]
        interval = (convert_ts[1] - convert_ts[0]).seconds
        logger.info(f"上传周期:{interval}")
        assert 170 <= interval <= 190, f"上传周期{interval}不在170到190s之间"

    @pytest.mark.full
    @allure.title("持久化数据_断网无法上传")  
    def test_caseid_1984961(self):
        self.ssh.set_airplane_mode(isOn.On)
        time.sleep(5)
        ping_result = self.mix.chk_bgm_ping()
        if ping_result[0] == 'BGM不能联网':
            cmd_result = self.ssh.bgm_ssh.type_commands("ls /data/monitor_agent/metric_data.log")
            assert 'No such' not in cmd_result, "文件metric_data.log丢失"
        else:
            assert False

    @pytest.mark.full
    @allure.title("重启查看持久化信息")  
    def test_caseid_1984958(self):
        data_lines = self.ssh.bgm_ssh.type_commands("wc -l /data/monitor_agent/metric_data.log")
        data_lines = data_lines.split(" ")[0]
        self.sd_tester.reset_bgm()
        time.sleep(30)
        reboot_data_lines = self.ssh.bgm_ssh.type_commands("wc -l /data/monitor_agent/metric_data.log")
        reboot_data_lines = reboot_data_lines.split(" ")[0]
        assert reboot_data_lines != 0 and reboot_data_lines != data_lines

    @pytest.mark.Sanity
    @allure.title("验证长时间断网后恢复网络，服务性能数据能正常上传")  
    def test_caseid_1984959(self):
        self.ssh.set_airplane_mode(isOn.On)
        time.sleep(180)
        self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(180)
        str_size = self.ssh.bgm_ssh.type_commands('/app/bin/zstdcat /log/jetlog_messages | grep "str size" | grep -v "error_code" | tail -1')
        ts = re.findall(r'"\d{10}', str_size)[0].strip('"')
        exist = self.ssh.bgm_ssh.type_commands(f"grep {ts} /data/monitor_agent/metric_data.log")
        assert exist == "", "数据未上传"