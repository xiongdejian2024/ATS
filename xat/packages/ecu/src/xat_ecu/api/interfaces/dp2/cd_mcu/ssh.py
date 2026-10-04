#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :ssh通信能力模拟 实现接口
"""
import os
import re
from xat_ecu.api.interfaces.dp2 import *
from xat_ecu.api.interfaces.dp2.base_common.ssh import Ssh as BaseSsh

from xat_ecu.legacy.common.constant import CDCQ_CONSTANT


class Ssh(BaseSsh):

    def clear_mcu_log(self, usr_path="/data/1022/usr"):
        rs1 = self.type_commands(device_name=DeviceName.CCU_CD,
                                 commands=f"rm -r {usr_path}/log/*;sync")
        rs2 = self.type_commands(device_name=DeviceName.CCU_CD,
                                 commands=f"rm -r {usr_path}/nohup.out;sync")
        rs3 = self.type_commands(device_name=DeviceName.CCU_CD,
                                 commands=f"rm -r /var/log/*;sync")
        logger.info(f"程序：{rs1} {rs2} {rs3}")

    def stop_qnx_app(self):
        """
        禁用QNX所有集度开发的应用程序;禁用Android（有Android依赖的不可操作此步骤）
        :return:
        """
        rs1 = self.type_commands(device_name=DeviceName.CCU_CD, commands="mv /mnt/scripts/slm/jidu_slm.xml /mnt/scripts/slm/jidu_slm_bk.xml")
        rs2 = self.type_commands(device_name=DeviceName.CCU_CD, commands="mv /mnt/vm/images/linux-la.img /mnt/vm/images/linux-la-bk.img")
        logger.info(f"已禁用程序：{rs1} {rs2}")
        # TODO 后续实现CCU CD继电器重启

    def get_mcu_forward_tool(self, mcu_forward_dir="/data/1022/usr"):
        rs = self.type_commands(device_name=DeviceName.CCU_CD, commands=f"ls -alt {mcu_forward_dir}")
        if "bin" not in rs:
            return False
        if "etc" not in rs:
            return False
        if "lib" not in rs:
            return False
        return True

    def start_qnx_app(self):
        """
        2. 恢复禁用应用程序
        :return:
        """
        rs1 = self.type_commands(device_name=DeviceName.CCU_CD, commands="mv /mnt/scripts/slm/jidu_slm_bk.xml /mnt/scripts/slm/jidu_slm.xml")
        rs2 = self.type_commands(device_name=DeviceName.CCU_CD, commands="mv /mnt/vm/images/linux-la-bk.img /mnt/vm/images/linux-la.img")
        logger.info(f"已恢复程序：{rs1} {rs2}")
        # TODO 后续实现CCU CD继电器重启

    def upload_mcu_forward_and_extract_to_ccu(self, file_path, to_path="/mnt"):
        """
        推送上位机文件到MCU解压并赋值权限
        :param file_path: 上位机文件路径，****.7z
        :param to_path: 推送到ccu cd中的路径
        :return:
        """
        # rs = self.type_commands(device_name=DeviceName.CCU_CD, commands=f"scp {file_path} root@172.20.5.11:{to_path}")
        # logger.info(f"推送：{file_path} 到cdc:{rs}")
        self.cd_soc.push_file_to_cd_soc_data(file_path, to_path)

        file_name = os.path.basename(file_path)
        self.type_commands(device_name=DeviceName.CCU_CD, commands=f"mount -uw {to_path}")
        if str(file_path).endswith(".zip"):
            self.type_commands(device_name=DeviceName.CCU_CD, commands=f"cd {to_path};unzip {file_name}")
        elif str(file_path).endswith(".7z") or str(file_path).endswith(".gz"):
            self.type_commands(device_name=DeviceName.CCU_CD, commands=f"cd {to_path};tar -zxvf {file_name}")
        else:
            raise AssertionError(f"文件类型错误：{file_path}")

        self.type_commands(device_name=DeviceName.CCU_CD, commands=f"chmod 777 {to_path}/usr/bin/service_monitor")
        self.type_commands(device_name=DeviceName.CCU_CD, commands=f"chmod 777 {to_path}/usr/etc/service_monitor.json")
        self.type_commands(device_name=DeviceName.CCU_CD, commands=f"chmod 777 {to_path}/usr/bin/mcu_forwarder_server")

    def start_mock_service(self, mock_server_path="/data/1022/usr", force_start=False, time_out=6):
        """
        启动ccu forward mock服务进程
        :param mock_server_path:
        :param force_start:
        :param time_out:
        :return:
        """
        # CDCQ_CONSTANT.CDCQ_PASSWORD = ""
        rs = self.type_commands(device_name=DeviceName.CCU_CD, commands="pidin |grep forwarder", timeout=time_out)
        forwarder_server_ps_list = set()
        for i in rs.split("\n"):
            result = re.findall("(\d+)\s+\d+\s+u_forwarder_server\s+.*", i)
            if result:
                forwarder_server_ps_list.add(int(result[0]))
        if not forwarder_server_ps_list:
            rs = self.type_commands(device_name=DeviceName.CCU_CD, commands=f"cd {mock_server_path};export LD_LIBRARY_PATH=./lib;export BOOTES_HOME_DIR=./etc;nohup ./bin/mcu_forwarder_server &", timeout=time_out)
            logger.info(f"已执行forwarder server启动命令：{rs}")
        else:
            logger.info(f"已经发现forwarder server服务在运行：{forwarder_server_ps_list}")

        ts = self.type_commands(device_name=DeviceName.CCU_CD, commands="pidin |grep service_monitor", timeout=time_out)
        monitor_server_ps_list = set()
        for i in ts.split("\n"):
            result = re.findall("(\d+)\s+\d+\s+in/service_monitor\s+.*", i)
            if result:
                monitor_server_ps_list.add(int(result[0]))
        if not monitor_server_ps_list:
            rs = self.type_commands(device_name=DeviceName.CCU_CD,
                                    commands=f"cd {mock_server_path};export LD_LIBRARY_PATH=./lib;export BOOTES_HOME_DIR=./etc;nohup ./bin/service_monitor -c ./etc/service_monitor.json &",
                                    timeout=time_out)
            logger.info(f"已执行monitor server启动命令：{rs}")
        else:
            logger.info(f"已经发现monitor server服务在运行：{forwarder_server_ps_list}")

        if force_start:
            self.stop_mock_service()
            rs = self.type_commands(device_name=DeviceName.CCU_CD,
                                    commands=f"cd {mock_server_path};export LD_LIBRARY_PATH=./lib;export BOOTES_HOME_DIR=./etc;nohup ./bin/mcu_forwarder_server &",
                                    timeout=time_out)
            logger.info(f"已执行forwarder server启动命令：{rs}")
            rs = self.type_commands(device_name=DeviceName.CCU_CD,
                                    commands=f"cd {mock_server_path};export LD_LIBRARY_PATH=./lib;export BOOTES_HOME_DIR=./etc;nohup ./bin/service_monitor -c ./etc/service_monitor.json &",
                                    timeout=time_out)
            logger.info(f"已执行monitor server启动命令：{rs}")

    def stop_mock_service(self, time_out=6):
        """
        停止mock service进程
        :return:
        """
        rs = self.type_commands(device_name=DeviceName.CCU_CD, commands="pidin |grep forwarder", timeout=time_out)
        forwarder_server_ps_list = set()
        for i in rs.split("\n"):
            result = re.findall("(\d+)\s+\d+\s+u_forwarder_server\s+.*", i)
            if result:
                forwarder_server_ps_list.add(int(result[0]))
        for pid in forwarder_server_ps_list:
            rs = self.type_commands(device_name=DeviceName.CCU_CD, commands=f"kill -9 {pid}", timeout=time_out)
            logger.info(f"发现forwarder server服务，杀掉：{pid}->{rs}")

        ts = self.type_commands(device_name=DeviceName.CCU_CD, commands="pidin |grep service_monitor", timeout=time_out)
        monitor_server_ps_list = set()
        for i in ts.split("\n"):
            result = re.findall("(\d+)\s+\d+\s+in/service_monitor\s+.*", i)
            if result:
                monitor_server_ps_list.add(int(result[0]))
        for pid in monitor_server_ps_list:
            rs = self.type_commands(device_name=DeviceName.CCU_CD, commands=f"kill -9 {pid}", timeout=time_out)
            logger.info(f"发现monitor server服务，杀掉：{pid}->{rs}")
