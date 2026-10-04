#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_cellular_network.py
@Time: 2023/11/17 10:21
@Author: yunpeng.zhou
@Software: Vscode
@Description: 蜂窝网络测试用例
@Examples:
"""
import inspect
import os
import sys
import time
import allure
import pytest

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("联网服务")
class Test_Cellular_network(TestABCBase):

    def before_class(self, ecu):
        self.soa.update(["NetStatService_client"])
        time.sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.soa.send_SetCellularNetSts_req(is_open=True)
        self.soa.send_SetNetResidentSts_req(is_5G=True)
        sleep(2)

    def after_class(self, ecu):
        super().after_class(self, ecu)


    @pytest.mark.sanity    
    @allure.title("5G使能的SOA接口")
    def test_caseid_1980294(self): 
        self.soa.send_SetNetResidentSts_req(is_5G=False)
        sleep(5)
        self.soa.send_Get5GNetSts_req_and_ck_resp(SA_sts.Off)
        self.soa.send_SetNetResidentSts_req(is_5G=True)

    @pytest.mark.full     
    @allure.title("APN4开关SOA接口实现")
    def test_caseid_1980292(self): 
        self.soa.send_SetCellularNetSts_req(is_open=False)
        sleep(5)
        self.soa.send_GetNetSts_req_and_ck_resp(ApnSts.unavailable)
        sleep(5)
        self.soa.send_SetCellularNetSts_req(is_open=True)
        sleep(2)
        self.soa.send_GetNetSts_req_and_ck_resp(ApnSts.available)
    
    @pytest.mark.sanity  
    @allure.title("5G网络状态广播")
    def test_caseid_1985710(self):
        self.soa.send_SetNetResidentSts_req(is_5G=False)
        self.soa.send_request_and_ck_resp("NetStatService_client", "GetNetSts", {}, 
                                          {"out":[{"ApnName":1,"ApnSts":0,"NetForm":7,"NADstatus":2,"ErrorCode":0},
                                                  {"ApnName":4,"ApnSts":0,"NetForm":7,"NADstatus":2,"ErrorCode":0}]}, 
                                           timeout=40)
        self.soa.send_SetNetResidentSts_req(is_5G=True)
        self.soa.send_request_and_ck_resp("NetStatService_client", "GetNetSts", {}, 
                                          {"out":[{"ApnName":1,"ApnSts":0,"NetForm":9,"NADstatus":2,"ErrorCode":0},
                                                  {"ApnName":4,"ApnSts":0,"NetForm":9,"NADstatus":2,"ErrorCode":0}]}, 
                                           timeout=40)

    @pytest.mark.smoke
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2321284?projectId=46")
    @allure.title("状态上报_网络断开_001")
    def test_caseid_100669_100660(self):
        """
           网络断开or驻网成功，检查状态上报
        """
        with self.log_manage.check_jetlog_by_keywords(log_type="syncNetworkStatus", keywords='tsp.perceptor-service:syncNetworkStatus', timeout=20):
            self.ssh.set_airplane_mode(isOn.On) #打开飞行模式
            self.ssh.set_airplane_mode(isOn.Off) #关闭飞行模式 

    @pytest.mark.full
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2321316?projectId=46")
    @allure.title("状态上报_制式切换_003")
    def test_caseid_100605(self):
        """
           5G切换4G, 检查状态上报
        """
        with self.log_manage.check_jetlog_by_keywords(log_type="syncNetworkStatus", keywords='tsp.perceptor-service:syncNetworkStatus', timeout=30):
            self.soa.send_SetNetResidentSts_req(is_5G=False)  #切4G
            sleep(5) 
            self.soa.send_SetNetResidentSts_req(is_5G=True)  #切5G
    
    @pytest.mark.smoke
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2323937?projectId=46")
    @allure.title("多DNS服务器_域名解析")
    def test_caseid_100504(self):
        data = self.ssh.type_commands(DeviceName.TCAM,"cat /tmp/jidu_resolv.conf")
        with allure.step('校验域名服务器'):    
            assert "nameserver 211.136.150.86" in data,f"TCAM域名服务器不存在"
            assert "nameserver 211.136.150.88" in data,f"TCAM域名服务器不存在"
            assert "nameserver 114.114.114.114" in data,f"TCAM域名服务器不存在"

    @pytest.mark.smoke
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/100504?projectId=46")
    @allure.title("域名解析")
    def test_caseid_100680(self):
        data = self.ssh.type_commands(DeviceName.TCAM, "ip ro sh ta 32")
        with allure.step('校验域名解析'):    
            assert "dev bridge32" in data,f"TCAM域名解析失败"

    @pytest.mark.full
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2324022?projectId=46")
    @allure.title("联网服务_上下电")
    def test_caseid_100913_100909(self):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f",timeout=5)
        sleep(120)
        with allure.step("TCAM重启后再次查看网络"):
            result = self.mix.chk_tcam_ping()
        assert len(result) == 0 , f"支持协议3GPP失败"

    @pytest.mark.smoke
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2324040?projectId=46")
    @allure.title("联网服务_支持协议3GPP")
    def test_caseid_100589(self):
        self.ssh.set_cell_band(Cell_band.LTE) #切4G
        with allure.step("查看TCAM联网情况:"):
            result1 = self.mix.chk_tcam_ping()
        self.ssh.set_cell_band(Cell_band.SA) #切5G
        with allure.step("查看TCAM联网情况:"):
            result2 = self.mix.chk_tcam_ping()    
        assert len(result1 + result2) == 0 , f"支持协议3GPP失败"

    @pytest.mark.full
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2321341?projectId=46")
    @allure.title("联网服务_飞行模式")
    def test_caseid_100503(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="CellPingSts", 
                                                      keywords=['mApnIndex is null',
                                                                'rmnet_data0, ICMPTime=',
                                                                'rmnet_data1, ICMPTime='],timeout=40):
            self.ssh.set_airplane_mode(isOn.On) #打开飞行模式
            self.ssh.set_airplane_mode(isOn.Off) #关闭飞行模式

    @pytest.mark.join_smoke
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/2321358?projectId=46")
    @allure.title("联网服务_与BGM互通")
    def test_caseid_100340(self):
        bgm_data = self.mix.chk_bgm_ping()
        data_tcam = self.mix.chk_bmg_ping_tcam()
        assert len(bgm_data) == 0, f"BGM不能联网"
        assert len(data_tcam) == 0, f"BGM不通"

    @pytest.mark.smoke
    @allure.title("cell模块相关进程监控")
    def test_caseid_1986122(self):
        result=self.ssh.type_commands(DeviceName.TCAM, "ps | grep bin | awk '{print $4}'", timeout=5).split('\n')
        expected_processes = ["/oemapp/bin/gnss_location", "/oemapp/bin/network_manager", "/oemapp/bin/gnss_service", "/oemapp/bin/CellNetworkManager", "/usr/bin/location_hal_daemon"]
        assert all(proc in result for proc in expected_processes), f"cell模块相关进程未启动"
        dns=self.ssh.type_commands(DeviceName.TCAM, "ps | grep dns | awk '{print $4}'", timeout=5).split('\n')
        assert len(dns)==3,f"dns进程未启动"
    
     
    # def test_chec_route_timer(self):
    #     failed = []
    #     with allure.step("TCAM重启后检查网络:"):
            
    #         while True:
    #             try:
    #                 aa = self.ssh.type_commands("pwd")
    #                 if aa:
    #                     logger.info(f"tcam已唤醒{aa}")
    #                     break
    #             except:
    #                 logger.info("tcam没有唤醒, 等待30s")
    #                 time.sleep(30)
    #                 continue
    #     with allure.step("重启后检查路由是否生成:"):
    #         start_time = time.time()
    #         while True:
    #             try:
    #                 route = self.ssh.type_commands("route", timeout=5)
    #                 if "rmnet_data1" and "rmnet_data0" in route:
                        
    #                     end_time = time.time()
    #                     recovery_time = end_time - start_time
    #                     logger.info(f"路由生成时间为:{recovery_time}")
    #                     return recovery_time
    #             except:
    #                 logger.info("默认路由未生成, 等待5s")
    #                 time.sleep(5)
    #                 continue



if __name__ == '__main__':
    pytest.main()

# pytest -vs -p no:warnings Cellular_network/test_cellular_network.py -k test_caseid_1568423