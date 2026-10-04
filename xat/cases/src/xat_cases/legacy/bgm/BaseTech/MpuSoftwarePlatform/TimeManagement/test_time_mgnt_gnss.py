#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_


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
class Test_Time_manage_gnss(TestABCBase):
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


    # @pytest.mark.sanity
    # @allure.title("无RTC时间，GNSS时间小于默认时间，BGM UTC时间为2021-01-01_00:00:00")
    # def test_caseid_1989101(self):
    #     # 启动GNSS服务
    #     GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
    #     self.partner = GNSSServiceServer([
    #         ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
    #     ])
    #     self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
    #     time.sleep(2)
    #     # 开启飞行模式
    #     self.ssh.set_airplane_mode(sts=isOn.On) 
    #     time.sleep(1)
    #     # BGM上下电
    #     self.io.bgm_power_off()
    #     time.sleep(1)
    #     self.io.bgm_power_on()
    #     time.sleep(15)
    #     # 发送GNSS请求
    #     logger.info(f'输入的UTCData：input_utc')
    #     gnss_info = {"gnssInfo": {"UTCDate": 200519, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
    #     self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
    #     time.sleep(2)
    #     # 获取BGM的UTC时间
    #     find_cmd = "date +'%Y-%m-%d %H:%M:%S'"
    #     bgm_utcdate = parser.parse(self.ssh.bgm_ssh.type_commands(find_cmd), fuzzy=True)
    #     #默认时间为2021-01-01_00:00:00，bgm_utcdate误差范围为8s
    #     defaut_time=parser.parse("2021-01-01 00:00:00")
    #     logger.info(f'当前时间差为：{abs(bgm_utcdate - defaut_time).seconds}')
    #     assert  abs(bgm_utcdate - defaut_time).seconds <= 8, f'BGM当前时间为：{bgm_utcdate}'
    #     #恢复测试环境
    #     self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
    #     self.ssh.set_airplane_mode(sts=isOn.Off) 
    #     self.io.bgm_power_on()
    #     time.sleep(15)


    # @pytest.mark.sanity
    # @allure.title("BGM获取TCAM GNSS时间_001")
    # def test_caseid_111291(self):
    #     GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
    #     logger.info(f'开启GNSS服务')
    #     self.partner = GNSSServiceServer([
    #         ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
    #     ])
    #     self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
    #     time.sleep(2)
    #     # 开启飞行模式
    #     self.ssh.set_airplane_mode(sts=isOn.On) 
    #     time.sleep(1)
    #     # BGM上下电
    #     self.io.bgm_power_off()
    #     time.sleep(1)
    #     self.io.bgm_power_on()
    #     time.sleep(15)
    #     # 获取当前时间
    #     today = datetime.datetime.today()
    #     year = int(str(today.year)[-2:])
    #     day = today.day
    #     # 发送GNSS请求
    #     input_utc = int(f'{day}01{year-2}')
    #     logger.info(f'输入的UTCData：input_utc')
    #     gnss_info = {"gnssInfo": {"UTCDate": input_utc, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
    #     self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
    #     time.sleep(2)
    #     # 从jetlog中获取结果
    #     find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
    #     outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
    #     logger.info(f'日志结果：{outmsg}')
    #     assert '"SynchronizationStatus":4' in outmsg and f'"UTCData":{input_utc}' in outmsg, f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc}不在日志结果中,日志结果为：{outmsg}'
    #     #恢复测试环境
    #     self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
    #     self.io.bgm_power_on()
    #     time.sleep(15)



    @pytest.mark.sanity
    @allure.title("验证时间源同时存在时，遵循先到先用的原则，无RTC时间，先NTP，后GNSS场景")
    def test_caseid_1989105(self):
        #开启NTP同步
        # BGM上下电,清除RTC时间
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        logger.info('开启GNSS服务')
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
        time.sleep(2) 
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(28)
        # 获取当前时间
        today = datetime.datetime.today()
        year = int(str(today.year)[-2:])
        day = today.day
        # 发送GNSS请求
        input_utc = int(f'{day}02{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info = {"gnssInfo": {"UTCDate": input_utc, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
        time.sleep(2)
        
        # 从jetlog中获取结果
        find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
        logger.info(f'日志结果：{outmsg}')
        assert '"SynchronizationStatus":3' in outmsg,f'"SynchronizationStatus":3 不在日志结果中,日志结果为：{outmsg}'
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)

    @pytest.mark.sanity
    @allure.title("验证时间源同时存在时，遵循先到先用的原则，无RTC时间，先GNSS，后NTP场景")
    def test_caseid_1989104(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # 启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc = int(f'{day}03{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info = {"gnssInfo": {"UTCDate": input_utc, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info)
        time.sleep(2)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
        logger.info(f'日志结果：{outmsg}')
        assert '"SynchronizationStatus":4' in outmsg and f'"UTCData":{input_utc}' in outmsg,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc}不在日志结果中,日志结果为：{outmsg}'
        
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)

    @pytest.mark.sanity
    @allure.title("GNSS时钟源完成1次授时后，拔插BGM、TCAM的 K30、K15，NTP重新授时，180s内完成gptp同步")
    def test_caseid_1989031(self):
        logger.info("开启GNSS服务")
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}04{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        logger.info("关闭GNSS服务")
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        logger.info("BGM、TCAM上下电")
        self.io.bgm_power_off()
        self.io.tcam_power_off()
        time.sleep(30)
        self.io.tcam_power_on()
        time.sleep(240)
        self.io.bgm_power_on()
        time.sleep(17)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)


    @pytest.mark.sanity
    @allure.title("1FFF_10 82，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989052(self):
        logger.info("开启GNSS服务")
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
        time.sleep(2)
        logger.info("开启飞行模式")
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        logger.info("BGM上下电")
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        # 获取当前时间
        today = datetime.datetime.today()
        year = int(str(today.year)[-2:])
        day = today.day
        logger.info('发送GNSS信号1')
        input_utc1 = int(f'{day}06{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1082')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1FFF, '1101')
        time.sleep(20)

        logger.info('发送GNSS信号2')
        input_utc2 = int(f'{day}07{year-2}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(5)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')  
        find_cmd3 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        self.ssh.bgm_ssh.type_commands(find_cmd3)
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)



    @pytest.mark.sanity
    @allure.title("GNSS时钟源完成1次授时后，拔插BGM、TCAM的 K30、K15，NTP重新授时，完成gptp同步")
    def test_caseid_1989030(self):
        logger.info("开启GNSS服务")
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
        time.sleep(2)
        logger.info("开启飞行模式")
        self.ssh.set_airplane_mode(sts=isOn.On) 
        time.sleep(1)
        logger.info('BGM上下电')
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(15)
        logger.info('获取当前时间')
        today = datetime.datetime.today()
        year = int(str(today.year)[-2:])
        day = today.day
        # 发送GNSS请求
        input_utc1 = int(f'{day}05{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        #TCAM和BGM同时下电
        logger.info("TCAM和BGM同时下电")
        self.io.tcam_power_off()
        self.io.bgm_power_off()
        time.sleep(30)
        self.io.tcam_power_on()
        time.sleep(200)
        self.io.bgm_power_on()
        time.sleep(15)
        logger.info("关闭飞行模式")
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        # NTP完成授时
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        # #恢复测试环境
        # self.io.bgm_power_off()
        # time.sleep(2)
        # self.io.bgm_power_on()
        # time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1002_10 82，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989044(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}08{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1082')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}09{year-2}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)



    @pytest.mark.sanity
    @allure.title("1001_10 82，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989048(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}10{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1082')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}11{year-2}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1FFF_10 02，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989050(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}12{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1002')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1FFF, '1101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}01{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1002_10 02，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989042(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}02{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1002', '5002')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}02{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1001_10 02，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989046(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}03{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1002', '5002')
        time.sleep(20)
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}04{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1FFF_11 81，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989051(self):
        logger.info('启动GNSS服务')
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}05{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1181')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}06{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1002_11 81，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989043(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}07{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1181')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}08{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)



    @pytest.mark.sanity
    @allure.title("1001_11 81，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989047(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}09{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1181')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}10{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)



    @pytest.mark.sanity
    @allure.title("1FFF_11 01，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989049(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}11{year-1}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1FFF, '1101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}12{year-1}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("1002_11 01，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989041(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}01{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1002, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}02{year-2}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)



    @pytest.mark.sanity
    @allure.title("1001_11 01，存在有效的RTC时间，有GNSS时钟源，校准系统时间，更新RTC时间，10s完成gptp同步")
    def test_caseid_1989045(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        input_utc1 = int(f'{day}03{year-2}')
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 800, "timestamp": 800, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(20)

        #发送GNSS信号
        input_utc2 = int(f'{day}04{year-2}')
        gnss_info2 = {"gnssInfo": {"UTCDate": input_utc2, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info2)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd2 = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:'"
        outmsg2 = self.ssh.bgm_ssh.type_commands(find_cmd2)
        logger.info(f'日志结果：{outmsg2}')
        assert f'get gnss from acu succeed  GNSSStatus 1 date {input_utc2}' in outmsg2 , f'失败，日志结果为：{outmsg2}'

        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)

    @pytest.mark.sanity
    @allure.title("验证单独对MPU进行硬复位后，监测心跳以及BootCompleted")
    def test_caseid_1988629_1988630(self):
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(20)
        self.ssh.verify_time_synchronization(DeviceName.BGM, 2)
        time.sleep(60)
        find_cmd1 = '/app/bin/zstdcat /log/jetlog_messages |grep -iE "sent heart beat to mcu" | tail -1'
        ret = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{ret}')
        #发送诊断指令
        logger.info("发送BGM诊断复位命令")
        self.sd_tester.send_data_and_check(0x1001, '1101', '5101')
        time.sleep(20)
        # 当前时间
        now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"启动时间是{now_local}")
        time.sleep(40)
        logger.info("提取所有日志")
        find_cmd1 = '/app/bin/zstdcat /log/jetlog_messages |grep -iE "PWMGR:|sent heart beat to mcu"'
        self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info("提取关键日志")
        find_cmd = '/app/bin/zstdcat /log/jetlog_messages | grep "successful to send BootCompleted" | tail -1'
        outmsg = self.ssh.bgm_ssh.type_commands(find_cmd)
        logger.info(f'日志结果：{outmsg}')
        pattern1 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3})\s+\d+\s+\d+\s+.*: (\d+)'  # 提取时间和日期
        match1 = re.search(pattern1, outmsg)
        log_time = parser.parse(match1.group(1))
        assert abs(log_time - parser.parse(now_local)).seconds <= 40, f'本次获取到的log非本次执行的记录{parser.parse(now_local)}脚本开始执行'


    @pytest.mark.sanity
    @allure.title("验证DD00的时间分辨率为100ms为1bit")
    def test_caseid_1987151(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        # today = datetime.datetime.today()
        # year = int(str(today.year)[-2:])
        # day = today.day
        # 发送GNSS请求
        input_utc1 = int(10130)
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00000000')
        time.sleep(15)
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("验证全局时间 > (初始时间+0xBC1FAB00)后，读取DD00，值为全局时间超出(初始时间+0xBC1FAB00)的部分")
    def test_caseid_1987150(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        # today = datetime.datetime.today()
        # year = int(str(today.year)[-2:])
        # day = today.day
        # 发送GNSS请求
        input_utc1 = int(10130)
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00000000')
        time.sleep(15)
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)


    @pytest.mark.sanity
    @allure.title("验证DD00的初始化时间为0")
    def test_caseid_1987152_(self):
        GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"
        # TCAM下电，启动GNSS服务
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD") # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
        ])
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD, timeout=60)
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
        # today = datetime.datetime.today()
        # year = int(str(today.year)[-2:])
        # day = today.day
        # 发送GNSS请求
        input_utc1 = int(10130)
        logger.info(f'输入的UTCData：input_utc')
        gnss_info1 = {"gnssInfo": {"UTCDate": input_utc1, "UTCTime": 0, "timestamp": 0, "fixType": 0, "GNSSStatus": 1, "longitude": 0.0, "latitude": 0.0, "ellipsoid": 0.0, "velocityOverGround": 0.0, "trueNorthVelocity": 0.0, "trueEastVelocity": 0.0, "downVelocity": 0.0, "heading": 0.0, "estimateHorizontalAccuracy": 0.0, "estimatedLongPrecision": 0.0, "estimatedLatPrecision": 0.0, "estimatedHighPrecision": 0.0, "estimateVelocityAccuracy": 0.0, "estimatedNorthVelocityPrecision": 0.0, "estimatedEastVelocityPrecision": 0.0, "estimatedDownVelocityPrecision": 0.0, "estimatedHeadingPrecision": 0.0, "satellitesInView": 0, "satellitesInUse": 0, "CN0": 0.0, "PDOP": 0.0, "HDOP": 0.0, "GDOP": 0.0, "TDOP": 0.0, "VDOP": 0.0, "leapSecond": 0.0, "GNSSErrorCode": 0, "coordinateSystem": 0, "satelliteInViewInfo": {"numberOfSatellitesInView": 0, "satelliteInfo": [{"satelliteID": 0, "elevationInDegrees": 0, "azimuthInDegrees": 0, "sNRIndB": 0, "fixStatus": 0}]}}}
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation", gnss_info1)
        time.sleep(2)
        # 从jetlog中获取结果
        find_cmd1 = "/app/bin/zstdcat /log/jetlog_messages | grep 'Notify VehicleTimeInfo:' |tail -1"
        outmsg1 = self.ssh.bgm_ssh.type_commands(find_cmd1)
        logger.info(f'日志结果：{outmsg1}')
        assert '"SynchronizationStatus":4' in outmsg1 and f'"UTCData":{input_utc1}' in outmsg1,f'"SynchronizationStatus":4 或者 "输入的UTCData":{input_utc1}不在日志结果中,日志结果为：{outmsg1}'
        
        self.sd_tester.send_data_and_check(0x1002, '22DD00', '62dd00000000')
        time.sleep(15)
        #恢复测试环境
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.io.bgm_power_on()
        time.sleep(15)