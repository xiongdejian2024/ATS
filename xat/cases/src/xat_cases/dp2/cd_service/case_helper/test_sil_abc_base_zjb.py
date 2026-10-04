#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_sil_abc_base.py
@Time         :2024/10/23 10:36
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from ... import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import partner_process_check
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2 import MockUdp, MockTcp
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import TcpChannel, UdpChannel
from xat_ecu.api.interfaces.dp2.cd_service.soa import Soa


class TestSILAbcBase():
    def before_class_setup(self, ecu):
        self.before_class(self, ecu)
    
    def after_class_teardown(self, ecu):
        self.after_class(self, ecu)

    def before_class(self, ecu: EcuInfo):
        # super().before_class(self, ecu)
        self.veh_type = 'jupiter'
        self.bl_ver = 'v_0_4_0'
        partner_process_check()
        self.mockudp = MockUdp(channel_dict=None, veh_type=self.veh_type, bl_ver=self.bl_ver)
        self.mocktcp = MockTcp(channel_dict=None, veh_type=self.veh_type, bl_ver=self.bl_ver)
        self.soa = Soa()

    def before_each_func(self, ecu: EcuInfo):
        # super().before_each_func(ecu)
        pass

    def after_each_func(self, ecu: EcuInfo):
        # super().after_each_func(ecu)
        pass

    def after_class(self, ecu: EcuInfo):
        # super().after_class(self, ecu)
        self.soa.stop_soa()
        self.mockudp.stop_mock()
        self.mocktcp.stop_mock()
