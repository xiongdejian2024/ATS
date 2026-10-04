

# -*- coding: utf-8 -*-
"""
@File        : test_send1181_to_check_coredump.py
@Author      : lei.tao@jiduatuo.com
@Time        : 2023/05/10 15:00 PM
@Description : S2S进程稳定性
"""
import sys
import os
import pytest
import allure
import time
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import check_bgm_error_log_init, check_bgm_error_log, recover_bgm_log

coredumplis = []


@allure.feature("性能稳定性")
@allure.story("系统稳定性/进程稳定性")
@pytest.mark.soa
class TestBGM_CPU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        check_bgm_error_log_init(self.bgmcli)
        # 超负载随机设置信号增加CPU load
        lin_channel_list = ["cem_lin1", "cem_lin2", "cem_lin3", "cem_lin4", "cem_lin5", "cem_lin6"]
        can_channel_list = [
            "bodycan","propulsioncan","chassiscan1", "chassiscan2", "passivesafetycan",
            "diagnosticcan", "infocanfd", "adcanfd", "bodyalmcanfd1", "connectivitycanfd",
            "bodyexposedcanfd", "bodyalmcanfd2"
        ]
        fr_channel_list = ['backbonefr']
        all_channel = lin_channel_list + can_channel_list + fr_channel_list
        # for name in all_channel:
        #     self.ipdu.set_random_signal_thread_start(name, 100, interval_time=5)
        global coredumplis
        try:
            self.sd_tester.send_data([0x11, 0x81])
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"重启失败==》》{str(e)}")
        time.sleep(40)
        self.coredump_lis = self.bgmcli.get_bgm_coredump()
        coredumplis=self.coredump_lis
        logger.error(f"第一次获取的 coredump 文件=====》》{self.coredump_lis} ")

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        # self.ipdu.set_random_signal_thread_all_stop()
        recover_bgm_log(self.bgmcli)
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")
        super().after_class(self, ecu)

    def process_pcap(self):
        sf = SniffPacket()
        name =sf.get_network_card_name_by_ip()
        # current_working_dir = os.getcwd()
        # local_path = os.path.join(os.getcwd(), 'case_helper/config/1.1Udp_unvlan_revise_mac_revise_ip.pcap')
        local_path = '/root/test_data/1.1Udp_unvlan_revise_mac_revise_ip.pcap'
        cmd=f"sudo tcpreplay -i {name} -l 10000 {local_path}"
        print(f"执行的指令为={cmd}")
        with allure.step(cmd):
            pass
        os.system(cmd)

    def find_log_and_delete(self, file_tag):
        """找到所有log并删除除最新的log以外的log, file_tag"""
        cmd = f'ls | grep jetlog_{file_tag}'
        log_lis = self.bgmcli.type_commands(cmd)
        log_name_list = [item.strip() for item in log_lis.split('\n') if item.strip()]
        logger.info(f"log_name_list>>>{log_name_list}<<<<")

        max_num = 0
        for file in log_name_list:
            num = file.split('_')[1].replace('bts', '').replace('messages', '').replace('s2s', '')
            if num == '':
                continue
            else:
                if int(num) > max_num:
                    max_num = int(num)
        for file in log_name_list:
            if f"jetlog_{file_tag}" == file:
                continue
            if f"jetlog_{file_tag}{max_num}" not in file:
                self.bgmcli.type_commands(f"rm -rf {file}")

    @pytest.mark.repeat(200)
    @pytest.mark.sanity
    @allure.title("诊断重启压测")
    def test_caseid_1983933(self, request):
        try:
            self.sd_tester.send_data([0x11, 0x81])
        except Exception as e:
            logger.warning(f"重启失败==》》{str(e)}")
            assert 0, "bgm重启失败"

        time.sleep(30)
        # 检测每次启动是否为热启
        data = self.bgmcli.type_commands("cat /sys/power/sys_resumed")
        if data == "1":
            logger.info("BGM是镜像启动的")
        else:
            assert False,f"BGM为冷启"
        # 检测Error日志和coredump文件
        i = int(request.node.name.split('[')[1].split('-')[0])
        if i == 200:
            logger.info("检测到本轮测试是否有coredump文件")
            global coredumplis
            local_path = os.path.dirname(__file__)
            coredump_lis = self.bgmcli.get_bgm_coredump()
            if len(coredump_lis) != len(coredumplis):
                coredumplis = coredump_lis
                logger.info(f"获取 coredump 文件==》》{coredump_lis}")
                with allure.step(f"获取 coredump 文件==》》{coredump_lis}"):
                    self.bgmcli.get_log(local_path)
                    assert 0, "产生 coredump 文件"
            logger.info("检测到本轮测试是否有S2S的Error日志")
            flag,data = check_bgm_error_log(self.bgmcli)
            # 方便排查日志，有问题的日志打包拉到data目录下
            from datetime import datetime
            
            if not flag:
                if "E s2s" in data:
                    data_jet = [j for j in data.split('\n') if j != '']
                    logger.info(f"有Error的日志为{data_jet}")
                    for j in data_jet:
                        error_time = datetime.strptime(j.split(' ')[0].split(":")[-1] + ' ' + j.split(' ')[1], "%Y-%m-%d %H:%M:%S.%f")
                        stop_time_list = self.bgmcli.type_commands("/app/bin/zstdcat /log/jetlog_messages*|grep 'S2SService OnStop'|awk '{print $1,$2}'").split("\n")
                        for i in stop_time_list:
                            if  -2 <= (datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") - error_time).total_seconds() <= 2:
                                logger.info("s2s的Error日志属于下电流程产生的，不属于问题")
                                flag = True
                        if not flag:
                            self.bgmcli.type_commands(f"rm /data/bgm_error_s2s*;cd /log;ionice -c 3 tar -cvzf /data/bgm_error_s2s_{time.strftime('%Y%m%d%H%M%S', time.localtime())}.tar.gz jetlog* &", timeout=3*60)
                            self.bgmcli.type_commands("\x03")
                            assert flag,data



# pytest test_stability/test_send1181_to_check_coredump.py 






