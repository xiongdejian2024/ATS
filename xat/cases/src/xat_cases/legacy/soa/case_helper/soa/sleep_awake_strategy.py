#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#四域休眠唤醒case


import json
import os
import sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.ecuinterface import *
from xat_ecu.legacy.driver.adb_client import Adb
from xat_cases.legacy.soa.case_helper.soa.poweroff_strategy import PoweroffStrategy


class SleepAwakeStrategy(object):

    def __init__(self, strategy_node, tc_config, ipdu, bgm_ip, nucapp) -> None:
        self._sleep_awkae_list = strategy_node["poweroff"]
        self._times = int(strategy_node["times"])
        self._space = int(strategy_node["space"])
        if "title" in strategy_node:
            self._title = str(strategy_node["title"])
        else:
            self._title = None
        self.ipdu = ipdu
        self.tc_config = tc_config
        self.bgm_ip = bgm_ip
        self.nucapp = nucapp
        self.reboot = PoweroffStrategy(strategy_node, self.tc_config, self.nucapp)

    def times(self):
        return self._times
    
    def titles(self):
        return self._title
    
    def wait(self):
        """
        等待域控启动,服务连接
        """
        logger.info(f"开始等待发包信息日志：{self._space}秒")
        time.sleep(self._space)

    def pause_fr_send(self):
        logger.info("关闭Tosunfr")
        os.system("ps -ef|grep -i IniMap|awk '{printf $2\"\\n\"}'|xargs kill -9;ps -ef|grep -i IniMap")
        time.sleep(5)

    def resume_fr_send(self):
        i = 5
        while i > 0:
            data = os.popen("ps -ef|grep -i IniMap|grep -v grep").read()
            if "IniMap" in data:
                logger.info("Tosunfr打开成功")
                break
            else:
                dir = os.path.join(project_root, "test_case/soa")
                os.system(f"cd {dir};/usr/local/lib/python3.8/dist-packages/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap configfr.ini &'\\n'")
                time.sleep(5)
            i -= 1
        else:
            logger.info("Tosunfr打开失败")

    def check_all_channel_recv_no_msg(self):
        '''
        接收所有通道
        '''
        all_bus = self.tc_config.get('bus', None)
        # lin 通道
        lin_channel_list = ["cem_lin1", "cem_lin2", "cem_lin3", "cem_lin4", "cem_lin5", "cem_lin6"]
        # can 通道
        can_channel_list = ["bodycan", "propulsioncan", "chassiscan1", "chassiscan2", "passivesafetycan",
                            "diagnosticcan", "infocanfd", "adcanfd", "bodyalmcanfd1", "connectivitycanfd",
                            "bodyexposedcanfd", "bodyalmcanfd2"]
        # fr 通道
        fr_channel_list = ['backbonefr']
        all_channel = lin_channel_list + can_channel_list + fr_channel_list

        if all_bus:
            all_channel = [i for i in list(all_bus.keys()) if 'can' in i or 'lin' in i or 'backbonefr' in i]

        # 清除缓存
        self.ipdu.rx_flag_reset_all()
        err_list = []
        for channel in all_channel:
            logger.info(f"{channel} 开始接收报文")
            try:
                msgs = self.ipdu.check_bus_recv_message(channel)
                string = ''
            except Exception as e:
                msgs = ""
                string = str(e)
            logger.info(f"{channel} 通道{'本不应接收到报文，实际' if msgs else '未'}接收报文 {string}")
            if msgs:
                err_list.append(channel)
        if len(err_list):
            logger.error(f"本不应接收到报文，{err_list}通道接收到报文")
            return False
        return True
    
    def reboot_bgm(self):
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        logger.info("bgm上下电后等待30s")
        time.sleep(30)

    def set_usage_mode_status_is_abandoned(self, enter_time=5*60):
        '''
        校验 usage 状态
        '''
        # logger.info("快速进入abandoned状态,bgm上下电")
        # self.reboot.sd_reboot_bgm()
        # 挂P档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        sleep(1)
        # 车速为0
        self.resume_fr_send()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0.0)
        # 在lin6找BmsCem_Lin6Fr05_CEM_LIN6帧，调整智能补电信号BattSocRaw_CEM_LIN6(物理值100%)，BattURaw_CEM_LIN6(物理值15Volt)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSocRaw', 1)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw_0_BmsCem_Lin6SignalIPdu05', 15)
        lin_msg = [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff]
        self.ipdu.send_pdu("cem_lin6", 0x06, lin_msg)
        time.sleep(5)
        self.ipdu.rx_flag_reset_all()
        t = time.time()
        while time.time() - t < enter_time:
            result, realvalue, expectedvalue = self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02", "0", timeout=30, do_assert=False)
            logger.info(f"当前模式为{realvalue}期望模式为{expectedvalue}")
            if result:
                logger.info(f"成功进入abandoned状态")
                return True
            else:
                time.sleep(5)
        else:
            logger.info(f"进入abandoned状态失败")
            return False


    def cdc_sleep_awake(self):
        rst = self.set_usage_mode_status_is_abandoned() 
        if not rst:
            logger.info(f"未进入ABANDONED状态,检查环境,确认下,bodycan是否能收到报文")     
        i = 0
        j = 0
        while True:
            # cdc休眠
            self.ipdu.pause_all_bus_send()
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            time.sleep(1)
            data = Adb().shell(args="ping 172.16.5.11 -c 4", timeout=5)
            logger.info(data)
            if "ttl=" in data and "icmp_seq=" in data:
                logger.info("CDC未休眠, 等待5s") 
                j += 1
                time.sleep(5)
                if j == 10:
                    self.nucapp.cdc_power_off()
            else:
                i += 1
                if i == 3:
                    logger.info("CDC已休眠")
                    break
            
    def acu_sleep_awake(self):
        self.cdc_sleep_awake()     
        i = 0
        # acu休眠,221台架需要重启才能休眠
        self.reboot.sd_reboot_acu(self.ipdu)
        while True:
            data = Adb().shell(args="ping 172.16.5.21 -c 4", timeout=10)
            logger.info(data)
            if "ttl=" in data and "icmp_seq=" in data:
                self.ipdu.pause_all_bus_send()
                self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
                logger.info("ACU未休眠, 等待30s") 
                time.sleep(30)
            else:
                i += 1
                if i == 3:
                    logger.info("ACU已休眠")
                    break
        
    def bgm_sleep_awake(self):
        self.acu_sleep_awake()
        while True:
            # bgm休眠
            ret = self.check_all_channel_recv_no_msg()
            if not ret:
                logger.info("bgm 未休眠, 进入可以收到报文, 等待60s")
                self.ipdu.pause_all_bus_send()
                self.pause_fr_send()
                self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
                time.sleep(60)
            else:
                logger.info("BGM已休眠")
                break

    def tcam_sleep_awake(self):
        self.bgm_sleep_awake()
        time.sleep(30)
        logger.info("TCAM已休眠")

    def powersleep(self):
        """
        不同域控休眠
        """
        global _time
        global domain
        for domain_name in self._sleep_awkae_list:
            if "sleep" in domain_name :
                domain = domain_name
                _time = eval(domain_name.strip()[6:-1])
                continue
        self._sleep_awkae_list.pop()
        logger.info(f"开始休眠: {self._sleep_awkae_list}")
        self.ipdu.rx_flag_reset_all()
        logger.info("关闭bgm的诊断激活线")
        self.nucapp.bgm_diag_line_down()
        # logger.info("关闭cdc的诊断激活线")
        # self.nucapp.cdc_diag_line_down()
        logger.info("关闭tcam的诊断激活线")
        self.nucapp.tcam_kl15_down()

        if self._sleep_awkae_list == ['cdc']:
            self.cdc_sleep_awake()
        elif self._sleep_awkae_list == ['cdc', 'acu']:
            self.acu_sleep_awake()
        elif self._sleep_awkae_list == ['cdc', 'acu', 'bgm']:
            self.bgm_sleep_awake()
        elif self._sleep_awkae_list == ['cdc', 'acu', 'bgm', 'tcam']:
            self.tcam_sleep_awake()
            time.sleep(30)
        else:
            logger.info("暂不支持此休眠唤醒场景")
            exit()
            
        for domain_name in self._sleep_awkae_list:
            logger.info(f"{domain_name}完成休眠")

        self._sleep_awkae_list.append(domain)
        logger.info(f'休眠后等待{_time}s唤醒')
        time.sleep(_time)



    def powerawake(self):
        """
        不同域控唤醒
        """
        logger.info(f"开始唤醒: {self._sleep_awkae_list}")    
        logger.info("开启bgm的诊断激活线")
        self.nucapp.bgm_diag_line_up()
        self.nucapp.cdc_power_on()
        # logger.info("开启cdc的诊断激活线")
        # self.nucapp.cdc_diag_line_up()
        logger.info("开启tcam的诊断激活线")
        self.nucapp.tcam_kl15_up()
        time.sleep(30)
        for domain_name in self._sleep_awkae_list:
            logger.info(f"{domain_name}完成唤醒")
        
