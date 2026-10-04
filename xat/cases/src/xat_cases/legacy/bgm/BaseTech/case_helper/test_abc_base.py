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
from xat_ecu.legacy.sdk.sdk_tools import *
from framework.automotive.utils.data_type import EcuInfo


class TestABCBase(CommonABCTestBase):
    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        """子类重写该接口，自定义台架类型为单域、两域或者四域"""
        return ecu
    
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.taskid =  self.tc_config.get("task_id")
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

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.bgm_diag_line_up()