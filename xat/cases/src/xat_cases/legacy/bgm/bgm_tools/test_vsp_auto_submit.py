# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :

"""
import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

import os
import sys
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
# path_json = "../../../task.json"
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

@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        time.sleep(60)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    def handle_app(self, app_name: str):
        appStatus, appId= self.tsp.check_appStatus(app_name) 
        if appStatus == 0:
            #app上库，但未提测
            self.tsp.submit_app(app_name=app_name) #提测app
            return True
        elif appStatus == 10:
            #app上库，且已提测
            return True
        elif appStatus == None:
            #app未上库，直接报错
            logger.info(f"{app_name} 还没上库")
            return False
        else:
            assert False, f"Wrong Status with {app_name}: {appStatus}"        
    
    def test_vsp_auto_submit(self):
        pattern = r'\/(\d{10}[A-Z]{2,3})\.bin'
        match = re.search(pattern, file_url)
        app_name = match.group(1) + '.bin'
        if self.handle_app(app_name=app_name):
            pass
        else:
            time.sleep(60)
            assert self.handle_app(app_name=app_name)

