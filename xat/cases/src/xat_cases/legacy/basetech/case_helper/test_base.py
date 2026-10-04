# -*- coding: utf-8 -*-
"""
@File        : test_base.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/11 11:33
@Description : 
@Examples    :
"""

test_count=0
now_time=0
fail_num=0

import os, sys
import time
from xat_cases.legacy.common_test_base import CommonTestBase
from xat_ecu.legacy.common.logger import logger
import inspect
import subprocess
import re
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import SniffPacket
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import delete_log_file
import shutil
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.common.sniff_packet import SniffPacket_process

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

class TestBase(CommonTestBase):
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
        
    def before_each_func(self, ecu, start=True):
        super().before_each_func(ecu)
            
        #开启进程抓包
        global test_count
        test_count += 1
        try:
            self.sniff = SniffPacket_process(iface=self.tc_config['bus']['eth_obd'],save_path=self.log_path)
            self.sniff.set_save_name(f"第{test_count}次_{self.__class__.__name__}_{ecu.get('testname')}_测试_上位机抓包")
            self.sniff.sniff_start_proccess()
        except Exception as e:
            logger.warning(f"抓包错误：{e}")
        logger.info("########################################Test running########################################")
        

    def after_each_func(self, ecu, start=True):
        super().after_each_func(ecu)
        
        #结束抓包
        try:
            self.sniff.sniff_stop_process()
        except Exception as e:
            logger.warning(f"抓包停止错误：{e}")
        logger.info("########################################Test ending########################################")
                
        #失败用例的检查
        if ecu.get("testresult") != "Pass":
            global fail_num
            fail_num += 1

    def after_class(self, ecu):
        super().after_class(self, ecu)
        #如果测试过程中有失败的case,取bgm日志 如果测试的是BGM,单取BGM日志 否则如果执行的是TCAM的话,取BGM,TCAM的log 如果是stress目录下的话,取BGM日志
        # global fail_num
        # try:
        #     if fail_num > 0 :
        #         if self.test_ecu == 'bgm':
        #             logger.info("bgm用例执行失败 开始取BGM日志")
        #             self.bgmcli.get_jetlogs(self.log_path)
        #         elif self.test_ecu == 'tcam':
        #             logger.info("tcam用例执行失败 开始取BGM&TCAM 日志")
        #             self.bgmcli.get_jetlogs(self.log_path)
        #             self.tcamcli = TCAM_SSH()
        #             self.tcamcli.get_log(self.log_path)
        #         elif self.test_ecu == 'stress':
        #             logger.info("stress用例执行失败 开始取BGM日志")
        #             self.bgmcli.get_jetlogs(self.log_path)
        #         else:
        #             assert False,"无对应的执行目录,请检查"
        #     else:
        #         logger.info("用例全PASS，无需取日志")
        # except Exception as e:
        #     logger.info(f"ERROR:{e}")
        # finally:
        #     # ret=os.system(f"cp /root/test_log/* {self.log_path}")
        #     os.popen(f"cp /root/test_case_log/* {self.log_path}")
        #     os.popen(f'cp ./Can.asc {self.log_path};cp ./FlexRay.asc {self.log_path}')
        #
        #     #恢复fail_num=0
        #     fail_num=0
        #
        #     #恢复test_count=0
        #     global test_count
        #     test_count=0
        
    def arping_172_16_9_2(self,num=4):
        cmd = f'arping 172.16.9.2 -c {num}'
        outmsg=self.bgmcli.type_commands(cmd,root_permission=True)
        result=outmsg.split('\n')[-1]
        pattern = re.compile(r'\d+')
        receive_num = int(pattern.findall(result)[0])
        logger.info(f"获取的 bgm 的{cmd}的结果为 {outmsg}")
        # . 匹配任意字符，除了换行符
        # + 匹配1个或多个的表达式
        # ? 匹配0个或1个由前面的
        # 正则表达式定义的片段，非贪婪方式
        # 查找丢失的 数据包
        if receive_num:
            value = str(int((num-receive_num)/num * 100)) + '%'
            logger.info(f"bgm  ping 172.16.9.2 {num}次，丢包率为 {value}")
            if value == "100%":
                # 未ping 通
                return False
            else:
                return True
        return False
    