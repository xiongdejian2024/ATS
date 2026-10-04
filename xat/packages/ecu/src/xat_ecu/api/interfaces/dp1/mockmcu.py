#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :diagmock.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :整车 server ecu 诊断能力模拟抽象接口
"""
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.interface import CommonMockMcu


class MockMcu(CommonMockMcu):
    
    def start_run(self):
        return 0

    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", host="172.16.5.1", port=30500, **kwargs):
        return self.bgm_eth_internal.start_bgm_tcpdump(name, iface, host, port, **kwargs)

    def stop_tcpdump_and_parse_signal(self, sleep_time=0):
        return self.bgm_eth_internal.stop_tcpdump_and_parse_signal(sleep_time)
    
    def start_tcpdump(self):
        return self.bgm_eth_internal.start_tcpdump()

    def stop_tcpdump(self):
        return self.bgm_eth_internal.stop_tcpdump()

    def empty(self):
        return self.bgm_eth_internal.empty()

    def get_signal_items(self, signal_name):
        return self.bgm_eth_internal.get_signal_items(signal_name)

    def get_signal_values(self, signal_name):
        return self.bgm_eth_internal.get_signal_values(signal_name)

    def get_last_signal(self, signal_name):
        return self.bgm_eth_internal.get_last_signal(signal_name)

    def set_signal(self, signal_name: str, value: int, send_pdu_immediately=False):
        """
        设定pdu中的指定信号的数值
        @param signal_name:  信号名
        @param signal_value:  信号设定的值
        @param send_pdu_immediately: 是否立即发送一帧
        """
        logger.info(f"设置信号：{signal_name}={value}")
        return self.bgm_eth_internal.set_signal(signal_name, value, send_pdu_immediately)

    def write_ccp(self, new_ccp_map: dict):
        """
        通过仿真tcp数据直接发送ccp给到MPU
        @param new_ccp_map: {ccp_index: ccp_value}, index从1开始
        """
        for index, ccp_value in new_ccp_map.items():
            self.ccp[index-1] = ccp_value
        logger.info(f"修改ccp：{new_ccp_map}")
        self.bgm_eth_internal.set_signal("CarConfig", DataTypeHanding.to_int(self.ccp), send_pdu_immediately=True)
