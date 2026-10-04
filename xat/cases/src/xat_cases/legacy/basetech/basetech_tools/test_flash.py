# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm_willow.py
@Author      : wenyu.liang_ext@jiduauto.com
@Time        : 2023/11/2 11:00
@Description : 
@Examples    :
"""

import time
import pytest
import allure
import sys, os


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','interface')
sys.path.append(work_path_2)

work_path_3 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','driver')
sys.path.append(work_path_3)

from sat.test_case.basetech.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *

# path =f'./willow_flash_log'

class TestFlash(TestBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
            self.diagtest = DiagTestBase(self.ipdu,self.nucapp,self.tc_config) # 初始化
            
        os.system("mkdir ../report")
        os.system("touch ../report/report_summary.json")

        willow_path=get_willow_file_path()
        if willow_path:
            path_json=os.path.join(willow_path, "task.json")
        else:
            path_json="task.json"

        logger.info(f'path_json {path_json}')
        if os.path.exists(path_json):
            with open(path_json, "r") as f:
                task_dict = json.load(f)
                file_url = task_dict.get("img_url")
                keyinfo = task_dict.get("keyinfo")
                file_url1 = task_dict.get("img_url1")
                keyinfo1 = task_dict.get("keyinfo1")
                flash_flag = task_dict.get("flash_flag")
                img_url_boot = task_dict.get("img_url_boot")
                keyinfo_boot = task_dict.get("keyinfo_boot")
                mcu_ver = task_dict.get("mcu_ver", '').upper().replace(' ', '')
                blt_ver = task_dict.get("blt_ver", '').upper().replace(' ', '')
                switch_ver = task_dict.get("switch_ver", '').upper().replace(' ', '')
                switch_ver_b = task_dict.get("switch_ver_b", '').upper().replace(' ', '')  # f 样以后
                inputTestScriptCMD = task_dict.get("inputTestScriptCMD")
                
                self.file_url = file_url
                self.keyinfo = keyinfo
                self.flash_flag = flash_flag
                self.img_url_boot = img_url_boot
                self.keyinfo_boot = keyinfo_boot
                self.mcu_ver = mcu_ver
                self.blt_ver = blt_ver
                self.switch_ver = switch_ver
                self.switch_ver_b = switch_ver_b
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
 
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        with allure.step(f"关闭BGM/TCAM连接"):
            self.diagtest.close()
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)
    
    def test_flash_bgm_boot_willow(self):
        try:
            if self.flash_flag:
                self.flash_bgm(self.keyinfo_boot,self.img_url_boot,log_path=self.log_path)
                assert True
            else:
                logger.info("flash_flag为False 无需刷写bgm boot")
                assert True
            
            with open("../report/report_summary.json", "w") as f:
                report_summary = {"start": True}
                json.dump(report_summary, f)

        except Exception as e:
            with open("../report/report_summary.json", "w") as f:
                    report_summary = {"start": False}
                    json.dump(report_summary, f)
                    logger.error("BGM FLASH ERROR IS {}".format(str(e)))
            logger.info(f"刷写失败：ERROR:{e}")
            assert False
        finally:
            self.diagtest.close()
            
    def test_flash_bgm_app_willow(self):
        try:
            if self.flash_flag:
                self.flash_bgm(self.keyinfo,self.file_url,log_path=self.log_path)
            else:
                logger.info("flash_flag为False 无需刷写bgm app")
        except Exception as e:
            logger.info(f"刷写失败：ERROR:{e}")
            assert False
    
    def test_flash_tcam_willow(self):
        try:
            if self.flash_flag:
                self.flash_tcam(self.keyinfo,self.file_url,log_path=self.log_path)
            else:
                logger.info("flash_flag为False 无需刷写tcam")
        except Exception as e:
            logger.info(f"刷写失败：ERROR:{e}")
            assert False
            
    def test_flash_bgm_boot_and_app_local(self):
       
        #设置boot包地址
        img_url_boot="https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.0.0/6160110200FD/2960110200BB.bin"
        #设置boot包的keyinfo
        keyinfo_boot=__import__("os").environ['XAT_CREDENTIAL_SCAN_7E0F6377CD3D5016709A'] 
        #设置app包的下载地址
        file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.0.0/6160110200FD/6160110200FD.bin"
        #设置app包的keyinfo
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_25699B321D4F4D573889']

        #开始连接BGM
        self.diagtest.connect(0x1001)
        self.diagtest.init_boot_per()
        
        #先刷写boot
        self.diagtest.flash_bgm(keyinfo_boot,img_url_boot)
        #再刷写app
        self.diagtest.flash_bgm(keyinfo,file_url)
    
    def test_flash_tcam_local(self):
        #设置app包的下载地址
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v1.3.0/6110110130AO/6110110130AO.bin"
        #设置app包的keyinfo
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_025D16A0F4C2430E470F']

        #开始连接TCAM
        self.diagtest = DiagTestBase(self.ipdu,self.nucapp,self.tc_config)
        self.diagtest.connect(0x1011,'TCAM')
        self.diagtest.init_boot_per()
        #刷写TCAM
        self.diagtest.flash_tcam(keyinfo,file_url)
        
    def flash_bgm(self,keyinfo=None,file_url=None,log_path='.'):
        if not file_url:
            assert False,'BGM刷写包url为空'
            
        if not keyinfo:
            assert False,'BGM刷写包keyinfo为空'
        
        self.diagtest = DiagTestBase(self.ipdu,self.nucapp,self.tc_config)
        self.diagtest.connect(0x1001)
        self.diagtest.init_boot_per()
        self.diagtest.flash_bgm(keyinfo,file_url,save_path=log_path)
    
    def flash_tcam(self,keyinfo=None,file_url=None,log_path='.'):
        if not file_url:
            assert False,'TCAM刷写包url为空'
            
        if not keyinfo:
            assert False,'TCAM刷写包keyinfo为空'
        
        self.diagtest = DiagTestBase(self.ipdu,self.nucapp,self.tc_config)
        self.diagtest.connect(0x1011,'TCAM')
        self.diagtest.init_boot_per()
        self.diagtest.flash_tcam(keyinfo,file_url,save_path=log_path)


#执行本地刷写TCAM：pytest basetech_tools//test_flash.py::TestFlash::test_flash_tcam_local
#执行本地刷写BGM app以及boot： pytest basetech_tools/test_flash.py::TestFlash::test_flash_bgm_boot_and_app_local --disable_partner='true'
#执行willow刷写BGM boot：pytest basetech_tools/test_flash.py::TestFlash::test_flash_bgm_boot_willow
#执行willow刷写BGM app：pytest basetech_tools/test_flash.py::TestFlash::test_flash_bgm_app_willow
#执行willow刷写TCAM：pytest basetech_tools/test_flash.py::TestFlash::test_flash_tcam_willow