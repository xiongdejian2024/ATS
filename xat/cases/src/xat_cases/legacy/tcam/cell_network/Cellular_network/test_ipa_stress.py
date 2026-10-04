#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

import time
import allure
import pytest

from threading import *
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.driver.ssh_interface import command_send


@allure.feature("TCAM交付")
@allure.story("蜂窝网络/IPA压力测试")
class Test_IPA_Stress(TestABCBase):

    def before_class(self, ecu):
        # self.ssh.type_commands(DeviceName.TCAM, "iptables -nvL -t mangle;ip route show table 32;iptables -nvL -t nat;ip r s;ip route", timeout=10)
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.mix.set_tcam_bgm_to_wakeup()
        # self.mix.network_wakeup()
        # self.ssh.type_commands(DeviceName.BGM, "cd /tmp/jiduer/;pkill -f curl", timeout=5)
        # self.ssh.type_commands(DeviceName.TCAM, "cd /sdcard/;pkill -f top", timeout=5)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)


    # 测试前需先将case_helper/下的curl_download.sh和curl_upload.sh文件分别复制到bgm的/data/speed_log和/data/upload目录下
    
    def ck_ipa_failure(self):
        TX_before = self.ssh.type_commands(DeviceName.TCAM, "ifconfig bridge32 | grep 'bytes:' | awk '{print $6}'", timeout=5).split(':')[1]
        RX_before = self.ssh.type_commands(DeviceName.TCAM, "ifconfig bridge32 | grep 'bytes:' | awk '{print $2}'", timeout=5).split(':')[1]
        
        self.ssh.type_commands(DeviceName.BGM, "cd /data/speed_log;chmod 777 curl_download.sh;./curl_download.sh &", timeout=5)  
        self.ssh.type_commands(DeviceName.BGM, "cd /data/upload/;chmod 777 curl_upload.sh;./curl_upload.sh &", timeout=5)
        date=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
        self.ssh.type_commands(DeviceName.TCAM, f"cd /sdcard/top_log;top > 'top_{date}.txt' &", timeout=10)
        sleep(180)

        TX_after = self.ssh.type_commands(DeviceName.TCAM, "ifconfig bridge32 | grep 'bytes:' | awk '{print $6}'", timeout=5).split(':')[1]
        RX_after = self.ssh.type_commands(DeviceName.TCAM, "ifconfig bridge32 | grep 'bytes:' | awk '{print $2}'", timeout=5).split(':')[1]
        
        self.ssh.type_commands(DeviceName.BGM, "cd /tmp/jiduer/;pkill -f curl", timeout=5)
        self.ssh.type_commands(DeviceName.TCAM, "cd /sdcard/;pkill -f top", timeout=5)
        
        tx_speed = (int(TX_after) - int(TX_before)) / 1024 / 180
        rx_speed = (int(RX_after) - int(RX_before)) / 1024 / 180
        if tx_speed > 100 or rx_speed > 100:
            logger.info(f"下载/上传完成后，检测到IPA失效，准备重试。TX增速: {tx_speed:.2f} KB/s, RX增速: {rx_speed:.2f} KB/s")
            return False
        else:
            logger.info(f"下载/上传完成后，TX增速: {tx_speed:.2f} KB/s, RX增速: {rx_speed:.2f} KB/s, 未检测到IPA失效")
            return True
    
    def cap_ipa_logs(self):
        logger.info("已达到最大重试次数，但IPA仍然失效，开始抓取ipacm日志")
        self.ssh.type_commands(DeviceName.BGM, "cd /data/speed_log;chmod 777 curl_download.sh;./curl_download.sh &", timeout=5)  
        self.ssh.type_commands(DeviceName.BGM, "cd /data/upload/;chmod 777 curl_upload.sh;./curl_upload.sh &", timeout=5)
        self.ssh.type_commands(DeviceName.TCAM, "iptables -nvL -t mangle;ip route show table 32;iptables -nvL -t nat;ip r s;ip route", timeout=10)
        self.ssh.type_commands(DeviceName.TCAM, "cd /sdcard/;sh /mnt/sdcard/log_ipa_0802.sh 120", timeout=1800)
        self.ssh.type_commands(DeviceName.BGM, "cd /tmp/jiduer/;pkill -f curl", timeout=5)
        self.ssh.type_commands(DeviceName.TCAM, "cd /sdcard/;pkill -f top", timeout=5)

        logger.info("抓取ipacm日志完成，开始清理日志，并重启tcam重新测试")
        self.ssh.type_commands(DeviceName.TCAM, "cd /sdcard/;rm -rf ipacm_log.txt", timeout=10)
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=10)
        sleep(240)
        self.ssh.type_commands(DeviceName.TCAM, "iptables -nvL -t mangle;ip route show table 32;iptables -nvL -t nat;ip r s;ip route", timeout=10)
        assert False, "IPA出现失效"
    
    def ck_ipa_and_cap_logs(self):
        retries = 0
        max_retries = 3
        while retries < max_retries:
            if not self.ck_ipa_failure():
                retries += 1
                logger.info(f"IPA失效重试已尝试{retries}次")
            else:
                logger.info("下载/上传完成后，未检测到IPA失效")
                break

        if retries == max_retries:
            self.cap_ipa_logs()
    
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_休眠下kill ipacm场景")
    def test_ipa_caseid_1990146(self):
        self.io.tcam_kl15_down()
        self.ssh.type_commands(DeviceName.TCAM, "ps -ef | grep ipacm | awk '{print $1}' | xargs kill -9", timeout=5)
        self.mix.network_sleep()
        sleep(120)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(300)
        self.ck_ipa_and_cap_logs()

    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_快速link up/down场景")
    def test_ipa_caseid_1990145(self):
        for _ in range(5):
            self.io.bgm_power_off()
            self.io.bgm_power_on()
            sleep(3)
        self.ck_ipa_and_cap_logs()          
    
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_高负载场景")
    def test_ipa_caseid_1990143(self):
        retries = 0
        max_retries = 3

        self.ssh.type_commands(DeviceName.TCAM, "yes > /dev/null &", timeout=10)

        while retries < max_retries:
            if not self.ck_ipa_failure():
                retries += 1
                logger.info(f"IPA失效重试已尝试{retries}次")
            else:
                logger.info("下载/上传完成后，未检测到IPA失效")
                self.ssh.type_commands(DeviceName.TCAM, "pkill -f yes", timeout=5)
                break

        if retries == max_retries:
            self.ssh.type_commands(DeviceName.TCAM, "pkill -f yes", timeout=5)
            self.cap_ipa_logs()


    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_反复重新拨号场景")
    def test_ipa_caseid_1914176(self):

        # for _ in range(5):
        #     cmd="cd /oemapp/bin/;./trigger.sh cell cell deactivate_apn4;sleep 2;./trigger.sh cell deactivate_apn1"
        #     command_send(device_name='TCAM', cmd=cmd, timeout=10, connect_type='obd', alias=1)
        #     command_send(device_name='TCAM', cmd=cmd, timeout=10, connect_type='obd', alias=1)
        #     sleep(45)
        #     self.ssh.type_commands(DeviceName.BGM, "cd /data/speed_log;chmod 777 curl_download.sh;./curl_download.sh &", timeout=5)  
        #     self.ssh.type_commands(DeviceName.BGM, "cd /data/upload/;chmod 777 curl_upload.sh;./curl_upload.sh &", timeout=5)
        #     sleep(10)
        
        # apn1、4均重新拨号
        # for _ in range(5):
        #     self.ssh.type_commands(DeviceName.TCAM, "cd /oemapp/bin/;./trigger.sh cell deactivate_apn4;sleep 2;./trigger.sh cell deactivate_apn1", timeout=10)
        #     self.ssh.type_commands(DeviceName.TCAM, "cd /oemapp/bin/;./trigger.sh cell deactivate_apn4;sleep 2;./trigger.sh cell deactivate_apn1", timeout=10)
        #     sleep(45)
        
        # 仅apn4重新拨号
        for _ in range(5):
            self.ssh.type_commands(DeviceName.TCAM, "cd /oemapp/bin/;./trigger.sh cell deactivate_apn4", timeout=10)
            self.ssh.type_commands(DeviceName.TCAM, "cd /oemapp/bin/;./trigger.sh cell deactivate_apn4", timeout=10)
            self.ssh.type_commands(DeviceName.TCAM, "cd /oemapp/bin/;./trigger.sh cell deactivate_apn4", timeout=10)
            sleep(45)
        self.ck_ipa_and_cap_logs()
    
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_curl下载场景")
    def test_ipa_caseid_1986711(self):
        self.ck_ipa_and_cap_logs()
        
    @pytest.mark.longtime
    @pytest.mark.join_santiy
    @pytest.mark.repeat(100)
    @allure.title("IPA稳定性_kill ipacm进程_休眠场景")
    def test_ipa_caseid_1990112(self):
        self.ssh.type_commands(DeviceName.TCAM, "ps -ef | grep ipacm | awk '{print $1}' | xargs kill -9", timeout=5)
        self.mix.network_sleep()
        sleep(600)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(25)
        self.ck_ipa_and_cap_logs()
    
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    @pytest.mark.join_santiy
    @allure.title("IPA稳定性_重启场景")
    def test_ipa_caseid_1914175(self):
        self.io.tcam_power_off()
        sleep(30)
        self.io.tcam_power_on()
        sleep(240)
        self.ck_ipa_and_cap_logs()
    
    @pytest.mark.longtime
    @pytest.mark.join_santiy
    @pytest.mark.repeat(100)
    @allure.title("IPA稳定性_休眠唤醒场景")
    def test_ipa_caseid_19901124(self):
        self.mix.network_sleep()
        sleep(600)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(25)
        self.ck_ipa_and_cap_logs()
    
    
            