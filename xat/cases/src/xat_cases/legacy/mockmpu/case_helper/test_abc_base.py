# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""
from xat_ecu.legacy.interface.nuc_app import exec_shell, setup_vlan
from xat_ecu.api.abc_interface import *
from framework.automotive.utils.data_type import EcuInfo
from xat_cases.legacy.common_abc_test_base import CommonABCTestBase

import time


def setup_vlan_for_mock_mpu(iface='enx207bd2765e50'):
    res_str = exec_shell('ifconfig').get('output')
    for ip in ['172.16.5.1', '172.16.9.1']:
        if res_str.find(ip) == -1:
            vlan = ip.split('.')[2]
            if res_str.find(f'eth0.{vlan}') and vlan != 9:
                exec_shell(f'ip link delete eth0.{vlan}')
            exec_shell(f'ip link add link {iface} name eth0.{vlan} type vlan id {vlan}')
            exec_shell(f'ip addr add {ip}/24 dev eth0.{vlan}')
            exec_shell(f'ip link set dev eth0.{vlan} address 02:00:00:00:10:01')
            exec_shell(f'ifconfig eth0.{vlan} netmask 255.255.255.0 broadcast 172.16.{vlan}.255')
            exec_shell(f'ifconfig eth0.{vlan} up')


class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        setup_vlan_for_mock_mpu(iface=ecu.tb_config.get('eth_vlan'))
        time.sleep(2)
        self.mockmpu = MockMpu()

    def after_class(self, ecu: EcuInfo):
        self.mockmpu.close_socket()
        time.sleep(2)
        setup_vlan(iface=ecu.tb_config.get('eth_vlan'), domin=ecu.tb_config.get('partner_domin', 'acu'))
        super().after_class(self, ecu)
