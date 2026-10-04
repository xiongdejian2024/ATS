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
import yaml

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase


class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        willow_task_id = ecu.get("task_id")
        if willow_task_id:
            with open(os.path.join(project_root, 'test_case/bgm/config/UA_conf.yaml'), 'r') as f:
                data = yaml.safe_load(f)
                data['task_id'] = int(willow_task_id)
            with open(os.path.join(project_root, 'test_case/bgm/config/UA_conf.yaml'), 'w') as fn:
                yaml.safe_dump(data, fn)
            self.taskid = int(willow_task_id)
        else:
            self.taskid =  self.tc_config.get("task_id")
        with open(os.path.join(project_root, 'test_case/bgm/config/UA_conf.yaml'), 'r') as f:
            conf = yaml.safe_load(f)
            self.BGM_Download_Req = conf['BGM_Download_Req']
        self.sd_tester.stop_tester_present()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
        self.sd_tester.stop_tester_present()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.bgm_diag_line_up()