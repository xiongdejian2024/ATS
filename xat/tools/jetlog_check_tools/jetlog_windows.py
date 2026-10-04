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
from Powershell import *


class Test_jetlog2(object):

    def test_bgm(self, file_path="./log_folder"):
        jet_failed = []
        bgm = {
            'arbitrate_mgr': ['ARB_C', 'ARB_MGR'], 'calibration': ['CALI_SV'], 'certificate_manager': ['CERT_SERVICE'],
            'em': ['EM'], 'fota': ['fota'], 'power_mgr': ['PWMGR', 'PWIMP'], 'propservice': ['prop'],
            'remote_vehicle_status': ['RemoteVehicleStatus'], 'ua': ['update_agent_service'], 'uds_server': ['UDSM'],
            'v2t_sync_engine': ['sync'], 'vehicle_time': ['vehicle_time'],
            'obt': ['OBTService', 'OBT_RECEIVER', 'OBTCL', 'OBT_Update', 'OBTDM'], 'config_service': ['confS', 'confC'],
            'etcm_service': ['etc'], 'vehicle_setting_service': ['vehSetting']
        }

        file_list = os.listdir(file_path)
        for file in file_list:
            for k, w in bgm.items():
                if len(w) == 1:
                    for i in w:
                        with PowerShell('GBK') as ps:
                            data, error = ps.run(f"type {file} " + "| awk '{print $6}' " + f"| findstr {w}")

                        if not data:
                            jet_failed.append(k)
                            print(f'没有查询到{k}模块日志记录的{i}标签')
                        else:
                            print(f'查询到{k}模块日志记录的{i}标签')
                else:
                    success = []
                    for i in w:
                        with PowerShell('GBK') as ps:
                            data, error = ps.run(f"type {file} " + "| awk '{print $6}' " + f"| findstr {w}")

                        if not data:
                            print(f'没有查询到{k}模块日志记录的{i}标签')
                            continue
                        else:
                            success.append(i)
                            print(f'查询到{k}模块日志记录的{i}标签')
                            break

        print(f"BGM065版本日志记录的tag检查有误的是：{jet_failed}")
        assert len(jet_failed) == 0

    def test_tcam(self, file_path="./log_folder"):
        jet_failed = []
        tcam = {'ecall': ['eCall'], 'gb32960': ['gb'], 'gnss_service': ['gnss'], 'misc': ['misc'],
                'net_status_service': ['netstatus'], 'rcv': ['remoteCtrl'], 'rtc': ['reserve'],
                'ua': ['ua_service'], 'v2t_connect_service': ['v2tl', 'mqtt'], 'config_service': ['confS', 'confC'],
                'em': ['EM'], 'power_manager': ['power'], 'propservice': ['prop'], 'tee': ['SECO']}

        file_list = os.listdir(file_path)
        for file in file_list:
            for k, w in tcam.items():
                if len(w) == 1:
                    for i in w:
                        with PowerShell('GBK') as ps:
                            data, error = ps.run(f"type {file} " + "| awk '{print $6}' " + f"| findstr {w}")

                        if not data:
                            jet_failed.append(k)
                            print(f'没有查询到{k}模块日志记录的{w}标签')
                        else:
                            print(f'查询到{k}模块日志记录的{i}标签')
                else:
                    success = []
                    for i in w:
                        with PowerShell('GBK') as ps:
                            data, error = ps.run(f"type {file} " + "| awk '{print $6}' " + f"| findstr {w}")

                        if not data:
                            print(f'没有查询到{k}模块日志记录的{i}标签')
                            continue
                        else:
                            success.append(i)
                            print(f'查询到{k}模块日志记录的{i}标签')
                            break

            print(f"TCAM065版本日志记录的tag检查有误的是：{jet_failed}")
            assert len(jet_failed) == 0


if __name__ == '__main__':
    pytest.main(['-vs', 'jetlog.py'])
