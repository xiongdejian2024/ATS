#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#四域上下电case
#
#

import os
import sys
import time

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
import subprocess
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import DiagTestBase
from xat_ecu.legacy.driver.adb_client import Adb
from xat_cases.legacy.soa.case_helper.soa.pre_build import *


global a, b, c
# a为诊断上下电的次数，b为多域上下电的次数，c为进程重启后其他域的客户端服务端连接成功的次数
a = 1
b = 1
c = 1

@allure.feature("性能稳定性")
@allure.story("业务稳定性/交叉上下电服务连接稳定性")
@pytest.mark.full
class Test_Power_up_down(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # 环境准备 只需要执行一次
        logger.info("环境准备")
        init_pre(self.nucapp)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        logger.info("检查磁盘剩余空间")
        init_disk()
      
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        reset_env()


# ============================== 诊断四域上下电 case ===========================

    @pytest.mark.smoke
    @allure.title(f"诊断四域同时上下电{a}次")
    def test01_caseid_1913747(self):
        data=[
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "cdc",
                    "bgm",
                    "acu",
                    "tcam",
                    "sleep(300)"
                ],
                "times": a,
                "space": 6,
                "title": f"诊断四域同时上下电{a}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu, sd=True)
        logger.info(msg)
        assert ret,msg
        
    @pytest.mark.smoke
    @allure.title(f"诊断单域bgm上下电{a}次")
    def test02_caseid_1913748(self):
        data=[
            {
                "poweroff": [
                    "bgm",
                ],
                "poweron": [
                    "bgm",
                    "sleep(60)"
                ],
                "times": a,
                "space": 6,
                "title": f"诊断单域bgm上下电{a}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu, sd=True)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"诊断单域tcam上下电{a}次")
    def test03_caseid_1913749(self):
        data=[
            {
                "poweroff": [
                    "tcam",
                ],
                "poweron": [
                    "tcam",
                    "sleep(300)"
                ],
                "times": a,
                "space": 6,
                "title": f"诊断单域tcam上下电{a}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu, sd=True)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"诊断单域acu上下电{a}次")
    def test04_caseid_1913750(self):
        data=[
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    "acu",
                    "sleep(180)"
                ],
                "times": a,
                "space": 6,
                "title": f"诊断单域acu上下电{a}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu, sd=True)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"诊断单域cdc上下电{a}次")
    def test05_caseid_1913751(self):
        data=[
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    "cdc",
                    "sleep(60)"
                ],
                "times": a,
                "space": 6,
                "title": f"诊断单域cdc上下电{a}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu, sd=True)
        logger.info(msg)
        assert ret,msg
 

# ============================== 四域进程重启 case ===========================
    
    def bgm(self):
        bgm_addr = get_obd_ip()
        config = get_config_info()
        for i in range(c):
            logger.info(f"第{i+1}次检测进程s2s_service重启后，其他域控客户端服务端正常连接的测试")
            cmd = f"sshpass -p {config['bgm_pwd']} ssh -o StrictHostKeyChecking=no {config['bgm_uname']}@{bgm_addr} ps -ef| grep s2s_service| grep -v grep| " + "awk '{print $2}'"
            pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='utf-8').communicate()[0].strip()
            logger.info(f"进程s2s_service的pid为: {pid}")
            if pid:
                logger.info("进程s2s_service已启动")
            logger.info("关闭s2s_service进程")

            kill_cmd = f"sudo kill -9 {pid}"
            from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
            BGM_SSH(bgm_addr).type_commands(kill_cmd)
            time.sleep(20)
            logger.info("20s后再次检测s2s_service进程是否重启")
            new_pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
            if new_pid:
                logger.info("进程s2s_service已重新启动")
            else:
                assert 0, "进程s2s_service重启失败"

    def tcam(self, devices="99c4cd39"):
        # v2trouter, em2
        config = get_config_info()
        for i in range(c):
            logger.info(f"第{i+1}次检测进程v2trouter重启后，其他域控客户端服务端正常连接的测试")
            cmd = "ps -ef| grep v2trouter| grep -v grep| awk '{print $1}'"
            pid = Adb(serialno=devices).shell(args=cmd, pwd=config['tcam_pwd']).strip()
            logger.info(f"进程v2trouter的pid为: {pid}")
            if pid:
                logger.info("进程v2trouter已启动")
            logger.info("关闭v2trouter进程")
            from pexpect import spawn, EOF
            kill_cmd = f"kill -9 {pid}"
            Adb(serialno=devices).shell(kill_cmd, config['tcam_pwd'])
            logger.info("v2trouter进程已杀死")
            time.sleep(10)
            logger.info("10s后再次检测v2trouter进程是否重启")
            new_pid = Adb(serialno=devices).shell(cmd, config['tcam_pwd']).strip()
            logger.info(f"进程v2trouter重启后的pid为: {new_pid}")
            if new_pid:
                logger.info("进程v2trouter已重新启动")
            else:
                assert 0, f"进程v2trouter第{i+1}次重启失败"

    def cdca(self, devices="169.254.19.1:1313"):
        # car_input_service
        for i in range(c):
            logger.info(f"第{i+1}次检测进程car_input_service重启后，其他域控客户端服务端正常连接的测试")
            cmd = "ps -ef| grep car_input_service| grep -v grep"
            data = os.popen(f"adb -s {devices} shell '{cmd}'").read().strip()
            logger.info(f"执行命令结果{data}")
            pid_data = [i for i in data.split(" ") if i != '']
            logger.info(f"获取pid结果{pid_data}")
            if "car_input_service" in data:
                pid = int(pid_data[1])
                logger.info(f"进程car_input_service的pid为: {pid}")
                logger.info("进程car_input_service已启动")
                logger.info("关闭car_input_service进程")
                kill_cmd = f"kill -9 {pid}"
                os.system(f"adb -s {devices} shell '{kill_cmd}'")
            time.sleep(10)
            logger.info("20s后再次检测car_input_service进程是否重启")
            _pid = os.popen(f"adb -s {devices} shell '{cmd}'").read().strip()
            logger.info(f"执行命令结果{_pid}")
            pid_data = [i for i in _pid.split(" ") if i != '']
            logger.info(f"获取pid结果{pid_data}")
            if "car_input_service" in _pid:
                new_pid = int(pid_data[1])
                assert pid != new_pid
                logger.info(f"进程car_input_service已重新启动,进程号为:{new_pid}")
            else:
                assert 0, f"进程car_input_service第{i+1}次重启失败"

    def cdcq(self):
        # car_service
        bgm_addr = get_obd_ip()
        config = get_config_info()
        os.system(f"sshpass -p {config['bgm_pwd']} scp -r {project_root}/xat_cases/legacy/soa/case_helper/cdcq_process_kill.sh {config['bgm_uname']}@{bgm_addr}:~/")
        time.sleep(2)
        os.system(f"sshpass -p {config['bgm_pwd']} ssh {config['bgm_uname']}@{bgm_addr} 'chmod 777 -R /tmp/jiduer/cdcq_process_kill.sh' ")
        for i in range(c):
            logger.info(f"第{i+1}次检测进程car_service重启后，其他域控客户端服务端正常连接的测试")
            os.system(f"sshpass -p {config['bgm_pwd']} ssh {config['bgm_uname']}@{bgm_addr} '/tmp/jiduer/cdcq_process_kill.sh' ")
            time.sleep(2)

    @pytest.mark.smoke
    @allure.title(f"BGM进程s2s_service重启后，其他域控客户端服务端正常连接的测试{c}次")
    def test_bgm_check_caseid_1903470(self):
        data = [
        {
            "poweroff": [
                "sleep(0)"
            ],
            "poweron": [
                "sleep(100)"
            ],
            "times": c,
            "space": 6,
            "title": f"BGM进程s2s_service重启后，校验其他域控客户端服务端是否正常连接"
        }]
        config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version = before(data, self.tc_config, self.ipdu, self.nucapp)
        self.bgm()
        ret,msg = after(self.nucapp,self.tc_config,config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"tcam进程v2trouter重启后，其他域控客户端服务端正常连接的测试{c}次")
    def test_tcam_check_caseid_1903471(self):
        data = [
        {
            "poweroff": [
                "sleep(0)"
            ],
            "poweron": [
                "sleep(100)"
            ],
            "times": c,
            "space": 6,
            "title": f"tcam进程v2trouter重启后，校验其他域控客户端服务端是否正常连接"
        }]
        config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version = before(data, self.tc_config, self.ipdu, self.nucapp)
        self.tcam()
        ret,msg = after(self.nucapp,self.tc_config,config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"cdca进程car_input_service重启后，其他域控客户端服务端正常连接的测试{c}次")
    def test_cdca_check_caseid_1903472(self):
        data = [
        {
            "poweroff": [
                "sleep(0)"
            ],
            "poweron": [
                "sleep(100)"
            ],
            "times": c,
            "space": 6,
            "title": f"cdca进程car_input_service重启后，校验其他域控客户端服务端是否正常连接"
        }]
        config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version = before(data, self.tc_config, self.ipdu, self.nucapp)
        time.sleep(10)
        self.cdca()
        ret,msg = after(self.nucapp,self.tc_config,config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.smoke
    @allure.title(f"cdcq进程car_service重启后，其他域控客户端服务端正常连接的测试{c}次")
    def test_cdcq_check_caseid_1984125(self):
        data = [
        {
            "poweroff": [
                "sleep(0)"
            ],
            "poweron": [
                "sleep(100)"
            ],
            "times": c,
            "space": 6,
            "title": f"cdcq进程car_service重启后，校验其他域控客户端服务端是否正常连接"
        }]
        config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version = before(data, self.tc_config, self.ipdu, self.nucapp)
        self.cdcq()
        ret,msg = after(self.nucapp,self.tc_config,config,bgm_addr,cdca_addr,file_path,file_name,bgm_version,cdca_version,tcam_version,acu_version)
        logger.info(msg)
        assert ret,msg


    # acu域pavaro，kill后暂不支持自动重启，暂搁置




# ============================== 四域上下电 case ===========================

    @pytest.mark.smoke
    @allure.title(f"四域同时上下电{b}次")
    def test_00_caseid_111680(self):
        data=[
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "cdc",
                    "bgm",
                    "acu",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"四域同时上下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg


# ============================== 单域上下电 case ===========================
    @pytest.mark.smoke
    @allure.title(f"BGM上电后下电{b}次")
    def test_01_caseid_111679(self):
        data=[
            {
                "poweroff": [
                    "bgm",
    
                ],
                "poweron": [
    
                     "bgm",
                     "sleep(60)"
    
                ],
                "times": b,
                "space": 6,
                "title": f"BGM上电后下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.repeat(5)
    @pytest.mark.sanity
    @allure.title(f"BGM间隔1-5秒连续上下电{b}次")
    def test_02_caseid_111678(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data=[
            {
                "poweroff": [
                    "bgm",

                ],
                "poweron": [
                    f"sleep({i})",
                    "bgm",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM间隔{i}秒连续上下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.repeat(15)
    @pytest.mark.sanity
    @allure.title(f"BGM间隔6-20秒连续上下电{b}次")
    def test_02_caseid_111677(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data=[
            {
                "poweroff": [
                    "bgm",

                ],
                "poweron": [
                    f"sleep({5+i})",
                    "bgm",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM间隔{5+i}秒连续上下电{b}次"
                }
        ]
        ret,msg=start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret,msg

    @pytest.mark.sanity
    @allure.title(f"BGM间隔60秒连续上下电{b}次")
    def test_03_caseid_111676(self):
        data = [
            {
                "poweroff": [
                    "bgm",

                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM间隔60秒连续上下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.smoke
    @allure.title(f"TCAM上电后立马下电{b}次")
    def test_04_caseid_111675(self):
        data = [
            {
                "poweroff": [
                    "tcam",

                ],
                "poweron": [
                    "tcam",
                    "sleep(300)"

                ],
                "times": b,
                "space": 6,
                "title": f"TCAM上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(5)
    @pytest.mark.sanity
    @allure.title(f"TCAM上电1-5秒后再下电{b}次")
    def test_05_caseid_111674(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "tcam",
                ],
                "poweron": [
                    f"sleep({i})",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM上电{i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(15)
    @pytest.mark.sanity
    @allure.title(f"TCAM上电6-20秒后再下电{b}次")
    def test_06_caseid_111673(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "tcam",
                ],
                "poweron": [
                    f"sleep({5+i})",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM上电{5+i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.sanity
    @allure.title(f"TCAM上电60秒后再下电{b}次")
    def test_07_caseid_111672(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                ],
                "poweron": [
                    "sleep(60)",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM上电60秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.smoke
    @allure.title(f"ACU上电后立马下电{b}次")
    def test_08_caseid_111671(self):
        data = [
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    "sleep(0)",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"ACU上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(5)
    @pytest.mark.sanity
    @allure.title(f"ACU上电1-5秒后再下电{b}次")
    def test_09_caseid_111670(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    f"sleep({i})",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"ACU上电{i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(15)
    @pytest.mark.sanity
    @allure.title(f"ACU上电6-20秒后再下电{b}次")
    def test_10_caseid_111669(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    f"sleep({5+i})",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"ACU上电{5+i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.sanity
    @allure.title(f"ACU上电60秒后再下电{b}次")
    def test_11_caseid_111668(self):
        data = [
            {
                "poweroff": [
                    "acu",
                ],
                "poweron": [
                    "sleep(60)",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"ACU上电60秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.smoke
    @allure.title(f"CDC上电后立马下电{b}次")
    def test_12_caseid_111667(self):
        data = [
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    "sleep(0)",
                    "cdc",
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC上电后立马下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(5)
    @pytest.mark.sanity
    @allure.title(f"CDC上电1-5秒后再下电{b}次")
    def test_13_caseid_111666(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    f"sleep({i})",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC上电{i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.repeat(15)
    @pytest.mark.sanity
    @allure.title(f"CDC上电6-20秒后再下电{b}次")
    def test_14_caseid_111665(self, request):
        i = int(request.node.name.split('[')[1].split('-')[0])
        data = [
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    f"sleep({5+i})",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC上电{5+i}秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @pytest.mark.sanity
    @allure.title(f"CDC上电60秒后再下电{b}次")
    def test_15_caseid_111664(self):
        data = [
            {
                "poweroff": [
                    "cdc",
                ],
                "poweron": [
                    "sleep(60)",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"CDC上电60秒后再下电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg




# ============================== 两域上下电 case ===========================

    @allure.title(f"BGM、ACU两域下电0秒后再上电{b}次")
    def test_16_caseid_111659(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "acu"
                ],
                "poweron": [

                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、ACU两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、ACU两域下电5秒后再上电{b}次")
    def test_17_caseid_111658(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "acu"
                ],
                "poweron": [
                    "sleep(5)",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、ACU两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、ACU两域下电20秒后再上电{b}次")
    def test_18_caseid_111657(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "acu"
                ],
                "poweron": [
                    "sleep(20)",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、ACU两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、ACU两域下电60秒后再上电{b}次")
    def test_19_caseid_111656(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "acu"
                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "acu",
                    "sleep(300)",
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、ACU两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC两域下电0秒后再上电{b}次")
    def test_20_caseid_111655(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",

                ],
                "poweron": [
                    "bgm",
                    "cdc",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC两域下电5秒后再上电{b}次")
    def test_21_caseid_111654(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",

                ],
                "poweron": [
                    "sleep(5)",
                    "bgm",
                    "cdc",
                    "sleep(60)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC两域下电20秒后再上电{b}次")
    def test_22_caseid_111653(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "sleep(10)",
                    "cdc",

                ],
                "poweron": [
                    "sleep(20)",
                    "bgm",
                    "cdc",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC两域下电60秒后再上电{b}次")
    def test_23_caseid_111652(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",

                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "cdc",
                    "sleep(60)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM两域下电0秒后再上电{b}次")
    def test_24_caseid_111663(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",

                ],
                "poweron": [
                    "bgm",
                    "tcam",
                    "sleep(300)"

                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg


    @allure.title(f"BGM、TCAM两域下电5秒后再上电{b}次")
    def test_25_caseid_111662(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",

                ],
                "poweron": [
                    "sleep(5)",
                    "bgm",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM两域下电20秒后再上电{b}次")
    def test_26_caseid_111661(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",

                ],
                "poweron": [
                    "sleep(20)",
                    "bgm",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM两域下电60秒后再上电{b}次")
    def test_27_caseid_111660(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",

                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "tcam",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、ACU两域下电0秒后再上电{b}次")
    def test_28_caseid_111651(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "acu",

                ],
                "poweron": [
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、ACU两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、ACU两域下电5秒后再上电{b}次")
    def test_29_caseid_111650(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "acu",

                ],
                "poweron": [
                    "sleep(5)",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、ACU两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg


    @allure.title(f"TCAM、ACU两域下电20秒后再上电{b}次")
    def test_30_caseid_111649(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "acu",

                ],
                "poweron": [
                    "sleep(20)",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、ACU两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、ACU两域下电60秒后再上电{b}次")
    def test_31_caseid_111648(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "acu",

                ],
                "poweron": [
                    "sleep(60)",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、ACU两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC两域下电0秒后再上电{b}次")
    def test_32_caseid_111647(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "cdc",

                ],
                "poweron": [
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC两域下电5秒后再上电{b}次")
    def test_33_caseid_111646(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "cdc",

                ],
                "poweron": [
                    "sleep(5)",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC两域下电20秒后再上电{b}次")
    def test_34_caseid_111645(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "cdc",

                ],
                "poweron": [
                    "sleep(20)",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC两域下电60秒后再上电{b}次")
    def test_35_caseid_111644(self):
        data = [
            {
                "poweroff": [
                    "tcam",
                    "cdc",

                ],
                "poweron": [
                     "sleep(60)",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"ACU、CDC两域下电0秒后再上电{b}次")
    def test_36_caseid_111643(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "cdc",

                ],
                "poweron": [
                    "acu",
                    "cdc",
                    "sleep(300)",
                ],
                "times": b,
                "space": 6,
                "title": f"ACU、CDC两域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"ACU、CDC两域下电5秒后再上电{b}次")
    def test_37_caseid_111642(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "cdc",

                ],
                "poweron": [
                    "sleep(5)",
                    "acu",
                    "cdc",
                    "sleep(300)",
                ],
                "times": b,
                "space": 6,
                "title": f"ACU、CDC两域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"ACU、CDC两域下电20秒后再上电{b}次")
    def test_38_caseid_111641(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "cdc",

                ],
                "poweron": [
                    "sleep(20)",
                    "acu",
                    "cdc",
                    "sleep(300)",
                ],
                "times": b,
                "space": 6,
                "title": f"ACU、CDC两域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"ACU、CDC两域下电60秒后再上电{b}次")
    def test_39_caseid_111640(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "cdc",

                ],
                "poweron": [
                    "sleep(60)",
                    "acu",
                    "cdc",
                    "sleep(300)",

                ],
                "times": b,
                "space": 6,
                "title": f"ACU、CDC两域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg



# ============================== 三域上下电 case ===========================


    @allure.title(f"BGM、CDC、ACU三域下电0秒后再上电{b}次")
    def test_40_caseid_111639(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "cdc",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC、ACU三域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC、ACU三域下电5秒后再上电{b}次")
    def test_41_caseid_111638(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "sleep(5)",
                    "cdc",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC、ACU三域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC、ACU三域下电20秒后再上电{b}次")
    def test_42_caseid_111637(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "sleep(20)",
                    "cdc",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC、ACU三域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、CDC、ACU三域下电60秒后再上电{b}次")
    def test_43_caseid_111636(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "cdc",
                    "acu"
                ],
                "poweron": [
                    "sleep(60)",
                    "cdc",
                    "bgm",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、CDC、ACU三域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、ACU三域下电0秒后再上电{b}次")
    def test_44_caseid_111631(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "acu"
                ],
                "poweron": [
                    "sleep(0)",
                    "bgm",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、ACU三域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、ACU三域下电5秒后再上电{b}次")
    def test_45_caseid_111630(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "acu"
                ],
                "poweron": [
                    "sleep(5)",
                    "bgm",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、ACU三域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、ACU三域下电20秒后再上电{b}次")
    def test_46_caseid_111629(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "acu"
                ],
                "poweron": [
                    "sleep(20)",
                    "bgm",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、ACU三域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、ACU三域下电60秒后再上电{b}次")
    def test_47_caseid_111628(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "acu"
                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "tcam",
                    "acu",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、ACU三域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、CDC三域下电0秒后再上电{b}次")
    def test_48_caseid_111635(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(0)",
                    "bgm",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、CDC三域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、CDC三域下电5秒后再上电{b}次")
    def test_49_caseid_111634(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(5)",
                    "bgm",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、CDC三域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、CDC三域下电20秒后再上电{b}次")
    def test_50_caseid_111633(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(20)",
                    "bgm",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、CDC三域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"BGM、TCAM、CDC三域下电60秒后再上电{b}次")
    def test_51_caseid_111632(self):
        data = [
            {
                "poweroff": [
                    "bgm",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(60)",
                    "bgm",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"BGM、TCAM、CDC三域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC、ACU三域下电0秒后再上电{b}次")
    def test_52_caseid_111627(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(0)",
                    "acu",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC、ACU三域下电0秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC、ACU三域下电5秒后再上电{b}次")
    def test_53_caseid_111626(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(5)",
                    "acu",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC、ACU三域下电5秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC、ACU三域下电20秒后再上电{b}次")
    def test_54_caseid_111625(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(20)",
                    "acu",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC、ACU三域下电20秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg

    @allure.title(f"TCAM、CDC、ACU三域下电60秒后再上电{b}次")
    def test_55_caseid_111624(self):
        data = [
            {
                "poweroff": [
                    "acu",
                    "tcam",
                    "cdc"
                ],
                "poweron": [
                    "sleep(60)",
                    "acu",
                    "tcam",
                    "cdc",
                    "sleep(300)"
                ],
                "times": b,
                "space": 6,
                "title": f"TCAM、CDC、ACU三域下电60秒后再上电{b}次"
            }
        ]
        ret, msg = start_pre(data, self.nucapp, self.tc_config, self.ipdu)
        logger.info(msg)
        assert ret, msg