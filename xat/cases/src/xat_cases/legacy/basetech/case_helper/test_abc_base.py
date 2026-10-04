# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""

import os
import sys

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase
import inspect
import time
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.sniff_packet import SniffPacket_thread
from xat_ecu.legacy.common.sniff_packet import SniffPacket_process
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
import re
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import delete_log_file

test_count=0
now_time=0
fail_num=0

class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        #获取当前被测ecu信息
        self.test_ecu = inspect.stack()[1].filename.split('/')[-2]
        
        #获取执行当前的时间
        global now_time
        if not now_time:
            now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
            
        #获取当前执行的脚本名字
        script_name = inspect.stack()[1].filename.split('/')[-1].split('.py')[0]
        #获取当前日志保存的路径
        self.log_path = os.path.join('test_log',script_name,now_time)
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path) 
            
        #当日志目录下文件大于10个，删除多余文件
        self.log_dir = os.path.join('test_log',script_name)
        delete_log_file(log_path=self.log_dir)
        
        try:
            #获取BGM TCAM的安全等级7的安全常数
            self.bgm_l7 = self.ssh.get_bgm_l7_constant()
            self.tcam_l7 = self.ssh.get_tcam_l7_constant()
            self.tc_config['sec_con']['BGM'][3]=self.bgm_l7
            self.tc_config['sec_con']['TCAM'][3]=self.tcam_l7
        except Exception as e:
            logger.info('获取安全等级7安全常数失败')
            self.bgm_l7=self.tc_config['sec_con']['BGM'][3]
            self.tcam_l7=self.tc_config['sec_con']['TCAM'][3]
        
    def before_each_func(self, ecu, start=True):
        super().before_each_func(ecu)
        
        #开启进程抓包
        global test_count
        test_count += 1
        self.sniff = SniffPacket_process(iface=self.tc_config['bus']['eth_obd'],save_path=self.log_path)
        self.sniff.set_save_name(f"第{test_count}次_{self.__class__.__name__}_{ecu.get('testname')}_测试_上位机抓包")
        self.sniff.sniff_start_proccess()
        logger.info("########################################Test running########################################")
        

    def after_each_func(self, ecu, start=True):
        #结束抓包
        self.sniff.sniff_stop_process()
        logger.info("########################################Test ending########################################")
        
        #失败用例的检查
        if ecu.get("testresult") != "Pass":
            global fail_num
            fail_num += 1
        super().after_each_func(ecu)

    def after_class(self, ecu):
        #如果测试过程中有失败的case,取bgm日志 如果测试的是BGM,单取BGM日志 否则如果执行的是TCAM的话,取BGM,TCAM的log 如果是stress目录下的话,取BGM日志
        global fail_num
        try:
            if fail_num > 0 :
                if self.test_ecu == 'bgm':
                    logger.info("bgm用例执行失败 开始取BGM日志")
                    self.ssh.bgm_ssh.get_jetlogs(self.log_path)
                elif self.test_ecu == 'tcam':
                    logger.info("tcam用例执行失败 开始取BGM&TCAM 日志")
                    self.ssh.bgm_ssh.get_jetlogs(self.log_path)
                    self.ssh.tcam_ssh.get_log(self.log_path)
                elif self.test_ecu == 'stress':
                    logger.info("stress用例执行失败 开始取BGM日志")
                    self.ssh.bgm_ssh.get_jetlogs(self.log_path)
                else:
                    assert False,"无对应的执行目录,请检查"
            else:
                logger.info("用例全PASS，无需取日志")
        except Exception as e:
            logger.info(f"ERROR:{e}")
        finally:
            os.popen(f"cp /root/test_case_log/* {self.log_path}")
            os.popen(f'cp ./Can.asc {self.log_path};cp ./FlexRay.asc {self.log_path}')
                
            #恢复fail_num=0
            fail_num=0
            
            #恢复test_count=0
            global test_count
            test_count=0
        
            logger.info(f'本次测试的全部日志保存地址: {self.log_path}')
            super().after_class(self, ecu)
