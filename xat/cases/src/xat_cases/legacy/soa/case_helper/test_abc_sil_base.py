# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""
import allure
import pytest
from time import sleep
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_ecu.legacy.interface.nuc_app import partner_process_check
from xat_ecu.api.common import *
from framework.automotive.core.common_sil_test_base import CommonSILTestBase


class TestSoaAbcSILBase(CommonSILTestBase):
    
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.ssh.bgm_ssh.type_commands(commands='cd /tmp;touch s2s_startup_flag')
        self.ssh.bgm_ssh.type_commands(commands='cd /root;mkdir bgm_log')
        self.ssh.run_bgm_process(BgmApp.jetlogd)
        self.ssh.run_bgm_process(BgmApp.service_monitor)
        self.ssh.run_bgm_process(BgmApp.s2s_service)
        self.ssh.run_bgm_process(BgmApp.em2)

    
    

    
    
    
    
    
