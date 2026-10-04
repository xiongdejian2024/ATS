#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :ssh通信能力模拟 实现接口
"""
from xat_ecu.api.interfaces.dp2.base_common.ssh import Ssh as BaseSsh


class Ssh(BaseSsh):

    def start_cd_soc_tcpdump(self, name=None, iface="eth0.5", **kwargs):
        """
        启动针对特定网络接口的tcpdump捕获。

        参数:
            name (str, 可选): tcpdump捕获文件的名称前缀。如果未提供，则默认为"cd_soc_"。
            iface (str, 可选): 要捕获的网络接口名称。默认为"eth0.5"。
            **kwargs: 其他可选的关键字参数，用于定制tcpdump命令。

        注意:
            此方法仅在设备域为CCU_CD时有效。
        """
        return self.cd_soc.start_cd_soc_tcpdump(name, iface, **kwargs)

    def stop_cd_soc_tcpdump(self):
        """
        停止当前的tcpdump捕获。

        注意:
            此方法将停止由`start_cd_soc_tcpdump`方法启动的tcpdump进程。
        """
        return self.cd_soc.stop_cd_soc_tcpdump()

    def delete_cd_soc_tcpdump_file(self, cd_soc_log_name="*.pcap", path='/update/', **kwargs):
        """
        删除指定路径下的tcpdump日志文件。

        参数:
            cd_soc_log_name (str, 可选): 要删除的tcpdump日志文件的名称或通配符模式。
                                        默认为"*.pcap"，表示删除所有.pcap后缀的文件。
            path (str, 可选): 要搜索和删除文件的路径。默认为'/update/'。
            **kwargs: 其他可选的关键字参数，可根据实际情况传递额外信息。

        返回值:
            根据`self.cd_soc.delete_cd_soc_tcpdump_file`方法的实现，可能返回删除操作的结果或状态。

        注意:
            此方法将调用`self.cd_soc.delete_cd_soc_tcpdump_file`来执行实际的删除操作。
            请确保在执行此方法之前，已经正确配置了`self.cd_soc`对象，并且具有足够的权限来删除文件。
        """
        return self.cd_soc.delete_cd_soc_tcpdump_file(cd_soc_log_name, path, **kwargs)
