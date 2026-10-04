#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/12/12 11:12  
@Author: lei.tao
@File: jetlog_check.py
@Software: PyCharm
@Description: 
@Example: 
"""
import pytest
import paramiko
import os
import sys

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger


class Test_mqtt(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.obdip()
        print(ip)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        os.system("ps -ef|grep -i ssh|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i ssh")
        logger.debug("清除所有ssh进程")
        super().after_class(self, ecu)


    def con_bgm(self, cmd):
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connection.connect(hostname=ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____JETLOG_CHECK_TOOLS_JETLOG_LINUX_PY_PASSWORD', ""))
        stdin, stdout, stderr = connection.exec_command(cmd)
        data = stdout.read().decode('utf-8')
        connection.close()
        return data


    def con_tcam(self, cmd):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____JETLOG_CHECK_TOOLS_JETLOG_LINUX_PY_PASSWORD', ""))
        transport = conn.get_transport()
        dest_addr = ("172.16.5.31", 22)
        local_addr = (ip, 22)
        channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

        conn1 = paramiko.SSHClient()
        conn1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn1.connect(hostname="172.16.5.31", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____JETLOG_CHECK_TOOLS_JETLOG_LINUX_PY_PASSWORD', ""), sock=channel)

        stdin, data, error = conn1.exec_command(cmd)
        return data.read().decode('utf-8')

    def test_bgm(self):
        jet_failed = []
        bgm = {
            'arbitrate_mgr': ['ARB_C', 'ARB_MGR'], 'calibration': ['CALI_SV'], 'certificate_manager': ['CERT_SERVICE'],
            'em': ['EM'], 'fota': ['fota'], 'power_mgr': ['PWMGR', 'PWIMP'], 'propservice': ['prop'],
            'remote_vehicle_status': ['RemoteVehicleStatus'], 'ua': ['update_agent_service'], 'uds_server': ['UDSM'],
            'v2t_sync_engine': ['sync'], 'vehicle_time': ['vehicle_time'],
            'obt': ['OBTService', 'OBT_RECEIVER', 'OBTCL', 'OBT_Update', 'OBTDM'], 'config_service': ['confS', 'confC'],
            'etcm_service': ['etc'], 'vehicle_setting_service': ['vehSetting']
        }
      
        for k, w in bgm.items():
            if len(w) == 1:
                for i in w:
                    data = self.con_bgm(cmd="cat /log/jetlog_messages | awk '{print $6}'" + f"| grep {i}")
                    if not data:
                        jet_failed.append(k)
                        print(f'没有查询到{k}模块日志记录的{i}标签')
                    else:
                        print(f'查询到{k}模块日志记录的{i}标签')
            else:
                success = []
                for i in w:
                    data = self.con_bgm(cmd="cat /log/jetlog_messages | awk '{print $6}'" + f"| grep {i}")
                    if data:
                        success.append(i)
                        print(f'查询到{k}模块日志记录的{i}标签')
                        break
                    else:
                        print(f'没有查询到{k}模块日志记录的{i}标签')
                        continue
                if len(success) == 0:
                    jet_failed.append(k)     

        print(f"BGM065版本日志记录的tag检查有误的模块是：{jet_failed}")
        assert len(jet_failed) == 0

    def test_tcam(self):
        jet_failed = []
        tcam = {'ecall': ['eCall'], 'gb32960': ['gb'], 'gnss_service': ['gnss'], 'misc': ['misc'],
                'net_status_service': ['netstatus'], 'rcv': ['remoteCtrl'], 'rtc': ['reserve'],
                'ua': ['ua_service'], 'v2t_connect_service': ['v2tl', 'mqtt'], 'config_service': ['confS', 'confC'],
                'em': ['EM'], 'power_manager': ['power'], 'propservice': ['prop'], 'tee': ['SECO']}
        for k, w in tcam.items():
            if len(w) == 1:
                for i in w:
                    data = self.con_tcam("cat /mnt/sdcard/log/jetlog_messages | awk '{print $6}'" + f" | grep {i}")
                    if not data:
                        jet_failed.append(k)
                        print(f'没有查询到{k}模块日志记录的{i}标签')
                    else:
                        print(f'查询到{k}模块日志记录的{i}标签')
            else:
                success = []
                for i in w:
                    data = self.con_tcam("cat /mnt/sdcard/log/jetlog_messages | awk '{print $6}'" + f" | grep {i}")
                    if data:
                        success.append(i)
                        print(f'查询到{k}模块日志记录的{i}标签')
                        break
                    else:
                        print(f'没有查询到{k}模块日志记录的{i}标签')
                        continue
                if len(success) == 0:
                    jet_failed.append(k) 

        print(f"TCAM065版本日志记录的tag检查有误的模块是：{jet_failed}")
        assert len(jet_failed) == 0


if __name__ == '__main__':
    pytest.main(['-vs', 'jetlog_linux.py'])
