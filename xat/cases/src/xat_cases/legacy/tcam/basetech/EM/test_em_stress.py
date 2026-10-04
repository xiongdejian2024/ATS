#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import pytest
import allure
from time import sleep

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("软件平台/EM")
class TestCertificate(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 


    @pytest.mark.repeat(50)
    @pytest.mark.Full
    def test_caseid_1985775(self):
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)
        sleep(20)
        chanel_data = self.ssh.chk_net_channel()
        assert len(chanel_data) == 2, "tcam net channel 异常"
        tcam_ping = self.mix.chk_tcam_ping() #检查两个网卡是否都能ping通
        assert len(tcam_ping) == 0 
