#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

import inspect
import os
import sys
import time
import allure
import pytest
import datetime
from datetime import datetime, timezone

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("联网服务")
class Test_Cellular_Did(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        global ip
        ip = self.tc_config.get('gateway_ip')
        # self.soa.update(["CallService_client"])
        # sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        # self.ssh.type_commands(DeviceName.TCAM,'cat /dev/smd8 & echo -en "at+gtact=21\\r\\n" > /dev/smd8;sleep 1;cat /dev/smd8 & echo -en "at+gtact=21\\r\\n" > /dev/smd8', timeout=5)
        # self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.ssh.set_airplane_mode(isOn.Off) #关闭飞行模式
        super().after_class(self, ecu)


    @pytest.mark.join_full    
    @allure.title("UDS_ReadAPNAccountName_D9C0")
    def test_caseid_1987404(self): 
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9C0,SESSION.DEFAULT,'62d9c0434d4d544d35474a44422e53480000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000434d4d544d35474a44442e5348000000000000000000000000000000000000000000000000000000')

    @pytest.mark.join_full   
    @allure.title("UDS_ReadGPS_UTCtime_D9A7")
    def test_caseid_1987403(self): 
        result=self.sd_tester.read_did_and_check(TA.TCAM,0xD9A7,SESSION.DEFAULT,'62d9a7')
        now_utc = datetime.datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        ascii_result = ''.join(chr(int(result[i+6:i+8], 16)) for i in range(0, len(result)-6, 2))
        assert abs(int(now_utc) - int(ascii_result))<=1,f"D9A7读取UTC time不准确" 

    @pytest.mark.join_full 
    @allure.title("验证D917功能")
    def test_caseid_1987398(self): 
        result=self.sd_tester.read_did_and_check(TA.TCAM,0xD917,SESSION.DEFAULT,'62d917')   
        ascii_result = ''.join(chr(int(result[i+6:i+8], 16)) for i in range(0, len(result)-6, 2))
        data = self.ssh.type_commands(DeviceName.TCAM,'cat /dev/smd8 & echo -en "at+cimi\\r\\n" > /dev/smd8;sleep 1;cat /dev/smd8 & echo -en "at+cimi\\r\\n" > /dev/smd8', timeout=5).split('\n')[1]
        assert int(ascii_result) == int(data),f"D917读取SIM卡IMI不正确"
    
    @pytest.mark.join_full  
    @allure.title("验证D99D功能")
    def test_caseid_1987397(self): 
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99D,SESSION.DEFAULT,'62d99d03')  
        self.ssh.set_airplane_mode(isOn.On) #打开飞行模式
        sleep(2)
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99D,SESSION.DEFAULT,'62d99d01')  
        self.ssh.set_airplane_mode(isOn.Off) #关闭飞行模式
    
    # @pytest.mark.join_full    
    # @allure.title("验证D99E功能")
    # def test_caseid_1987396(self): 
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.DEFAULT,'62d99e0640') 
    #     self.ssh.type_commands(DeviceName.TCAM,'cat /dev/smd8 & echo -en "at+gtact=3\\r\\n" > /dev/smd8;sleep 1;cat /dev/smd8 & echo -en "at+gtact=3\\r\\n" > /dev/smd8', timeout=5)
    #     sleep(10)
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.DEFAULT,'62d99e')
    #     self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
    #     # 接通后10s挂断
    #     sleep(10)
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.DEFAULT,'62d99ee800') 
    #     self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)
    #     self.ssh.type_commands(DeviceName.TCAM,'cat /dev/smd8 & echo -en "at+gtact=21\\r\\n" > /dev/smd8;sleep 1;cat /dev/smd8 & echo -en "at+gtact=21\\r\\n" > /dev/smd8', timeout=5)
     



if __name__ == '__main__':
    pytest.main()

# pytest -vs -p no:warnings Cellular_network/test_cellular_network.py -k test_caseid_1568423