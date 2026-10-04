#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_time_manage.py
@Time: 2022/11/01 12:00
@Author: lei.tao
@Software: PyCharm
@Description: 时间管理测试用例
@Examples:
"""

import re
import os
import sys
import pytest
import allure
import threading
import datetime
import pytz
import time
from dateutil import parser

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import (
    send_can_wake_data,
    get_signal_value_from_pdu_data2,
    partner_client_method_request,
)
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.soa_partner.src import partner_client
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_cases.legacy.soa.case_helper.gnss_server import GNSSServiceServer
from xat_ecu.legacy.soa_partner.src.base_partner import *



@allure.feature("架构基础")
@allure.story("网络架构/时间管理")
class Test_Time_manage(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.partner = SOAOperator("S2S", 16789)
        self.partner.run_operator()
        self.result = False
        self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info(f"case开始运行{'=' * 70}")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行{'=' * 70}")
        super().after_each_func(ecu)
        time.sleep(5)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.partner.stop_operator()
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)
    


    @pytest.mark.sanity
    @allure.title("验证BGM存在时钟源，BGM会外发gptp")
    def test_caseid_1988716(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(13)
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(8)
        ret = self.ssh.type_commands(DeviceName.BGM, '/app/bin/zstdcat /jetlog_messages | grep -E "set system time|start ptp41 succeed"')
        assert ret != '', 'BGM没有发送gptp'
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("验证BGM延迟加载时钟源，BGM会外发gptp")
    def test_caseid_1988717(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(35)
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(8)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        

    @pytest.mark.sanity
    @allure.title("先1FFF_10 82再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989075(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1082')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1FFF, '1101')
        time.sleep(60)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("先1FFF_10 02再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989073(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1002')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1FFF, '1101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("先1001_10 82再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989071(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1082', '')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)

    @pytest.mark.sanity
    @allure.title("先1001_10 02再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989069(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1002', '5002')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)

    @pytest.mark.sanity
    @allure.title("先1002_10 82再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989067(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1082', '')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)

    @pytest.mark.sanity
    @allure.title("先1002_10 02再诊断复位，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989065(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1002', '5002')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)

        
    @pytest.mark.sanity
    @allure.title("完成1次授时后，有NTP时钟源，BGM、TCAM 断电，NTP重新授时，240s完成gptp同步")
    def test_caseid_1989053(self):
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.tcam_power_off()
        time.sleep(30)
        self.io.bgm_power_on()
        self.io.tcam_power_on()
        time.sleep(240)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("完成1次授时后，有NTP时钟源，仅BGM 断电，NTP重新授时，10s完成gptp同步")
    def test_caseid_1989054_1989057(self):
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        
    @pytest.mark.sanity
    @allure.title("完成1次NTP授时后，有GNSS时钟源，仅拔插BGM K15，上电后校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989034(self):
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.io.tcam_kl15_down()
        time.sleep(1)
        self.io.tcam_kl15_up()
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        
    @pytest.mark.sanity
    @allure.title("1FFF_11 81，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989074(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1181')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')


    @pytest.mark.sanity
    @allure.title("1001_11 81，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989070(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'1181','')
        time.sleep(15)
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("1002_11 81，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989066(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181','')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')


    @pytest.mark.sanity
    @allure.title("1FFF_11 01，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989072(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)  
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')

    @pytest.mark.sanity
    @allure.title("1001_11 01，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989068(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'1101','5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)  
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')


    @pytest.mark.sanity
    @allure.title("1002_11 01，存在有效的RTC时间，有NTP时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989064(self):
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now_local}时开始执行用例")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1101','5101')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)  
        self.mix.log_special_obj.verify_time_synchronization_and_log(DeviceName.BGM, now_local, 'Set UTC Time to MCU succeed')


    @pytest.mark.sanity
    @allure.title("BGM断电后上电，验证断电清除RTC时间")
    def test_caseid_111299(self): 
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(2)
        # BGM上下电
        logger.info('断电')
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(11)
        # 获取BGM的UTC时间
        find_cmd = "date +'%Y-%m-%d %H:%M:%S'"
        bgm_utcdate = parser.parse(self.ssh.bgm_ssh.type_commands(find_cmd), fuzzy=True)
        #默认时间为2021-01-01_00:00:00，bgm_utcdate误差范围为8s
        defaut_time=parser.parse("2021-01-01 00:00:00")
        logger.info(f'当前时间差为：{abs(bgm_utcdate - defaut_time).seconds}')
        assert  abs(bgm_utcdate - defaut_time).seconds <= 10, f'BGM当前时间为：{bgm_utcdate}'
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(13)



    @pytest.mark.sanity
    @allure.title("验证BGM没有时钟源，BGM不会外发gptp")
    def test_caseid_1988715(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(2)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(13)
        ret=self.ssh.type_commands(DeviceName.BGM, "/app/bin/logcat -F | grep -iE 'start ptp41 succeed|set system time'")
        assert ret == "", "BGM没有时钟源，BGM不应该外发gptp"
        self.ssh.set_airplane_mode(sts=isOn.Off)
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(13)

    @pytest.mark.sanity
    @allure.title("验证通过诊断命令使BGM复位后，能完成时间同步")
    def test_caseid_1987986(self):
        self.mix.init_boot_per()
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1002', '5002')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(15)
        ret1=self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        assert ret1 != "", "BGM时间同步失败"
        self.sd_tester.send_data_and_check(0x1002, '1082', '')
        time.sleep(15)
        self.sd_tester.send_data_and_check(0x1002, '1181', '')
        time.sleep(15)
        ret2=self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        assert ret2 != "", "BGM时间同步失败"


    @pytest.mark.sanity
    @allure.title("验证在BGM进行NTP时间同步期间断网，BGM的时间同步会失败")
    def test_caseid_1987154(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(5)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(3)
        self.io.bgm_power_on()
        # time.sleep(15)
        # ret=self.ssh.type_commands(DeviceName.BGM, '/app/bin/zstdcat /log/jetlog_messages | grep "\'""SynchronizationStatus":0"\'"')
        ret=self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /log/jetlog_messages | grep SynchronizationStatus")
        logger.info(f'ret:{ret}')
        #ret中是否包含"SynchronizationStatus":0
        assert '"SynchronizationStatus":0' in ret, "测试失败"
        # assert ret != "", "BGM时间同步失败"
        self.ssh.set_airplane_mode(sts=isOn.Off)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(2)
        self.io.bgm_power_on()
        time.sleep(13)
 

    @pytest.mark.sanity
    @allure.title("验证DD00为只读DID")
    def test_caseid_1987148(self):
        self.mix.init_boot_per()
        self.sd_tester.send_data_and_check(0x1002, '2EDD005151BE94', '7f2e31')
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00')
        time.sleep(15)

    @pytest.mark.sanity
    @allure.title("诊断复位BGM场景验证时间同步")
    def test_caseid_111302(self):
        with allure.step("发送BGM诊断复位命令"):
            self.sd_tester.send_data_and_check(0x1002, '1002', '5002')
        time.sleep(15)
        self.ssh.verify_time_synchronization(DeviceName.TCAM, 2)
        with allure.step("恢复测试环境"):
            self.sd_tester.send_data_and_check(0x1002, '1001', '5001')
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到PassiveSafetyCAN总线,，且信号的值为2021-01-01_00:00:00")
    def test_caseid_1988740(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(20)
        #监控bodycan
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("passivesafetycan",'AsdmPassSafeCANFr15', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)

        
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到PassiveSafetyCAN总线：当前UTC时间")
    def test_caseid_1988029(self):
        bus_name = self.tb_config["bus"]["passivesafetycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "passivesafetycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("passivesafetycan", {
                                "AsdmPassSafeCANFr15": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataYr1"]
            month = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataMth1"]
            day = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataDay"]
            hour = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataHr1"]
            minite = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataMins1"]
            second = result_dict["AsdmPassSafeCANFr15"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl

     
    @pytest.mark.sanity
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到InfoCANFD总线,，且信号的值为2021-01-01_00:00:00")
    def test_caseid_1988741(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        #监控infocanfd
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("infocanfd",'BgmInfoCanFdFr19', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)
    

    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到InfoCANFD总线：当前UTC时间")
    def test_caseid_1988028(self):
        bus_name = self.tb_config["bus"]["infocanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "infocanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("infocanfd", {
                                "BgmInfoCanFdFr19": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataYr1"]
            month = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataMth1"]
            day = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataDay"]
            hour = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataHr1"]
            minite = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataMins1"]
            second = result_dict["BgmInfoCanFdFr19"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl

        
    @pytest.mark.sanity
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到ConnectivityCANFD总线,，且信号的值为2021-01-01_00:00:00")
    def test_caseid_1988742(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        #监控connectivitycanfd
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("connectivitycanfd",'BgmConnectivityFr04', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)   


    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到ConnectivityCANFD总线：当前UTC时间")
    def test_caseid_1988027(self):
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "BgmConnectivityFr04": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["BgmConnectivityFr04"]["VehTiAndDataYr1"]
            month = result_dict["BgmConnectivityFr04"]["VehTiAndDataMth1"]
            day = result_dict["BgmConnectivityFr04"]["VehTiAndDataDay"]
            hour = result_dict["BgmConnectivityFr04"]["VehTiAndDataHr1"]
            minite = result_dict["BgmConnectivityFr04"]["VehTiAndDataMins1"]
            second = result_dict["BgmConnectivityFr04"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl


    @pytest.mark.sanity
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到ADCANFD总线,，且信号的值为2021-01-01_00:00:00")
    def test_caseid_1988743(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        #监控adcanfd
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("adcanfd",'BgmADCANFDFr03', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4) 

    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到ADCANFD总线：当前UTC时间")
    def test_caseid_1988026(self):
        bus_name = self.tb_config["bus"]["adcanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "adcanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("adcanfd", {
                                "BgmADCANFDFr03": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["BgmADCANFDFr03"]["VehTiAndDataYr1"]
            month = result_dict["BgmADCANFDFr03"]["VehTiAndDataMth1"]
            day = result_dict["BgmADCANFDFr03"]["VehTiAndDataDay"]
            hour = result_dict["BgmADCANFDFr03"]["VehTiAndDataHr1"]
            minite = result_dict["BgmADCANFDFr03"]["VehTiAndDataMins1"]
            second = result_dict["BgmADCANFDFr03"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl


    @pytest.mark.sanity
    @allure.title("验证BGM的MCU会广播信号组VehTiAndData到BodyCAN总线，且信号的值为2021-01-01_00:00:00")
    def test_caseid_1990659(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        #监控bodycan
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataYr1',21, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataMth1',1, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataDay',1, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataHr1',0, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataMins1',0, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataSec1',0, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndDataDataValid',0, 220,10)
        self.bus_comm.check("bodycan",'CemBodyFr107', 'VehTiAndData_UB',0, 220,10)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)

    @pytest.mark.smoke
    @allure.title("BGM获取NTP时间_001")
    def test_caseid_1912725(self):
        result_list = []
        result_details = []
        with allure.step("1、验证BGM是否可以通过Vlan32 ping通tcam(172.16.32.31)"):
            for i in range(2):
                stdin = self.ssh.bgm_ssh.type_commands('ping 172.16.32.31 -c 4')
                res = filter(lambda x: x.count('icmp_seq') == 1, stdin.split('\n'))
                res_list = list(res)
                if len(res_list) == 4:
                    break
            if stdin:
                allure.attach("    {}".format(stdin), f"命令(ping 172.16.32.31 -c 4)执行结果")
                if len(res_list) >= 1:
                    allure.attach("    {}".format(stdin), "执行成功信息")
                    result_list.append(True)
                    result_details.append("BGM可以ping通tcam")
                    logger.info("BGM可以ping通tcam")
                else:
                    allure.attach("{}".format(stdin), "执行失败信息")
                    result_list.append(False)
                    result_details.append("BGM ping tcam 失败")
                    logger.info("BGM ping tcam 失败")
            else:
                allure.attach("    {}".format("未获取任何结果"), "执行失败信息")
                result_list.append(False)
                result_details.append("BGM ping tcam 失败")

        assert all(result_list), "结果概要: " + result_details.__str__()

    @pytest.mark.smoke
    @allure.title("BGM获取NTP时间_002")
    def test_caseid_1912729(self):
        result_list = []
        result_details = []
        url_list = [
            "cn.pool.ntp.org",
            "edu.pool.ntp.org",
            "hk.pool.ntp.org",
            "tw.pool.ntp.org",
        ]
        for url in url_list:
            with allure.step(f"验证BGM是否可以ping通{url}"):
                stdin = self.ssh.bgm_ssh.type_commands(f'ping {url} -c 4')
                if stdin:
                    allure.attach("{}".format(stdin), f"命令(ping {url} -c 4)执行结果")
                    res = filter(lambda x: x.count('icmp_seq') == 1, stdin.split('\n'))
                    res_list = list(res)
                    if len(res_list) >= 1:
                        allure.attach("{}".format(stdin), "执行成功信息")
                        result_list.append(True)
                        result_details.append(f"BGM可以ping通 {url}")
                        logger.info(f"BGM可以ping通 {url}")
                        break
                    else:
                        allure.attach("    {}".format(stdin), "执行失败信息")
                        result_list.append(False)
                        result_details.append(f"BGM {url} 失败")
                        logger.info(f"BGM ping {url} 失败")
                else:
                    allure.attach(
                        "    执行命令(ping {} -c 4)，{}".format(url, "未获取到任何结果"), "执行失败信息"
                    )
                    result_list.append(False)
                    result_details.append(f"BGM ping {url} 失败")
        # 增加重试次数
        for url in url_list:
            with allure.step(f"验证BGM是否可以ping通{url}"):
                stdin = self.ssh.bgm_ssh.type_commands(f'ping {url} -c 4')
                if stdin:
                    allure.attach("{}".format(stdin), f"命令(ping {url} -c 4)执行结果")
                    res = filter(lambda x: x.count('icmp_seq') == 1, stdin.split('\n'))
                    res_list = list(res)
                    if len(res_list) >= 1:
                        allure.attach("{}".format(stdin), "执行成功信息")
                        result_list.append(True)
                        result_details.append(f"BGM可以ping通 {url}")
                        logger.info(f"BGM可以ping通 {url}")
                        break
                    else:
                        allure.attach("    {}".format(stdin), "执行失败信息")
                        result_list.append(False)
                        result_details.append(f"BGM {url} 失败")
                        logger.info(f"BGM ping {url} 失败")
                else:
                    allure.attach(
                        "    执行命令(ping {} -c 4)，{}".format(url, "未获取到任何结果"), "执行失败信息"
                    )
                    result_list.append(False)
                    result_details.append(f"BGM ping {url} 失败")

        assert any(result_list), "结果概要: " + result_details.__str__()

    @pytest.mark.sanity
    @allure.title("BGM下发MCU时间_001")
    def test_caseid_111287(self):
        result_list = []
        result_details = []
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x11,0x01])
        time.sleep(20)

        with allure.step("验证BGM能否下发MCU时间"):
            find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'set rtc time'"
            stdin = self.ssh.bgm_ssh.type_commands(find_cmd)
            if stdin:
                result_list.append(True)
                result_details.append("验证BGM能下发MCU时间 成功")
                allure.attach("    {}".format(stdin), f"执行成功信息")
                logger.info("验证BGM能下发MCU时间成功:{}".format(stdin))
            else:
                allure.attach("    未查找到关键日志", f"执行失败信息")
                result_list.append(False)
                result_details.append("验证BGM能下发MCU时间 执行失败")
                logger.info("验证BGM能下发MCU时间 执行失败")

        assert all(result_list), "结果概要: " + result_details.__str__()

    @pytest.mark.smoke
    @allure.title("验证BGM能否同步TCAM时间")
    def test_caseid_1912732(self):
        result_list = []
        result_details = []

        with allure.step("验证BGM能否同步TCAM时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            dt = datetime.datetime.utcnow()
            dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            allure.attach("     " + dt_str, "当前时间：{}".format(dt_str))
            stdin = self.ssh.tcam_ssh.type_commands(date_curr)
            print(f"stdin ================> {stdin}")
            dt_tcam = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach(
                "     " + dt_tcam.__str__(), "BGM时间为：{}".format(dt_tcam.__str__())
            )
            period = (dt_tcam - dt).seconds if dt_tcam > dt else (dt - dt_tcam).seconds
            rsl = True if period <= 20 else False
            allure.attach(
                "    TCAM上的时间与当前时间误差: {}秒，，允许最大误差20秒".format(str(period)),
                "验证结果：{}".format(rsl),
            )
            logger.info("    TCAM上的时间与当前时间误差: {}秒，允许最大误差20秒".format(str(period)))
            result_list.append(rsl)
            if rsl:
                result_details.append("TCAM上日期为当前时间")
            else:
                result_details.append("TCAM上日期与当前时间相差超过20秒")

        assert all(result_list), "结果概要: " + result_details.__str__()

    @pytest.mark.smoke
    @allure.title("BGM获取NTP时间_003")
    def test_caseid_1912723(self):
        result_list = []
        result_details = []

        with allure.step("判断BGM日志中存在同步NTP时间关键字SynchronizationStatus为3"):
            self.io.bgm_power_off()
            time.sleep(5)
            self.io.bgm_power_on()
            time.sleep(20)
            find_cmd = "/app/bin/zstdcat /log/jetlog_messages |grep -E 'vehicle_time:.*VehicleTimeInfo' | tail -1"
            stdin = self.ssh.bgm_ssh.type_commands(find_cmd)
            sync_status = re.search(r'"SynchronizationStatus":\d', stdin).group().split(":")[1]
            print(f"sync_status ==============> {sync_status}")
            assert int(sync_status) == 3, "BGM的时间并非由NTP同步"

        with allure.step("验证BGM上的日期是否为当前时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            dt = datetime.datetime.utcnow()
            dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            allure.attach("     " + dt_str, "当前时间：{}".format(dt_str))
            stdin = self.ssh.bgm_ssh.type_commands(date_curr)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach(
                "     " + dt_bgm.__str__(), "BGM时间为：{}".format(dt_bgm.__str__())
            )
            period = (dt_bgm - dt).seconds if dt_bgm > dt else (dt - dt_bgm).seconds
            rsl = True if period <= 2 else False
            allure.attach(
                "    BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                "验证结果：{}".format(rsl),
            )
            logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
            result_list.append(rsl)
            if rsl:
                result_details.append("BGM上日期为当前时间")
            else:
                result_details.append("BGM上日期与当前时间相差超过2秒")

        assert all(result_list), "结果概要: " + result_details.__str__()

    @pytest.mark.full
    @allure.title("SOC广播时间通过服务_001")
    def test_caseid_1912744(self):
        partner_client_method_request(
            'VehicleTimeService', 'GetVehicleTimeInfo', '', "method"
        )
        time.sleep(5)
        resp_back = partner_client.resp.copy()
        resp_back_type = partner_client.resp_type.copy()
        if resp_back is None:
            logger.info("============================")
            logger.info("实际结果：{}".format("执行结果为空"))
            logger.info("============================")
            assert False
        if 'FAILTYPE_SUCCESS' not in resp_back_type:
            assert False
        else:
            logger.info("============================")
            logger.info("响应结果：{}".format(resp_back))
            logger.info("响应结果类型：{}".format(resp_back_type))
            logger.info("============================")
            assert True

    @pytest.mark.sanity
    @allure.title("MCU广播时间到CAN总线_001")
    def test_caseid_1912786(self):
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(10)  # 确保总线监听线程处于ready状态

        result_details = []
        with allure.step("验证BGM上的日期是否为总线CarTiGlb信号的时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach(
                "     " + dt_bgm.__str__(), "BGM时间为：{}".format(dt_bgm.__str__())
            )

            # 从总线获取到的报文中，获取信号CarTiGlb_5_CEMBodySignalIPdu30的值
            result, aa = get_signal_value_from_pdu_data2(
                self.bus_comm.ipdu, "bodycan", 880, 'CarTiGlb'
            )
            logger.info(aa)
            # import datetime
            if aa:
                in_date = '2020-01-01 00:00:00'
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = (dt + datetime.timedelta(seconds=int(aa / 10))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info("获取到的CarTiGlb信号值：{}".format(aa))
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                allure.attach(out_date.__str__(), "获取到总线CarTiGlb信号的时间：")
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 15 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差15秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差15秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过15秒")
                assert rsl
            else:
                assert False


    @pytest.mark.smoke
    @allure.title("MCU广播时间到CAN总线_002")
    def test_caseid_1912787(self):
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送

        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodycan", {
                                "CemBodyFr107": [
                                    "VehTiAndDataYr1",
                                    "VehTiAndDataMth1",
                                    "VehTiAndDataDay",
                                    "VehTiAndDataHr1",
                                    "VehTiAndDataMins1",
                                    "VehTiAndDataSec1",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        with allure.step("验证BGM上的日期是否为总线VehTiAndData信号时间"):
            date_curr = "date +'%Y-%m-%d %H:%M:%S'"
            stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
            dt_bgm = datetime.datetime.strptime(
                str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S'
            )
            allure.attach("     " + dt_bgm.__str__(), "BGM时间为：")

            year = result_dict["CemBodyFr107"]["VehTiAndDataYr1"]
            month = result_dict["CemBodyFr107"]["VehTiAndDataMth1"]
            day = result_dict["CemBodyFr107"]["VehTiAndDataDay"]
            hour = result_dict["CemBodyFr107"]["VehTiAndDataHr1"]
            minite = result_dict["CemBodyFr107"]["VehTiAndDataMins1"]
            second = result_dict["CemBodyFr107"]["VehTiAndDataSec1"]
            if year and month and day and hour and minite and second:
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date.__str__(), "获取到总线VehTiAndData信号的时间：")
                logger.info("============================")
                logger.info("BGM 上date命令返回时间：{}".format(dt_bgm))
                logger.info(
                    "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                        year, month, day, hour, minite, second
                    )
                )
                logger.info("总线获取到的时间：{}".format(out_date))
                logger.info("============================")
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (dt_bgm - out_date).seconds
                    if dt_bgm > out_date
                    else (out_date - dt_bgm).seconds
                )
                rsl = True if period <= 10 else False
                allure.attach(
                    "    BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
                logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
                if rsl:
                    result_details.append("BGM上日期为当前时间")
                    self.result = True
                else:
                    result_details.append("BGM上日期与当前时间相差超过10秒")
                assert rsl

    @pytest.mark.sanity
    @allure.title("验证总线上不同信号的时间是否同步:CarTiGlb=>VehTiAndData")
    def test_CarTiGlb_VehTiAndData(self):
        """
        如果总线时间同步:bodycan=>CarTiGlb或者bodycan=>VehTiAndData失败
        以该用例测试结果为准
        """
        if not self.result:
            result_details = []
            bus_name = self.tb_config["bus"]["bodycan"]
            th1 = threading.Thread(
                target=send_can_wake_data, args=(bus_name, "bodycan")
            )
            th1.start()  # 唤醒报文持续发送
            with allure.step("获取总线上CarTiGlb信号的时间："):
                result, aa = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 880, 'CarTiGlb_5_CEMBodySignalIPdu30'
                )
                logger.info(aa)
                if aa:
                    in_date = '2020-01-01 00:00:00'
                    dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                    out_date_CarTiGlb = (
                        dt + datetime.timedelta(seconds=int(aa / 10))
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    allure.attach(out_date_CarTiGlb, "CarTiGlb信号的时间")
                    out_date_CarTiGlb = datetime.datetime.strptime(
                        out_date_CarTiGlb, '%Y-%m-%d %H:%M:%S'
                    )
                    logger.info("============================")
                    logger.info("获取到的信号值：{}".format(aa))
                    logger.info("总线获取到CarTiGlb信号的时间：{}".format(out_date_CarTiGlb))
                    logger.info("============================")

            if True:
                # 从总线获取到的报文中，获取信号CarTiGlb_5_CEMBodySignalIPdu30的值

                _, second = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 960, 'VehTiAndDataSec1_5_CemBodySignalIPdu107'
                )
                _, minite = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu,
                    "bodycan",
                    960,
                    'VehTiAndDataMins1_5_CemBodySignalIPdu107',
                )
                _, year = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 960, 'VehTiAndDataYr1_5_CemBodySignalIPdu107'
                )
                _, month = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 960, 'VehTiAndDataMth1_5_CemBodySignalIPdu107'
                )
                _, day = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 960, 'VehTiAndDataDay_5_CemBodySignalIPdu107'
                )
                _, hour = get_signal_value_from_pdu_data2(
                    self.bus_comm.ipdu, "bodycan", 960, 'VehTiAndDataHr1_5_CemBodySignalIPdu107'
                )

            with allure.step("获取总线上VehTiAndData信号的时间："):
                in_date = '20{}-{}-{} {}:{}:{}'.format(
                    year, month, day, hour, minite, second
                )
                dt = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
                out_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(out_date, "获取到总线VehTiAndData信号的时间：")
            logger.info("============================")
            logger.info(
                "获取到的信号值：20{}-{}-{} {}:{}:{}".format(
                    year, month, day, hour, minite, second
                )
            )
            logger.info("总线获取到VehTiAndData信号的时间：{}".format(out_date))
            logger.info("============================")
            with allure.step("开始校验CarTiGlb信号和VehTiAndData信号的时间差："):
                out_date = datetime.datetime.strptime(out_date, '%Y-%m-%d %H:%M:%S')
                period = (
                    (out_date_CarTiGlb - out_date).seconds
                    if out_date_CarTiGlb > out_date
                    else (out_date - out_date_CarTiGlb).seconds
                )
                rsl = True if period <= 5 else False
                allure.attach(
                    "    CarTiGlb信号和VehTiAndData信号时间误差: {}秒，允许最大误差5秒".format(
                        str(period)
                    ),
                    "验证结果：{}".format(rsl),
                )
                logger.info(
                    "   CarTiGlb信号和VehTiAndData信号时间误差: {}秒，允许最大误差5秒".format(str(period))
                )
                if rsl:
                    result_details.append("CarTiGlb上时间为当前VehTiAndData上时间")
                else:
                    result_details.append("CarTiGlb上时间与VehTiAndData上时间相差超过5秒")
                assert rsl

        else:
            logger.info(f"测试用例4和5成功，该条略过")

    @pytest.mark.sanity
    @allure.title("gPTP时间校准_001")
    def test_caseid_111285(self):
        self.io.nuc_app.bgm_power_off()
        time.sleep(5)
        self.io.nuc_app.bgm_power_on()
        time.sleep(30)
        bgm_current_date = self.ssh.bgm_ssh.type_commands("date +%F", root_permission=False)
        server_date = time.strftime("%Y-%m-%d", time.gmtime())
        logger.info(f"BGM当前时间为：{bgm_current_date}，服务器时间为：{server_date}")
        assert bgm_current_date == server_date, f"{bgm_current_date} != {server_date}, gPTP时间校准出错"

    @pytest.mark.sanity
    @allure.title("gPTP时间校准_002")
    def test_caseid_111292(self):
        self.ssh.set_airplane_mode(sts=isOn.On) 
        logger.info("开启飞行模式")
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(10)
        #默认时间为2021-01-01_00:00:00，bgm_utcdate误差范围为10s
        defaut_time=parser.parse("2021-01-01 00:00:00")
        # 获取BGM的UTC时间
        bgm_utcdate = parser.parse(self.ssh.type_commands(DeviceName.BGM, "date +'%Y-%m-%d %H:%M:%S'"), fuzzy=True)
        logger.info(f'当前时间差为：{abs(bgm_utcdate - defaut_time).seconds}')
        assert  abs(bgm_utcdate - defaut_time).seconds <= 10, f'BGM当前时间为：{bgm_utcdate}'
        self.ssh.set_airplane_mode(sts=isOn.Off)
        logger.info("检查rmnet_data1、rmnet_data0都包含在ifconfig结果中")
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(2)
        self.ssh.type_commands(DeviceName.TCAM, 'ping -I rmnet_data1 www.baidu.com -c 4')
        self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'")
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到BodyCAN总线，且初始值为1年")
    def test_caseid_1988736(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodycan", {
                                "CEMBodyFr30": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyFr30"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到BodyCAN总线")
    def test_caseid_1988023(self):
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodycan", {
                                "CEMBodyFr30": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyFr30"]["CarTiGlb"]
        rsl = True if period <= 2 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过2秒")
            assert rsl

    
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到PassiveSafetyCAN总线，且初始值为1年")
    def test_caseid_1988735(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["passivesafetycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "passivesafetycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("passivesafetycan", {
                                "AsdmPassSafeCANFr04": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["AsdmPassSafeCANFr04"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到PassiveSafetyCAN总线")
    def test_caseid_1988024(self):
        bus_name = self.tb_config["bus"]["passivesafetycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "passivesafetycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("passivesafetycan", {
                                "AsdmPassSafeCANFr04": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["AsdmPassSafeCANFr04"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过2秒")
            assert rsl

    
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到BodyExposedCANFD总线，且初始值为1年")
    def test_caseid_1988737(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["bodyexposedcanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodyexposedcanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodyexposedcanfd", {
                                "CEMBodyExpoCommonFr07": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyExpoCommonFr07"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)
   
    
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到BodyExposedCANFD总线")
    def test_caseid_1988022(self):
        bus_name = self.tb_config["bus"]["bodyexposedcanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodyexposedcanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodyexposedcanfd", {
                                "CEMBodyExpoCommonFr07": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyExpoCommonFr07"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl

    
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到InfoCANFD总线，且初始值为1年")
    def test_caseid_1988738(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["infocanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "infocanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("infocanfd", {
                                "BgmInfoCanFdFr18": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["BgmInfoCanFdFr18"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)

        
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到InfoCANFD总线")
    def test_caseid_1988021(self):
        bus_name = self.tb_config["bus"]["infocanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "infocanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("infocanfd", {
                                "BgmInfoCanFdFr18": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["BgmInfoCanFdFr18"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过2秒")
            assert rsl

    
    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到ConnectivityCANFD总线，且初始值为1年")
    def test_caseid_1988739(self):
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "VgmConnFr12": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["VgmConnFr12"]["CarTiGlb"]
        rsl = True if period <= 10 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差10秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过10秒")
            assert rsl
        #恢复测试环境
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        time.sleep(2)
        #'rmnet_data1', 'rmnet_data0'都包含在ifconfig结果中
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.smoke
    @allure.title("验证BGM的MCU会广播信号CarTiGlb到ConnectivityCANFD总线")
    def test_caseid_1988020(self):
        bus_name = self.tb_config["bus"]["connectivitycanfd"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "connectivitycanfd"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("connectivitycanfd", {
                                "VgmConnFr12": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["VgmConnFr12"]["CarTiGlb"]
        rsl = True if period <= 2 else False
        allure.attach(
                "BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)),
                    "验证结果：{}".format(rsl),
                )
        logger.info("   BGM上的时间与当前时间误差: {}秒，允许最大误差2秒".format(str(period)))
        if rsl:
            result_details.append("BGM上日期为当前时间")
            self.result = True
        else:
            result_details.append("BGM上日期与当前时间相差超过2秒")
            assert rsl


    @pytest.mark.sanity
    @allure.title("验证DD00的值与CarTiGlb信号的值保持一致")
    def test_caseid_1987148(self):
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00')
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodycan", {
                                "CEMBodyFr30": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyFr30"]["CarTiGlb"]
        rsl = True if period <= 2 else False

    
    @pytest.mark.sanity
    @allure.title("验证当bgm硬复位后，读取DD00的值，与CarTiGlb信号的值保持一致")
    def test_caseid_1987149(self):
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(15)  
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00')
        bus_name = self.tb_config["bus"]["bodycan"]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name, "bodycan"))
        th1.start()  # 唤醒报文持续发送
        time.sleep(5)  
        result_dict = self.bus_comm.ipdu.get_multiple_signals("bodycan", {
                                "CEMBodyFr30": [
                                    "CarTiGlb",
                                ]
                        })
        logger.info(f"获取到的总线结果为：{result_dict}")

        result_details = []
        date_curr = "date +'%Y-%m-%d %H:%M:%S'"
        stdin = self.ssh.bgm_ssh.type_commands(date_curr, root_permission=False)
        dt_bgm = datetime.datetime.strptime(str(stdin).rstrip(), '%Y-%m-%d %H:%M:%S')
        # BGM UTC 时间减去2021-01-01 00:00:00
        delt=dt_bgm - datetime.datetime(2021, 1, 1, 0, 0, 0)
        period = delt.total_seconds()-result_dict["CEMBodyFr30"]["CarTiGlb"]
        rsl = True if period <= 2 else False

    @pytest.mark.sanity
    @allure.title("BGM休眠唤醒_RTC时间_001")
    def test_caseid_111296(self): 
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        self.mix.network_sleep()
        time.sleep(5)
        logger.info("已休眠")
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        time.sleep(8)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


# ============================================================GNSSService=====================================================================

    @pytest.mark.sanity
    @allure.title("BGM获取ACU GNSS时间_002")
    def test_caseid_111297(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # 启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        time.sleep(2)
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        # 获取当前时间
        today = datetime.datetime.today()
        year = int(str(today.year)[-2:])
        day = today.day
        # 发送GNSS请求
        input_utc = int(f'{day}06{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info = {"gnssInfo": {"UTCDate": input_utc, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
        assert '"SynchronizationStatus":4' in outmsg and f'"UTCData":{input_utc}' in outmsg, f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc}不在日志结果中,日志结果为：{outmsg}'
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("无RTC时间，GNSS时间小于默认时间，BGM UTC时间为2021-01-01_00:00:00")
    def test_caseid_1989101(self):
        # 启动GNSS服务
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        time.sleep(2)
        # 开启飞行模式
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        # BGM上下电
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        # 发送GNSS请求
        logger.info(f'输入的UTCData：input_utc')
        gnss_info = {"gnssInfo": {"UTCDate": 200519, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
        time.sleep(2)
        # 获取BGM的UTC时间
        find_cmd = "date +'%Y-%m-%d %H:%M:%S'"
        bgm_utcdate = parser.parse(self.ssh.bgm_ssh.type_commands(find_cmd), fuzzy=True)
        #默认时间为2021-01-01_00:00:00，bgm_utcdate误差范围为8s
        defaut_time=parser.parse("2021-01-01 00:00:00")
        logger.info(f'当前时间差为：{abs(bgm_utcdate - defaut_time).seconds}')
        assert  abs(bgm_utcdate - defaut_time).seconds <= 8, f'BGM当前时间为：{bgm_utcdate}'
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.ssh.set_airplane_mode(sts=isOn.Off) 
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("BGM获取TCAM GNSS时间_001")
    def test_caseid_111291(self):
        logger.info("TCAM下电，启动GNSS服务")
        self.io.tcam_power_off()
        time.sleep(15)
        GNSS_SERVICE_SERVER_HD = "GNSSService_server"
        self.io.tcam_power_off
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        time.sleep(2)
        logger.info("TCAM上电，开启飞行模式")
        self.io.tcam_power_on()
        time.sleep(200)
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        logger.info("BGM下电清除RTC时间")
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        # 获取当前时间
        today = datetime.datetime.today()
        year = int(str(today.year)[-2:])
        day = today.day
        # 发送GNSS请求
        input_utc = int(f'{day}06{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info = {"gnssInfo": {"UTCDate": input_utc, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
        assert '"SynchronizationStatus":4' in outmsg and f'"UTCData":{input_utc}' in outmsg, f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc}不在日志结果中,日志结果为：{outmsg}'
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        sleep(4)
        self.io.bgm_power_on()
        time.sleep(15)
        # self.io.tcam_power_on()
        # time.sleep(180)

