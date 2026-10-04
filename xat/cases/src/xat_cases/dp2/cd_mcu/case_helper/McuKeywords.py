#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : McuKeywords.py

**********************

------------------------------------------------------------------
@Time    : 2024/11/25 10:12
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import os
import time

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.utils.utils import exec_shell_command
from xat_ecu.api.interfaces.dp2.cd_mcu.ssh import Ssh
from xat_ecu.api.interfaces.dp2.cd_mcu.tsp import Tsp
from xat_ecu.api.interfaces.dp2.cd_mcu.mix import Mix
from xat_cases.dp2.cd_mcu.case_helper.test_abc_base import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.eth_internal_dp20 import *

vlan_config = {
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


class McuKeywords(object):
    ETH_LCUL = None
    ETH_LCUR = None
    ETH_CDSOC = None
    ETH_ADMCU = None

    def __init__(self, bus_comm):
        self.bus_comm = bus_comm

    def creat_lcul_eth_internal_dp20(self, mock_ecu="LCUL", test_ecu="CCUMCUCD", mcu_forward_port=9999):
        self.ETH_LCUL = CCUCDEthInternalDp20(mock_ecu=mock_ecu, test_ecu=test_ecu, mcu_forward_port=mcu_forward_port)

    def creat_lcur_eth_internal_dp20(self, mock_ecu="LCUR", test_ecu="CCUMCUCD", mcu_forward_port=9998):
        self.ETH_LCUR = CCUCDEthInternalDp20(mock_ecu=mock_ecu, test_ecu=test_ecu, mcu_forward_port=mcu_forward_port)

    def creat_cd_soc_eth_internal_dp20(self, mock_ecu="CCUSOCCD", test_ecu="CCUMCUCD", mcu_forward_port=None):
        self.ETH_CDSOC = CCUCDEthInternalDp20(mock_ecu=mock_ecu, test_ecu=test_ecu, mcu_forward_port=mcu_forward_port)

    def creat_ad_mcu_eth_internal_dp20(self, mock_ecu="CCUMCUAD", test_ecu="CCUMCUCD", mcu_forward_port=9995):
        self.ETH_ADMCU = CCUCDEthInternalDp20(mock_ecu=mock_ecu, test_ecu=test_ecu, mcu_forward_port=mcu_forward_port)

    def start_mock_ecu(self):
        self.creat_lcul_eth_internal_dp20()
        self.creat_lcur_eth_internal_dp20()
        self.creat_cd_soc_eth_internal_dp20()
        self.creat_ad_mcu_eth_internal_dp20()

    def stop_mock_ecu(self):
        try:
            self.ETH_CDSOC.environment_teardown()
        except Exception as e:
            logger.warning(f"停止cdsoc对象报错：{e}")
        try:
            self.ETH_LCUL.environment_teardown()
        except Exception as e:
            logger.warning(f"停止lcul对象报错：{e}")
        try:
            self.ETH_LCUR.environment_teardown()
        except Exception as e:
            logger.warning(f"停止lcur对象报错：{e}")
        try:
            self.ETH_ADMCU.environment_teardown()
        except Exception as e:
            logger.warning(f"停止admcu对象报错：{e}")

    def start_mcu_forward_and_pre_env_to_ready(self, ccu_deploy_path="/var/ota_cache", need_config_vlan=False,
                                               force_start=True):
        """
        配置网卡；准备mcu forward服务；准备partner工具；清理ccu log
        :param need_config_vlan: True:需要配置
        :param ccu_deploy_path:
        :return:
        """
        exec_shell_command(f"route add -net 239.255.5.1 netmask 255.255.255.255 dev vlan5-R")
        if need_config_vlan:
            self.config_mcu_forward_vlan(vlan_config)
        self.config_partner_tool_in_nuc()
        self.clear_real_mcu_log(ccu_deploy_path + "/usr")
        self.start_mcu_forwarder_config(mkdir=ccu_deploy_path, force_start=force_start)

    def clear_real_mcu_log(self, path):
        ssh_obj = Ssh("CCU_CD")
        ssh_obj.clear_mcu_log(path)
        # exec_shell_command(f"rm ")

    def config_partner_tool_in_nuc(self, check_path="/opt"):
        """
        配置检查partner工具
        :return:
        """
        target_check_file = os.path.join(check_path, "partnerEnv")
        if not os.path.exists(target_check_file):
            logger.info(f"开始下载partner工具")
            tsp_obj = Tsp()
            local_path = tsp_obj.download_partner_to_nuc(local_path=check_path + "/")
            logger.info(f"partner工具下载到：{local_path}")
            exec_shell_command(f"cd {check_path};tar -zxvf {local_path}")
        else:
            logger.info(f"检查到有partner工具，不远程拉取。")

    def config_mcu_forward_vlan(self, config: dict = None):
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

    def start_mcu_forwarder_config(self, mkdir="/data/1022", force_start=False):
        """
        检查forward服务并拉起服务
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
        ssh_obj.start_mock_service(mock_server_path=mkdir + "/usr", force_start=force_start)

    def get_usgmod(self):
        message_inf = {
            "CCUMCUCDPropulsionCANFDFr01":
                [
                    "VMMGlbSigUsgModSts"
                ]
        }
        logger.info("get_usgmod")
        expectedvalue = self.bus_comm.ipdu.get_multiple_signals("propulsioncanfd", message_inf)
        logger.info(f"expectedvalue:{expectedvalue}")
        return expectedvalue["CCUMCUCDPropulsionCANFDFr01"]["VMMGlbSigUsgModSts"]

    def ChangeUsgMod(self, usgmod=1):
        current_usgmod = self.get_usgmod()
        logger.info(f"current_usgmod:{current_usgmod}")
        if current_usgmod <= 1:
            self.ETH_CDSOC.set_signal_value("SetUsgModUpProxyReq", 1)
        else:
            self.ETH_CDSOC.set_signal_value("SetUsgModDwnProxyReq", 1)
        logger.info(f"设置UsgMode为:{usgmod}")
        if usgmod > 1:
            self.ETH_CDSOC.set_signal_value("SetUsgModUpProxyReq", usgmod)
        else:
            self.ETH_CDSOC.set_signal_value("SetUsgModDwnProxyReq", usgmod)

    def SetVehMovgDir(self, VehMovgDir=1):
        # self.bus_comm.set('propulsioncanfd', 'BCU1PropulsionCANFDFr02', 'VehMovgDir_UB',1)
        self.bus_comm.set('propulsioncanfd', 'BCU1PropulsionCANFDFr02', 'VehMovgDirVehMovgDir', VehMovgDir)

    def SetDoorOpenClsSts(self, FL=2, RL=2, FR=2, RR=2, Tr=2):
        logger.info(
            f"设置FLDoorOpenClsSts为{FL}，RLDoorOpenClsSts为{RL}，FRDoorOpenClsSts为{FR}，RRDoorOpenClsSts为{RR}，TrSts为{Tr}")
        self.ETH_LCUL.set_signal_value("FLDoorOpenClsSts", FL)
        time.sleep(1)
        self.ETH_LCUL.set_signal_value("RLDoorOpenClsSts", RL)
        time.sleep(1)
        self.ETH_LCUR.set_signal_value("FRDoorOpenClsSts", FR)
        time.sleep(1)
        self.ETH_LCUR.set_signal_value("RRDoorOpenClsSts", RR)
        time.sleep(1)
        self.ETH_LCUR.set_signal_value("TrSts", Tr)

    def GetSignalvalues_Eth(self, EthName, SignalName):
        if EthName == "ETH_CDSOC":
            result = self.ETH_CDSOC.get_signal_values(SignalName)
        elif EthName == "ETH_LCUL":
            result = self.ETH_LCUL.get_signal_values(SignalName)
        elif EthName == "ETH_LCUR":
            result = self.ETH_LCUR.get_signal_values(SignalName)
        else:
            pass
        if len(result):

            return result[-1]
        else:
            logger.info(f"{EthName}信号{result}获取失败")

    def CheckSignal_Eth(self, EthName, SignalName, expectValue):
        result = self.GetSignalvalues_Eth(EthName, SignalName)
        logger.info(f"{EthName}信号{SignalName}真实值为{result}，qiwang")

    def CheckDoorOpenClsSts(self, FL, RL, FR, RR, Tr):
        logger.info("检查门关开状态")
        if FL > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr02",
                                "FLDoorOpenClsSts", FL, 1)
        if RL > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr02",
                                "RLDoorOpenClsSts", RL, 1)
        if FR > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr02",
                                "FRDoorOpenClsSts", FR, 1)
        if RR > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr02",
                                "RRDoorOpenClsSts", RR, 1)
        if Tr > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr02",
                                "TrSts", Tr, 1)

    def CheckCenLockSts(self, CenLockSts=-1, TrigSrc=-1, TrigSrcType=-1, UpdateEvnt=-1):
        # self.ETH_CDSOC.empty()
        # time.sleep(1)
        McutoSoc_CenLockSts = self.ETH_CDSOC.get_signal_values("CenLockStsAndKeyIDLockSts")
        McutoSoc_TrigSrc = self.ETH_CDSOC.get_signal_values("CenLockStsAndKeyIDTrigSrc")
        # McutoSoc_CenLockSts = self.ETH_CDSOC.get_signal_values("
        # CenLockSts")
        # McutoSoc_TrigSrc = self.ETH_CDSOC.get_signal_values("CentralLockStsTrigSrc")
        McutoSoc_TrigSrcType = self.ETH_CDSOC.get_signal_values("CentralLockStsTrigSrcType")
        McutoSoc_UpdateEvnt = self.ETH_CDSOC.get_signal_values("CentralLockStsUpdateEvnt")
        if CenLockSts > -1:
            logger.info(f"McutoSoc_CenLockSts期望为{CenLockSts}，实际为{McutoSoc_CenLockSts}")
            # logger.info(f"McutoSoc_CenLockSts期望为{CenLockSts}，实际为{McutoSoc_CenLockSts[-1]}")
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr03",
                                "CentralLockStsCenLockSts", CenLockSts, 1)
        if TrigSrc > -1:
            logger.info(f"McutoSoc_TrigSrc期望为{TrigSrc}，实际为{McutoSoc_TrigSrc}")
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr03",
                                "CentralLockStsTrigSrc", TrigSrc, 1)
        if TrigSrcType > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr03",
                                "CentralLockStsTrigSrcType", TrigSrcType, 1)
        if UpdateEvnt > -1:
            self.bus_comm.check("infocanfd", "CCUMCUCDInfoCANFDFr03",
                                "CentralLockStsUpdateEvnt", UpdateEvnt, 1)
        print(1)

    def SetLocalCenLockCtrl(self, CentralLockCmd, CmdTrigSrc):
        for i in range(16):
            logger.info("LocalCenLockCtrlKeyIDByte" + str(i))
            self.ETH_CDSOC.set_signal_value("LocalCenLockCtrlKeyIDByte" + str(i), 1)
        # time.sleep(1)
        # logger.info(f"设置LocalCenLockCtrlCentralLockCmd为{CentralLockCmd}，CmdTrigSrc为{CmdTrigSrc}")
        # logger.info(f"设置SocToMCU信号CmdTrigSrc为{CmdTrigSrc}")
        # self.ETH_CDSOC.set_signal_value("LocalCenLockCtrlLockCmdTrigSrc", CmdTrigSrc)
        # logger.info(f"设置SocToMCU信号LocalCenLockCtrlCentralLockCmd为{CentralLockCmd}")
        # self.ETH_CDSOC.set_signal_value("LocalCenLockCtrlCentralLockCmd", CentralLockCmd)
        logger.info(f"设置SocToMCU信号LocalCenLockCtrlCentralLockCmd为{CentralLockCmd},CmdTrigSrc为{CmdTrigSrc}")
        self.ETH_CDSOC.set_signal_multiple_value(
            {"LocalCenLockCtrlLockCmdTrigSrc": CmdTrigSrc, "LocalCenLockCtrlCentralLockCmd": CentralLockCmd})

    def CenLockStsTest_SOCtoMCU(self, VehMovgDir=1, FL=2, RL=2, FR=2, RR=2, Tr=2,
                                CentralLockCmd=1, CmdTrigSrc=6,
                                CenLockSts=1, TrigSrc=0x1, TrigSrcType=2, UpdateEvnt=-1):
        self.SetVehMovgDir(VehMovgDir)
        self.SetDoorOpenClsSts(FL, RL, FR, RR, Tr)
        time.sleep(1)
        self.CheckDoorOpenClsSts(FL, RL, FR, RR, Tr)
        self.SetLocalCenLockCtrl(0, 0)
        time.sleep(3)
        self.SetLocalCenLockCtrl(CentralLockCmd, CmdTrigSrc)
        self.CheckCenLockSts(CenLockSts, TrigSrc, TrigSrcType, UpdateEvnt)

    def CenLockStsTest_SOCtoMCU1(self, kwargs):
        VehMovgDir = kwargs.get('VehMovgDir', 2)
        FL = kwargs.get('FLDoorSts', 2)
        FR = kwargs.get('FRDoorSts', 2)
        RL = kwargs.get('RLDoorSts', 2)
        RR = kwargs.get('RRDoorSts', 2)
        Tr = kwargs.get('TrSts', 2)
        CentralLockCmd = kwargs.get('CentralLockCmd', 1)
        CmdTrigSrc = kwargs.get('CmdTrigSrc', 1)
        CenLockSts = kwargs.get('CenLockSts', 1)
        TrigSrc = kwargs.get('TrigSrc', 1)
        TrigSrcType = kwargs.get('TrigSrcType', 1)
        UpdateEvnt = kwargs.get('UpdateEvnt', -1)
        self.CenLockStsTest_SOCtoMCU(VehMovgDir, FL, RL, FR, RR, Tr,
                                     CentralLockCmd, CmdTrigSrc,
                                     CenLockSts, TrigSrc, TrigSrcType, UpdateEvnt)
