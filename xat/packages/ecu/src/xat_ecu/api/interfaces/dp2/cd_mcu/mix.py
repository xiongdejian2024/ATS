#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mix.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :需要多个基础能力一起模拟的场景，提供对应实现接口；
"""
import os
import time
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.interfaces.dp2.cd_mcu.ssh import Ssh
from xat_ecu.api.interfaces.dp2.cd_mcu.tsp import Tsp
from xat_ecu.api.interfaces.dp2.base_common.mix import Mix as BaseMix


class Mix(BaseMix):

    def config_mcu_forward_vlan(self, config: dict=None):
        """
        配置mcu forward vlan网卡
        :param config:
        :return:
        """
        if not config:
            config = {
                "enxf8e43b81f4e1": {
                    "vlan_id": 5,
                    "addr": "172.20.5.21/24",
                    "vlan_name": "vlan5-SOC",
                    "vlan_mac": "02:00:00:00:20:21"
                },
                "enx00e04c2c8348": {
                    "vlan_id": 5,
                    "addr": "172.20.5.1/24",
                    "vlan_name": "vlan5-L",
                    "vlan_mac": "02:00:00:00:20:01"
                },
                "enx00e04c3d6048": {
                    "vlan_id": 5,
                    "addr": "172.20.5.2/24",
                    "vlan_name": "vlan5-R",
                    "vlan_mac": "02:00:00:00:20:02"
                }
            }
        for k, info in config.items():
            cmd = None
            try:
                vlan_name = info["vlan_name"]
                vlan_id = info["vlan_id"]
                addr = info["addr"]
                vlan_mac = info["vlan_mac"]
                cmd = os.popen(
                    f"ip link add link {k} name {vlan_name} type vlan id {vlan_id};ip addr add {addr} dev {vlan_name};ifconfig {vlan_name} up;ifconfig {vlan_name} hw ether {vlan_mac};")
                logger.info(f"{vlan_name} 网卡配置完成:{cmd}")
            finally:
                if isinstance(cmd, os._wrap_close):
                    cmd.close()

    def start_mcu_forwarder_config(self, mkdir="/data/1022"):
        """

        :param mkdir:
        :return:
        """
        ssh_obj = Ssh("CCU_CD")
        if not ssh_obj.get_mcu_forward_tool(f"{mkdir}/usr"):
            logger.info(f"开始下载MCU转发工具")
            tsp_obj = Tsp()
            local_path = tsp_obj.download_mcu_forwarder_to_nuc()
            logger.info(f"MCU转发工具下载到：{local_path}")

            logger.info(f"开始推送本地文件到ccu")
            ssh_obj.upload_mcu_forward_and_extract_to_ccu(local_path, mkdir)
            logger.info(f"推送完成")
            time.sleep(2)
        ssh_obj.start_mock_service()
