#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :ssh通信能力模拟 实现接口
"""
import time

from xat_ecu.api.interfaces.dp2.base_common.ssh import Ssh as BaseSsh
from xat_ecu.legacy.common.logger import logger


class Ssh(BaseSsh):
    def export_env(self, env=None):
        if env is not None:
            self.cd_soc.type_commands(f"{env}")
        else:
            self.cd_soc.type_commands("export BOOTES_HOME_DIR=/mnt/etc/soa/common && export LD_LIBRARY_PATH=/mnt/lib64:/mnt/ifs/lib64")

    def run_log_j(self):
        self.run_ccucd_soc_process("log_j")
    
    def run_service_monitor(self):
        self.run_ccucd_soc_process("service_monitor")
    
    def run_car_service(self):
        self.run_ccucd_soc_process("car_service")
    
    def run_dumper(self):
        self.run_ccucd_soc_process("dumper")
    
    def is_process_running(self, process_name):
        ret = self.cd_soc.type_commands(f"pidin arg | grep {process_name} | grep -v grep " + "| awk '{print $1}'", timeout=0)
        if "\n" in ret:  # 如果有换行符，说明返回带之前的结果需要注意判别
            pid = ret.split("\n")[0].split()[0]
            if pid.isdigit():
                return True, int(pid)
            else:
                return False, None
        elif ret:
            pid = ret.split()[0]
            if pid.isdigit():
                return True, int(pid)
            else:
                return False, None
        else:
            return False, None
    
    def run_ccucd_soc_process(self, process_name):
        process_cmd = {"dumper": "cd /mnt/bin && ./dumper &", 
                       "log_j": "cd /mnt/bin && ./log_j &",
                       "service_monitor": "cd /mnt/bin && ./service_monitor -c /mnt/etc/soa/common/service_monitor.json &", 
                       "car_service":"cd /mnt/bin && ./car_service &"}
        if process_name not in process_cmd:
            raise ValueError(f"Invalid process name: {process_name}, please check your input.")
        is_running, pid = self.is_process_running(process_name)
        if is_running:
            logger.info(f"{process_name} is running, pid: {pid}")
        else:
            logger.info(f"{process_name} is not running, start it now...")
            self.cd_soc.type_commands(process_cmd[process_name], timeout=0)
    
    def service_sil_test_preparation(self):
        self.export_env()
        self.run_dumper()
        self.run_log_j()
        self.run_service_monitor()
        self.run_car_service()
    
    def kill_ccucd_soc_process(self, pid):
        self.cd_soc.type_commands(f"kill -9 {pid}", timeout=0)
        
    def rerun_process(self, process_name, sleep_time=5):
        is_running, pid = self.is_process_running(process_name)
        if is_running:
            self.kill_ccucd_soc_process(pid)
            time.sleep(sleep_time)
            self.run_ccucd_soc_process(process_name)
    
    def rerun_car_service(self, sleep_time=5):
        self.rerun_process("car_service", sleep_time)