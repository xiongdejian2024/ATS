#!/usr/bin/python3
# coding=UTF-8

import os, sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.utils import hand_usbrelay_on,hand_usbrelay_off
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import DiagTestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester



class PoweroffStrategy(object):
    def __init__(self, strategy_node, tc_config, nucapp=None) -> None:
        self._poweroff_list = strategy_node["poweroff"]
        self._times = int(strategy_node["times"])
        self._space = int(strategy_node["space"])
        if "title" in strategy_node:
            self._title = str(strategy_node["title"])
        else:
            self._title = None
        logger.info(self.__dict__)
        self._poweron_list = strategy_node.get("poweron",self._poweroff_list)
        self.tc_config = tc_config
        self.nucapp=nucapp
        self.doip = Sd_Tester(**self.tc_config)
          

    def times(self):
        return self._times
    
    def titles(self):
        return self._title

    def powerons(self):
        return self._poweron_list

 
    def poweroff(self):
        """
        不同域控下电
        """
        logger.info(f"开始下电: {self._poweroff_list}")
        for domain_name in self._poweroff_list:
            if "sleep" in domain_name :
                logger.info(f'延时{domain_name[6:-1]}s')
                time.sleep(eval(domain_name.strip()[6:-1]))
                continue
            logger.info(f"{domain_name}开始下电")
            hand_usbrelay_off(domain_name,self.nucapp)
            # os.system(f'poweroff {domain_name}')
            logger.info(f"{domain_name}完成下电")

    def wait(self):
        """
        等待域控启动,服务连接
        """
        logger.info(f"开始等待发包信息日志：{self._space}秒")
        time.sleep(self._space)


    def poweron(self):
        """
        不同域控上电
        """
        logger.info(f"开始上电: {self._poweron_list}")
        for domain_name in self._poweron_list:
            if "sleep" in domain_name :
                logger.info(f'延时{domain_name[6:-1]}s')
                time.sleep(eval(domain_name.strip()[6:-1]))
                continue
            logger.info(f'{domain_name} 开始上电')
            hand_usbrelay_on(domain_name,self.nucapp)
            logger.info(f"{domain_name}完成上电")


    def sd_reboot_bgm(self):
        """
        诊断重启bgm
        """
        self.doip.update_serverdoipid(0x1002)
        self.doip.diagnostic_client_sim_start()
        self.doip.tester_present()
        if "bgm" in self._poweron_list:
            logger.info("诊断重启bgm")
            self.doip.send_data([0x11, 0x81])
        self.doip.stop_tester_present()
        self.doip.diagnostic_client_sim_close()  


    def sd_reboot_tcam(self, ipdu):
        """
        诊断重启tcam
        """
        self.doip.update_serverdoipid(0x1011)
        self.doip.diagnostic_client_sim_start()
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',0)
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
        time.sleep(0.5)
        if "tcam" in self._poweron_list:
            logger.info("进入扩展会话")
            self.doip.send_data([0x10, 0x03])
            time.sleep(0.5)
            logger.info("诊断重启tcam")
            self.doip.send_data([0x11, 0x03])
        self.doip.stop_tester_present()
        self.doip.diagnostic_client_sim_close()


    def sd_reboot_cdc(self, ipdu):
        """
        诊断重启tcam
        """
        self.doip.update_serverdoipid(0x1201)
        self.doip.diagnostic_client_sim_start()
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',0)
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
        time.sleep(0.5)
        if "tcam" in self._poweron_list:
            logger.info("诊断重启cdc")
            self.doip.send_data([0x11, 0x81])
        self.doip.stop_tester_present()
        self.doip.diagnostic_client_sim_close()

    def sd_reboot_acu(self, ipdu):
        """
        诊断重启acu
        """
        self.doip.update_serverdoipid(0x1401)
        self.doip.diagnostic_client_sim_start()
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',0.0)
        ipdu.set(ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
        time.sleep(0.5)
        if "acu" in self._poweron_list:
            logger.info("诊断重启acu")
            self.doip.send_data([0x11, 0x81])
        self.doip.stop_tester_present()
        self.doip.diagnostic_client_sim_close()


    def sd_reboot_domian(self, ipdu):
        logger.info(f"开始重启: {self._poweroff_list}")
        for domain_name in self._poweroff_list:
            logger.info(f"{domain_name}开始重启")
            domain = domain_name.lower()
            if domain == "tcam":
                self.sd_reboot_tcam(ipdu)
            elif domain == "cdc":
                self.sd_reboot_cdc(ipdu)
            elif domain == "acu":
                self.sd_reboot_acu(ipdu)
            elif domain == "bgm":
                self.sd_reboot_bgm()
            elif domain == "all":
                self.sd_reboot_tcam(ipdu)
                self.sd_reboot_cdc(ipdu)
                self.sd_reboot_acu(ipdu)
                self.sd_reboot_bgm()
            else:
                logger.error("domian入参不对，请线下修正")
            if "sleep" in domain_name :
                logger.info(f'延时{domain_name[6:-1]}s')
                time.sleep(eval(domain_name.strip()[6:-1]))
                continue
