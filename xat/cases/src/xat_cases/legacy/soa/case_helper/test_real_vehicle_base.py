# -*- coding: utf-8 -*-

from xat_cases.legacy.common_test_base import CommonTestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


class TestBase(CommonTestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bgmcli.check_bgm_start_type(self.nucapp)
        # 由基类控制诊断仪启动，并且先读取台架ccp
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        curr_ccp_str, self.tb_ccp_list = self.sd_tester.read_ccp()

    def after_class(self, ecu):
        # 由基类控制诊断仪关闭，并且需恢复台架ccp
        self.sd_tester.write_multi_ccp({index + 1: self.tb_ccp_list[index] for index in range(1556)})
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def before_each_func(self, ecu, start=False):
        super().before_each_func(ecu, start)

    def after_each_func(self, ecu, start=False):
        super().after_each_func(ecu, start)